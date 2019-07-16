import subprocess
import os
import psutil
import time

import EveconLib.Tools.Tools
import EveconLib.EveconMiniDebug as EveconMiniDebug
import EveconLib.EveconExceptions as EveconExceptions

class MegacmdC:
    def __init__(self, path):
        self.path = path + "\\MEGAclient.exe"
        self.MegacmdServer = EveconMiniDebug.MegaCmdServerTest()
        #self.Running = False
        self.LoggedIn = False
        self.email = None
        self.pw = None
    def __start__(self, command): # the client for an action
        if self.Running:
            subprocess.call([self.path] + list(command))
        else:
            self.startServer()
            subprocess.call([self.path] + list(command))
    def __del__(self):
        self.logout()
        #self.stopServer()
    def _running(self):
        if "MEGAcmdServer.exe" in (p.name() for p in psutil.process_iter()):
            return True
        else:
            return False
    Running = property(_running)
    def startServer(self):
        if not self.Running:
            if "MEGAcmdServer.exe" in (p.name() for p in psutil.process_iter()):
                pass
            else:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                self.MegacmdServer = subprocess.Popen([self.path], startupinfo=startupinfo, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     #stderr=subprocess.PIPE, shell=False)
                                     stderr = subprocess.PIPE, shell = True)

                time.sleep(1)

                EveconLib.Tools.Tools.cls()
                print("Started Server!")
        else:
            pass

    def stopServer(self):
        if self.Running:
            if not self.LoggedIn:
                pass
                #self.MegacmdServer.kill()
                #self.Running = False
            else:
                self.logout()
                #self.MegacmdServer.kill()
                #self.Running = False
            print("Stopped Server! (not really)")
        else:
            raise EveconExceptions.MegaNotRunning
    def login(self, email, pw):
        if not self.LoggedIn:
            self.LoggedIn = True
            self.email = email
            self.pw = pw
            self.__start__(["login", email, pw])
            print("Logged In!")
        else:
            self.logout()
            self.login(email, pw)
    def logout(self):
        if self.LoggedIn:
            self.LoggedIn = False
            self.email = None
            self.pw = None
            self.__start__(["logout"])
            print("Logged Out!")
        else:
            pass
    def upload(self, localfilesx, remotepath, Eveconpath=True): # put \test.txt /Evecon
        if self.LoggedIn:
            localfiles = []
            if Eveconpath:
                if type(localfilesx) == list:
                    for x in range(len(localfilesx)):
                        localfiles.append(os.getcwd() + "\\" + localfilesx[x])
                else:
                    localfiles = [os.getcwd() + "\\" + localfilesx]
            else:
                localfiles = [localfilesx]
            print("Uploading")
            self.__start__(["put"] + localfiles + [remotepath])
            #print(["put"] + localfiles + [remotepath])
            print("Upload successful!")
        else:
            raise EveconExceptions.MegaNotLoggedIn("upload")
    def download(self, remotepath, localpathx, Eveconpath = True): # get ! remotepath could also be a normal download link
        if Eveconpath:
            localpath = [os.getcwd() + "\\" + localpathx]
        else:
            localpath = [localpathx]
        print("Downloading")
        self.__start__(["get"] + [remotepath] + localpath)
        print("Download successful!")
    def rm(self, remotepath): # rm (removes folder, file)
        self.__start__(["rm"] + [remotepath])
    def mkdir(self, remotepath): # mkdir
        self.__start__(["mkdir"] + [remotepath])
    def cd(self, remotepath): # cd
        self.__start__(["mkdir"] + [remotepath])
    def exit(self):
        self.logout()
        self.stopServer()
    def debug_reset(self):
        self.LoggedIn = False
        self.email = None
        self.pw = None
        if self.Running:
            self.stopServer()
        self.MegacmdServer = False
    def debug_start(self):
        self.LoggedIn = True

MegaCMD = MegacmdC("Programs\\MEGAcmd")