import os
import csv
from jira import JIRA

jira_server = "https://kone.atlassian.net"
jira_user = "narayanan.azhagappan@kone.com"
jira_pass = os.getenv('JIRA_PASS')

jira_connect = JIRA(server=jira_server, basic_auth=(jira_user, jira_pass))

jira_projects = ["CHSS", "MODS", "NSS", "MATE", "CSCAI", "COTC"]

issues = []

try:
    for project in jira_projects:
        print(f"Processing project: {project}")
        issues += jira_connect.search_issues(f'project = "{project}" AND issuetype IN (Epic, Story, Bug, Task) AND sprint IN opensprints()')
    print("Connection Successful")
except Exception as e:
    print(f"Error connecting: {str(e)}")

# Fields to extract
jirafields = ["project", "team", "sprint", "issuetype", "summary", "issuekey", "created", "updated", "assignee", "email", "tester", "status"]

# Create directory if it doesn't exist
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, 'extracted_issues.csv')

with open(output_file, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=jirafields)
    writer.writeheader()

    for issue in issues:
        issue_detail = jira_connect.issue(issue.key)
        issue_data = {field: getattr(issue_detail.fields, field, '') for field in jirafields}
        writer.writerow(issue_data)

print(f"Data written successfully to {output_file}")
