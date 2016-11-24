from abc import ABCMeta, abstractmethod
from pyaml import safe_dump as dump

class File:
    __metaclass__ = ABCMeta

    @abstractmethod
    def write(self, fp):
        pass

class DockerCompose(File):
    def __init__(self):
        self.services = {}

    def __setitem__(self, service, definition):
        self.services[service] = definition

    def __getitem__(self, service):
        if not service in self.services:
            self.services[service] = {}
        return self.services[service]

    def write(self, fp):
        dump(self.services, fp)
