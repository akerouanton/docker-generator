from dockerize.file import File
import dockerize.rabbitmq.configfile_generator as generator

class ConfigFile(File):
    def __init__(self, tracing=False, tracing_directory=''):
        self.config = {
            'tracing': tracing,
            'tracing_directory': tracing_directory
        }

    def write(self, fp):
        fp.write(generator.generate(self.config))
