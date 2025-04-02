import os
import csv
from jira import JIRA

jira_server = "https://kone.atlassian.net"
jira_user = "narayanan.azhagappan@kone.com"
jira_pass = os.getenv('JIRA_PASS')

options = {'server': jira_server, 'rest_api_version': '3'}
jira_connect = JIRA(options=options, basic_auth=(jira_user, jira_pass))

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

# Fetch all fields
fields = jira_connect.fields()
field_names = [field['name'] for field in fields]
field_ids = [field['id'] for field in fields]

# Define the required field names
required_fields = ["project", "team", "sprint", "issuetype", "summary", "issuekey", "created", "updated", "assignee", "email", "tester", "status"]

# Filter the field names and ids to include only the required fields
filtered_field_names = [field for field in field_names if field.lower() in required_fields]
filtered_field_ids = [field_ids[field_names.index(field)] for field in filtered_field_names]

# Create directory if it doesn't exist
output_dir = 'C:/Users/k64152761/OneDrive - KONE Corporation/Documents/QADashboard/output'
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, 'extracted_issues.csv')

with open(output_file, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=filtered_field_names)
    writer.writeheader()

    for issue in issues:
        issue_detail = jira_connect.issue(issue.key)
        issue_data = {}
        for field, field_id in zip(filtered_field_names, filtered_field_ids):
            if field == "team":
                team_field = getattr(issue_detail.fields, 'customfield_10001', None)
                issue_data[field] = team_field.name if team_field else ''
            elif field == "sprint":
                sprint_field = getattr(issue_detail.fields, 'customfield_10020', None)
                issue_data[field] = sprint_field.name if sprint_field else ''
            else:
                issue_data[field] = getattr(issue_detail.fields, field_id, '')
        writer.writerow(issue_data)

print(f"Data written successfully to {output_file}")

# Print contents of Scripts directory
print("Contents of Scripts directory:")
print(os.listdir(output_dir))
