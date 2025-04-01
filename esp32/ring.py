from machine import Pin
from time import sleep


class Ring:
    def __init__(self, p):
        self.pin = Pin(p, Pin.OUT)
        self.warning = 0

    def start(self):
        self.pin.value(1)

    def close(self):
        self.pin.value(0)

    def ring(self, t):
        self.start()
        sleep(t)
        self.close()

    def warn(self):
        while self.warning:
            self.ring(0.1)
            sleep(0.1)


