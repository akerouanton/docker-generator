import unittest
import types
from mock import Mock, MagicMock
from dockerize.config_parser.expectations import *

class TestLambdaExpectation(unittest.TestCase):
    def test_init(self):
        expectation = LambdaExpectation(lambda config, complete_key: True, "Error message")

        self.assertTrue(isinstance(expectation, LambdaExpectation))

    def test_true_expectation(self):
        callable = MagicMock(return_value=True)

        expectation = LambdaExpectation(callable, "Error message")
        expectation({}, "test")

        callable.assert_called_with({}, "test")

    def test_false_expectation(self):
        callable = MagicMock(return_value=False)
        expectation = LambdaExpectation(callable, "Error message")

        with self.assertRaises(ExpectationFailed) as cm:
            expectation({}, "test")

        callable.assert_called_with({}, "test")
        self.assertEqual(cm.exception.message, "Error message")

class TestTypeExpectation(unittest.TestCase):
    def test_init(self):
        expectation = TypeExpectation(types.DictType)
        self.assertTrue(isinstance(expectation, TypeExpectation))

    def test_right_type(self):
        expectation = TypeExpectation(types.DictType)
        expectation({"test": {}}, "test")

    def test_bad_type(self):
        expectation = TypeExpectation(types.DictType)
        with self.assertRaises(TypeExpectationFailed):
            expectation({"test": False}, "test")
