from machine import Pin, I2S


class MAX98357:
    def __init__(self):
        self.i2s = I2S(1,
                       sck=Pin(19),
                       ws=Pin(18),
                       sd=Pin(21),
                       bits=16,
                       mode=I2S.TX,
                       rate=24000,
                       ibuf=1024,
                       format=I2S.MONO
                       )

    def play(self, sock):
        while True:
            v = sock.receive_voice()
            if v:
                self.i2s.write(v)  # 播放音频
