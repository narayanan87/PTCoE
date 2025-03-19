import csv
from jira import JIRA

jira_server = "https://kone.atlassian.net"
jira_user = "narayanan.azhagappan@kone.com"
jira_pass = "ATATT3xFfGF0qlCQHF3zmK0eI4PLxpcgQU73Grnl4ZwpbigT_aoFuY_Q_E_2E6SqywrmoG5RGFiuyVpvnAO1q0jyarGAg3DZ9jCcYiuay-ZIPkcZyyx-sLK99dvIqFzb8px0Flye0E7c1xfaafFCOZKQB8AYB75fq_WD9-JN2FR7Tnr4bgQiB5o=52ECCA4A"

jira_connect = JIRA(server = jira_server, basic_auth = (jira_user, jira_pass))

jira_projects = jira.projects()
print("List of All Projects")

issues = []

try:
  issues = jira.search_issues("project = \"" + jira_projects + "\" AND issuetype IN (Epic, Story, Bug, Task)")
  print("Connection Successful")
except Exception as e:
  print("Error connecting: {str(e)}")

# Fields to extract
fields = ["project", "team", "sprint", "issueType", "summary", "issueKey", "created", "updated", "assignee", "E-Mail", "Tester", "status"]
