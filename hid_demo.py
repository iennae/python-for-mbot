import sys
import threading
from time import sleep

from lib.mBot import *

dev = None
hidapi = hid()
hidapi.hid_init()
dev = hidapi.hid_open(0x0416, 0xFFFF)
exiting = False


def excepthook(exctype, value, traceback):
    global exiting
    exiting = True
    hidapi.hid_close(dev)


def __onRead():
    index = 0
    while 1:
        if exiting:
            break
        buf = hidapi.hid_read(dev, 64)
        _ = buf[0]
        if index == 10:
            index = 0
            hidapi.hid_write(dev, [0, 7, 0xFF, 0x55, 0x4, 1, 0x1, 0x1, 3])
        sleep(0.1)
        index += 1


th = threading.Thread(target=__onRead)
th.start()
sys.excepthook = excepthook
while 1:
    sleep(0.1)
