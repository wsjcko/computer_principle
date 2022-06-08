# -*- encoding=utf-8 -*-

import socket
import sys
import os
import struct


# 套接字存放路径及名称
SOCKET_PATH = './udp_unix_socket'

# 缓冲区大小
BUFFER_SIZE = 1024

def UDPServerUnixSocket():
    # 创建unix套接字,udp通信方式
    sock = socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM)
    
    # 绑定套接字文件
    if os.path.exists(SOCKET_PATH):
        # 如果套接字存在就删除
        os.unlink(SOCKET_PATH) 
    
    # 绑定套接字文件成功后，会在指定路径下生成一个域套接字文件
    if sock.bind(SOCKET_PATH):
        sys.stderr.write('socket bind error')

    
    # 与TCP相比，不需要监听连接，直接接收消息
    while True:
        print('waiting for recv msg')
        try:
            while True:
                clientMsg = sock.recv(BUFFER_SIZE)
                if clientMsg:
                    print('recv clientMsg "%s" ' %(clientMsg.decode('utf-8')))
                    
                else:
                    break 
        except Exception as e:
            print(e)

if __name__== '__main__':
    UDPServerUnixSocket()