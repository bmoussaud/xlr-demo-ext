import httplib
import urllib
import base64
import string
from xml.dom.minidom import parse, parseString

#version="Applications/Java/PetPortal/3.0-CD-20140911-102023"
#satisfiesProperty="satisfiesReleaseNotes"

xld_info = {'url':'http://localhost:4516','username':'admin','password':'admin'}
xld_request = HttpRequest(xld_info, 'admin', 'admin')

readResponse = xld_request.get("/deployit/repository/ci/Applications/%s" % version, contentType = 'application/xml')

dom = parseString(readResponse.response)
print "Actual State %s" % dom
versionci=dom.getElementsByTagName("udm.DeploymentPackage")[0]

node=versionci.getElementsByTagName(satisfiesProperty)[0]
node.firstChild.replaceWholeText("true")
updatedci=str(dom.toxml())
print "New State %s" % updatedci

updateResponse = xld_request.put("/deployit/repository/ci/Applications/%s" % version, updatedci,contentType = 'application/xml')

