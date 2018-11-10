import threading
import time

class ddbug(threading.Thread):
    def __init__(self):
        super().__init__()
        self.work = True

    def run(self):
        while self.work:
            time.sleep(1)

def turnStr(word: str):
    wordfin = ""
    for x in range(len(word)):
        wordfin += word[len(word) - 1 - x]
    return wordfin


def lsame(fullword: str, partword: str, exact=True):
    matches = 0
    if not exact:
        fullword = fullword.lower()
        partword = partword.lower()
    for x, y in zip(fullword, partword):
        if x == y:
            matches += 1
    if matches == len(partword):
        return True
    else:
        return False


def rsame(fullword: str, partword: str, exact=True):
    matches = 0
    if not exact:
        fullword = fullword.lower()
        partword = partword.lower()
    fullwordX = turnStr(fullword)
    partwordX = turnStr(partword)
    for x, y in zip(fullwordX, partwordX):
        if x == y:
            matches += 1
    if matches == len(partword):
        return True
    else:
        return False




class TimerC:
    def __init__(self):
        self.starttime = 0
        self.stoptime = 0
        self.startpausetime = 0
        self.stoppausetime = 0
        self.Time = 0
        self.Pause = 0

        self.Running = False
        self.Paused = False
        self.End = False

    def start(self):
        self.reset()
        self.Running = True
        self.starttime = time.time()

    def stop(self):
        if self.Running:
            if self.Paused:
                self.unpause()
            self.stoptime = time.time()
            self.reload()
            self.End = True

    def pause(self):
        if not self.End:
            if not self.Paused:
                self.Paused = True
                self.startpausetime += time.time()

    def unpause(self):
        if not self.End:
            if self.Paused:
                self.Paused = False
                self.stoppausetime += time.time()
                self.reload()

    def reset(self):
        self.starttime = 0
        self.stoptime = 0
        self.startpausetime = 0
        self.stoppausetime = 0
        self.Time = 0
        self.Pause = 0

        self.Running = False
        self.Paused = False
        self.End = False

    def switch(self):
        if not self.Paused:
            self.pause()
        else:
            self.unpause()

    def reload(self):
        if self.Paused:
            self.Pause = time.time() - self.startpausetime
        else:
            self.Pause = self.stoppausetime - self.startpausetime

        if self.End:
            self.Time = self.stoptime - self.starttime - self.Pause
        else:
            self.Time = time.time() - self.starttime - self.Pause

    def getTime(self):
        self.reload()
        return self.Time

    def getTimeFor(self):
        self.reload()
        return TimeFor(self.Time)

def TimeFor(Time):
    if (round(Time) % 60) == 0:
        TimeFor = "%s:%s%s" % (round(Time) // 60, 0, 0)
    elif (round(Time) % 60) < 10:
        TimeFor = "%s:%s%s" % (round(Time) // 60, 0, round(Time) % 60)
    else:
        TimeFor = "%s:%s" % (round(Time) // 60, round(Time) % 60)
    return TimeFor
