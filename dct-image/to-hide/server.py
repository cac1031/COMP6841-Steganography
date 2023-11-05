# completed using python3
from socket import *
import sys
import os.path
import re

server_port = int(sys.argv[1])

if len(sys.argv) < 2:
    server_port = 80

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('127.0.0.1', server_port))
server_socket.listen(1)
print("The server is ready to receive")

while (True):
    connectionSocket, addr = server_socket.accept()
    connectionSocket.settimeout(3)
    while (True):
        try:
            request = connectionSocket.recv(1024).decode()
            headers = request.split('\r\n')
            filename = headers[0].split()[1][1:]
            
            file_exists = os.path.exists(filename)
            response = ''

            if (file_exists):
                response = "HTTP/1.1 200 OK\r\nConnection: Keep-Alive\r\nKeep-Alive: max=1, timeout=60\r\nContent-Type: "
                content = ''

                if (re.search(r".*\.png$", filename)):
                    with open(filename, "rb") as file:
                        content = file.read()
                        response += "image/png\r\n\n"
                    connectionSocket.send(response.encode())
                    connectionSocket.send(content)
                else:
                    with open(filename, "r") as file:
                        content = file.read()
                        response += "text/html\r\n\n" + content
                    connectionSocket.send(response.encode())

            else:
                content = """
                <html>
                    File Does Not Exist.
                </html>
                """
                response = "HTTP/1.1 404 NOT FOUND\r\nFile Does Not Exist" "Content-Type: text/html\r\n\n" + content
                connectionSocket.send(response.encode())
        except error:
            break

    connectionSocket.close()
server_socket.close()
