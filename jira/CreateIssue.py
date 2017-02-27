import sys, string
import com.xhaus.jyson.JysonCodec as json

ISSUE_CREATED_STATUS = 201

content = """
{
    "fields": {
       "project":
       {
          "key": "%s"
       },
       "summary": "%s",
       "description": "%s",
       "issuetype": {
          "name": "%s"
       }
   }
}
""" % (project, title, description, string.capwords(issueType))

if jiraServer is None:
    print "No server provided."
    sys.exit(1)

jiraURL = jiraServer['url']
if jiraURL.endswith('/'):
    jiraURL = jiraURL[:len(jiraURL)-1]

request = HttpRequest(jiraServer, username, password)
#response = request.post('/rest/api/2/issue', content, contentType = 'application/json')

issueId = "JIRA-1973"
print "Created %s in JIRA at %s." % (issueId, jiraURL)
