import sys

def get_name(ci_id):
    return ci_id.split('/')[-1]

def remove_first(ci_id):
    return "/".join(ci_id.split('/')[1:])

def add_task(version, env):
    print "Create a new task %s -> %s " % (version,env)
    phase = getCurrentPhase()
    current_task = getCurrentTask()
    task = taskApi.newTask("xldeploy.DeployTask")
    task.title = "Deploy %s -> %s" % (version, env)
    task.pythonScript.xldeployServer = current_task.getPythonScript().getProperty("server")
    task.pythonScript.deploymentPackage = version
    task.pythonScript.environment = env
    taskApi.addTask(phase.id, task)

def add_deploy_task(version, env):
    print "Create a xldeploy task %s -> %s " % (version,env)
    phase = getCurrentPhase()
    current_task = getCurrentTask()
    task = taskApi.newTask("xldeploy.Deploy")
    task.title = "Deploy %s to %s" % (remove_first(version), get_name(env))
    task.pythonScript.server = current_task.getPythonScript().getProperty("server")
    task.pythonScript.deploymentPackage = remove_first(version)
    task.pythonScript.deploymentEnvironment = remove_first(env)
    taskApi.addTask(phase.id, task)

def add_undeploy_task(deployed_application, env):
    print "Create a xldeploy undeploy %s -> %s " % (deployed_application,env)
    phase = getCurrentPhase()
    current_task = getCurrentTask()
    task = taskApi.newTask("xldeploy.UndeployTask")
    task.title = "Undeploy %s from %s" % (deployed_application, get_name(env))
    task.pythonScript.xldeployServer = current_task.getPythonScript().getProperty("server")
    task.pythonScript.deployedApplication = deployed_application
    task.pythonScript.environment = env
    taskApi.addTask(phase.id, task)


for key, value in deployments.iteritems():
    if undeploy:
        add_undeploy_task(key,value)
    else:
        add_deploy_task(key,value)

