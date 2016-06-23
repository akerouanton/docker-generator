import dockerize.file as file
import dockerize.mysql.configfile_generator as generator

class ConfigFile(file.File):
    def __init__(self, sql_mode):
        self.sql_mode = sql_mode

    def write(self, fp):
        fp.write(generator.generate(self.sql_mode))
