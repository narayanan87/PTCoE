import csv
from jira import JIRA

jira_server = "https://kone.atlassian.net"
jira_user = "narayanan.azhagappan@kone.com"
jira_pass = ""

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

