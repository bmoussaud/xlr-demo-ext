import sys, string
import com.xhaus.jyson.JysonCodec as json

if jiraServer is None:
    print "No server provided."
    sys.exit(1)

restUrl = "/rest/api/2/"
issueUrl = restUrl + "issue/" + issueId

# Check for ticket
request = HttpRequest(jiraServer, username, password)
#response = request.get(issueUrl, contentType = 'application/json')
#

print "Updated " + issueId + " in JIRA at " + jiraServer['url']
