#!/usr/bin/env python3

import subprocess

def get_vault_key(search='test-pw-1'):
  command = 'bw get password %s' % search
  key = subprocess.run(command.split(), check=True, stdout=subprocess.PIPE)
  return key.stdout.decode('utf-8')

def main():
  print(get_vault_key())

if __name__ == '__main__':
  main()
