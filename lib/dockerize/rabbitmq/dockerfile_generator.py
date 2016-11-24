import os
from jinja2 import Template

def generate(config):
    with open(os.path.dirname(os.path.realpath(__file__)) + '/templates/Dockerfile.j2') as template:
        return Template(template.read()).render(
            version=config['version'],
            plugins=sorted(config['plugins']),
            config_file=config['config_file'],
            tracing=config['tracing'],
            tracing_directory=config['tracing_directory'])
