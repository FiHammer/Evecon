class MegacmdC:
    def __init__(self, path):
        self.path = path + "NOTHING HERE"
        self.MegacmdServer = None
        #self.Running = False
        self.LoggedIn = False
        self.email = None
        self.pw = None
    def __start__(self, command):
        pass
    def __del__(self):
        pass
    def _running(self):
        return False
    Running = property(_running)
    def startServer(self):
        pass

    def stopServer(self):
        pass
    def login(self, email, pw):
        pass
    def logout(self):
        pass
    def upload(self, localfilesx, remotepath, Eveconpath=True):
        pass
    def download(self, remotepath, localpathx, Eveconpath = True):
        pass
    def rm(self, remotepath): # rm (removes folder, file)
        pass
    def mkdir(self, remotepath): # mkdir
        pass
    def cd(self, remotepath): # cd
        pass
    def exit(self):
        pass
    def debug_reset(self):
        pass
    def debug_start(self):
        pass

MegaCMD = MegacmdC("RIP")