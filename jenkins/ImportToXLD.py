import httplib
import base64
import string
from java.util import Map
from xml.dom.minidom import parse, parseString
from com.google.common.collect import Maps

#url="http://localhost:8080/view/List/job/PetPortal-build-only/ws/dar/target/PetPortal-3.0-CD-SNAPSHOT.dar"
#url=http://localhost:8080/           job/PetPortal-build-only/ws/dar/target/PetPortal-3.0-CD-SNAPSHOT.dar
xld_info = {'url':'http://localhost:4516','username':'admin','password':'admin'}
xld_request = HttpRequest(xld_info, 'admin', 'admin')
url="%s/job/%s/ws/%s" % (jenkinsServer['url'], jobName, pathInWorkspace)
print "URL %s " % (url)

importResponse = xld_request.post("/deployit/package/fetch",url, contentType = 'application/xml')
if importResponse.isSuccessful():
    doc = parseString(importResponse.response)
    version=doc.getElementsByTagName("udm.DeploymentPackage")[0]
    #[13:] remove /Applications...
    packageVersion = version.attributes['id'].value[13:]
    sys.exit(0)
else:
    print "Error when importing"
    print importResponse.response
    sys.exit(1)


