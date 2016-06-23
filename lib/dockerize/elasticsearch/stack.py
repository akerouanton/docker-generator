from dockerize.file import DockerCompose
from dockerize.elasticsearch.files.dockerfile import Dockerfile

def build_config_parser(root):
    root['elasticsearch'].default(False).is_true(lambda config, complete_key: root['elasticsearch'].apply_defaults())
    root['elasticsearch']['version'].one_of(['2.1.0', '2.1.1', '2.1.2']).default('2.1.2')
    root['elasticsearch']['plugins'].list([])

def add_files(files, stack_config):
    if stack_config['elasticsearch'] is False:
        return

    version = stack_config['elasticsearch']['version']
    plugins = stack_config['elasticsearch']['plugins']

    if stack_config['dev']:
        files['docker/elasticsearch/Dockerfile-dev'] = Dockerfile(version, sorted(plugins + Dockerfile.dev_plugins))

        files['docker/dev.yml'] = DockerCompose()
        files['docker/dev.yml']['elasticsearch'] = {'build': 'elasticsearch', 'dockerfile': 'Dockerfile-dev'}
    if stack_config['prod']:
        files['docker/elasticsearch/Dockerfile-prod'] = Dockerfile(version, sorted(plugins))

        files['docker/prod.yml'] = DockerCompose()
        files['docker/prod.yml']['elasticsearch'] = {'build': 'elasticsearch', 'dockerfile': 'Dockerfile-prod'}
