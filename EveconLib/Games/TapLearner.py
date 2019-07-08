import time
import random
import EveconLib.Programs.Scanner
import EveconLib.Config

def play():
    lastTime = time.time()

    # statistics
    alltries = 0
    righttries = 0
    alltimes = 0

    pressKey = random.randint(0, len(EveconLib.Config.Alphabet) - 1)
    print(EveconLib.Config.Alphabet[pressKey].lower())

    def fastWrite(key):
        global lastTime, pressKey, righttries, alltimes, alltries

        alltries += 1
        if key.lower() == EveconLib.Config.Alphabet[pressKey].lower():
            righttries += 1
        alltimes += time.time() - lastTime

        # print(str(key.lower() == EveconLib.Alphabet[pressKey].lower()) + ": " + str(time.time() - lastTime))
        print(str(key.lower() == EveconLib.Config.Alphabet[pressKey].lower()) + ": " + "Average time: %s, Tries: %s/%s" % (
        alltimes / alltries, righttries, alltries))

        pressKey = random.randint(0, len(EveconLib.Config.Alphabet) - 1)
        print(EveconLib.Config.Alphabet[pressKey].lower())
        lastTime = time.time()

    s = EveconLib.Programs.Scanner(fastWrite)
    s.start()