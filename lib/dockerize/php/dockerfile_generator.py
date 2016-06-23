from dockerize.php.php_config import PhpConfig
from jinja2 import Template
import os

def generate(config):
    if not isinstance(config, PhpConfig):
        raise ValueError("config must be a PhpConfig instance.")

    with open(os.path.dirname(os.path.realpath(__file__)) + '/templates/Dockerfile.j2', 'r') as template:
        src_dir = config.src_dir.rstrip('/') + '/'
        packages = sorted(config.packages)
        php_extensions = sorted(config.php_extensions.keys())
        pecl_extensions = format_pecl_extensions(config.pecl_extensions)
        php_ini = format_php_ini(config.php_ini)
        php_fpm = format_php_fpm(config.php_fpm)

        return Template(template.read()).render(
            php_version=config.version,
            src_dir=src_dir,
            packages=packages,
            php_extensions=php_extensions,
            pecl_extensions=pecl_extensions,
            php_ini_configs=php_ini,
            php_fpm_configs=php_fpm,
            extra_steps=config.extra_steps,
            enable_xdebug=config.enable_xdebug
        )

def format_pecl_extensions(pecl_extensions):
    return sorted([extension if version == '*' else extension + '-' + version for extension, version in pecl_extensions.items()])

def format_php_ini(php_ini):
    return sorted([key + "=" + value for key, value in php_ini])

def format_php_fpm(php_fpm):
    return sorted([key + "=" + value for key, value in php_fpm])
