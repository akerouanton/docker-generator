#!/usr/bin/env python

import json, re
from jinja2 import Template

PHP_EXTENSIONS = ['exif', 'gd', 'gmp', 'intl', 'mbstring', 'pcntl', 'pdo_mysql', 'zip']
PECL_EXTENSIONS = ['amqp', 'memcache', 'sundown', 'xdebug']
PACKAGES = {
        'gd': ['libgd3', 'libpng12-dev'],
        'gmp': ['libgmp-dev'],
        'memcache': ['libmemcached-dev'],
        'amqp': ['librabbitmq-dev'],
        'intl': ['libicu-dev'],
        'openssl': ['libssl-dev']
}

def get_version(constraint):
    return (re.search('(\d.\d+|\w+)', constraint).group(0) if re.search('\d.\d+', constraint) is not None else None)

def extract_required_exts(composer_json):
    return {package[4:]: version for package, version in composer_json['require'].items() if package.startswith('ext-')}

def extract_php_version(composer_json):
    return [get_version(version) for package, version in composer_json['require'].items() if package == 'php' and get_version(version) is not None].pop()

def get_php_exts(required_exts):
    return {package: version for package, version in required_exts.items() if package in PHP_EXTENSIONS}

def get_pecl_packages(required_exts):
    return {package: version for package, version in required_exts.items() if package in PECL_EXTENSIONS}

def is_xdebug_required(composer_json):
    return True

def format_pecl_package_names(pecl_packages):
    return [package if version == '*' else package + '-' + version for package, version in pecl_packages.items()]

def get_packages(extensions):
    return [package for extension in extensions if extension in PACKAGES for package in PACKAGES[extension]]

def get_pecl_extension_declarations(pecl_packages):
    return ["extension=%s.so" % package for package in pecl_packages]

composer_json = json.loads(open('composer.json', 'r').read())
required_exts = extract_required_exts(composer_json)

src_dir = '/usr/src/app'
php_version = extract_php_version(composer_json)
custom_php_exts = get_php_exts(required_exts)
custom_pecl_packages = get_pecl_packages(required_exts)

packages = ['git', 'zlib1g-dev'] + get_packages(required_exts)
php_extensions = ['zip'] + custom_php_exts.keys()
pecl_packages = format_pecl_package_names(custom_pecl_packages)
php_ini_configs = [
    "date.timezone=Europe/Paris",
    "cgi.fix_pathinfo=0",
] + get_pecl_extension_declarations(custom_pecl_packages)
php_fpm_configs = [
    "catch_worker_output = yes",
    "user = 1000",
    "group = 1000",
    "request_terminate_timeout = 300"
]

php_dockerfile = Template(open('Dockerfile-php.j2', 'r').read()).render(
    php_version=php_version,
    src_dir=src_dir.rstrip('/') + '/',
    packages=sorted(packages),
    php_extensions=sorted(php_extensions),
    pecl_packages=sorted(pecl_packages),
    php_ini_configs=sorted(php_ini_configs),
    php_fpm_configs=sorted(php_fpm_configs),
    pre_ext_install='ln -s /usr/include/x86_64-linux-gnu/gmp.h /usr/include/gmp.h',
    enable_xdebug=is_xdebug_required(composer_json)
)

open('Dockerfile', 'w').write(php_dockerfile)
