from jira import JiraServer

jira = JiraServer(jiraServer, username, password)

#issues = jira.query(query)
issues = {'PET-45':'Fix the color on the main page','PET-47':'Performance issues','PET-56':'Fix NPE'}
