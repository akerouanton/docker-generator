from dockerize.file import File
import dockerize.elasticsearch.dockerfile_generator as generator

class Dockerfile(File):
    dev_plugins = [
        'royrusso/elasticsearch-HQ'
        # 'https://github.com/NLPchina/elasticsearch-sql/releases/download/2.3.3.0/elasticsearch-sql-2.3.3.0.zip'
    ]

    def __init__(self, version, plugins):
        self.config = {'version': version, 'plugins': plugins}

    def write(self, fp):
        fp.write(generator.generate(self.config))
