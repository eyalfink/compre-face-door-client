# Python 3 server example
from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler, HTTPServer
import time
import click

hostName = "localhost"
serverPort = 7823

class MyServer(BaseHTTPRequestHandler):

  def do_OPTIONS(self):
    self.send_response(200)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.end_headers()

  def do_POST(self):
    click.MicrobitClicker().click()
    self.send_response(200)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write('OK')

if __name__ == "__main__":
  webServer = HTTPServer((hostName, serverPort), MyServer)
  print("Server started http://%s:%s" % (hostName, serverPort))

  try:
    webServer.serve_forever()
  except KeyboardInterrupt:
      pass

  webServer.server_close()
  print("Server stopped.")
