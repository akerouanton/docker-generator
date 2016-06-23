import os
from jinja2 import Template

def generate(config):
    with open(os.path.dirname(os.path.realpath(__file__)) + '/templates/rabbitmq.config.j2', "r") as template:
        return Template(template.read()).render(
            tracing=config['tracing'],
            tracing_directory=config['tracing_directory']
        )
