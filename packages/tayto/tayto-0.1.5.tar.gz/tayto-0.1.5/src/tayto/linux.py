from os import system
from uuid import uuid4

def exe(code:str) -> str:
  import subprocess
  return subprocess.Popen(code.split(' '), stdout=subprocess.PIPE).communicate()[0].decode('UTF-8')[:-1]

def bash(code:str) -> None:
  sh = f'/tmp/{uuid4()}.sh'
  tmp_file = open(sh, 'w')
  tmp_file.write('#!/usr/bin/bash\n' + code)
  tmp_file.close()
  system(f'chmod +x {sh}')
  system(sh)
  system(f'rm -f {sh}')

def ssh(host:str, code:str) -> None:
  sh = f'/tmp/{uuid4()}.sh'
  tmp_file = open(sh, 'w')
  tmp_file.write('#!/usr/bin/bash\n' + code)
  tmp_file.close()
  bash(f'''
chmod +x {sh}
scp -O {sh} {host}:{sh}
ssh {host} {sh}
ssh {host} rm -f {sh}
rm -f {sh}
''')

def wait(host:str, wait_time:int=60) -> None:
  from time import sleep
  while system(f'ping -c 1 {host}'): pass
  sleep(wait_time)

def path_break(path:str) -> tuple[str,str,str]:
  '''return folder, filname, ext'''
  path = path.split('/')
  folder = '/'.join(path[:-1])
  filename = path[-1].split('.')
  len_ = len(filename)
  if len_ == 1: return folder, filename[0], ''
  elif len_ == 2: return folder, filename[0], filename[-1]
  else: return folder, '.'.join(filename[:-1]), filename[-1]

