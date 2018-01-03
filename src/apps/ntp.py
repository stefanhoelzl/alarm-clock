import machine
import time

import uasyncio as asyncio
import usocket as socket
import ustruct as struct
from settings import TIME_ZONE, DST
from uaos import App


class NTP(App):
    requires = ['Network']
    not_mandatory = True

    OFFSET = 0

    def __init__(self):
        super().__init__()
        self.settime(tz=TIME_ZONE, dst=DST)

    async def __call__(self):
        while True:
            await asyncio.sleep(3600)
            self.settime(tz=TIME_ZONE, dst=DST)

    # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
    NTP_DELTA = 3155673600

    host = "pool.ntp.org"

    @staticmethod
    def query_time():
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
    def time():
        return time.time() + NTP.OFFSET

    def settime(self, tz=0, dst=None):
        try:
            ntp_time = NTP.query_time() + tz*3600
            if dst:
                tm = time.localtime(ntp_time)
                month = tm[1]
                day = tm[2]
                c = month + day/100
                if DST[0] <= c < DST[1]:
                    ntp_time += 3600
            NTP.OFFSET = ntp_time - time.time()
        except:
            return False
        return True
        #tm = utime.localtime(t+tz*3600)
        #tm = tm[0:3] + (0,) + tm[3:6] + (0,)
        #machine.RTC().datetime(tm)
        #return utime.localtime()

NTP.register()
