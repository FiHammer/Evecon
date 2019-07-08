import threading
import datetime
import time

import EveconLib.Config
import EveconLib.Tools
import EveconLib.Networking

class title_time(threading.Thread):

    def __init__(self, freq):
        threading.Thread.__init__(self)
        self.stop = 0
        self.freq = freq
        # self.stopped = False
        self.pause = False
        self.stop = False
        self.ss = False
        self.sstime = ""
        self.normrun = True

    def run(self):
        while not self.stop:
            while self.normrun:
                EveconLib.Tools.title()
                time.sleep(self.freq)
            time.sleep(0.1)
            while self.ss:
                first = time.time()
                while self.ss:
                    time.sleep(0.25)

                    if (round(time.time() - first) % 60) < 10:
                        self.sstime = str(round(time.time() + EveconLib.Config.pausetime - first) // 60) + ":0" + str(
                            round(time.time() + EveconLib.Config.pausetime - first) % 60)
                    else:
                        self.sstime = str(round(time.time() + EveconLib.Config.pausetime - first) // 60) + ":" + str(
                            round(time.time() + EveconLib.Config.pausetime - first) % 60)

                    EveconLib.Tools.title("OLD", "OLD", self.sstime)

    def deac(self):
        self.stop = True
        self.normrun = False
        self.ss = False

    def ss_switch(self):
        if self.ss:
            self.pause = True
            self.ss = False
        else:
            self.pause = False
            self.ss = True



def LogServerless(functioni, info, typei = "Normal", printIt=False):
    part_time = "[" + datetime.datetime.now().strftime("%H:%M:%S:%f") + "]"
    if typei == "Debug" or typei == -1:
        part_type = "[Debug]"
    elif typei == "Normal" or typei == 0:
        part_type = "[Info]"
    elif typei == "Warning" or typei == 1:
        part_type = "[Warning]"
    elif typei == "Error" or typei == 2:
        part_type = "[Error]"
    else:
        part_type = ""
    part_func = "[" + functioni + "]"

    log_write = part_time + " " + part_type + " " + part_func + ": " + str(info) + "\n"

    if printIt:
        print(log_write.rstrip())

    log_file = open(EveconLib.Config.logFile, "a+")
    log_file.write(log_write)
    log_file.close()

    return log_write

# noinspection PyTypeChecker
def Log(functioni, info, typei = "Normal", printIt=False):
    part_time = "[" + datetime.datetime.now().strftime("%H:%M:%S:%f") + "]"
    if typei == "Debug" or typei == -1:
        part_type = "[Debug]"
    elif typei == "Normal" or typei == 0:
        part_type = "[Info]"
    elif typei == "Warning" or typei == 1:
        part_type = "[Warning]"
    elif typei == "Error" or typei == 2:
        part_type = "[Error]"
    else:
        part_type = ""
    part_func = "[" + functioni + "]"

    log_write = part_time + " " + part_type + " " + part_func + ": " + str(info) + "\n"

    try:
        if EveconLib.Config.logServer.running:
            EveconLib.Config.logServer.sendToAll(log_write)
    except AttributeError:
        pass
    if printIt:
        print(log_write.rstrip())

    log_file = open(EveconLib.Config.logFile, "a+")
    log_file.write(log_write)
    log_file.close()

    return log_write

