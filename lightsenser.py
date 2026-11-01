from lib.mBot import *


def onLight(value):
    print("light = ", value)


if __name__ == "__main__":
    bot = mBot()
    bot.startWithSerial()
    try:
        while True:
            bot.requestLightOnBoard(1, onLight)
            sleep(0.5)
    except KeyboardInterrupt:
        bot.close()
