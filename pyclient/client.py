
import argparse
import cv2
import requests
import time

def watch(args):
  key = args.key
  if args.view:
    cv2.namedWindow("preview")

  vc = cv2.VideoCapture(0)
  vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # set new dimensionns to cam object (not cap)
  vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

  if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
  else:
    rval = False

  frame_id = 0
  while rval:
    rval, frame = vc.read()
    if args.view:
      cv2.imshow("preview", frame)
      cv2.imwrite(f'/tmp/{frame_id}.jpg', frame)

    retval, bframe = cv2.imencode('.jpg', frame)
    files = {'file': ('blob.jpeg', bframe)}
    r = requests.post('http://localhost:8000/api/v1/recognition/recognize',
                      headers={
                        "x-api-key": key
                      },
                      files=files)
    print(r.json())
    data = r.json()
    if 'result' in data and data['result'][0]['subjects'][0]['similarity'] > 0.99:
      requests.post('http://localhost:7823')
      time.sleep(5)

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
  parser.add_argument('--add', action='store_true',
                      help='Add new subjest')
  parser.add_argument('--name',
                      help='New subjest name')
  parser.add_argument('--view', action='store_true',
                      help='Show stream')

  args = parser.parse_args()

  if args.add:
    add_new_subject(args.name)
  else:
    watch(args)

if __name__ == "__main__":
  main()
