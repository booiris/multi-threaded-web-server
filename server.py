# -*- coding: utf-8 -*-
import socket
import threading

max_connection = 20


############    主线程
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name = socket.gethostname()
host_name = socket.gethostbyname(host_name)
address = (host_name, 8888)
server_socket.bind(address)
server_socket.settimeout(120)
server_socket.listen()
############

class worker(threading.Thread):
    def __init__(self, request_id):
        self.start()
    def work(self, tcp_socket):
        pass

while True:
    try: 
        clie?!?jedi=0, nt,addr = server_socket.accept()?!? (*_**values: object*_*, sep: Optional[str]=..., end: Optional[str]=..., file: Optional[SupportsWrite[str]]=..., flush: bool=...) ?!?jedi?!?
        print(client.getpeername(),client.gethostname)
    except socket.timeout:
        print("main server timeout")

