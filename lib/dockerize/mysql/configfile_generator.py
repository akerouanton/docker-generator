from jinja2 import Template
import os

def generate(sql_mode):
    with open(os.path.dirname(os.path.realpath(__file__)) + '/templates/custom.cnf.j2', 'r') as template:
        return Template(template.read()).render(sql_mode=sql_mode)
