from lib.mBot import *

if __name__ == "__main__":
    bot = mBot()
    bot.startWithSerial()

    def onDistance(dist):
        print("distance:", dist)
        if dist < 20:
            bot.doMove(-100, -100)
            sleep(0.5)
            bot.doMove(100, -100)
            sleep(0.1)
        bot.doMove(100, 100)

    try:
        while True:
            bot.requestUltrasonicSensor(1, 3, onDistance)
            sleep(0.2)
    except KeyboardInterrupt:
        bot.doMove(0, 0)
        bot.close()
