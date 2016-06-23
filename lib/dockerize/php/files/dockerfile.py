from dockerize.file import File
import dockerize.php.dockerfile_generator as dockerfile_generator
from dockerize.php.php_config import PhpConfig

class Dockerfile(File):
    def __init__(self, config):
        if not isinstance(config, PhpConfig):
            raise ValueError("config must be a PhpConfig instance.")
        self.config = config

    def write(self, fp):
        fp.write(dockerfile_generator.generate(self.config.normalize()))
