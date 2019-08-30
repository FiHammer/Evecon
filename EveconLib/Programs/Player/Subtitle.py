import os
import threading
import time
import pyvtt
import EveconLib

class SubTitleParser:
    """
    parses a .vtt file to a method time => subtitle part
    """

    VALID_TYPES = ["vtt"]

    def __init__(self, filePath: str):
        self.path = filePath

        self.file = self.path.split(EveconLib.Config.path_seg)[-1]
        self.fileExt = self.file.split(".")[-1]

        self.pyvttObj = None

        self.validation = None
        self.read = False

    def validate(self):
        if not os.path.exists(self.path):
            self.validation = False
            return False

        if not os.path.isfile(self.path):
            self.validation = False  # no file
            return False

        if not self.fileExt in self.VALID_TYPES:
            self.validation = False  # wrong type
            return False

        self.validation = True
        return True

    def readFile(self):
        if self.validation is None:
            self.validate()
        if not self.validation:
            return

        self.pyvttObj = pyvtt.open(self.path)
        self.read = True

    def getSub(self, time: float):
        if not self.read:
            self.readFile()
        if not self.read:
            return
        for dataPart in self.pyvttObj.data:
            if dataPart.start.ordinal <= time*1000 < dataPart.end.ordinal:
                return dataPart.text
        return ""  # nothing found

    def timeToNextSub(self, time: float):
        if not self.read:
            self.readFile()
        if not self.read:
            return
        pre = 0.0  # time to prev
        nex = float("inf")  # time to next

        for dataPart in self.pyvttObj.data:
            if dataPart.start.ordinal <= time*1000 < dataPart.end.ordinal:
                pre = dataPart.start.ordinal - time*1000
                nex = dataPart.end.ordinal - time*1000
                break  # found best possibilities
            else:
                if dataPart.start.ordinal <= time*1000:  # we bigger; set prev
                    if pre > dataPart.start.ordinal - time*1000:
                        pre = dataPart.start.ordinal - time*1000
                if dataPart.end.ordinal >= time*1000:  # we tinier; set nex
                    nex = dataPart.end.ordinal - time*1000
                    break  # found it
        return nex/1000

class SubTitleParserChanger(threading.Thread):
    """
    changes a string on end of the subtitle part
    """
    def __init__(self, setFunc, subFile, timer=None):
        super().__init__()
        self.setFunc = setFunc
        self.sub = SubTitleParser(subFile)
        self.time = 0.0
        self.timer = timer

        self.lastSub = ""

    def run(self):
        self.sub.readFile()
        if not self.sub.validation:
            return
        if self.timer is None:
            while self.sub.timeToNextSub(self.time) != float("inf"):  # new sub
                self.setFunc(self.sub.getSub(self.time))
                self.time = self.sub.timeToNextSub(self.time) + 0.1
                time.sleep(self.time)
        else:
            while self.timer.getTime() == 0:  # wait for begin
                time.sleep(0.3)

            while self.sub.timeToNextSub(self.timer.getTime()) != float("inf"):  # new sub
                self.setFunc(self.sub.getSub(self.timer.getTime()))
                self.time = self.sub.timeToNextSub(self.timer.getTime()) + 0.1
                time.sleep(self.time)

    def canChange(self):  # can i change the sub
        if self.lastSub != self.sub.getSub(self.timer.getTime()):
            self.lastSub = self.sub.getSub(self.timer.getTime())
            return self.lastSub
        return False