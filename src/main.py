import os
from uaos import uaOS

if "storage" not in os.listdir("/"):
    os.mkdir("/storage")

uaOS.setup()
uaOS.start()
