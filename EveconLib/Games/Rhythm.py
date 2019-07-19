import time
import EveconLib.Programs.Scanner

# how to: 1. setLastTime 2. LOOP every key press: 2.1 printIt 2.2 setLastTime

class Game:
    def __init__(self, maxPressToSave=10):
        self.alltries = 0
        self.righttries = 0
        self.alltimes = 0
        self.lastTime = 0

        self.maxPressToSave = maxPressToSave

        self.lastPresses = []

    def newPress(self):
        if len(self.lastPresses) >= self.maxPressToSave:
            del self.lastPresses[0]
        self.lastPresses.append(time.time() - self.lastTime)
        self.setLastTime()

    def setLastTime(self, key=""):
        self.lastTime = time.time()

    def getPrint(self, lastPresses=5):
        out = []
        if lastPresses > len(self.lastPresses):
            lastPresses = len(self.lastPresses)
        for index in range(lastPresses):
            out.append(self.lastPresses[index])
        return out


    def printIt(self, lastPresses=5):
        EveconLib.Tools.cls()
        for line in self.getPrint(lastPresses):
            print(line)

    def start(self):
        self.setLastTime()

    def reset(self):
        self.lastTime = 0
        self.alltries = 0
        self.righttries = 0
        self.alltimes = 0


def play():
    game = Game()
    game.start()

    def pushBtn(key):
        game.newPress()
        game.printIt(10)

    s = EveconLib.Programs.Scanner(pushBtn)
    s.start()