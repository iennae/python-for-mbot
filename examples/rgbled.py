from lib.mBot import *

if __name__ == "__main__":
    bot = mBot()
    bot.startWithSerial()
    try:
        while True:
            bot.doRGBLedOnBoard(1, 100, 0, 0)
            sleep(0.5)
            bot.doRGBLedOnBoard(1, 0, 100, 0)
            sleep(0.5)
    except KeyboardInterrupt:
        bot.doRGBLedOnBoard(0, 0, 0, 0)
        bot.close()
