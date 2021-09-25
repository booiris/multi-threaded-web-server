#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

port = input()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_name = socket.gethostbyname(host_name)
address = (host_name, int(port))
client_socket.bind(address)
client_socket.settimeout(120)
client_socket.connect((host_name,8888))
client_socket.close()