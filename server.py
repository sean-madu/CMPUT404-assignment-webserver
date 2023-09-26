#  coding: utf-8
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got a request of: %s\n" % self.data)
        response = 'HTTP/1.0 200 OK\n\n'
        content = ''
        # decode byte array into string so we can do string operations on it
        string_data = self.data.decode('utf-8')

        # get all the headers in easier to get format
        headers = string_data.split("\n")
        # if not a GET request return 405
        if (not headers[0].startswith("GET")):
            response = 'HTTP/1.1 405 Method Not Allowed\nContent-Type: text/html\nAllow: GET'
        else:
            #Get directory where request is
            directory = headers[0].split(" ")[1]
            directory = "." + directory  # make it relative
            # TODO handle bad requests here and 301's here
            try:
                f = open(directory)
                content = f.read()
                f.close()
            except FileNotFoundError as e:
                response = 'HTTP/1.1 404 Not Found'



        self.request.sendall(bytearray(response + content, 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
