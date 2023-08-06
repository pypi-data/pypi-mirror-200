from datetime import datetime, timezone
from typing import List

from .JiraSchema import IssueSchema, IssueTypeSchema
from .core.JiraFormRest import JiraFormRest
from .core.JiraRest import JiraRest
from .core.JiraSession import JiraSession


class JiraManager:
    def __init__(self, session: JiraSession):
        self.rest_client = JiraRest(jira_session=session)
        self.form_client = JiraFormRest(jira_session=session)

    def get_issue(self, issue_key):
        issue_data = self.rest_client.get_issue(issue_key)
        return self.parse_issue_data(issue_data)

    def get_issue_labels(self, issue_key) -> List[str]:
        return self.rest_client.get_issue(issue_key, fields="labels")["fields"]["labels"]

    # # Ensure issue labels, skip if existed already, append if not exists.And don't change origin labels.
    def ensure_issue_labels(self, issue_key, labels: List[str]):
        final_labels: List[str] = self.get_issue_labels(issue_key)
        for label in labels:
            if label not in final_labels:
                final_labels.append(label)
        return self.rest_client.sync_issue_labels(issue_key, final_labels)

    def change_issue_labels(self, issue_key, from_label, to_label):
        labels = self.get_issue_labels(issue_key)
        labels[labels.index(from_label)] = to_label
        return self.rest_client.sync_issue_labels(issue_key, labels)

    # Add/Switch/Remove tag status identified by two-level label
    # self.switch_pre_marked_label(xxx,label='A',mark="mark:")
    # will remove all label startswith "mark:", and then add label "mark:A"
    def sync_pre_marked_labels(self, issue_key, labels: List[str] = None, mark="AutomationStatus:"):
        labels = [] if labels is None else labels
        labels = [mark + label for label in labels]
        final_labels: List[str] = self.get_issue_labels(issue_key)
        for label in filter(lambda x: not x.startswith(mark), final_labels):
            labels.append(label)
        return self.rest_client.sync_issue_labels(issue_key, labels)

    def do_transition(self, issue_key_or_id, to_status, comment=None):
        status_mapping = {
            "Resolved": "https://jira.digital.ingka.com/rest/api/2/status/5",
            "Closed": "https://jira.digital.ingka.com/rest/api/2/status/6"
        }

        issue_transitions = self.rest_client.get_issue_transition(issue_key_or_id)["transitions"]
        done_transition = filter(lambda x: x["to"]["self"] == status_mapping.get(to_status),
                                 issue_transitions).__next__()
        return self.rest_client.do_issue_transition(issue_key_or_id, done_transition["id"], comment=comment)

    def resolve_issue(self, issue_key, comment="Resolved"):
        return self.do_transition(issue_key, "Resolved", comment=comment)

    def close_issue(self, issue_key, comment="Close"):
        return self.do_transition(issue_key, "Closed", comment=comment)

    @staticmethod
    def parse_issue_data(issue_data) -> IssueSchema:
        fields = issue_data["fields"]
        assignee = fields.get("assignee", None)
        if assignee:
            assignee = assignee.get("emailAddress")

        reporter = fields["reporter"]
        if reporter:
            reporter = reporter.get("emailAddress")
        issue_type = IssueTypeSchema(
            **fields["issuetype"]
        )

        LOCAL_TIMEZONE = datetime.now(timezone.utc).astimezone().tzinfo
        TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'
        created = datetime.strptime(fields["created"], TIME_FORMAT).astimezone(LOCAL_TIMEZONE)
        updated = datetime.strptime(fields["updated"], TIME_FORMAT).astimezone(LOCAL_TIMEZONE)

        return IssueSchema(
            issueKey=issue_data["key"],
            labels=fields["labels"],
            status=fields["status"]["name"],
            summary=fields.get("summary"),
            created=created,
            reporter=reporter,
            assignee=assignee,
            project=fields["project"]["key"],
            issueType=issue_type,
            updated=updated
        )

    def jql_search(self, jql, fields='*all'):
        issues = self.rest_client.jql_search(jql=jql, fields=fields)
        for issue_date in issues:
            yield self.parse_issue_data(issue_date)

    def get_forms(self, issue):
        forms = self.form_client.list_issue_forms(issue)
        form_qa = []
        for form in forms:
            questions = form['design']['questions']
            answers = form['state']['answers']
            qa_map = {}
            for k, v in answers.items():
                question_key = questions[k].get("questionKey")
                if not question_key:
                    question_key = k
                question_answer = answers[k]
                if __ := question_answer.get("text"):
                    # Answer is plain text
                    answer_value = __
                elif __ := question_answer.get("choices"):
                    # Answer is choices[single or multi]
                    answer_choice_options = questions[k]["choices"]
                    answer_selected_choice = __
                    answer_value = [y["label"] for y in
                                    filter(lambda x: x["id"] in answer_selected_choice, answer_choice_options)]
                elif __ := question_answer.get("users"):
                    answer_value = [x["name"] for x in __]
                elif __ is None:
                    answer_value = None
                else:
                    raise NotImplemented
                qa_map[question_key] = answer_value
            form_qa.append(qa_map)
        return form_qa

    def create_subtask(self, issue_key, summary, assignee_user_name=None, fields=None):
        _fields = {
            "parent": {
                "key": issue_key
            }
        }
        if fields:
            _fields.update(fields)
        issue_types = self.rest_client.list_issue_types()
        sub_task = filter(lambda x: x['subtask'] is True, issue_types).__next__()
        issue = self.get_issue(issue_key)
        return self.rest_client.create_issue(
            project_key=issue.project,
            assignee_user_name=assignee_user_name,
            issue_type_id=sub_task['id'],
            summary=summary,
            fields=_fields
        )
