from dockerize.memcached.files.dockerfile import Dockerfile
from dockerize.file import DockerCompose

def build_config_parser(root):
    root['memcached'].default(False).is_true(lambda config, complete_key: root['memcached'].apply_defaults())
    root['memcached']['version'].string('1.4.25').one_of(['1.4.25'])

def add_files(files, stack_config):
    if stack_config['memcached'] is False:
        return

    files['docker/memcached/Dockerfile'] = Dockerfile(stack_config['memcached']['version'])

    files['docker/common.yml'] = DockerCompose()
    files['docker/common.yml']['memcached'] = {'build': 'memcached', 'restart': 'on-failure'}

    if stack_config['dev']:
        files['docker/dev.yml'] = DockerCompose()
        files['docker/dev.yml']['memcached'] = {'extends': {'file': 'common.yml', 'service': 'memcached'}}
    if stack_config['prod']:
        files['docker/prod.yml'] = DockerCompose()
        files['docker/prod.yml']['memcached'] = {'extends': {'file': 'common.yml', 'service': 'memcached'}}
