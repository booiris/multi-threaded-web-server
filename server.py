# -*- coding: utf-8 -*-
import socket
from worker import tasks, working_thread, worker
import threading
import time

max_connection = 10  #
port = 8888

############    主线程
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_name = socket.gethostbyname(host_name)
address = ("0.0.0.0", port)
server_socket.bind(address)
server_socket.settimeout(60)
server_socket.listen()

print(host_name + ':' + str(port))
############


class thread_pool(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.start()

    def run(self):
        for i in range(max_connection):
            worker()
        while True:
            working_thread_cnt = working_thread.qsize()
            for i in range(5):
                if (working_thread.qsize() == max_connection):
                    working_thread.get().restart(is_terminate=True)
                time.sleep(0.2)
            print("now working thread: " + str(working_thread_cnt) +
                  " ; free thread: " +
                  str(max_connection - working_thread_cnt) +
                  " ; now waiting request: " + str(tasks.qsize()))


thread_pool()

while True:
    try:
        client, addr = server_socket.accept()
        tasks.put(client)
        print("recv: ", client.getpeername(), client.getsockname())
        # ！！！！ qsize不是阻塞的 当多个请求同时到达qsize不是当前的值
        # if (working_thread.qsize() == max_connection):
        #     working_thread.get().restart()

    except socket.timeout:
        print("main server timeout")
        break
