# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python server to interact with Unity
# Sergio. Julio 2021

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json

import numpy as np
import tiposNodos

size = 3
percent = 50

def initCity(size, percent):
    grafo = tiposNodos.City(size, percent)
    city = tiposNodos.City(size, percent)
    graph = city.getCity()
    print(type(graph))

#from boid import Boid

# Size of the board:
#width = 30
#height = 30

# Set the number of agents here:
#flock = [Boid(*np.random.rand(2)*30, width, height) for _ in range(5)] #deben coincidir estos con el número de agentes

def updatePositions():
    city = tiposNodos.City(size, percent)
    graph = city.getCity()
    return graph

def positionsToJSON(ps):
    posDICT = []
    pos = dict()
    for key, streets in ps.items():
            pos[str(key)] = []
            print("key:", key)
            for i, node in enumerate(streets):
                pos[str(key)].append(node.getStreet())
            print(pos[str(key)])
    posDICT.append(pos)
    print(posDICT)
    return json.dumps(pos)


class Server(BaseHTTPRequestHandler):
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        positions = updatePositions()
        self._set_response()
        resp = "{\"data\":" + positionsToJSON(positions) + "}"
        self.wfile.write(resp.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), json.dumps(post_data))
        positions = updatePositions()
        self._set_response()
        resp = "{\"data\":" + positionsToJSON(positions) + "}"
        self.wfile.write(resp.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n") # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt: # CTRL+C stops the server
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()