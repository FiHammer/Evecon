import EveconMiniDebug

def title(x=None, y=None, z=None):
    return False

class szipCLin:
    def __init__(self):
        pass
    def create_archive(self, archive, filenames, switches=None, workpath=None, archive_type="zip"):
        pass
    def extract_archive(self, archive, output=None, switches=None, EveconPath=True):
        pass

class MegacmdCLin:
    def __init__(self):
        pass
    def __start__(self, command):
        pass
    def startServer(self):
        pass
    def stopServer(self):
        pass
    def login(self, email, pw):
        pass
    def logout(self):
        pass
    def upload(self, localfilesx, remotepath, Eveconpath=True): # put \test.txt /Evecon
        pass
    def download(self, remotepath, localpathx, Eveconpath = True): # get ! remotepath could also be a normal download link
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


class MPlayerCLin:
    def __init__(self):
        pass
    def start(self, track):
        pass
    def stop(self):
        pass
    def pause(self):
        pass
    def unpause(self):
        pass
    def switch(self):
        pass