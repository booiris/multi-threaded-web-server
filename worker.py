import threading
from queue import Queue
import socket

tasks = Queue()
working_thread = Queue()


def get(client, file_name, is_head=False):
    bad_flag = False
    try:
        open(file_name, "rb")
        content = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
    except IOError:
        bad_flag = True
        content = b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n"
        file_name = "404.html"
    page = b''
    if not is_head:
        with open(file_name, "rb") as f:
            for line in f:
                page += line
    content += b'\r\n'
    content += page
    client.sendall(content)
    if bad_flag:
        client.close()


def post(client):
    pass


class worker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            client = tasks.get()
            working_thread.put(self)
            message = client.recv(8000).decode("utf-8")
            print(message)
            message = message.splitlines()
            message = message[0].split()
            file_name = "index.html"
            if (len(message) > 2):
                file_name = message[1][1:]

            if (message[0] == 'GET'):
                get(client, file_name)
            elif (message[0] == 'POST'):
                post(client)
            elif (message[0] == 'HEAD'):
                get(client, file_name, True)
            else:
                content = b"HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n"
                client.sendall(content)
                client.close()
