from machine import Pin
from time import sleep


def monitor(ring, pin):
    p = Pin(pin, Pin.IN)  # 读取光敏传感器

    if p.value() == 0:
        ring.warning = 0
        while True:
            if p.value() == 1:
                return True
            sleep(0.1)

