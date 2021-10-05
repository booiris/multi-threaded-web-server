import threading
from queue import Queue
import subprocess
import os

tasks = Queue()
working_thread = list()


class worker(threading.Thread):
    def __init__(self):
        self.file_handle = None
        self.socket = None
        self.proc = None
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.start()

    def restart(self):
        if (self.file_handle != None):
            self.file_handle.close()
            self.file_handle = None
        if (self.socket != None):
            try:
                self.socket.shutdown(2)
                self.socket.close()
            except Exception as e:
                print("socket error:", e)
                self.socket = None
        if (self.proc != None and self.proc.poll() != None):
            self.proc.kill()
            self.proc = None

    def get(self, file_name, is_head=False):
        if (os.path.isfile(file_name)):
            file_suffix = file_name.split('.')
            file_suffix = file_suffix[-1].encode()
            content = b"HTTP/1.1 200 OK\r\nContent-Type: text/" + file_suffix + b";charset=utf-8\r\n"
        else:
            content = b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html;charset=utf-8\r\n"
            file_name = "404.html"
        content += b'\r\n'
        self.socket.sendall(content)
        if not is_head:
            self.file_handle = open(file_name, "rb")
            for line in self.file_handle:
                self.socket.sendall(line)


    def post(self, file_name, args):
        ## TODO 计算器可能有写小 bug ，在手机访问的时候传入的参数不对，到时候修一修
        command = 'python ' + file_name + ' "' + args + '" "' + self.socket.getsockname(
        )[0] + '" "' + str(self.socket.getsockname()[1]) + '"'
        self.proc = subprocess.Popen(command,
                                     shell=True,
                                     stdout=subprocess.PIPE)
        self.proc.wait()
        if (self.proc.poll() == 2):  ## 文件不存在时返回值为2
            content = b"HTTP/1.1 403 Forbidden\r\nContent-Type: text/html;charset=utf-8\r\n"
            page = b''
            self.file_handle = open("403.html", "rb")
            for line in self.file_handle:
                page += line
            content += b'\r\n'
            content += page
        else:
            content = b"HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n"
            content += self.proc.stdout.read()
        self.socket.sendall(content)

    def run(self):
        while True:
            self.socket = tasks.get()
            working_thread.append(self)
            message = self.socket.recv(8000).decode("utf-8")
            message = message.splitlines()
            if (message):
                key_mes = message[0].split()
            else:
                self.restart()
            file_name = "index.html"
            if (key_mes[1] != "/"):
                file_name = key_mes[1][1:]

            try:
                if (key_mes[0] == 'GET'):
                    self.get(file_name)
                elif (key_mes[0] == 'POST'):
                    self.post(file_name, message[-1])
                elif (key_mes[0] == 'HEAD'):
                    self.get(file_name, True)
                else:
                    content = b"HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n"
                    self.socket.sendall(content)
            except Exception as e:
                print("reason:", e)
            self.restart()
            working_thread.remove(self)
