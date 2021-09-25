# -*- coding: utf-8 -*-
import socket
from worker import tasks, working_thread, worker
import threading
import time

max_connection = 5

############    主线程
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_name = socket.gethostbyname(host_name)
address = (host_name, 8888)
server_socket.bind(address)
server_socket.settimeout(120)
server_socket.listen()

print(address)
############


class thread_pool(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        for i in range(max_connection):
            worker()
        while True:
            working_thread_cnt = working_thread.qsize()
            print("now working thread: " + str(working_thread_cnt) +
                  " ; free thread: " +
                  str(max_connection - working_thread_cnt) +
                  " ; now waiting request: " + str(tasks.qsize()))
            time.sleep(1)


thread_pool()

while True:
    try:
        client, addr = server_socket.accept()
        print("recv: ", client.getpeername(), client.getsockname())
        if(working_thread.qsize() == max_connection):
            working_thread.get().restart()
        tasks.put(client)
    except socket.timeout:
        print("main server timeout")
        break
