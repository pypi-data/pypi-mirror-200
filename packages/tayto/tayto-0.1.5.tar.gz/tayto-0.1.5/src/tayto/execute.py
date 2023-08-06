import sys, os
from tayto import linux

version = ''.join(sys.version.split('.')[:2])
home = os.getcwd()
path, mode, *_ = sys.argv[1:]
folder, filename, ext = linux.path_break(path)


if mode == 'exe':
  if ext == 'py':
    os.system(f'python3 {path}')
  elif ext == 'sh':
    os.system(f'chmod +x {path}')
    os.system(f'/usr/bin/bash {path}')
  elif ext == 'js':
    os.system(f'node {path}')
  elif ext == 'star':
    from starlark_go import Starlark
    Starlark().exec(open(path, 'r').read())

if mode == 'test': pass


