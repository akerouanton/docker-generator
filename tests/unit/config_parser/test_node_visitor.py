import unittest
from mock import Mock, MagicMock
import dockerize.config_parser.node_visitor as node_visitor
from pprint import pprint

class TestGetNode(unittest.TestCase):
    def test_get_node_should_return_the_given_element(self):
        self.assertEqual(
            node_visitor.get_node({"a": {"b": "c"}}, "a.b"),
            "c"
        )

    def test_get_node_should_raise_exception_if_the_node_does_not_exist(self):
        with self.assertRaises(node_visitor.ElementNotFoundException) as cm:
            node_visitor.get_node({}, "a.b")
        self.assertEqual(cm.exception.message, "Element \"a.b\" not found.")

class TestGetParent(unittest.TestCase):
    def test_get_parent_needs_a_compound_key(self):
        with self.assertRaises(TypeError) as cm:
            node_visitor.get_parent({}, "a")
        self.assertEquals(cm.exception.message, "You should provide a compound key.")

    def test_get_parent_returns_the_parent(self):
        self.assertEqual(
            node_visitor.get_parent({"a": {"b": "c"}}, "a.c"),
            {"b": "c"}
        )

    def test_get_parent_should_raise_exception_if_the_parent_does_not_exist(self):
        with self.assertRaises(node_visitor.ElementNotFoundException) as cm:
            node_visitor.get_parent({}, "a.b")
        self.assertEqual(cm.exception.message, "Element \"a\" not found.")

class TestApplyConfigBuilder(unittest.TestCase):
    def test_it_executes_expectations(self):
        expectation = MagicMock()

        config = {"a": {"b": "c"}, "d": "e"}
        config_builder = MagicMock()
        config_builder.expectations = [expectation]
        config_builder.complete_key = "a.b"
        node_visitor.apply_config_builder(config_builder, config)

        expectation.assert_called_with(config, "a.b")

    def test_it_executes_transformers(self):
        config = {"a": {"b": "c"}, "d": "e"}
        transformer = MagicMock(side_effect=self.set_true)

        config_builder = MagicMock()
        config_builder.transformers = [transformer]
        config_builder.complete_key = "a.b"
        node_visitor.apply_config_builder(config_builder, config)

        transformer.assert_called_with(config, "a.b")
        self.assertEqual(config, {"a": {"b": True}, "d": "e"})

    def set_true(self, config, complete_key):
        config["a"]["b"] = True

    def remove_nodes(self, config, complete_key):
        del config["a"]

    def test_it_stops_the_visit_if_the_node_does_not_exists(self):
        config_builder = MagicMock()
        config_builder.complete_key = "a"
        config_builder.children = MagicMock()
        config_builder.children.items = MagicMock()

        node_visitor.apply_config_builder(config_builder, {})
        self.assertFalse(config_builder.children.items.called)

    def test_it_visits_node_recursively(self):
        child_config_builder = MagicMock()
        root_config_builder = MagicMock()
        root_config_builder.complete_key = "a"
        root_config_builder.children.items = MagicMock(return_value=[("b", child_config_builder)])

        node_visitor.apply_config_builder(root_config_builder, {"a": {"b": "c"}})
        root_config_builder.children.items.assert_called_with()
        child_config_builder.children.items.assert_called_with()
