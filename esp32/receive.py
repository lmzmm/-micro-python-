import socket
from threading import Thread


def receive_data():
    global p_weight
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定到本地地址和端口
    server_address = ('0.0.0.0', 12345)
    sock.bind(server_address)

    print(f"正在监听 {server_address} ...")

    try:
        while True:
            # 接收数据
            data, address = sock.recvfrom(1024)
            p_weight = data.decode('utf-8')
            print(f"接收到来自 {address} 的数据：{data.decode('utf-8')}")
    except KeyboardInterrupt:
        print("接收已中断")
    finally:
        # 关闭套接字
        sock.close()


def run():
    thread1 = Thread(target=receive_data)
    thread1.start()


if __name__ == '__main__':
    thread = Thread(target=receive_data)
    thread.start()
