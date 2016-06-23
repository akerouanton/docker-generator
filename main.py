#!/usr/bin/env python

from yaml import load, dump
import dockerize.config_parser.node_builder as node_builder
import dockerize.config_parser.node_visitor as node_visitor
from dockerize.file_collection import FileCollection
import dockerize.php.stack as php_stack
import dockerize.mysql.stack as mysql_stack
import dockerize.memcached.stack as memcached_stack
import dockerize.elasticsearch.stack as elasticsearch_stack
import dockerize.rabbitmq.stack as rabbitmq_stack

if __name__ == "__main__":
    root = node_builder.NodeBuilder()
    root['dev'].bool(True)
    root['prod'].bool(False)

    components = [php_stack, mysql_stack, memcached_stack, elasticsearch_stack, rabbitmq_stack]

    for component in components:
        component.build_config_parser(root)

    with open("testing/stack.yml") as stack:
        config = load(stack.read())
        node_visitor.apply_config_builder(root, config)

        files = FileCollection()

        for component in components:
            component.add_files(files, config)

        files.save_all('testing/')
