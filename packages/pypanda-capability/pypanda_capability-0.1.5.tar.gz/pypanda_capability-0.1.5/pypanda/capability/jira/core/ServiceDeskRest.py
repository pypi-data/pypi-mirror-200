from .JiraSession import JiraSession


class ServiceDeskRest:

    def __init__(self, jira_session: JiraSession):
        self.jira_session = jira_session
        self.endpoint = f"{self.jira_session.server}/rest/servicedeskapi"
        # Enable preview version api for SOP desk group type api
        self.jira_session.session.headers.setdefault("X-ExperimentalApi", "opt-in")

    def request(self, method, path, *args, **kwargs):
        url = f"{self.endpoint}/{path}"
        return self.jira_session.request(method, url, *args, **kwargs)

    def iter_resource_page(self, path, page_size=50, **kwargs):
        start = 0
        page_size = page_size
        __next__ = True
        params = kwargs.pop("params", {})

        while __next__:
            params.update(dict(start=start, limit=page_size))
            paged_resource = self.request("get", path, params=params, **kwargs).json()
            for value in paged_resource["values"]:
                yield value
            if paged_resource["isLastPage"] is False:
                start = start + page_size
                continue
            else:
                __next__ = False

    def get_aggregated_page(self, path, **kwargs):
        return list(self.iter_resource_page(path, **kwargs))

    def get_portal(self, project_key):
        return self.request("get", f"portals/project/{project_key}").json()

    def list_queues(self, desk_id):
        return self.get_aggregated_page(f"servicedesk/{desk_id}/queue")

    def get_queue(self, desk_id, queue_id):
        return self.request("get", f"servicedesk/{desk_id}/queue/{queue_id}").json()

    def get_request_type_groups(self, desk_id):
        return self.get_aggregated_page(f"servicedesk/{desk_id}/requesttypegroup")

    def get_request_types(self, desk_id):
        return self.get_aggregated_page(f"servicedesk/{desk_id}/requesttype")

    def get_request(self, id_or_key):
        return self.request("get", f"request/{id_or_key}").json()

    def comment_on_request(self, request_key_or_id, comment: str, public: bool = False) -> dict:
        return self.request("post", f"request/{request_key_or_id}/comment",
                            json=dict(body=comment, public=public)).json()

    def get_request_transition(self, request_key_or_id):
        return self.request("get", f"request/{request_key_or_id}/transition").json()

    def do_transition(self, request_key_or_id, target_state_id, comment=None):
        payload = dict(id=target_state_id)
        if comment:
            payload["additionalComment"] = {
                "body": "I have fixed the problem."
            }
        return self.request("post", f"request/{request_key_or_id}/transition", json=payload)

    def resolve_issue(self, request_key_or_id, comment="Resolved"):
        transitions = self.get_request_transition(request_key_or_id)

    def add_participants(self, request_key_or_id, usernames=None):
        participants = {
            "usernames": usernames
        }

        return self.request("post", f"request/{request_key_or_id}/participant", json=participants).json()

    def get_participants(self, request_key_or_id):
        return self.request("get", f"request/{request_key_or_id}/participant").json()

    def list_approvals(self, issue_key_or_id):
        return self.get_aggregated_page(f"request/{issue_key_or_id}/approval")

    def answer_approval(self, issue_key_or_id, approval_id, decision: str):
        """
        Parameters
        ----------
        issue_key_or_id: service desk key or id
        approval_id: approval_id get from list_approvals
        decision: approve or decline

        Returns
        -------

        """
        return self.request("post", f"request/{issue_key_or_id}/approval/{approval_id}", json={'decision': decision})
