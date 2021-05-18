#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess

def is_logged_in():
  if 'BW_SESSION' not in os.environ:
    cmd = 'bw status'
    out = subprocess.run(cmd.split(), check=True, stdout=subprocess.PIPE)
    if 'unauthenticated' in out.stdout.decode('utf-8'):
      print('Please login to your vault using \'bw login\', '
            'set the environment variable BW_SESSION, '
            'then re-run your command')
      sys.exit(1)
    elif 'locked' in out.stdout.decode('utf-8'):
      print('Please unlock your vault using \'bw unlock\', '
            'set the environment variable BW_SESSION, '
            'then re-run your command')
      sys.exit(2)
  else:
    return True

def get_p(search):
  cmd = 'bw get password {}'.format(search)
  p = subprocess.run(cmd.split(), check=True, stdout=subprocess.PIPE)
  return p.stdout.decode('utf-8')

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--item', help='Retrieve password from this item')
  args = parser.parse_args()

  if is_logged_in():
    print(get_p(args.item))

if __name__ == '__main__':
  main()
