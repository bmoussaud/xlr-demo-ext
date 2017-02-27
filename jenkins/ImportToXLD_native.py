import httplib
import base64
import string
from xml.dom.minidom import parse, parseString
from com.xebialabs.xlrelease.domain.configuration import HttpConnection

#url="http://localhost:8080/view/List/job/PetPortal-build-only/ws/dar/target/PetPortal-3.0-CD-SNAPSHOT.dar"

xld_conn = HttpConnection({'url':'http://localhost:4516','username':'admin','password':'admin'})
xld_request = HttpRequest(xld_request, 'admin', 'admin')
url="%s/view/List/job/%s/ws/%s" % (jenkinsServer['url'], jobName, pathInWorkspace)
print "URL %s " % (url)

importReponse = xld_request.post("/deployit/package/fetch",url, contentType = 'application/xml')
if buildResponse.isSuccessful():
    dom = parseString(importResponse.response)
    version=dom.getElementsByTagName("udm.DeploymentPackage")[0]

#auth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
#headers = {"Content-type": "application/xml", "Accept": "application/xml","Authorization":"Basic %s" % auth}
#conn = httplib.HTTPConnection("localhost:4516")
#conn.request("POST", "/deployit/package/fetch", url, headers)
response = conn.getresponse()
print response
data = response.read()
print data
version=dom.getElementsByTagName("udm.DeploymentPackage")[0]
#[13:] remove /Applications...
packageVersion = version.attributes['id'].value[13:]
conn.close()
