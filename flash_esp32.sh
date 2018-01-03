../mpy-dev-tools/venv/bin/esptool.py --chip esp32 --port /dev/tty.SLAB_USBtoUART erase_flash
../mpy-dev-tools/venv/bin/esptool.py --chip esp32 --port /dev/tty.SLAB_USBtoUART write_flash -z 0x1000 /Users/stefan/Downloads/esp32-20171230-v1.9.3-238-g42c4dd09.bin
