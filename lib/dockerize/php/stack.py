from dockerize.php.php_config import *
from dockerize.php.files.dockerfile import Dockerfile
from dockerize.file import DockerCompose

def build_config_parser(root):
    root['php'].default(False).is_true(lambda config, key: root['php'].apply_defaults())
    root['php']['version'].string('7.0-fpm')
    root['php']['packages'].list([])
    root['php']['php_ini'].dict({})
    root['php']['php_fpm'].dict({})
    root['php']['timezone'].string('Europe/Paris')
    root['php']['src_dir'].regex('^/.+').default('/usr/src/app')
    root['php']['exts'].dict({})
    root['php']['extra_steps'].dict({})
    root['php']['extra_steps']['pre_apt'].list([])
    root['php']['extra_steps']['pre_exts'].list([])
    root['php']['extra_steps']['pre_config'].list([])
    root['php']['extra_steps']['pre_composer'].list([])
    root['php']['extra_steps']['pre_copy'].list([])

def add_files(files, stack_config):
    if stack_config['php'] is False:
        return

    if stack_config['dev']:
        files['docker/php/Dockerfile-dev'] = Dockerfile(PhpConfigFactory.create(stack_config['php'], True))

        files['docker/dev.yml'] = DockerCompose()
        files['docker/dev.yml']['php'] = {'build': '..', 'dockerfile': 'docker/php/Dockerfile-dev'}

    if stack_config['prod']:
        files['docker/php/Dockerfile-prod'] = Dockerfile(PhpConfigFactory.create(stack_config['php'], False))

        files['docker/prod.yml'] = DockerCompose()
        files['docker/prod.yml']['php'] = {'build': '..', 'dockerfile': 'docker/php/Dockerfile-prod'}
