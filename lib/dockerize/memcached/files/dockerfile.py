from dockerize.file import File
import dockerize.memcached.dockerfile_generator as generator

class Dockerfile(File):
    def __init__(self, version):
        self.config = {'version': version}

    def write(self, fp):
        fp.write(generator.generate(self.config))
