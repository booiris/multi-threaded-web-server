import threading
from queue import Queue
import subprocess

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
        working_thread.get()
        if self.file_handle != None:
            self.file_handle.close()
            self.file_handle = None
        if self.socket != None:
            self.socket.close()
            self.socket = None
        if self.proc != None:
            self.proc.kill()
            self.proc = None

    def get(self, file_name, is_head=False):
        try:
            open(file_name, "rb") ## TODO 可能未关闭句柄，用os实现查看文件是否存在
            file_suffix = file_name.split('.')
            file_suffix = file_suffix[-1].encode()
            content = b"HTTP/1.1 200 OK\r\nContent-Type: text/" + file_suffix + b"\r\n"
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
        ## TODO 403 页面
        ## TODO 计算器可能有写小 bug ，在手机访问的时候传入的参数不对，到时候修一修
        command = 'python ' + file_name + ' "' + args + '" "' + self.socket.getsockname(
        )[0] + '" "' + str(self.socket.getsockname()[1]) + '"'
        self.proc = subprocess.Popen(command,
                                     shell=True,
                                     stdout=subprocess.PIPE)
        self.proc.wait()
        res = self.proc.stdout.read()
        content = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
        content += res
        print(content)
        self.socket.sendall(content)
        self.proc = None

    def run(self):
        while True:
            self.socket = tasks.get()
            working_thread.put(self)
            message = self.socket.recv(8000).decode("utf-8")
            print(message)
            message = message.splitlines()
            if(message):
                key_mes = message[0].split()
            else:
                self.restart()
            file_name = "index.html"
            if (key_mes[1] != "/"):
                file_name = key_mes[1][1:]

            ## TODO 添加异常中断达到重启线程的目的
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
