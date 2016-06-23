import copy

class PhpConfig:
    def __init__(self, version, src_dir, packages, pecl_extensions, php_extensions, php_ini, php_fpm, extra_steps, timezone='UTC', debug=False):
        self.version = version
        self.src_dir = src_dir
        self.packages = packages
        self.pecl_extensions = pecl_extensions
        self.php_extensions = php_extensions
        self.php_ini = php_ini
        self.php_fpm = php_fpm
        self.extra_steps = extra_steps
        self.timezone = timezone
        self.enable_xdebug = debug
        self.debug = debug

    def normalize(self):
        config = copy.deepcopy(self)

        if 'gmp' in config.php_extensions.keys():
            config.extra_steps['pre_exts'].append('ln -s /usr/include/x86_64-linux-gnu/gmp.h /usr/include/gmp.h')

        config.packages = config.packages + ['git', 'zlib1g-dev']

        config.php_extensions.update({'zip': '*'})

        config.php_ini = config.php_ini.items() + [("date.timezone", config.timezone), ("cgi.fix_pathinfo", "0")]
        config.php_ini = config.php_ini + [("extension", package+".so") for package in config.pecl_extensions.keys()]

        config.php_fpm = config.php_fpm.items() + [
            ("catch_worker_output", "yes"),
            ("user", "1000"),
            ("group", "1000"),
            ("request_terminate_timeout", "300")]

        return config

class PhpConfigFactory:
    PHP_EXTENSIONS = ['exif', 'gd', 'gmp', 'intl', 'mbstring', 'pcntl', 'pdo_mysql', 'zip']
    PECL_EXTENSIONS = ['amqp', 'memcache', 'memcached', 'sundown', 'xdebug']
    PACKAGES = {
        'gd': ['libgd3', 'libpng12-dev'],
        'gmp': ['libgmp-dev'],
        'memcached': ['libmemcachedd-dev'],
        'amqp': ['librabbitmq-dev'],
        'intl': ['libicu-dev'],
        'openssl': ['libssl-dev']
    }

    @staticmethod
    def create(php_config, debug=False):
        packages = php_config['packages'] + PhpConfigFactory._get_packages(php_config['exts'])
        pecl_extensions = PhpConfigFactory._get_pecl_extensions(php_config['exts'])
        php_extensions = PhpConfigFactory._get_php_extensions(php_config['exts'])

        return PhpConfig(
            php_config['version'],
            php_config['src_dir'],
            packages,
            pecl_extensions,
            php_extensions,
            php_config['php_ini'],
            php_config['php_fpm'],
            php_config['extra_steps'],
            php_config['timezone'],
            debug)

    @staticmethod
    def _get_packages(extensions):
        return [package for extension in extensions if extension in PhpConfigFactory.PACKAGES for package in PhpConfigFactory.PACKAGES[extension]]

    @staticmethod
    def _get_pecl_extensions(extensions):
        return {extension: version for extension, version in extensions.items() if extension in PhpConfigFactory.PECL_EXTENSIONS}

    @staticmethod
    def _get_php_extensions(extensions):
        return {extension: version for extension, version in extensions.items() if extension in PhpConfigFactory.PHP_EXTENSIONS}
