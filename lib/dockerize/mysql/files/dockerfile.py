import dockerize.file as file
import dockerize.mysql.dockerfile_generator as generator

class Dockerfile(file.File):
    def __init__(self, version):
        self.config = {'version': version}

    def write(self, fp):
        fp.write(generator.generate(self.config))
