from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import sys
import json
from configparser import ConfigParser

class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers(self):
        if self.client_address[0] not in '194.87.219.96':
            self.send_response(401, 'request not allowed')
        else:
            SimpleHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
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
      with open('data.json', 'w') as out_file:
            json.dump(response, out_file, sort_keys = True, indent = 4,
                        ensure_ascii = False)      
      test(CORSRequestHandler, HTTPServer, port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000)