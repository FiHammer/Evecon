import EveconLib.Config
import threading
import time

class ddbug(threading.Thread):
    def __init__(self):
        super().__init__()
        self.work = True

    def run(self):
        while self.work:
            time.sleep(1)

def setupDDbugger(force=False):
    if force or EveconLib.Config.DEBUGGING:
        EveconLib.Config.ddbugger = ddbug()
        EveconLib.Config.ddbugger.start()

def setupDebuggingExtreme(force=False):
    if force or EveconLib.Config.DEBUGGING:
        setupDDbugger()
        EveconLib.Config.DEBUGGING = True
        EveconLib.Config.NEVERCLEAR = True
        EveconLib.Config.alwaysPrintLog = True
