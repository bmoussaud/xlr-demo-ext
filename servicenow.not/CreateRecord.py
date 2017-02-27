#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time
import com.xhaus.jyson.JysonCodec as json

print "CREATE RECORD...."

RECORD_CREATED_STATUS = 201

if servicenowServer is None:
    print "No server provided."
    sys.exit(1)

servicenowUrl = servicenowServer['url']

credentials = CredentialsFallback(servicenowServer, username, password).getCredentials()
content = """
{"short_description":"%s","comments":"%s"}
""" % (shortDescription, comments)


print "Sending content %s" % content

servicenowAPIUrl = servicenowUrl + '/api/now/v1/table/' + tableName

#servicenowResponse = XLRequest(servicenowAPIUrl, 'POST', content, credentials['username'], credentials['password'], 'application/json').send()

sysId = "SYSID"+str(time.time())
print "Created %s in Service Now." % (sysId)

