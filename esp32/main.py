from time import sleep
from h711 import EleScale
from ring import Ring
from server import Server
import network
import _thread
from light import monitor
from AHT10 import AHT10
from INMP441 import AudioStreamer
from MAX98357 import MAX98357
import gc


def receive():
    while True:
        res = u.receive()
        if res == '1':
            ring.ring(0.1)
        elif res == '2':
            u.send(scale.getWeight())
        elif res == '3':
            ring.warning = 1
            _thread.start_new_thread(ring.warn, ())
        elif res == '4':
            ring.warning = 0
        elif res == '5':
            u.send(sensor.get_data())


def open_box():
    while True:
        if monitor(ring, pin=17):  # 监测光照变化
            sleep(3)
            w = scale.getWeight()
            u.send_weight(w)
            print(w)
        sleep(0.5)  # 避免频繁查询


def mic():
    gc.collect()
    microphone.stream_audio(u)


def speaker_play():
    speaker.play(u)


if __name__ == "__main__":

    """
    ring：蜂鸣器对象
    u：udp通信对象
    microphone：麦克风对象
    speaker：扬声器对象
    scale：重力传感器对象"""

    ring = Ring(2)
    u = Server()
    microphone = AudioStreamer()
    speaker = MAX98357()
    scale = EleScale(clk_pin=13, data_pin=12, cap_value=679.5)

    # 检查WiFi状态
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("WiFi not connected!")
        ring.ring(0.1)
    else:
        print("WiFi is connected.")
        ring.ring(0.1)
        sleep(0.1)
        ring.ring(0.1)

    scale.tare()  # 零点校准

    sensor = AHT10(scl_pin=4, sda_pin=16)

    _thread.start_new_thread(receive, ())   # 数据接收线程
    _thread.start_new_thread(open_box, ())  # 开关状态检测线程
    _thread.start_new_thread(mic, ())   # 麦克风接收线程
    _thread.start_new_thread(speaker_play, ())  # 扬声器控制线程





