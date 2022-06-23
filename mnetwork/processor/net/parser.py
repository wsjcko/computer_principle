# -*- encoding=utf-8 -*-


import struct
import socket

# IP报文解析器
class IPParser:
    IP_HEAD_LENGTH = 20
    
    @classmethod
    def parse_ip_header(cls, ip_header):
        
        """
        IP报文格式
        1. 4位IP-version 4位IP头长度 8位服务类型 16位报文总长度
        2. 16位标识符 3位标记位 13位片偏移 暂时不关注此行
        3. 8位TTL 8位协议 16位头部校验和
        4. 32位源IP地址
        5. 32位目的IP地址
        :param ip_header:
        :return:
        """
        
        # 第一行，四字节
        line1 = struct.unpack('>BBH',ip_header[:4]) 
        # eg: 11110000 => 1111
        ip_version = line1[0]>>4
        # eg: 11111111 => 00001111 & 00001111
        iph_length = line1[0] & 15
        pkg_length = line1[2]
        
        # 第三行
        line3 = struct.unpack('>BBH',ip_header[8:12])
        ttl = line3[0]
        protocol = line3[1]
        iph_checksum = line3[2]
        # 第四行
        line4 = struct.unpack('>4s',ip_header[12:16])
        src_ip = socket.inet_ntoa(line4[0])
        # 第五行
        line5 = struct.unpack('>4s',ip_header[16:20])
        dst_ip = socket.inet_ntoa(line5[0])
        
        return {
            # 第一行. 4位版本号，4位ip头部长度，8位服务类型，16位总长度（字节）
            'ip_version': ip_version,
            'iph_length':iph_length,
            'packet_length': pkg_length,
            # 第二行. 16位标识符，3位标记位，3位片偏移
            # 第三行. 8位TTL报文寿命,8位协议（protocol 协议号 1 ICMP协议 6 TCP协议 17 UDP协议）,16位IP头校验和
            'TTL':ttl,
            'protocol':protocol,
            'iph_checksum': iph_checksum,
            # 第四行.32位源IP地址
            'src_ip': src_ip,
            # 第五行.32位目的IP地址
            'dst_ip':dst_ip,
        }
        
    @classmethod
    def parse(cls,packet):
        ip_header = packet[:20]
        return cls.parse_ip_header(ip_header)