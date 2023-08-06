def render(template:str, data:dict) -> str:
  from jinja2 import Template
  return Template(open(template, 'r').read()).render(**data)