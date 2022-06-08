# -*- encoding=utf-8 -*-

import socket
import struct



# 缓冲区大小
BUFFER_SIZE = 1024


def sendMsg(sock,msg):
    msg = msg.encode('utf-8')
    dataHead = struct.pack('i', len(msg))  # 把消息长度打包成固定长度的bytes
    sock.send(dataHead)  # 发送包头
    sock.sendall(msg) # 发送消息
    print('send msg ok')

def recvMsg(sock):
    print('recv msg start')
    buffer = sock.recv(BUFFER_SIZE)  # 先获取包头
    print('recv msg start11111')
    if len(buffer)==4:
        dataLen = struct.unpack('i', buffer)[0]  # 把包头解包成int类型
        print('recv msg start222222222')

        # 开始读取长度为 dataLen 的数据
        recData = b''  # 获取到的消息
        print('recv msg start333333333333333')

        page = dataLen // BUFFER_SIZE  # 分片
        print('recv msg start44444444')

        if page > 0:
            print('recv msg start55555555')

            for i in range(page):
                print('recv msg start66666')
                recData += sock.recv(BUFFER_SIZE)
            pageEnd = dataLen % BUFFER_SIZE  # 最后一片
            recData += sock.recv(pageEnd)
            print('recv msg start77777777')
        else:
            print('recv msg start8888888888')
            recData += sock.recv(dataLen)
        print('recv msg start9999999999')
        msg = recData.decode('utf-8')
        print('recv msg ok')
        return msg
    else:
        print('out range buffer "%d" "%s"' % ( len(buffer), buffer.decode('utf-8')))
        return buffer.decode('utf-8')

def SocketServer():
    # 创建套接字,ipv4,tcp通信方式
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    # 绑定套接字
    host = "127.0.0.1"
    port = 6666
    sock.bind((host,port))
    
    # 监听
    sock.listen()
    
    while True:
        print('waiting for connecting')
        conn,clientAddr = sock.accept()
        print('Connect clientAddr: ',clientAddr)
        clientMsg = recvMsg(conn)
        print('recv client msg: %s' %(clientMsg))
        msg = 'recv success!!!'
        sendMsg(conn,msg)
        conn.close()
        
        
if __name__ == '__main__':
    SocketServer()
    
