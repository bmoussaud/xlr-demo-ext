from jira import JiraServer

if not jiraServer:
    raise Exception("JIRA server ID must be provided")
if not username:
    username = jiraServer["username"]
if not password:
    password = jiraServer["password"]

jira = JiraServer(jiraServer, username, password)
#issues = jira.queryIssues(query)

issues = {'PET-45':'Fix the color on the main page','PET-47':'Performance issues','PET-56':'Fix NPE'}
data = issues
