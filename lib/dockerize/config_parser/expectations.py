import node_visitor

class ExpectationFailed(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class TypeExpectationFailed(ExpectationFailed):
    def __init__(self, *args, **kwargs):
        ExpectationFailed.__init__(self, *args, **kwargs)

class LambdaExpectation(object):
    def __init__(self, expectation, message):
        self._expectation = expectation
        self._message = message

    def __call__(self, config, complete_key):
        if self._expectation(config, complete_key) is False:
            message = self._message(config, complete_key) if callable(self._message) else self._message
            raise ExpectationFailed(message)

class TypeExpectation(object):
    def __init__(self, expected_type):
        self.expected_type = expected_type

    def __call__(self, config, complete_key):
        node_type = type(node_visitor.get_node(config, complete_key))
        if node_type is not self.expected_type:
            raise TypeExpectationFailed(
                "Element %s is a %s, should be a %s." % (complete_key, node_type, self.expected_type)
            )
