import sys
sys.path.append('/lib')

import network

from settings import WIFI_SSID, WIFI_PWD

ap = network.WLAN(network.AP_IF)
ap.active(False)

nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect(WIFI_SSID, WIFI_PWD)
