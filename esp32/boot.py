import network
import time


def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("正在连接网络...")
        wlan.connect(ssid, password)
        for _ in range(5):
            if wlan.isconnected():
                break
            time.sleep(1)
    if wlan.isconnected():
        print("IP地址:", wlan.ifconfig())
    else:
        print("连接失败")


#  Wi-Fi 名称和密码
try:
    connect_to_wifi('zjx', '123456789')
except:
    print('连接失败')


