# -*- encoding=utf-8 -*-

import socket
import struct



# 缓冲区大小
BUFFER_SIZE = 1024


def TCPSocketServer():
    # 创建套接字,ipv4,udp通信方式
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    
    # 绑定套接字
    host = "127.0.0.1"
    port = 6666
    sock.bind((host,port))
    

    while True:
        print('waiting for recv msg')
        clientMsg = sock.recv(BUFFER_SIZE)
        print('recv client msg: %s' %(clientMsg.decode('utf-8')))
        
        
if __name__ == '__main__':
    TCPSocketServer()
    
