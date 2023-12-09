# 导入socket模块
import socket
# 导入threading模块，用于创建多线程
import threading

# 定义一个函数，用于在两个socket之间转发数据
def forward_data(sock1, sock2):
    # 循环接收和发送数据，直到其中一个socket关闭
    while True:
        # 接收sock1的数据
        data = sock1.recv(1024)
        # 如果没有数据，说明sock1已经关闭，退出循环
        if not data:
            break
        # 将数据发送给sock2
        sock2.sendall(data)
    # 关闭两个socket
    sock1.close()
    sock2.close()

# 定义一个函数，用于处理每个客户端连接
def handle_client(client, source_ip):
    # 创建一个新的socket，用于连接源IP的22端口
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 尝试连接源IP的22端口
    try:
        server.connect((source_ip, 22))
    except Exception as e:
        # 如果连接失败，打印错误信息，关闭客户端连接，返回
        print(f"Failed to connect to {source_ip}:22: {e}")
        client.close()
        return
    # 获取客户端的源IP地址
    source_ip = address[0]
    # 打印连接成功的信息
    print(f"Connected to {source_ip}:22")
    # 创建两个线程，分别用于转发客户端和服务器之间的数据
    t1 = threading.Thread(target=forward_data, args=(client, server))
    t2 = threading.Thread(target=forward_data, args=(server, client))
    # 启动两个线程
    t1.start()
    t2.start()

# 创建一个服务器对象，绑定0.0.0.0地址和22端口
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 22))

# 开始监听
server.listen(1)

# 循环等待客户端连接
while True:
    # 接受客户端连接，获取客户端socket和地址
    client, address = server.accept()
    # 打印客户端地址
    print(f"Received connection from {source_ip}")
    # 创建一个新的线程，用于处理客户端连接
    t = threading.Thread(target=handle_client, args=(client, source_ip))
    # 启动线程
    t.start()
