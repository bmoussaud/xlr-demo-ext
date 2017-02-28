from xldcommunicator import xldeploy
import sys
import string

standalone_test = False

def map_as_markdown_table(col1, col2, a_map):
    header = ["|{0}|{1}|".format(col1,col2),"| --- |---|"]
    return "\n".join(header+["|{0}|{1}|".format(key,value) for key, value in a_map.iteritems()])


def deployed_versions(env):
    return map(lambda deployed_app:repository.read(deployed_app.version) ,repository.mread(repository.search('udm.DeployedApplication',env)))

def deployed_application(ci_id):
    return repository.search('udm.DeployedApplication',ci_id)

def read_and_check_type(ci_id,ci_type):
    ci = repository.read(ci_id)
    if not ci.type == ci_type:
        raise "{0} is not {1} but {1}".format(ci_id,ci_type, ci.type)
    return ci


def target_env(envs,app_id):
    for env in envs:
        versions = deployed_versions(env.id)
        apps = filter(lambda v : v.application == app_id, versions)
        if len(apps) == 1:
            return env
    return None

def compute_deployments(source_env_id,dest_env_id):
    deployments = {}
    source = read_and_check_type(source_env_id, 'udm.Environment')
    destination = read_and_check_type(dest_env_id, 'udm.Environment')
    destination_deployed_application_ids = deployed_versions(destination.id)
    for deployed_version in deployed_versions(source.id):
        deployments[deployed_version.id] = destination.id
    return deployments

def compute_undeployments(source_env_id,dest_env_id):
    undeployments = {}
    source = read_and_check_type(source_env_id, 'udm.Environment')
    destination = read_and_check_type(dest_env_id, 'udm.Environment')
    for deployed_app_id in deployed_application(destination.id):
        deployed_application_name = deployed_app_id.split('/')[-1]
        source_deployed_application_id = "{0}/{1}".format(source.id,deployed_application_name)
        if repository.exists(source_deployed_application_id):
            continue
        undeployments[deployed_application_name]=dest_env_id


    return undeployments


if standalone_test:
    server={'url':'http://localhost:4516','username':'admin','password':'admin'}
    source='Environments/Dev/Tomcat-Dev'
    destination='Environments/Dev/Tomcat-Test'

cli = xldeploy.XLDeployCommunicator(server['url'], server['username'], server['password'])
repository = xldeploy.RepositoryService(cli)
deployments = compute_deployments(source,destination)
print map_as_markdown_table("Version","Environment",deployments)
print "\n"
undeployments = compute_undeployments(source,destination)
print map_as_markdown_table("Application","Environment",undeployments)
print "\n"
