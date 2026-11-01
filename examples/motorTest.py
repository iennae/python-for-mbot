from lib.mBot import *

if __name__ == "__main__":
    bot = mBot()
    bot.startWithSerial()
    try:
        while True:
            bot.doMove(100, 100)
            sleep(2)
            bot.doMove(-100, -100)
            sleep(2)
            bot.doMove(0, 0)
            sleep(2)
    except KeyboardInterrupt:
        bot.doMove(0, 0)
        bot.close()
