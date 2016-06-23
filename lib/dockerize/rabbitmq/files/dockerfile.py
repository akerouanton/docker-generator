from dockerize.file import File
import dockerize.rabbitmq.dockerfile_generator as generator

class Dockerfile(File):
    def __init__(self, version, plugins, config_file, tracing=False, tracing_directory=''):
        self.config = {
            'version': version,
            'plugins': plugins,
            'config_file': config_file,
            'tracing': tracing,
            'tracing_directory': tracing_directory
        }

    def write(self, fp):
        fp.write(generator.generate(self.config))
