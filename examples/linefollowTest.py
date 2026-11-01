from lib.mBot import *


def onLineFollower(value):
    print("status = ", value)


if __name__ == "__main__":
    bot = mBot()
    bot.startWithSerial()
    try:
        while True:
            bot.requestLineFollower(1, 2, onLineFollower)
            sleep(0.5)
    except KeyboardInterrupt:
        bot.close()
