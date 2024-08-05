#!/usr/local/bin/env python3

import salt.client
from jinja2 import Environment, FileSystemLoader
import os

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)

def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

def _gen_snippet():
  local = salt.client.Caller()
  state_info = local.cmd('baredoc.list_states')
  content = {
    'state_info': state_info
  }
  
  print(f"Generating basic saltstack.xml")
  with open('saltstack.xml', 'w') as f:
    snippet = render_template('intelij.j2', content)
    f.write(snippet)