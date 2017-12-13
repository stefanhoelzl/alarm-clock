import machine
import utime

import uasyncio as asyncio
import usocket as socket
import ustruct as struct
from settings import TIME_ZONE
from uaos import App


class NTP(App):
    requires = ['Network']
    not_mandatory = True

    def __init__(self):
        super().__init__()
        NTP.settime(tz=TIME_ZONE)

    async def __call__(self):
        while True:
            await asyncio.sleep(3600)
            NTP.settime(tz=TIME_ZONE)

    # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
    NTP_DELTA = 3155673600

    host = "pool.ntp.org"

    @staticmethod
    def time():
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1b
        addr = socket.getaddrinfo(NTP.host, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
        s.close()
        val = struct.unpack("!I", msg[40:44])[0]
        return val - NTP.NTP_DELTA

    @staticmethod
    def settime(tz=0):
        t = NTP.time()
        tm = utime.localtime(t+tz*3600)
        tm = tm[0:3] + (0,) + tm[3:6] + (0,)
        machine.RTC().datetime(tm)
        return utime.localtime()

NTP.register()
