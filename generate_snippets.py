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
  function_blacklist = ['mod_watch']

  for module, functions in state_info.items():
    for function in functions:
      for func, args in function.items():
        if func in function_blacklist:
          continue
        snippet_fname = f"{module}.{func}"
        snippet_path = os.path.join('Snippets/SaltStack', snippet_fname + '.sublime-snippet')
        content = {
          'module': module,
          'func': func,
          'args': args
        }
        if not os.path.exists(snippet_path):
          print(f"Generating basic {snippet_path}")
          with open(snippet_path, 'w') as f:
            snippet = render_template('snippet.j2', content)
            f.write(snippet)


def main():
  _gen_snippet()

if __name__ == "__main__":
  main()

