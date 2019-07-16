import time
import EveconLib.Programs.Scanner
import EveconLib.Config

alltries = 0
righttries = 0
alltimes = 0
lastTime = 0


def play():
    global lastTime, righttries, alltimes, alltries
    lastTime = time.time()

    def setLastTime(key):
        global lastTime
        print(time.time() - lastTime)
        lastTime = time.time()

    # statistics
    alltries = 0
    righttries = 0
    alltimes = 0


    s = EveconLib.Programs.Scanner(setLastTime)
    s.start()