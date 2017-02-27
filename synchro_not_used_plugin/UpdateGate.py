import sys

from com.xebialabs.deployit.plugin.api.reflect import Type
from com.xebialabs.xlrelease.api.v1.forms import Condition

def get_gate_task(task_name):
     return taskApi.searchTasksByTitle(task_name,None,release.id)[0]

def new_dependency(release_name,phase_name, task_name):
    print "* Dependency is %s/%s/%s" % (release_name,phase_name, task_name)
    master_release = releaseApi.searchReleasesByTitle(release_name)[0]
    result = taskApi.searchTasksByTitle(task_name, phase_name, master_release.id)
    target = result[0]
    return target

task = get_gate_task(gateTaskName)
print "* Gate task is %s" % task.title
target = new_dependency(masterReleaseName,masterPhaseName, masterTaskName)
taskApi.addDependency(task.id, target.id)

if addAConditionInTheMasterRelease:
    condition = Condition()
    condition.title = "Check If the '%s' release is ready" % release.title
    if len([i for i in target.conditions if i.title == condition.title]) > 0:
        print "* '%s' is already in the conditions" % condition.title
    else:
        print "* add the '%s' in the condition condition" % condition.title
        taskApi.addCondition(target.id,condition)






