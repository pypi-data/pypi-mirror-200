from .JiraSession import JiraSession


class JiraFormRest:
    """
    status: open(o) | locked(l) | submitted(s)
    locked and submitted status are both not allowed to be changed.
    locked means can only be reopened by project administrator
    submitted means can be reopened by non-administrator
    """

    def __init__(self, jira_session: JiraSession):
        self.jira_session = jira_session
        self.endpoint = f"{self.jira_session.server}/rest/proforma/api/2"

    def request(self, method, path, *args, **kwargs):
        url = f"{self.endpoint}/{path}"
        return self.jira_session.request(method, url, *args, **kwargs)

    def list_issue_forms(self, issue_key):
        return self.request('get', f"issues/{issue_key}/forms").json()

    def get_issue_form(self, issue_key, form_id):
        return self.request('get', f"issues/{issue_key}/forms/{form_id}").json()

    # Proforma api
    def unlock_form(self, issue_key, form_id):
        return self.request('put', f'issues/{issue_key}/forms/{form_id}/unlock')

    def reopen_form(self, issue_key, form_id):
        return self.request('post', f'issues/{issue_key}/forms/{form_id}', json={"status": "o"}).json()

    def submit_form(self, issue_key, form_id):
        return self.request('post', f'issues/{issue_key}/forms/{form_id}', json={"status": "l"}).json()
