import socket
import subprocess
import struct
import json
import hashlib
import os

md5 = hashlib.md5()
ip_port = ('127.0.0.1', 8085)
tcp_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket_server.bind(ip_port)
tcp_socket_server.listen(5)

while True:
    conn, addr = tcp_socket_server.accept()
    print('客户端', addr)

    while True:
        cmd = conn.recv(1024)
        if len(cmd) == 0: break
        print("recv cmd",cmd)

        # 第一步：先提取命令获得文件名。
        f_cmd, filename = cmd.decode('utf-8').split()
        print(filename)

        # err = res.stderr.read()
        # if err:  # 判断是否有错误信息。如有错误信息，返回的错误信息，除此返回正常的输出结果
        #     res_out = err
        # else:
        #     res_out = res.stdout.read()
        md5 = hashlib.md5(filename)  # 将数据使用MD5进行校验。产生一个MD5的对象

        # 第一步：指定一个自己的报头信息
        header_dict = {'filename': filename,
                       'size': len(res_out),
                       'md5': md5.hexdigest()}  # 制定一个自己设计的报头信息
        print(header_dict)
        header_json = json.dumps(header_dict)  # 将字典格式转换为字符串格式
        header_bytes = header_json.encode('utf-8')  # 将字符串格式转换为字节格式

        # 第二步：发送报头信息的长度
        conn.send(struct.pack('i',len(header_bytes)))  # 使用struct.pack将报头的长度信息封装成4个字节。并发送给客户端

        # 第三步： 发送报头信息
        conn.send(header_bytes)

        # 第四步：发送真实的数据。
        conn.send(res_out)
    conn.close()