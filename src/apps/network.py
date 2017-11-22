import network
from settings import WIFI_SSID, WIFI_PWD
from uaos import App


class Network(App):
    not_mandatory = True

    IP = None

    def __init__(self):
        ap = network.WLAN(network.AP_IF)
        ap.active(False)

        nic = network.WLAN(network.STA_IF)
        nic.active(True)
        nic.connect(WIFI_SSID, WIFI_PWD)
        while not nic.isconnected():
            pass
        Network.IP = nic.ifconfig()[0]

Network.register()
