
import os
import argparse
import cv2
import requests
import time
import click

import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

def send_open_command(args):
  if args.use_server:
    requests.post(args.use_server)
  else:
    click.MicrobitClicker().click()

def watch(args):
  key = args.key
  if args.view:
    cv2.namedWindow("preview")

  vc = cv2.VideoCapture(1)
  vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # set new dimensionns to cam object (not cap)
  vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

  if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
  else:
    rval = False

  frame_id = 0
  while rval:
    rval, frame = vc.read()
    if args.rotate:
      frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if args.view:
      cv2.imshow("preview", frame)
      cv2.imwrite(f'{frame_id}.jpg', frame)

    retval, bframe = cv2.imencode('.jpg', frame)
    files = {'file': ('blob.jpeg', bframe)}
    r = requests.post('http://localhost:8000/api/v1/recognition/recognize',
                      headers={
                        "x-api-key": key
                      },
                      files=files)
    logging.debug(r.json())
    if (frame_id % 3000) == 0:
      logging.info(f'frame: {frame_id}')
    
    data = r.json()
    face_detetced =  'result' in data
    if face_detetced: 
      logging.info(f'Face found on frame {frame_id}, {data}')
      who = data['result'][0]['subjects'][0]['subject']
      similarity = data['result'][0]['subjects'][0]['similarity']
      if similarity > 0.99:
        if not args.dontopen:
          send_open_command(args)
        logging.info(f'open door on frame {frame_id} for {who}')
        time.sleep(5)
      
      fname = f'{who}-{similarity}-{frame_id}.jpg'
      cv2.imwrite(os.path.join(args.img_log_dir, fname), frame)
      
    time.sleep(0.2)
    frame_id += 1

  vc.release()
  if args.view:
    cv2.destroyWindow("preview")

def add_new_subject(name):
  pass

def main():
  # Instantiate the parser
  parser = argparse.ArgumentParser()
  parser.add_argument('--key',
                      help='CfompreFace application key')
  parser.add_argument('--use_server',
                      default=None,
                      help='if given will send request to the given address')
  parser.add_argument('--add', action='store_true',
                      help='Add new subjest')
  parser.add_argument('--name',
                      help='New subjest name')
  parser.add_argument('--view', action='store_true',
                      help='Show stream')
  parser.add_argument('--rotate', action='store_true',
                      help='rotate the image')
  parser.add_argument('--dontopen', action='store_true',
                      help='just collect, dont open')
  parser.add_argument('--img_log_dir', default='/tmp')

  args = parser.parse_args()

  if args.add:
    add_new_subject(args.name)
  else:
    watch(args)

if __name__ == "__main__":
  main()
