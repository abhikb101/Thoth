import os
from jira import JIRA
JiraApiKey = os.getenv("JIRA_API_KEY")
jiraOptions = {'server': "https://venlabs.atlassian.net/"}
JiraEmail = os.getenv("JIRA_EMAIL")

jira = JIRA(options=jiraOptions, basic_auth=(JiraEmail, JiraApiKey))

issue_dict = {
    'project': {'key': 'VEN'},
    'summary': '',
    'description': '',
    'issuetype': {'name': 'Bug'},
}

def create_jira(prompt):
    issue_dict['summary'] = prompt
    issue_dict['description'] = prompt
    new_issue = jira.create_issue(fields=issue_dict)

def is_jira_issue_intent(prompt):
    if "jira" in prompt.lower():
        return True
    return False
