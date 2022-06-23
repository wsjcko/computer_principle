# -*- encoding=utf-8 -*-

import ctypes
import fcntl
import json
import socket
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from operate_system.mpool import ThreadPool as tpool
from operate_system.mtask import AsyncTask
from processor.net.parser import IPParser
from processor.trans.parser import TCPParser
from processor.trans.parser import UDPParser


# 缓冲区大小
BUFFER_SIZE = 1024

IFF_PROMISC = 0x100
SIOCGIFFLAGS = 0x8913
SIOCSIFFLAGS = 0x8914

# os.system ("clear || cls") 


class ifreq(ctypes.Structure):
    _fields_ = [("ifr_ifrn", ctypes.c_char * 16),
                ("ifr_flags", ctypes.c_short)]


class ProcessTask(AsyncTask):
    def __init__(self, packet, *args, **kwargs):
        self.packet = packet
        super(ProcessTask,self).__init__(func=self.process, *args, **kwargs)

    # 报文解析
    def process(self):
        
        headers = {
            'network_header': None,
            'transport_header': None
        }

        ip_header = IPParser.parse(self.packet)
        headers['network_header'] = ip_header
        if ip_header['protocol'] == 6:
            headers['transport_header'] = TCPParser.parser(self.packet)
        elif ip_header['protocol'] == 17:  # UDP协议
            headers['transport_header'] = UDPParser.parser(self.packet)
        return headers
class Server:
    def __init__(self) :
        # 工作协议类型，套接字类型，工作具体的协议(IPV4,原始套接字，IP协议)
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        self.sock = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, socket.IPPROTO_IP)
        # 假如端口呗socket使用过，并且利用socket.close()来关闭连接，
        # 但此时端口还没有释放，要经过一个，TIME_WAIT的过程之后才能使用，这是TNN的相当烦人，
        # 为了实现端口的马上复用，可以选择setsocket()函数来达到目的。
        # prevent socket from being left in TIME_WAIT state, enabling reuse
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
        # self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,True)
        # windows
        # self.sock.ioctl(socket.SIO_KEEPALIVE_VALS,(1,10000,1000))
        # linux
        # self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)
        # self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
        # self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
        
        
        # the public network interface
        # HOST = socket.gethostbyname(socket.gethostname())
        # print(HOST)

        # Include IP headers
        # self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # self.sock.bind((HOST, 0))
        # self.ip = '172.20.5.58'
        # self.port = 8888
        # self.sock.bind((self.ip,self.port))
        self.sock.bind(("127.0.1.1",int('5565',10)))
        # windows
        # 开启混杂模式，receive all packages
        # self.sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        # 关闭 disabled promiscuous mode
        # self.sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        
        # linux
        # 创建ifreq结构的实例，并填充它以达到所需的效果：
        ifr = ifreq()
        ifr.ifr_ifrn = b'eth0'
        # ifr_flags使用ioctl呼叫填充该字段，这样您就不会破坏接口上已经设置的任何标志：
        # 添加混杂标志：
        ifr.ifr_flags |= IFF_PROMISC
        
        fcntl.ioctl(self.sock.fileno(), SIOCGIFFLAGS, ifr) # G for Get

        # 并在接口上设置标志：
        fcntl.ioctl(self.sock.fileno(), SIOCSIFFLAGS, ifr) # S for Set
        # 要删除该标志，请将其掩盖并再次设置：
        # ifr.ifr_flags &= ~IFF_PROMISC
        # fcntl.ioctl(self.sock.fileno(), SIOCSIFFLAGS, ifr)
        

        
        
        # 线程池
        self.pool = tpool(10)
        self.pool.start()
        
    def loop_server(self):
        while True:
            # 接收
            packet, addr = self.sock.recvfrom(BUFFER_SIZE)
            # 生成任务
            task = ProcessTask(packet)
            # 任务提交
            self.pool.put(task)
            # 获取结果
            result = task.get_result()
            result = json.dumps(
                result,
                # 缩进
                indent=4 
            )
            print(result)
        pass
    
if __name__ == '__main__':
    server = Server()
    server.loop_server()