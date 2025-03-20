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
        start_at = 0
        max_results = 50
        while True:
            batch = jira_connect.search_issues(
                f'project = "{project}" AND issuetype IN (Epic, Story, Bug, Task) AND sprint IN opensprints()',
                startAt=start_at,
                maxResults=max_results
            )
            if not batch:
                break
            issues.extend(batch)
            start_at += len(batch)
    print("Connection Successful")
except Exception as e:
    print(f"Error connecting: {str(e)}")

# Fields to extract
jirafields = ["project", "team", "sprint", "issuetype", "summary", "issuekey", "created", "updated", "assignee", "email", "tester", "status"]

# Create directory if it doesn't exist
output_dir = 'C:/Users/k64152761/OneDrive - KONE Corporation/Documents/QADashboard/output'
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, 'extracted_issues.csv')

with open(output_file, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=jirafields)
    writer.writeheader()

    for issue in issues:
        issue_detail = jira_connect.issue(issue.key)
        issue_data = {
            "project": issue_detail.fields.project.key,
            "team": issue_detail.fields.customfield_10001.name if hasattr(issue_detail.fields.customfield_10001, 'name') else '',
            "sprint": issue_detail.fields.customfield_10020[0].name if issue_detail.fields.customfield_10020 else '',
            "issuetype": issue_detail.fields.issuetype.name,
            "summary": issue_detail.fields.summary,
            "issuekey": issue.key,
            "created": issue_detail.fields.created,
            "updated": issue_detail.fields.updated,
            "assignee": issue_detail.fields.assignee.displayName if issue_detail.fields.assignee else '',
            "email": issue_detail.fields.assignee.emailAddress if issue_detail.fields.assignee else '',
            "tester": tester,
            "status": issue_detail.fields.status.name
        }
        writer.writerow(issue_data)

print(f"Data written successfully to {output_file}")

# Print contents of Scripts directory
print(os.listdir(output_dir))
