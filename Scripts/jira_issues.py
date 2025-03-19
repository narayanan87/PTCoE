import os
import csv
from jira import JIRA

jira_server = "https://kone.atlassian.net"
jira_user = "narayanan.azhagappan@kone.com"
jira_pass = os.getenv('JIRA_PASS')

jira_connect = JIRA(server=jira_server, basic_auth=(jira_user, jira_pass))

jira_projects = jira_connect.projects()
print("List of All Projects")
for project in jira_projects:
    print(project.key)

issues = []

try:
    for project in jira_projects:
        issues += jira_connect.search_issues(f"project = \"{project.key}\" AND issuetype IN (Epic, Story, Bug, Task) AND sprint IN opensprints()")
    print("Connection Successful")
except Exception as e:
    print(f"Error connecting: {str(e)}")

# Fields to extract
jirafields = ["project", "team", "sprint", "issuetype", "summary", "issuekey", "created", "updated", "assignee", "email", "tester", "status"]

with open('C:/Users/k64152761/OneDrive - KONE Corporation/Documents/QADashboard/extracted_issues.csv', mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=jirafields)
    writer.writeheader()

    for issue in issues:
        issue_detail = jira_connect.issue(issue.key)
        issue_data = {field: getattr(issue_detail.fields, field, '') for field in jirafields}
        writer.writerow(issue_data)

print("Data written successfully to extracted_issues.csv")
