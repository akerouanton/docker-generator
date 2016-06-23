#!/usr/bin/env python

from node_builder import *
from pprint import pprint
from yaml import load

if __name__ == '__main__':
    root = NodeBuilder()
    root['dev'].bool(True)
    root['prod'].bool(False)

    root['php'].default(False).is_true(lambda config, key: root['php'].apply_defaults())
    root['php']['version'].string('7.0-fpm').one_of(['5.6-fpm', '7.0-fpm'])
    root['php']['packages'].list([])
    root['php']['php_ini'].dict({})
    root['php']['php_fpm'].dict({})
    root['php']['timezone'].string('Europe/Paris')
    root['php']['src_dir'].regex('^/.+').default('/usr/src/app')
    root['php']['exts'].dict({})
    root['php']['extra_steps'].dict({})
    root['php']['extra_steps']['pre_apt'].list([])
    root['php']['extra_steps']['pre_exts'].list([])
    root['php']['extra_steps']['pre_config'].list([])
    root['php']['extra_steps']['pre_composer'].list([])
    root['php']['extra_steps']['pre_copy'].list([])

    root['mysql'].default(False).is_true(lambda config, key: root['mysql'].apply_defaults())
    root['mysql']['version'].string('5.7.10').one_of(['5.7.10'])
    root['mysql']['sql_mode'].list([])

    root['memcached'].default(False)

    root['elasticsearch'].default(False).is_true(lambda config, key: root['elasticsearch'].apply_defaults())
    root['elasticsearch']['version'].one_of(['2.1.0', '2.1.1', '2.1.2']).default('2.1.2')

    root['rabbitmq'].default(False).is_true(lambda config, key: root['rabbitmq'].apply_defaults())

    visitor = NodeVisitor()

    with open('../examples/simple_stack/stack.yml') as stack_file:
        stack = load(stack_file.read())
        visitor.execute(root, stack)

        pprint(stack)
