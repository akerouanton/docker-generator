from dockerize.file import DockerCompose
from dockerize.mysql.files.configfile import ConfigFile
from dockerize.mysql.files.dockerfile import Dockerfile

def build_config_parser(root):
    root['mysql'].default(False).is_true(lambda config, key: root['mysql'].apply_defaults())
    root['mysql']['version'].string('5.7.10').one_of(['5.7.10'])
    root['mysql']['sql_mode'].list([])

def add_files(files, stack_config):
    if stack_config['mysql'] is False:
        return

    files['docker/mysql/Dockerfile'] = Dockerfile(stack_config['mysql']['version'])
    files['docker/mysql/custom.cnf'] = ConfigFile(stack_config['mysql']['sql_mode'])

    files['docker/common.yml'] = DockerCompose()
    files['docker/common.yml']['mysql'] = {'build': 'mysql', 'restart': 'on-failure'}

    if stack_config['dev']:
        files['docker/dev.yml'] = DockerCompose()
        files['docker/dev.yml']['mysql'] = {'extends': {'file': 'common.yml', 'service': 'mysql'}}
    if stack_config['prod']:
        files['docker/prod.yml'] = DockerCompose()
        files['docker/prod.yml']['mysql'] = {'extends': {'file': 'common.yml', 'service': 'mysql'}}
