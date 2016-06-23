from abc import ABCMeta, abstractmethod
import node_visitor

class Transformer:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

class LambdaTransformer(Transformer):
    def __init__(self, transformer, condition=None):
        self._transformer = transformer
        self._condition = condition

    def __call__(self, config, complete_key):
        if callable(self._condition) and self._condition(config, complete_key) is False:
            return
        self._transformer(config, complete_key)

class ApplyDefaultsTransformer(Transformer):
    def __init__(self, node_builder, force=True):
        self.node_builder = node_builder
        self.force_defaults = force

    def __call__(self, config, complete_key):
        node = node_visitor.get_node(config, complete_key)

        if complete_key is not None:
            parent = node_visitor.get_parent(config, complete_key)
            partial_key = complete_key.split('.').pop()
            if self.force_defaults or not partial_key in parent:
                if len(self.node_builder.children) > 0:
                    parent[partial_key] = node = {}
                else:
                    parent[partial_key] = node = self.node_visitor.default_value

        if not isinstance(node, dict):
            return

        for name, child in self.node_builder.children.items():
            if name not in node:
                node[name] = child.default_value
