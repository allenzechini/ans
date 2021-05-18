#!/usr/bin/env python3

import argparse
import subprocess

def get_key(search):
  command = 'bw get password {}'.format(search)
  key = subprocess.run(command.split(), check=True, stdout=subprocess.PIPE)
  return key.stdout.decode('utf-8')

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--item', help='Retrieve password from this item')
  args = parser.parse_args()

  # bw_login()
  print(get_key(args.item))

if __name__ == '__main__':
  main()
