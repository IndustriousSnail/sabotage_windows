import socket  # 导入 socket 模块


if __name__ == '__main__':
    s = socket.socket()  # 创建 socket 对象
    host = socket.gethostname()  # 获取本地主机名
    port = 12345  # 设置端口
    s.bind(("0.0.0.0", port))  # 绑定端口

    s.listen(5)  # 等待客户端连接
    while True:
        c, addr = s.accept()  # 建立客户端连接
        while True:
            try:
                data = c.recv(1024*1024)
                c.send(data.upper())
            except ConnectionResetError as e:
                break
        c.close()  # 关闭连接