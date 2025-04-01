from machine import Pin, I2S
from time import sleep


class AudioStreamer:
    def __init__(self):

        # 初始化 I2S 接口
        self.i2s = I2S(0,
                       sck=Pin(26),
                       ws=Pin(27),
                       sd=Pin(25),
                       bits=16,
                       mode=I2S.RX,
                       rate=8000,
                       ibuf=1024,
                       format=I2S.MONO)
        self.run = True

    def stream_audio(self, sock):
        by = bytearray(1024)
        while self.run:
            num_bytes = self.i2s.readinto(by)
            if num_bytes > 0:  # 只发送有效数据
                sock.send_voice(by[:num_bytes])
            sleep(0.05)

    def close(self):
        self.i2s.deinit()



