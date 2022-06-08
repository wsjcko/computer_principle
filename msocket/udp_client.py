# -*- encoding=utf-8 -*-

import socket
import struct


# 缓冲区大小
BUFFER_SIZE = 1024

def UDPSocketClient(i):
    # 创建套接字,ipv4,tcp通信方式
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
    # 连接
    host = "127.0.0.1"
    port = 6666
    sock.connect((host,port))
    data = 'client '+ str(i)
    sock.sendto(data.encode('utf-8'),(host,port))
    sock.close()
    
    
if __name__ == '__main__':
    for i in range (10):
        UDPSocketClient(i)