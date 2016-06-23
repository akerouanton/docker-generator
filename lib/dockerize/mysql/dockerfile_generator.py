from jinja2 import Template
import os

def generate(config):
    with open(os.path.dirname(os.path.realpath(__file__)) + '/templates/Dockerfile.j2', 'r') as template:
        return Template(template.read()).render(version=config['version'])
