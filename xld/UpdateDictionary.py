#
import httplib
import urllib
import base64
import string
from xml.dom.minidom import parse, parseString

def newEntryNode(dom,key,value):
    node = dom.createElement("entry")
    node.attributes['key']=key
    text = dom.createTextNode("DUMMY")
    node.appendChild(text)
    node.firstChild.replaceWholeText(value)
    return node



print "startPort %s " % startPort
print "endPort %s " % endPort
print "dictionaryId %s " % dictionaryId

xld_info = {'url':'http://localhost:4516','username':'admin','password':'admin'}
xld_request = HttpRequest(xld_info, 'admin', 'admin')
readResponse = xld_request.get("/deployit/repository/ci/%s" % dictionaryId, contentType = 'application/xml')
dom = parseString(readResponse.response)

print "Actual State %s" % dom
entries=dom.getElementsByTagName("entries")[0]
entries.appendChild(newEntryNode(dom,"startPort",startPort))
entries.appendChild(newEntryNode(dom,"endPort",endPort))

updatedci=str(dom.toxml())
print "updated %s " % updatedci
updateResponse = xld_request.put("/deployit/repository/ci/%s" % dictionaryId, updatedci,contentType = 'application/xml')




