from .config_parser.node_builder import NodeBuilder
from .config_parser.node_visitor import apply_config_parser
from .file_collection import FileCollection
import yaml
from abc import ABCMeta, abstractmethod

class Stack(object):
    def __init__(self, root_dir, filename='stack.yml'):
        self.root_dir = root_dir.rstrip('/')
        self.filename = filename
        self.modules = []

    def register_module(self, module):
        if not isinstance(module, StackModule):
            raise ValueError("You should provide a StackModule instance.")
        elif module in self.modules:
            raise ValueError("You can't add the same module twice.")

        self.modules.append(module)

    def generate(self):
        root = NodeBuilder()
        root['dev'].bool(True)
        root['prod'].bool(False)

        for module in self.modules:
            module.build_config_parser(root)

        with open('%s/%s' % (self.root_dir, self.filename)) as config_file:
            config = yaml.load(config_file.read())
            apply_config_parser(root, config)

            files = FileCollection()
            for module in self.modules:
                module.add_files(files, config)

            files.save_all(self.root_dir + '/')

class StackModule(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def build_config_parser(self, root):
        pass

    @abstractmethod
    def add_files(self, files, stack_config):
        pass
