import machine
import utime as time
from machine import Pin


class HCSR04:
    M_PER_SEC = 343

    def __init__(self, echo_pin, trigger_pin, max_m=1):
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)
        self.timeout_us = int((max_m/self.M_PER_SEC)*1000*1000)

    def measure(self):
        self.trigger.value(1)
        time.sleep_us(10)
        self.trigger.value(0)
        t = machine.time_pulse_us(self.echo, 1, self.timeout_us)
        return None if t == -1 else t

    @property
    def mm(self):
        nsecs = self.measure()
        if not nsecs:
            return None
        secs = nsecs/1000/1000
        roundtrip = secs * self.M_PER_SEC
        distance_mm = (roundtrip / 2)*1000
        return distance_mm
