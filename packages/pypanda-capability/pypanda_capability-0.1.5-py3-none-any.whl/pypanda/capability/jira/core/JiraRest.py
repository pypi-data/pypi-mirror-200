from typing import List

from .JiraSession import JiraSession


class JiraRest:

    def __init__(self, jira_session: JiraSession):
        self.jira_session = jira_session
        self.endpoint = self.jira_session.server + "/rest/api/2"

    def request(self, method, path, *args, **kwargs):
        url = f"{self.endpoint}/{path}"
        return self.jira_session.request(method, url, *args, **kwargs)

    def iter_resource_page(self, method, path, page_size=50, **kwargs):
        start_at = 0
        max_results = page_size
        count = 0
        __next__ = True
        params = kwargs.pop("params", {})
        while __next__:
            params.update(dict(startAt=start_at, maxResults=max_results))
            paged_resource = self.request(method, path, params=params, **kwargs).json()
            count += len(paged_resource["issues"])
            for issue in paged_resource["issues"]:
                yield issue
            if count < paged_resource["total"]:
                start_at = start_at + max_results
                continue
            else:
                __next__ = False

    def jql_search(self, jql, fields="*all"):
        return self.iter_resource_page("get", "search", page_size=50, params=dict(fields=fields, jql=jql))

    def get_issue(self, issue_key, fields="*all", trim_null=True):
        data = self.request("get", f"issue/{issue_key}", params={"fields": fields}).json()
        if trim_null:
            fields_trim = filter(lambda x: x[1] is not None, data['fields'].items())
            data['fields'] = dict(fields_trim)
        return data

    # Change issue labels,will  force delete origin labels.
    def sync_issue_labels(self, issue_key, labels: List[str]):
        if not isinstance(labels, list):
            raise NotImplementedError("labels must be a list if str")
        return self.request("put", f"issue/{issue_key}", json=dict(fields={"labels": labels}))

    def get_issue_transition(self, issue_key_or_id):
        return self.request("get", f"issue/{issue_key_or_id}/transitions").json()

    # Todo Don't pass comment. It will causer jira 5xx.Not sure this is a bug from jira or my code.
    def do_issue_transition(self, issue_key_or_id, target_state_id, comment=None):
        payload = dict(transition={"id": target_state_id})
        if comment:
            payload["update"] = {"comment": [{"add": {"body": comment}}]}
        return self.request("post", f"issue/{issue_key_or_id}/transitions", json=payload)

    def get_entities(self, issue_key_or_id):
        __ = self.request("get", f"issue/{issue_key_or_id}/properties").json()["keys"]
        return [x["key"] for x in __]

    def get_entity(self, issue_key_or_id, name):
        return self.request("get", f"issue/{issue_key_or_id}/properties/{name}").json()["value"]

    def list_project_status(self, project_key_or_id):
        return self.request("get", f"project/{project_key_or_id}/statuses").json()

    """
    https://docs.atlassian.com/software/jira/docs/api/REST/8.13.0/#api/2/user-findUsers
    query via username or email or name
    """

    def search_user(self, query):
        users = self.request("get",
                             f"user/search?username={query}").json()
        return users

    def comment(self, issue_key, comment, visibility=None):
        """
        visibility: | 'default' | dict | None
        """
        data = {
            "body": comment,
        }
        if visibility == 'default':
            data['visibility'] = {
                "type": "role",
                "value": "Administrators"
            }
        elif isinstance(visibility, dict):
            data['visibility'] = visibility

        return self.request("post", f"/issue/{issue_key}/comment", json={
            "body": comment,
            "visibility": visibility
        })

    def list_comments(self, issue_key):
        return self.request("get", f"/issue/{issue_key}/comment").json()

    def list_issue_types(self):
        return self.request("get", '/issuetype').json()

    def create_issue(self, project_key, issue_type_id, summary, assignee_user_name=None, fields=None):
        _fields = {
            "project": {
                "key": project_key
            },
            "issuetype": {
                "id": str(issue_type_id)
            },
            "summary": summary
        }

        if assignee_user_name:
            _fields["assignee"] = {"name": assignee_user_name}

        if fields:
            _fields.update(fields)
        _ticket = self.request("post", "/issue", json=dict(fields=_fields)).json()
        return _ticket

    def list_sub_task(self, issue_key):
        return self.request("get", f"/issue/{issue_key}/subtask").json()
