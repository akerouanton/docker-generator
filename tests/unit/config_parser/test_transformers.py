import unittest
from mock import MagicMock, patch
from dockerize.config_parser.transformers import *

class TestLambdaTransformer(unittest.TestCase):
    def test_init(self):
        transformer = LambdaTransformer(lambda config, complete_key: True)
        self.assertTrue(isinstance(transformer, LambdaTransformer))

    def test_transformation_is_applied_when_no_condition_specified(self):
        config = {"a": {"b": "c"}}

        callable = MagicMock(side_effect=lambda config, complete_key: config['a'].__setitem__("b", True))
        transformer = LambdaTransformer(callable)
        transformer(config, "a.b")

        callable.assert_called_with(config, "a.b")
        self.assertEqual(config, {"a": {"b": True}})

    def test_transformation_is_not_applied_when_condition_is_not_met(self):
        config = {"a": {"b": "c"}}

        callable = MagicMock()
        condition = MagicMock(return_value=False)
        transformer = LambdaTransformer(callable, condition)
        transformer(config, "a.b")

        condition.assert_called_with(config, "a.b")
        callable.assert_not_called()
        self.assertEqual(config, {"a": {"b": "c"}})

    def test_transformation_is_applied_when_condition_is_met(self):
        config = {"a": {"b": "c"}}

        callable = MagicMock(side_effect=lambda config, complete_key: config['a'].__setitem__("b", True))
        condition = MagicMock(return_value=True)
        transformer = LambdaTransformer(callable, condition)
        transformer(config, "a.b")

        condition.assert_called_with(config, "a.b")
        callable.assert_called_with(config, "a.b")
        self.assertEqual(config, {"a": {"b": True}})

class TestApplyDefaultsTransformer(unittest.TestCase):
    @patch('dockerize.config_parser.node_builder.NodeBuilder')
    def test_init(self, node_builder):
        transformer = ApplyDefaultsTransformer(node_builder)
        self.assertTrue(isinstance(transformer, ApplyDefaultsTransformer))
