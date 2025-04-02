import requests
from openpyxl import Workbook
from concurrent.futures import ThreadPoolExecutor

JIRA_USERNAME = "narayanan.azhagappan@kone.com"
JIRA_API_TOKEN = os.getenv('JIRA_PASS')
PROJECTS = ["CHSS", "MODS", "NSS", "MATE", "CSCAI", "COTC"]
THREAD_POOL_SIZE = 1
BATCH_SIZE = 1000

def fetch_and_process_issues(project, worksheet):
    start_at = 0
    max_results = 1000
    total = 1

    while start_at < total:
        project_jql = f'project = "{project}" AND issuetype IN (Epic, Story, Bug, Task)'
        response = requests.get(
            JIRA_BASE_URL,
            auth=(JIRA_USERNAME, JIRA_API_TOKEN),
            headers={"Accept": "application/json"},
            params={"jql": project_jql, "startAt": start_at, "maxResults": max_results}
        )

        if response.status_code == 200:
            data = response.json()
            total = data.get("total", 0)
            issues = data.get("issues", [])
            print(f"[{project}] Total Issues Retrieved: {total}")
            print(f"[{project}] Processing batch from index: {start_at}")

            for issue in issues:
                process_issue(issue, worksheet)

            start_at += len(issues)
        else:
            print(f"Error fetching issues for project {project}: {response.status_code}")
            break

def process_issue(issue, worksheet):
    key = issue.get("key", "N/A")
    fields = issue.get("fields", {})
    project = fields.get("project", {}).get("name", "N/A")
    issue_type = fields.get("issuetype", {}).get("name", "N/A")
    status = fields.get("status", {}).get("name", "N/A")
    summary = fields.get("summary", "N/A")
    priority = fields.get("priority", {}).get("name", "N/A")
    created = fields.get("created", "N/A")
    team = fields.get("customfield_10001", {}).get("name", "N/A")
    sprint = fields.get("customfield_10020", {}).get("name", "N/A")
    assignee = fields.get("assignee", {}).get("displayName", "Unassigned")
    email_address = fields.get("assignee", {}).get("emailAddress", "N/A")
    tester = fields.get("customfield_10702", {}).get("displayName", "N/A")

    worksheet.append([
        key, project, issue_type, status, summary, priority, created,
        team, sprint, assignee, email_address, tester
    ])

def main():
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "JIRA Issues"
    worksheet.append([
        "Issue Key", "Project", "Issue Type", "Status", "Summary", "Priority",
        "Created", "Team", "Sprint", "Assignee", "Assignee Email", "Tester"
    ])

    with ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE) as executor:
        futures = [executor.submit(fetch_and_process_issues, project, worksheet) for project in PROJECTS]
        for future in futures:
            future.result()

    workbook.save("JIRA_Issues.xlsx")
    print("Data written to JIRA_Issues.xlsx successfully.")

if __name__ == "__main__":
    main()
