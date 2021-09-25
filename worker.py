import threading
from queue import Queue
import subprocess
import sys

tasks = Queue()
working_thread = Queue()


class worker(threading.Thread):
    def __init__(self):
        self.file_handle = None
        self.socket = None
        self.proc = None
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def restart(self):
        if self.file_handle != None:
            self.file_handle.close()
            self.file_handle = None
        if self.socket != None:
            self.socket.close()
            self.socket = None
        if self.proc != None:
            self.proc.kill()
            self.proc = None
        working_thread.get()

    def get(self, file_name, is_head=False):
        try:
            open(file_name, "rb")
            content = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
        except IOError:
            content = b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n"
            file_name = "404.html"
        page = b''
        if not is_head:
            self.file_handle = open(file_name, "rb")
            for line in self.file_handle:
                page += line
            self.file_handle.close()
        content += b'\r\n'
        content += page
        self.socket.sendall(content)

    def post(self, file_name, args):
        command = 'python ' + file_name + ' "' + args + '" "' + self.socket.getsockname(
        )[0] + '" "' + str(self.socket.getsockname()[1]) + '"'
        self.proc = subprocess.Popen(command,
                                     shell=True,
                                     stdout=subprocess.PIPE)
        self.proc.wait()
        res = self.proc.stdout.read()
        content = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
        content += res
        self.socket.sendall(content)
        self.proc = None

    def run(self):
        while True:
            self.socket = tasks.get()
            working_thread.put(self)
            message = self.socket.recv(8000).decode("utf-8")
            print(message)
            message = message.splitlines()
            key_mes = message[0].split()
            file_name = "index.html"
            if (len(key_mes) > 2):
                file_name = key_mes[1][1:]

            if (key_mes[0] == 'GET'):
                self.get(file_name)
            elif (key_mes[0] == 'POST'):
                self.post(file_name, message[-1])
            elif (key_mes[0] == 'HEAD'):
                self.get(file_name, True)
            else:
                content = b"HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n"
                self.socket.sendall(content)
            self.restart()
