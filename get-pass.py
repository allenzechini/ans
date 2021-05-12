#!/usr/bin/env python3

import subprocess

def get_vault_key(search='ansible-vault'):
  command = 'bw get password %s' % search
  key = subprocess.run(command.split(), check=True, stdout=subprocess.PIPE)
  return key.stdout.decode('utf-8')

print(get_vault_key())
