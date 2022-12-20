from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import sys
import json
from configparser import ConfigParser

class CORSRequestHandler(SimpleHTTPRequestHandler):
      def end_headers(self):
            if self.client_address[0] not in '109.161.50.35':
                  self.send_response(401, 'request not allowed')
            else:
                  SimpleHTTPRequestHandler.end_headers(self)

      def do_GET(self):
            if self.path == '/':
                  self.send_response(200, 'OK')
                  self.send_header('Content-type', 'application/json')
                  self.end_headers()

                  config = ConfigParser()
                  response = {}

                  for peer in range(1, 11):
                        result = {}
                        config.read(f'/root/wireguard/config/peer{peer}/peer{peer}.conf')
                        interface = dict(config.items('Interface'))
                        peer = dict(config.items('Peer'))
                        address = interface['address']
                        publickey = peer['publickey']
                        result['address'] = address
                        result['publickey'] = publickey
                        response[f'peer{peer}'] = result
                  self.wfile.write(bytes(json.dumps(response), 'utf8'))
            else:
                  self.path = 'index.html'
                  return SimpleHTTPRequestHandler.do_GET(self)




if __name__ == '__main__':
    test(CORSRequestHandler, HTTPServer, port=int(sys.argv[1]) if len(sys.argv) > 1 else 8090)