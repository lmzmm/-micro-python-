import socket


class Server:
    def __init__(self):
        self.soket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.soket1.settimeout(5)
        self.addr1 = ("0.0.0.0", 12345)
        self.soket1.bind(self.addr1)

        self.soket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.soket2.settimeout(5)
        self.addr2 = ("0.0.0.0", 12346)
        self.soket2.bind(self.addr2)

        self.target_addr = "192.168.91.189"  # 服务器ip

    def receive(self):
        try:
            data, addr = self.soket1.recvfrom(1024)
        except:
            pass
        else:
            return data.decode('utf-8')

    def send(self, data):
        data = str(data).encode('utf-8')
        self.soket1.sendto(data, (self.target_addr, 12345))

    def send_weight(self, data):
        data = str(data).encode('utf-8')
        self.soket1.sendto(data, (self.target_addr, 12347))

    def send_voice(self, v):
        self.soket2.sendto(v, (self.target_addr, 12346))

    def receive_voice(self):
        try:
            data, addr = self.soket2.recvfrom(1024)
        except:
            pass
        else:
            return data
