import json
from jenkins import Jenkins
from time import sleep

jenkins_config = {
    'job_name': 'trident-build',
    'job_token': '1234',
    'server': 'http://46.101.49.248:8080',
    'username': 'admin',
    'password': '114bf5b7e836118198feed83a13b9e46e1'
}

jenkins = Jenkins(jenkins_config['server'], jenkins_config['username'], jenkins_config['password'])


def start_trident_build():
    q_idx = jenkins.build_job(name=jenkins_config['job_name'], token=jenkins_config['job_token'])
    result = jenkins.get_queue_item(q_idx)
    print(json.dumps(result, indent=4))


def get_trident_last_build():
    last_build_item = jenkins.get_job_info(jenkins_config['job_name'])['lastBuild']
    return last_build_item['number'], last_build_item['url']


def has_build_in_queue():
    return jenkins.get_job_info(jenkins_config['job_name'])['queueItem'] is not None


def get_trident_build_result(number):
    build_info = jenkins.get_build_info(jenkins_config['job_name'], number)
    return build_info['result']


def can_find_queue_index(queue_index):
    queue_info = jenkins.get_queue_info()
    for queue_item in queue_info:
        if queue_item['id'] == queue_index:
            return True
    return False
