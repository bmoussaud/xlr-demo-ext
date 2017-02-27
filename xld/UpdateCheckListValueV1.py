import httplib
import urllib
import base64
import string
from xml.dom.minidom import parse, parseString

#version="Applications/Java/PetPortal/3.0-CD-20140911-102023"
#satisfiesProperty="satisfiesReleaseNotes"

username="admin"
password="admin"
auth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
headers = {"Content-type": "application/xml", "Accept": "application/xml","Authorization":"Basic %s" % auth}
conn = httplib.HTTPConnection("localhost:4516")
conn.request("GET", "/deployit/repository/ci/Applications/%s" % version, "", headers)
response = conn.getresponse()
data = response.read()
dom = parseString(data)
print "Actual State %s" % dom
versionci=dom.getElementsByTagName("udm.DeploymentPackage")[0]

node=versionci.getElementsByTagName(satisfiesProperty)[0]
node.firstChild.replaceWholeText("true")
updatedci=str(dom.toxml())
print "New State %s" % updatedci

conn.request("PUT", "/deployit/repository/ci/Applications/%s" % version, updatedci, headers)
response = conn.getresponse()

conn.close()

