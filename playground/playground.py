import time

import machine
import neopixel

np = neopixel.NeoPixel(machine.Pin(17), 60, timing=True)

while True:
    for r in range(255):
        np.fill((r, r, r))
        np.write()
        time.sleep(0.001)
