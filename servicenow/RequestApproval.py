#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time
import com.xhaus.jyson.JysonCodec as json

RECORD_CHECK_STATUS = 200
RECORD_CREATED_STATUS = 201

if servicenowServer is None:
    print "No server provided."
    sys.exit(1)

servicenowUrl = servicenowServer['url']

credentials = CredentialsFallback(servicenowServer, username, password).getCredentials()
content = """
{"short_description":"%s","description":"%s","category":"XLDeploy","u_supporting_service":"Exchange Support","assignment_group":"Global Software Change Group","justification":"XLDeploy","requested_by_date":"08-08-2014"}
""" % (shortDescription, description)

print "Sending content %s" % content

servicenowAPIUrl = servicenowUrl + '/api/now/table/change_request'

sysId = "SYSID"+str(System.currentTimeMillis())
print "Created %s in Service Now." % (sysId)
sys.exit(1)

# Start query for approval
servicenowAPIUrl = servicenowUrl + '/api/now/table/change_request/' + sysId

approval = True
content = None

while(approval):
  status = "approved"
  print "Found %s in Service Now." % (status)
  if "approved" == status:
    approval = False
    print "ServiceNow approval received."
  elif "rejected" == status:
    print "Failed to get approval from ServiceNow"
    sys.exit(1)
  else:
    time.sleep(5) 
