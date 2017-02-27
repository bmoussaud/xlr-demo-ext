#
import httplib
import urllib
import base64
import string
from xml.dom.minidom import parse, parseString

#jiraID="JIRA-1239"
#satisfiesProperty="satisfiesChangeTicketNumber"
print "VERSION %s " % version
print "JIRA ID %s " % jiraID

xld_info = {'url':'http://localhost:4516','username':'admin','password':'admin'}
xld_request = HttpRequest(xld_info, 'admin', 'admin')
readResponse = xld_request.get("/deployit/repository/ci/Applications/%s" % version, contentType = 'application/xml')
dom = parseString(readResponse.response)

print "Actual State %s" % dom
versionci=dom.getElementsByTagName("udm.DeploymentPackage")[0]
nodeProperties=versionci.getElementsByTagName(satisfiesProperty)
if len(nodeProperties) > 0 :
    node = nodeProperties[0]
else:
    node = dom.createElement(satisfiesProperty)
    text = dom.createTextNode("DUMMY")
    node.appendChild(text)
    versionci.appendChild(node)

node.firstChild.replaceWholeText(jiraID)
updatedci=str(dom.toxml())
print "updated %s " % updatedci
updateResponse = xld_request.put("/deployit/repository/ci/Applications/%s" % version, updatedci,contentType = 'application/xml')




