import types
import re
from expectations import *
from transformers import *
import node_visitor

class NodeBuilder(object):
    def __init__(self):
        self.children = {}
        self.expectations = []
        self.transformers = [ApplyDefaultsTransformer(self, force=False)]
        self.complete_key = None

    def __getitem__(self, item):
        if not item in self.children:
            self.children[item] = ChildNodeBuilder(item, self)
        return self.children[item]

    def __setitem__(self, key, value):
        raise NotImplementedError("You can't set a NodeBuilder.")

# @TODO: Add "all_in" expectation
class ChildNodeBuilder(NodeBuilder):
    def __init__(self, key, parent):
        super(ChildNodeBuilder, self).__init__()
        self.complete_key = parent.complete_key + "." + key if parent.complete_key is not None else key
        self.default_value = None

    def is_true(self, transformer):
        self.transformers.append(LambdaTransformer(
            transformer,
            lambda config, key: node_visitor.get_node(config, key) is True)
        )
        return self

    def not_exists(self, transformer):
        self.transformers.append(LambdaTransformer(
            transformer,
            lambda config, key: not key.split('.').pop() in node_visitor.get_parent(config, key)
        ))
        return self

    def default(self, default_value):
        self.default_value = default_value
        return self

    def is_type(self, type, default_value=None):
        if default_value is not None:
            self.default_value = default_value

        self.expectations.append(TypeExpectation(type))
        return self

    def bool(self, default=None):
        return self.is_type(types.BooleanType, default)

    def string(self, default=None):
        return self.is_type(types.StringType, default)

    def dict(self, default=None):
        return self.is_type(types.DictType, default)

    def list(self, default=None):
        return self.is_type(types.ListType, default)

    def one_of(self, valid_values):
        self.expectations.append(LambdaExpectation(
            lambda config, key: node_visitor.get_node(config, key) in valid_values,
            lambda config, key: "Invalid value for %s, \"%s\" provided. Expected values are: %s." %
                                (self.complete_key, node_visitor.get_node(config, key), ', '.join(valid_values))
        ))
        return self

    def regex(self, regex):
        self.is_type(types.StringType)
        self.expectations.append(LambdaExpectation(
            lambda config, key: re.search(regex, node_visitor.get_node(config, key)) is not None,
            "Value %s should match regex \"%s\"." % (self.complete_key, regex)
        ))
        return self

    def apply_defaults(self, force=True):
        self.transformers.append(ApplyDefaultsTransformer(self, force))

    def add_transformer(self, transformer):
        if not isinstance(transformer, Transformer):
            raise ValueError("You should provide a Transformer instrance.")
        self.transformers.append(transformer)
