from dockerize.file import File
import os

class FileCollection(object):
    def __init__(self):
        self.files = {}

    def __setitem__(self, filename, file):
        if not isinstance(file, File):
            raise ValueError("You can only put File instances in the FileCollection.")
        if filename not in self.files:
            self.files[filename] = file

    def __getitem__(self, filename):
        if not filename in self.files:
            raise ValueError("File \"%s\" does not exists." % filename)
        return self.files[filename]

    def save_all(self, prefix):
        for filename, file in self.files.items():
            directory = os.path.dirname(prefix + filename)
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(prefix + filename, 'w') as fp:
                file.write(fp)
