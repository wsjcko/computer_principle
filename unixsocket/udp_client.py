# -*- encoding=utf-8 -*-

import socket


# 套接字存放路径及名称
SOCKET_PATH = './udp_unix_socket'

# 缓冲区大小
BUFFER_SIZE = 1024


def UDPClientUnixSocket(i):
    # 创建unix套接字，udp通信方式
    sock = socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM)
    
    msg = 'client '+ str(i)
    sock.sendto(msg.encode('utf-8'),SOCKET_PATH)
    sock.close()
    
if __name__== '__main__':
    for i in range(10):
        UDPClientUnixSocket(i)