
import os
import argparse
import requests
import time

import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


def add_user_imgs(args):
  key = args.key
  for root, dirs, _ in os.walk(args.root_dir):
    for name in dirs:
      for fname in os.listdir(os.path.join(root, name)):
        img_path = os.path.join(root, name, fname)
        logging.info(f'reading {img_path}')
        bframe = open(img_path, 'rb').read()
        files = {'file': ('blob.jpeg', bframe)}
        r = requests.post(f'http://localhost:8000/api/v1/recognition/faces?subject={name}',
                          headers={
                            "x-api-key": key
                          },
                          files=files)
        logging.info(r.json())

def main():
  # Instantiate the parser
  parser = argparse.ArgumentParser()
  parser.add_argument('--key',
                      required=True,
                      help='CfompreFace application key')
  parser.add_argument('--root_dir',
                      required=True,
                      help='directory with subdir for each user')

  args = parser.parse_args()

  add_user_imgs(args)

if __name__ == "__main__":
  main()
