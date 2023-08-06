from deprecation import deprecated

from .JiraSchema import FreeFieldsSchema, IssueSchema, ServiceDeskRequestSchema
from .core.JiraSession import JiraSession
from .core.ServiceDeskRest import ServiceDeskRest


class ServiceDeskManager:
    def __init__(self, session: JiraSession):
        self.rest_client = ServiceDeskRest(jira_session=session)

    def get_issue_peered_request(self, issue: IssueSchema) -> IssueSchema:
        try:
            request_data = self.rest_client.get_request(issue.issueKey)
            issue.request = ServiceDeskRequestSchema(
                requestTypeId=request_data["requestTypeId"],
                serviceDeskId=request_data["serviceDeskId"],
                requestFieldValues=[]
            )
            for field in request_data["requestFieldValues"]:
                issue.request.requestFieldValues.append(FreeFieldsSchema.parse_obj(field))
        except AssertionError:
            issue.request = None
        return issue

    def get_queue(self, portal, queue_name):
        if isinstance(portal, int):
            portal_id = portal
        else:
            portal_id = self.rest_client.get_portal(portal)['id']

        queue_list = self.rest_client.list_queues(portal_id)
        try:
            return filter(lambda x: x['name'] == queue_name, queue_list).__next__()
        except StopIteration:
            return None

    @deprecated(details="Use get_active_approvals instead")
    def get_active_approval(self, issue_key):
        _active_approvals = self.get_active_approvals(issue_key)
        assert len(_active_approvals) == 1, f"Should only one active approval but got multi: {_active_approvals}"
        return _active_approvals[0]

    def get_active_approvals(self, issue_key):
        _approvals = self.rest_client.list_approvals(issue_key)
        _active_approvals = list(filter(lambda x: x['canAnswerApproval'] is True, _approvals))
        return _active_approvals

    def approve_or_declined(self, issue_key, approve_or_decline):
        _approval = self.get_active_approval(issue_key)
        assert self.rest_client.jira_session.username in [x['approver']['name'] for x in _approval[
            'approvers']], "service account is not in approver list"
        return self.rest_client.answer_approval(issue_key, _approval['id'], approve_or_decline)

    def approve_issue(self, issue_key):
        return self.approve_or_declined(issue_key, 'approve')

    def decline_issue(self, issue_key):
        return self.approve_or_declined(issue_key, 'decline')
