import EveconLib.EveconExceptions as EveconExceptions
class MegaCmdServerTest:
    def __init__(self):
        self.init = True
        self.errors = 0
    def kill(self):
        self.errors += 1
        print("Server not started, Hi I'm MiniDebug")
        raise EveconExceptions.MegaNotRunning