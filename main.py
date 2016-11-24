#!/usr/bin/env python

from yaml import load
import dockerize.config_parser.node_builder as node_builder
import dockerize.config_parser.node_visitor as node_visitor
from dockerize.file_collection import FileCollection
import dockerize.php.stack as php_stack
import dockerize.mysql.stack as mysql_stack
import dockerize.memcached.stack as memcached_stack
import dockerize.elasticsearch.stack as elasticsearch_stack
import dockerize.rabbitmq.stack as rabbitmq_stack

if __name__ == "__main__":
    components = [php_stack, mysql_stack, memcached_stack, elasticsearch_stack, rabbitmq_stack]

    with open("testing/stack.yml") as stack:
        for component in components:
            component.add_files(files, config)

        files.save_all('testing/')
