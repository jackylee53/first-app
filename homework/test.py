import socket
import struct
import json

ip_port = ('127.0.0.1', 8085)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect_ex(ip_port)

while True:
    client.send(b'ls')
    client.send(b'ifconfig')
    msg = input('>>: ').strip()
    if len(msg) == 0: continue
    if msg == 'quit': break

    client.send(msg.encode('utf-8'))
    # 第一步：获取报头的长度
    head = client.recv(4)  # 由于struct.pack的封装后的大小4个字节。所以这里肯定先接收，数据的前4个字节。
    header_size = struct.unpack('i', head)[0]  # head=s.recv(4)返回的是一个元组。第一位就是报头信息的字节数

    # 第二步：再收报头信息
    header_bytes = client.recv(header_size)

    # 第三步：解析报头信息
    header_json = header_bytes.decode('utf-8')  # 对字节格式反编码为utf-8
    header_dict = json.loads(header_json)  # 重新加载为json格式
    print(header_dict)
    totle_size = header_dict['size']  # 解析出了数据的真实大小

    res_size = 0
    res_data = b''
    while res_size < totle_size:  # 设置一个循环。当接收数据的大小小于数据的总大小时，会一直循环，知道数据全部处理完成。
        res = client.recv(1024)  # 每次接收1024字节的数据
        res_data += res  # 将每次获得的数据内容进行相加
        res_size += len(res)  # 每次对真实获得数据的大小进行相加

    # 当循环处理完后，打印最后的结果。
    print(res_data.decode('utf-8'))