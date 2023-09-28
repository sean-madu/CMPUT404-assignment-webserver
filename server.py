#  coding: utf-8
import socketserver
from os.path import abspath

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
        response = 'HTTP/1.0 200 OK\r\n\n'
        content = ''
        # decode byte array into string so we can do string operations on it
        string_data = self.data.decode('utf-8')

        # get all the headers in easier to get format
        headers = string_data.split("\n")
        # if not a GET request return 405
        if (not headers[0].startswith("GET")):
            response = 'HTTP/1.1 405 Method Not Allowed\nContent-Type: text/html\nAllow: GET\r\n\r\n'
        else:
            # Get directory where request is
            directory = headers[0].split(" ")[1]

            directory = directory.replace("../", "")
            # filter out requests from moving back

            if (not directory.endswith("/") and not directory.endswith(".css") and not directory.endswith(".html")):
                # use 301 to path redirect
                newPath = directory + "/"
                response = 'HTTP/1.1 301 Moved Permanently\nLocation: %s\ncontent-Type: text/html\n\r\n' % newPath
                directory = newPath

                self.request.sendall(bytearray(response + content, 'utf-8'))

            try:
                # Use www as the base directory

                if ("www" not in directory):
                    # directory if correct is of the form /path to a file, if not correct we will get a 404 anyway
                    directory = "/www" + directory
                if (directory.endswith("/")):
                    directory += "index.html"

                directory = "." + directory  # make it relative
                f = open(directory)
                # Serve correct mime-type
                if (directory.endswith(".css")):
                    response = 'HTTP/1.1 200 OK\nContent-Type: text/css\n\r\n'
                elif (directory.endswith(".html")):
                    response = 'HTTP/1.1 200 OK\nContent-Type: text/html;\n\r\n'
                content = f.read()
                f.close()

            except:
                # Handle bad requests
                response = 'HTTP/1.1 404 Not Found\nContent-Type: text/html; charset=UTF-8\n\r\n'
                content = """
<!DOCTYPE html>
<html>
<head>
	<title>404 not found idk I didnt like this assingment</title>
        <meta http-equiv="Content-Type"
        content="text/html;charset=utf-8"/>
</head>

<body>
<p>This is a simple webpage saying you got a 404 error (The url could not be found) Now please give me an A+</p>
</body>
</html> 
"""

        self.request.sendall(bytearray(response + content, 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
