import os
from posixpath import dirname

from reactor_server.http_server.server import Server
from reactor_server.http_server.eventloop import EventLoop


pwd = dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    Server(EventLoop, root=pwd, thread_num=2, port=8888, host='0.0.0.0').run()
