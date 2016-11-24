from dockerize.config_parser.transformers import LambdaTransformer
from dockerize.config_parser.node_visitor import get_node
from dockerize.file import DockerCompose
from dockerize.rabbitmq.files.dockerfile import Dockerfile
from dockerize.rabbitmq.files.configfile import ConfigFile

def tracing_directory_condition(config, complete_key):
    return get_node(config, "rabbitmq.tracing") is True and \
           get_node(config, "rabbitmq.tracing_directory") is ""

def build_config_parser(root):
    root['rabbitmq'].default(False).is_true(lambda config, key: root['rabbitmq'].apply_defaults())
    root['rabbitmq']['version'].string('3.1').one_of(['3.1', '3.6.1'])
    root['rabbitmq']['plugins'].list([])
    root['rabbitmq']['tracing'].bool(False)
    root['rabbitmq']['tracing_directory'].string('/var/log/rabbitmq/tracing').add_transformer(LambdaTransformer(
        lambda config, complete_key: root['rabbitmq']['tracing_directory'].apply_defaults(),
        tracing_directory_condition
    ))

def add_files(files, stack_config):
    if stack_config['rabbitmq'] is False:
        return

    version = stack_config['rabbitmq']['version']
    plugins = stack_config['rabbitmq']['plugins']

    if stack_config['dev']:
        tracing = stack_config['rabbitmq']['tracing']
        tracing_directory = stack_config['rabbitmq']['tracing_directory']

        dev_plugins =  plugins + \
                  ['rabbitmq_management', 'rabbitmq_management_visualiser'] + \
                  ['rabbitmq_tracing' if stack_config['rabbitmq']['tracing'] is True else None]

        files['docker/rabbitmq/Dockerfile-dev'] = Dockerfile(
            version,
            [plugin for plugin in dev_plugins if plugin is not None],
            'rabbitmq.dev.config',
            tracing_directory)
        files['docker/rabbitmq/rabbitmq.dev.config'] = ConfigFile(tracing, tracing_directory)

        files['docker/dev.yml'] = DockerCompose()
        files['docker/dev.yml']['rabbitmq'] = {
            'build': 'rabbitmq',
            'dockerfile': 'Dockerfile-dev',
            'restart': 'on-failure'}
    if stack_config['prod']:
        files['docker/rabbitmq/Dockerfile-prod'] = Dockerfile(version, plugins, 'rabbitmq.prod.config')
        files['docker/rabbitmq/rabbitmq.prod.config'] = ConfigFile()

        files['docker/prod.yml'] = DockerCompose()
        files['docker/prod.yml']['rabbitmq'] = {
            'build': 'rabbitmq',
            'dockerfile': 'Dockerfile-prod',
            'restart': 'on-failure'}
