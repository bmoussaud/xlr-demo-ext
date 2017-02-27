from com.xebialabs.xlrelease.plugin.git import GitClient
from org.eclipse.jgit.api import Git
from org.eclipse.jgit.transport import UsernamePasswordCredentialsProvider
from org.eclipse.jgit.transport import JschConfigSessionFactory
from org.eclipse.jgit.api import TransportConfigCallback
from org.eclipse.jgit.lib import Constants

import sys
import datetime
from string import Template

class MySshSessionFactory(JschConfigSessionFactory):
    def __init__ (self):
        JschConfigSessionFactory.__init__(self)

    def configure( self, host, session ):
        pass

class MyTransportConfigCallback(TransportConfigCallback):
    def __init__(self):
        TransportConfigCallback.__init__(self)

    def configure(self,transport):
        setSshSessionFactory = MySshSessionFactory()
        transport.setSshSessionFactory(setSshSessionFactory)

if gitRepository is None:
    print "No repository provided."
    sys.exit(1)

lsRemoteCommand = Git.lsRemoteRepository().setRemote(gitRepository['url']).setTags(False);
lsRemoteCommand.setTransportConfigCallback(MyTransportConfigCallback())

refs = lsRemoteCommand.call()
if branch:
    base = "%s%s" % (Constants.R_HEADS,branch)
else:
    base = Constants.HEAD



filtered_refs = filter(lambda ref: ref.getName() == base, refs)
if len(filtered_refs) == 0:
    raise "%s not found in %s " % (base,gitRepository['url'])
else:
    previousTriggerState = triggerState
    commitId = filtered_refs[0].getObjectId().getName()
    triggerState = "%s" % commitId
    triggeredDate = str(datetime.datetime.now())
    template_variable_customer = templateVariables["${customer}"]



#credentials = CredentialsFallback(gitRepository, username, password).getCredentials()
#client = GitClient(gitRepository['url'], branch, credentials['username'], credentials['password'])
#triggerState = "%s" % client.getLatestRevision()
#commitId = triggerState
#print "22222     commitId == %s " % commitId
