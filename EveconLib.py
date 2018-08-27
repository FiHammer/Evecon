import time
import ctypes
import os
import sys
import datetime
import socket
import threading
import subprocess
import webbrowser
import EveconExceptions
import EveconMiniDebug
import psutil
import random
import win32process
import pyglet
import win32api
import win32gui
import win32con
import win32gui_struct
import itertools
import glob

ico = r"C:\Users\Mini-Pc Nutzer\Desktop\Evecon\data\Ico\Radio.ico"

def nircmd(preset="Man", a=None, b=None, c=None, d=None, every=False):

    def setsize(length=995, width=521, x=100, y=100):

        dir_tmp = os.getcwd()
        os.chdir("Programs\\nircmd")
        #subprocess.call(["nircmd", "win", "setsize", "process", "py.exe", x, y, length, width])
        #subprocess.call(["nircmd", "win", "setsize", "process", "/%s" % os.getpid(), x, y, length, width])
        os.system("nircmdc win setsize process py.exe %s %s %s %s" % (x, y, length, width))
        #os.system("nircmdc win setsize process /%s %s %s %s %s" % (os.getpid(), x, y, length, width))
        time.sleep(0.25)
        os.chdir(dir_tmp)

    def volume(volume_i):   #   0.45

        volume_o = round(65535 * volume_i)
        if volume_o > 65535:
            volume_o = 65535


        dir_tmp = os.getcwd()
        os.chdir("Programs\\nircmd")
        subprocess.call(["nircmd", "setsysvolume", str(volume_o)])
        # os.system("nircmdc nircmd setsysvolume %s" % volume_o)
        time.sleep(0.25)
        os.chdir(dir_tmp)

    def maxi():
        dir_tmp = os.getcwd()
        os.chdir("Programs\\nircmd")
        subprocess.call(["nircmdc", "win", "max", "process", "py.exe"])
        subprocess.call(["nircmdc", "win", "max", "process", "/%s" % os.getpid()])
        time.sleep(0.25)
        os.chdir(dir_tmp)

    def foreground():
        dir_tmp = os.getcwd()
        os.chdir("Programs\\nircmd")
        #global ttime_pause
        #ttime_pause = False
        #ctypes.windll.kernel32.SetConsoleTitleW("Evecon: Loading")
        subprocess.call(["nircmdc", "win", "activate", "process", "py.exe"])
        subprocess.call(["nircmdc", "win", "activate", "process", "/%s" % os.getpid()])
        #subprocess.call(["nircmdc", "win", "activate", "title", "Evecon: Loading"])
        #os.system('nircmd win activate title "Evecon: Loading"')
        #ttime_pause = True
        os.chdir(dir_tmp)

    if preset == "setsize":
        if a is None and b is None and c is None and d is None:
            setsize()
        elif every is True:
            setsize(a, b, c, d)
        else:
            setsize(a, b)
    elif preset == "volume":
        volume(a)
    elif preset == "maxi":
        maxi()
    elif preset == "foreground":
        foreground()

class szipC:
    def __init__(self, path):
        self.path = path + "\\7za.exe"
    def create_archive(self, archive, filenames, switches=None, workpath=None, archive_type="zip"):
        if archive[len(archive)-1] == archive_type[len(archive_type)-1] and archive[len(archive)-2] == archive_type[len(archive_type)-2] and archive[len(archive)-3] == archive_type[len(archive_type)-3]:
            if archive_type == "zip" : # is the archive_type supported?
                dir_tmp = os.getcwd()
                if workpath is None:
                    archive = dir_tmp + "\\" + archive
                    for x in range(len(filenames)):
                        filenames[x] = dir_tmp + "\\" + filenames[x]
                else:
                    archive = workpath + "\\" + archive
                    for x in range(len(filenames)):
                        filenames[x] = workpath + "\\" + filenames[x]

                if switches is None:
                    command = [self.path, "a", "-t" + archive_type, archive] + list(filenames)
                else:
                    command = [self.path, "a", "-t" + archive_type] + list(switches) + [archive] + list(filenames)

                subprocess.call(command)

            else:
                print("error archive type is not supported")
        else:
            print("error archive type is not the same as the archive name")

    def extract_archive(self, archive, output=None, switches=None, workpath=None):
        if os.path.exists(archive) or os.path.exists(workpath + "\\" + archive):
            dir_tmp = os.getcwd()
            if workpath is None:
                archive = dir_tmp + "\\" + archive
            else:
                archive = workpath + "\\" +  archive

            if switches is None:
                if output is None:
                    command = [self.path, "x", archive]
                else:
                    command = [self.path, "x", "-o" + output, archive]
            else:
                if output is None:
                    command = [self.path, "x"] + list(switches) + [archive]
                else:
                    command = [self.path, "x", "-o" + output] + list(switches) + [archive]


            subprocess.call(command)

        else:
            print("error archive not found")

szip = szipC("Programs\\7z")



class MegacmdC:
    def __init__(self, path):
        self.path = path + "\\MEGAclient.exe"
        self.MegacmdServer = EveconMiniDebug.MegaCmdServerTest()
        self.Running = False
        self.LoggedIn = False
        self.email = None
        self.pw = None
    def __start__(self, command):
        if self.Running:
            subprocess.call([self.path] + list(command))
        else:
            self.startServer()
            subprocess.call([self.path] + list(command))
    def startServer(self):
        if not self.Running:
            if "MEGAcmdServer.exe" in (p.name() for p in psutil.process_iter()):
                raise EveconExceptions.MegaIsRunning(True)
            else:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                self.MegacmdServer = subprocess.Popen([self.path], startupinfo=startupinfo, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=False)
                self.Running = True
                time.sleep(1)

                cls()
                print("Started Server!")
        else:
            raise EveconExceptions.MegaIsRunning(False)

    def stopServer(self):
        if self.Running:
            if not self.LoggedIn:
                self.MegacmdServer.kill()
                self.Running = False
            else:
                self.logout()
                self.MegacmdServer.kill()
                self.Running = False
            print("Stopped Server!")
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
            raise EveconExceptions.MegaLoggedIn
    def logout(self):
        if self.LoggedIn:
            self.LoggedIn = False
            self.email = None
            self.pw = None
            self.__start__(["logout"])
            print("Logged Out!")
        else:
            raise EveconExceptions.MegaNotLoggedIn("logout")
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

            self.__start__(["put"] + localfiles + [remotepath])
            print(["put"] + localfiles + [remotepath])
            print("Upload successful!")
        else:
            raise EveconExceptions.MegaNotLoggedIn("upload")
    def download(self, remotepath, localpathx, Eveconpath = True): # get ! remotepath could also be a normal download link
        if Eveconpath:
            localpath = [os.getcwd() + "\\" + localpathx]
        else:
            localpath = [localpathx]

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
        else:
            self.Running = False
        self.MegacmdServer = False
    def debug_start(self):
        self.LoggedIn = True
        self.Running = True

Megacmd = MegacmdC("Programs\\MEGAcmd")


class MPlayerC:
    def __init__(self, path):
        self.path = path + "\\mplayer.exe"
        self.Running = False
        self.Paused = False
        self.Stopped = False
        self.Type = None
        self.mplayer = None
        self.Track = None

    def start(self, track):
        if not self.Running:
            self.Track = track
            if lsame(self.Track, "http"):
                self.Type = "stream"
            else:
                self.Type = MusicType(self.Track, True)
            self.mplayer = subprocess.Popen([self.path, self.Track], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

            self.Stopped = False
            self.Running = True
            self.Paused = False

    def stop(self):
        if self.Running:
            self.mplayer.terminate()
            self.Stopped = True
            self.Track = None
            self.Type = None
            self.Running = False
            self.mplayer = None

    def pause(self):
        if not self.Paused:
            self.mplayer.terminate()
            self.Paused = True
            self.Running = False

    def unpause(self):
        if self.Paused:
            self.mplayer = subprocess.Popen([self.path, self.Track], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            self.Running = True
            self.Paused = False

    def switch(self):
        if self.Paused:
            self.unpause()
        else:
            self.pause()

MPlayer = MPlayerC("Programs\\MPlayer")

class MusicPlayerC(threading.Thread):
    def __init__(self):
        super().__init__()

        self.musiclist = []
        self.musiclistname = []
        self.musiclistpath = []
        self.musiclistdirname = []
        self.musiclistdirnamefull = []

        global musicrun
        musicrun = True
        self.musicrun = True

        self.musicpause = False
        self.musicwait = False
        self.musicwaitvol = False
        self.musicwaitvolp = False
        self.musicwaitseek = False
        self.musicwaitSpl = False
        self.musicback = False
        self.music_time = 0
        self.musicvolume = 0.5
        self.musicvolumep = 1
        self.musicplayer = None
        self.musicplaying = True
        self.musicexitn = False
        self.musicaddpl = False
        self.musicrunning = False

        self.musicman_list = []
        self.music_playlists_used = {}

        self.lastmusicnumber = 0
        self.thismusicnumber = 0
        self.nextmusicnumber = 0

        self.music_playlists = ["LiS", "Anime", "Phunk", "Caravan Palace", "Electro Swing", "Parov Stelar", "jPOP & etc", "OMFG"]
        self.music_playlists_key = ["lis", "an", "phu", "cp", "es", "ps", "jpop", "omfg"]
        self.music_playlists_active = []

        self.spl = False
        self.splmp = SplatoonC()

    def addMusic(self, key, loadMu=True): # key (AN, LIS)
        if not Computerfind_MiniPC:
            cls()
            print("Loading...")

            if key == "us":
                self.searchMusic("Music\\User", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "lis":
                self.searchMusic("Music\\Presets\\Life is Strange", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "an":
                self.searchMusic("Music\\Presets\\Anime", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "phu":
                self.searchMusic("Music\\Presets\\Phunk", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "cp":
                self.searchMusic("Music\\Presets\\Caravan Palace", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "es":
                self.searchMusic("Music\\Presets\\Electro Swing", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "ud":
                cls()
                self.searchMusic(input("Your path:\n"), loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "ps":
                self.searchMusic("Music\\Presets\\Parov Stelar", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "jpop":
                self.searchMusic("Music\\Presets\\jPOP-etc", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "omfg":
                self.searchMusic("Music\\Presets\\OMFG", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True

            else:
                return False

        else:
            cls()
            print("Loading... (On Mini-PC)")

            if key == "us":
                self.searchMusic("Music\\User", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "lis":
                self.searchMusic(MusicDir + "\\Games\\Life is Strange", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "an":
                self.searchMusic(MusicDir + "\\Anime", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "phu":
                self.searchMusic(MusicDir + "\\Phunk", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "cp":
                self.searchMusic(MusicDir + "\\Caravan Palace", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "es":
                self.searchMusic(MusicDir + "\\Electro Swing", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "ud":
                cls()
                self.searchMusic(input("Your path:\n"), loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return "ul"
            elif key == "ps":
                self.searchMusic(MusicDir + "\\Parov Stelar", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "jpop":
                self.searchMusic(MusicDir + "\\jPOP-etc", loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            elif key == "omfg":
                self.searchMusic(MusicDir + "\\OMFG" ,loadMu)
                self.music_playlists_active.append(key)
                print("Finished")
                return True
            else:
                return False
    def reloadMusic(self, tracknum):
        print(tracknum)
        self.musiclist[tracknum] = pyglet.media.load(self.musiclistpath[tracknum])

    def searchMusic(self, mDir, loadMu=True): # sucht nur
        firstDir = os.getcwd()
        os.chdir(mDir)

        dirtmp = os.getcwd()
        os.chdir("..")
        nowtmp = os.getcwd()
        os.chdir(dirtmp)

        dirx = dirtmp.lstrip(nowtmp)
        self.musiclistdirname.append(dirx)
        self.musiclistdirnamefull.append(str(os.getcwd()) + "\\" + dirx)

        dir1 = os.listdir(os.getcwd())
        for x1 in range(len(os.listdir(os.getcwd()))):
            if os.path.isdir(dir1[x1]):
                self.musiclistdirname.append(dir1[x1])
                self.musiclistdirnamefull.append(str(os.getcwd()) + "\\" + dir1[x1])
                os.chdir(dir1[x1])
                dir2 = os.listdir(os.getcwd())
                for x2 in range(len(os.listdir(os.getcwd()))):
                    if os.path.isdir(dir2[x2]):
                        self.musiclistdirname.append(dir2[x2])
                        self.musiclistdirnamefull.append(str(os.getcwd()) + "\\" + dir2[x2])
                        os.chdir(dir2[x2])
                        dir3 = os.listdir(os.getcwd())
                        for x3 in range(len(os.listdir(os.getcwd()))):
                            if os.path.isdir(dir3[x3]):
                                os.chdir(dir3[x3])
                                os.chdir("..")
                            if os.path.isfile(dir3[x3]):
                                if dir3[x3][len(dir3[x3]) - 3] == "m" and dir3[x3][len(dir3[x3]) - 2] == "p" and \
                                        dir3[x3][len(dir3[x3]) - 1] == "3":
                                    if loadMu:
                                        self.musiclist.append(pyglet.media.load(dir3[x3]))
                                    self.musiclistname.append(dir3[x3])
                                    self.musiclistpath.append(str(os.getcwd()) + "\\" + dir3[x3])
                                elif dir3[x3][len(dir3[x3]) - 3] == "m" and dir3[x3][len(dir3[x3]) - 2] == "p" and \
                                        dir3[x3][len(dir3[x3]) - 1] == "4":
                                    if loadMu:
                                        self.musiclist.append(pyglet.media.load(dir3[x3]))
                                    self.musiclistname.append(dir3[x3])
                                    self.musiclistpath.append(str(os.getcwd()) + "\\" + dir3[x3])
                        os.chdir("..")
                    if os.path.isfile(dir2[x2]):
                        if dir2[x2][len(dir2[x2]) - 3] == "m" and dir2[x2][len(dir2[x2]) - 2] == "p" and dir2[x2][
                            len(dir2[x2]) - 1] == "3":
                            if loadMu:
                                self.musiclist.append(pyglet.media.load(dir2[x2]))
                            self.musiclistname.append(dir2[x2])
                            self.musiclistpath.append(str(os.getcwd()) + "\\" + dir2[x2])
                        elif dir2[x2][len(dir2[x2]) - 3] == "m" and dir2[x2][len(dir2[x2]) - 2] == "p" and dir2[x2][
                            len(dir2[x2]) - 1] == "4":
                            if loadMu:
                                self.musiclist.append(pyglet.media.load(dir2[x2]))
                            self.musiclistname.append(dir2[x2])
                            self.musiclistpath.append(str(os.getcwd()) + "\\" + dir2[x2])

                os.chdir("..")
            if os.path.isfile(dir1[x1]):
                if dir1[x1][len(dir1[x1]) - 3] == "m" and dir1[x1][len(dir1[x1]) - 2] == "p" and dir1[x1][
                    len(dir1[x1]) - 1] == "3":
                    if loadMu:
                        self.musiclist.append(pyglet.media.load(dir1[x1]))
                    self.musiclistname.append(dir1[x1])
                    self.musiclistpath.append(str(os.getcwd()) + "\\" + dir1[x1])
                elif dir1[x1][len(dir1[x1]) - 3] == "m" and dir1[x1][len(dir1[x1]) - 2] == "p" and dir1[x1][
                    len(dir1[x1]) - 1] == "4":
                    if loadMu:
                        self.musiclist.append(pyglet.media.load(dir1[x1]))
                    self.musiclistname.append(dir1[x1])
                    self.musiclistpath.append(str(os.getcwd()) + "\\" + dir1[x1])
        os.chdir("..")
        os.chdir(firstDir)

    def Play(self):
        self.musicpause = False
        self.musicplayer.play()
    def Pause(self):
        self.musicpause = True
        self.musicplayer.pause()
    def Switch(self):
        if self.musicpause:
            self.Play()
        else:
            self.Pause()
    def Stop(self):
        global musicrun
        musicrun = False
        self.musicrun = False
        self.musicplaying = False
        self.musicpause = False
        self.musicrunning = False
    def Next(self):
        self.musicplaying = False
        if self.musicpause:
            self.musicpause = False
            self.musicplayer.play()
    def Last(self):
        pass
    def Del(self, mId):
        del self.musiclist[mId]
        del self.musiclistname[mId]
    def vol(self, vol):
        self.musicvolume = vol
        nircmd("volume", self.musicvolume)
    def volp(self, vol):
        self.musicvolumep = vol
        self.musicplayer.volume = self.musicvolumep
    def seek(self, ti):

        if ti < self.musiclist[self.thismusicnumber].duration:
            self.musicplayer.seek(ti)
            self.music_time = time.time() - ti
    def reroll(self):
        self.nextmusicnumber = random.randint(0, len(self.musiclist) - 1)
    def input(self, inpt):
        inpt = inpt.lower()
        if inpt == "":
            if not self.spl:
                self.musicplaying = False
                if self.musicpause:
                    self.musicpause = False
                    self.musicplayer.play()
            else:
                if self.spl:
                    if self.splmp.RoundOver:
                        self.splmp.RoundOverF()
                    else:
                        self.musicplaying = False
                        if self.musicpause:
                            self.musicpause = False
                            self.musicplayer.play()
        elif inpt == "play" or inpt == "pau" or inpt == "pause" or inpt == "p":
            self.Switch()
        elif inpt == "next" or inpt == "n":
            self.Next()
        elif inpt == "stop" or inpt == "exit":
            self.Stop()
        elif inpt == "del":
            self.Del(self.thismusicnumber)
            self.musicplaying = False
            if self.musicpause:
                self.musicpause = False
                self.musicplayer.play()
        elif inpt == "deln" or inpt == "delnext":
            nmnold = self.nextmusicnumber
            self.Del(self.nextmusicnumber)
            if nmnold < self.thismusicnumber:
                self.thismusicnumber -= 1
        elif inpt == "vol":
            self.musicwait = True
            self.musicwaitvol = True
            self.vol(float(input("Volume (Now: %s)\n" % self.musicvolume)))
            self.musicwait = False
            self.musicwaitvol = False
        elif inpt == "volp":
            self.musicwait = True
            self.musicwaitvolp = True
            self.volp(float(input("Volume Player")))
            self.musicwait = False
            self.musicwaitvolp = False
        elif inpt == "jump" or inpt == "j" or inpt == "seek" or inpt == "s":
            self.musicwait = True
            self.musicwaitseek = True
            self.seek(float(input().lower()))
            self.musicwait = False
            self.musicwaitseek = False
        elif inpt == "rm" or inpt == "rem" or inpt == "rerollm":
            self.reroll()
        elif inpt == "spl":
            if not self.spl:
                self.spl = True
            else:
                self.spl = False
        elif inpt == "exitn":
            self.musicexitn = True
        elif inpt == "addpl":
            self.musicaddpl = True
        elif self.musicaddpl:
            if inpt.lower() == "fin":
                self.musicaddpl = False
                self.printIt()
            else:
                x = self.addMusic(inpt.lower())

                if x:
                    self.music_playlists_used[inpt.lower()] = "X"
                elif x == "ul":
                    self.musicman_list.append("unkown list")

                self.printIt()

        else:
            if self.spl:
                self.splmp.input(inpt=inpt)

         # play, next, stop, pause, last, del, deln, vol, volp, mute, mutep, jump (to 0), reroll
         # SPL: spl (On/Off), wr, reroll, start (""), effect (E--)
    def run(self):

        self.thismusicnumber = random.randint(0, len(self.musiclist) - 1)
        self.nextmusicnumber = random.randint(0, len(self.musiclist) - 1)

        while self.musicrun:


            if self.musiclist[self.thismusicnumber].is_queued:
                self.reloadMusic(self.thismusicnumber)

            self.musicplayer = pyglet.media.Player()
            self.musicplayer.queue(self.musiclist[self.thismusicnumber])
            self.musicplayer.play()
            self.musicplayer.volume = self.musicvolumep
            self.music_time = time.time()
            self.musicrunning = True
            title("OLD", self.musiclistname[self.thismusicnumber], "Now Playing")

            self.musicplaying = True

            while self.musicplaying:

                time.sleep(0.25)
                for x in range(5):
                    if self.musicplayer.time == 0:
                        self.musicplaying = False
                    elif round(self.musiclist[self.thismusicnumber].duration) == round(time.time() - self.music_time):
                        self.musicplaying = False
                    time.sleep(0.05)
                while self.musicpause:
                    music_time_wait = time.time()

                    while self.musicpause:
                        time.sleep(0.25)
                    title("OLD", "OLD", "Now Playing:")
                    self.music_time += time.time() - music_time_wait

                    if self.spl:
                        self.splmp.PlaytimeStart += time.time() - music_time_wait
                        self.splmp.TimeLeftStart += time.time() - music_time_wait

            self.musicplayer.next()
            self.lastmusicnumber = self.thismusicnumber
            self.thismusicnumber = self.nextmusicnumber
            self.nextmusicnumber = random.randint(0, len(self.musiclist) - 1)
            self.musicrunning = False

            if self.musicexitn:
                self.Stop()



    def printIt(self):
        if self.musicrunning:
            cls()
            print("Musicplayer\n\nNow Playing:")
            if MusicType(self.musiclistname[self.thismusicnumber], True) == "mp3":
                print(self.musiclistname[self.thismusicnumber].rstrip(".mp3"))
            elif MusicType(self.musiclistname[self.thismusicnumber], True) == "mp4":
                print(self.musiclistname[self.thismusicnumber].rstrip(".mp4"))

            if (round(time.time() - self.music_time) % 60) < 10 and (
                    round(self.musiclist[self.thismusicnumber].duration) % 60) < 10:
                print(r"%s:%s%s\%s:%s%s" % (
                    round(time.time() - self.music_time) // 60, 0, round(time.time() - self.music_time) % 60,
                    round(self.musiclist[self.thismusicnumber].duration) // 60, 0,
                    round(self.musiclist[self.thismusicnumber].duration) % 60))
            elif (round(time.time() - self.music_time) % 60) < 10:
                print(r"%s:%s%s\%s:%s" % (
                    round(time.time() - self.music_time) // 60, 0, round(time.time() - self.music_time) % 60,
                    round(self.musiclist[self.thismusicnumber].duration) // 60,
                    round(self.musiclist[self.thismusicnumber].duration) % 60))
            elif (round(self.musiclist[self.thismusicnumber].duration) % 60) < 10:
                print(r"%s:%s\%s:%s%s" % (
                    round(time.time() - self.music_time) // 60, round(time.time() - self.music_time) % 60,
                    round(self.musiclist[self.thismusicnumber].duration) // 60, 0,
                    round(self.musiclist[self.thismusicnumber].duration) % 60))
            else:
                print(r"%s:%s\%s:%s" % (
                    round(time.time() - self.music_time) // 60, round(time.time() - self.music_time) % 60,
                    round(self.musiclist[self.thismusicnumber].duration) // 60,
                    round(self.musiclist[self.thismusicnumber].duration) % 60))

            print("\nNext Track:")
            if MusicType(self.musiclistname[self.thismusicnumber], True) == "mp3":
                print(self.musiclistname[self.nextmusicnumber].rstrip(".mp3"))
            elif MusicType(self.musiclistname[self.thismusicnumber], True) == "mp4":
                print(self.musiclistname[self.nextmusicnumber].rstrip(".mp4"))

            print("\n")
            if not self.musicwait:
                print("Pause (PAU), Stop (STOP), Next Track (NEXT), Volume (VOL)")
            elif self.musicwaitvol:
                print("Volume (Now: %s)\n" % self.musicvolume)
            elif self.musicwaitvolp:
                print("Volume Player:")
            elif self.musicwaitseek:
                print("Jump to (in sec) (DO NOT WORK!):")
            else:
                print("BUGGI")

            if self.spl:
                print("\n\n")
                self.splmp.printIt()

            if self.musicpause:
                cls()
                print("Musicplayer\n\nPaused:")
                if MusicType(self.musiclistname[self.thismusicnumber], True) == "mp3":
                    print(self.musiclistname[self.thismusicnumber].rstrip(".mp3"))
                elif MusicType(self.musiclistname[self.thismusicnumber], True) == "mp4":
                    print(self.musiclistname[self.thismusicnumber].rstrip(".mp4"))

                if (round(time.time() - self.music_time) % 60) < 10:
                    print(r"%s:%s%s\%s:%s" % (
                        round(time.time() - self.music_time) // 60, 0, round(time.time() - self.music_time) % 60,
                        round(self.musiclist[self.thismusicnumber].duration) // 60,
                        round(self.musiclist[self.thismusicnumber].duration) % 60))
                elif (round(self.musiclist[self.thismusicnumber].duration) % 60) < 10:
                    print(r"%s:%s\%s:%s%s" % (
                        round(time.time() - self.music_time) // 60, round(time.time() - self.music_time) % 60,
                        round(self.musiclist[self.thismusicnumber].duration) // 60, 0,
                        round(self.musiclist[self.thismusicnumber].duration) % 60))
                elif (round(time.time() - self.music_time) % 60) < 10 and (
                        round(self.musiclist[self.thismusicnumber].duration) % 60) < 10:
                    print(r"%s:%s%s\%s:%s%s" % (
                        round(time.time() - self.music_time) // 60, 0, round(time.time() - self.music_time) % 60,
                        round(self.musiclist[self.thismusicnumber].duration) // 60, 0,
                        round(self.musiclist[self.thismusicnumber].duration) % 60))
                else:
                    print(r"%s:%s\%s:%s" % (
                        round(time.time() - self.music_time) // 60, round(time.time() - self.music_time) % 60,
                        round(self.musiclist[self.thismusicnumber].duration) // 60,
                        round(self.musiclist[self.thismusicnumber].duration) % 60))

                print("\n\nPlay (PLAY), Stop (STOP)")

                if self.spl:
                    print("\n\n")
                    self.splmp.printIt()

            if self.musicaddpl:

                self.musicman_list = []
                self.music_playlists_used = {}

                for x in self.music_playlists_key:
                    self.music_playlists_used[x] = " "

                for x in self.music_playlists_active:
                    self.music_playlists_used[x] = "X"

                #if self.musicaddpl:
                music_playlists_used_List = []
                for x in self.music_playlists_key:
                    music_playlists_used_List.append(self.music_playlists_used[x])
                cls()
                print("Playlists:\n")
                # print(music_playlists_print)
                # print("User's list (US), User defined (UD)")
                # print("\nLoaded:")
                for xl, x2, x3 in zip(music_playlists_used_List, self.music_playlists,
                                      self.music_playlists_key):
                    print(" " + xl + " " + x2 + " (" + x3.upper() + ")")
                for x in self.musicman_list:
                    print(" X " + x)
                print("\nFinish (FIN)\n")
                #self.musicaddpl = False
        else:
            cls()
            print("Musicplayer\n\nLoading...")


def Music():

    def Play():
        class Printerr(threading.Thread):
            def run(self):
                while muPlayer.musicrun:
                    cls()
                    muPlayer.printIt()
                    time.sleep(0.75)
                    if muPlayer.musicpause:
                        cls()
                        muPlayer.printIt()
                    while muPlayer.musicpause:
                        time.sleep(0.5)

        Printer = Printerr()
        Printer.start()

        while muPlayer.musicrun:
            user_input = input()
            muPlayer.input(user_input)


    muPlayer = MusicPlayerC()

    music_playlists_print = ""
    for x, y in zip(muPlayer.music_playlists, muPlayer.music_playlists_key):
        music_playlists_print += x + " (" + y.upper() + "), "
    music_playlists_print = music_playlists_print.rstrip(", ")

    cls()
    print("Playlists:")
    print("\nFix Playlists:")
    print(music_playlists_print)
    print("\nCustom:")
    print("User's Playlist (US), User defined (UD), Mix (MIX), Multiple PL (MPL), All (ALL)\n")
    music_user_input = input()

    if music_user_input.lower() == "mix":
        muPlayer.addMusic("an")
        muPlayer.addMusic("phu")
        muPlayer.addMusic("cp")
        muPlayer.addMusic("es")
        muPlayer.addMusic("jpop")
    elif music_user_input.lower() == "j":
        muPlayer.addMusic("an")
        muPlayer.addMusic("jpop")
    elif music_user_input.lower() == "all":
        for x in muPlayer.music_playlists_key:
            muPlayer.addMusic(x)

    elif music_user_input.lower() == "mpl":
        musicman_search = True

        muPlayer.music_playlists.append("User's List")

        musicman_list = []
        music_playlists_used = {}

        for x in muPlayer.music_playlists_key:
            music_playlists_used[x] = " "

        while musicman_search:
            music_playlists_used_List = []
            for x in muPlayer.music_playlists_key:
                music_playlists_used_List.append(music_playlists_used[x])
            cls()
            print("Playlists:\n")
            #print(music_playlists_print)
            #print("User's list (US), User defined (UD)")
            #print("\nLoaded:")
            for xl, x2, x3 in zip(music_playlists_used_List, muPlayer.music_playlists, muPlayer.music_playlists_key):
                print(" " + xl + " " + x2 + " (" + x3.upper() + ")")
            for x in musicman_list:
                print(" X " + x)
            print("\nFinish (FIN)\n")

            musicman_user_input = input()


            if musicman_user_input.lower() == "fin":
                musicman_search = False

            else:
                x = muPlayer.addMusic(musicman_user_input.lower())

                if x:
                    music_playlists_used[musicman_user_input.lower()] = "X"
                elif x == "ul":
                    musicman_list.append("unkown list")

    elif music_user_input.lower() == "search":
        for x in muPlayer.music_playlists_key:
            muPlayer.addMusic(x, False)

        cls()
        print("What do you want to hear?")

        user_input_search = input()

        searchdir = Search(user_input_search, muPlayer.musiclistdirname)
        searchtrack = Search(user_input_search, muPlayer.musiclistname)

        musiclistpathold = muPlayer.musiclistpath
        muPlayer.musiclistpath = []
        musiclistnameold = muPlayer.musiclistname
        muPlayer.musiclistname = []

        for x in searchdir:
            muPlayer.searchMusic(muPlayer.musiclistdirnamefull[x])

        for x in searchtrack:
            muPlayer.musiclist.append(pyglet.media.load(musiclistpathold[x]))
            muPlayer.musiclistpath.append(musiclistpathold[x])
            muPlayer.musiclistname.append(musiclistnameold[x])

    else:
        muPlayer.addMusic(music_user_input.lower())

    if muPlayer.musiclist:
        muPlayer.start()
        Play()
    else:
        print("No track found")

    normaltitle()


def normaltitle():
    pass


def title(status="OLD", something="OLD", pc="OLD", deac=False):
    pass

def cls():
    os.system("cls")

Computerfind_MiniPC = True
MusicDir = "C:\\Users\\Mini-Pc Nutzer\\Desktop\\Musik\\Musik\\!Fertige Musik"
thisIP = "192.168.2.102"

class SplatoonC:
    def __init__(self, roundtime = 180):
        self.weapons = ["Disperser", "Disperser Neo", "Junior-Klechser", "Junior-Klechser Plus", "Fein-Disperser",
                   "Fein-Disperser Neo", "Airbrush MG", "Airbrush RG", "Klechser", "Tentatek-Klechser",
                   "Heldenwaffe Replik (Klechser)", "Okto-Klechser Replik", ".52 Gallon", ".52 Gallon Deko", "N-ZAP85",
                   "N-ZAP89", "Profi-Klechser", "Focus-Profi-Kleckser", ".96 Gallon", ".96 Gallon Deko", "Platscher",
                   "Platscher SE",

                   "Luna-Blaster", "Luna-Blaster Neo", "Blaster", "Blaster SE", "Helden-Blaster Replik",
                   "Fern-Blaster", "Fern-Blaster SE", "Kontra-Blaster", "Kontra-Blaster Neo", "Turbo-Blaster",
                   "Turbo-Blaster Deko", "Turbo-Blaster Plus", "Turbo-Blaster Plus Deko",

                   "L3 Tintenwerfer", "L3 Tintenwerfer D", "S3 Tintenwerfer", "S3 Tintenwerfer D", "L3 Tintenwerfer",
                   "Quetscher", "Quetscher Fol",

                   "Karbonroller", "Karbonroller Deko", "Klecksroller", "Medusa-Klecksroller", "Helden-Roller Replik",
                   "Dynaroller", "Dynaroller Tesla", "Flex-Roller", "Flex-Roller Fol",
                   "Quasto", "Quasto Fresco", "Kalligraf", "Kalligraf Fresco", "Helden-Pinsel Replik",

                   "Sepiator Alpha", "Sepiator Beta", "Klecks-Konzentrator", "Rilax-Klecks-Konzentrator",
                   "Helden-Konzentrator Replik", "Ziel-Konzentrator", "Rilax-Ziel-Konzentrator", "E-liter 4K",
                   "E-liter 4K SE", "Ziel-E-liter 4K", "Ziel-E-liter 4K SE", "Klotzer 14-A", "Klotzer 14-B", "T-Tuber",
                   "T-Tuber SE",

                   "Schwapper", "Schwapper Deko", "Helden-Schwapper Replik", "3R-Schwapper", "3R-Schwapper Fresco",
                   "Knall-Schwapper", "Trommel-Schwapper", "Trommel-Schwapper Neo", "Wannen-Schwapper",

                   "Klecks-Splatling", "Sagitron-Klecks-Splatling", "Splatling", "Splatling Deko",
                   "Helden-Splatling Replik", "Hydrant", "Hydrant SE", "Kuli-Splatling", "Nautilus 47",

                   "Sprenkler", "Sprenkler Fresco", "Klecks-Doppler", "Enperry-Klecks-Doppler", "Helden-Doppler Replik",
                   "Kelvin 525", "Kelvin 525 Deko", "Dual-Platscher", "Dual-Platscher SE", "Quadhopper Noir",
                   "Quadhopper Blanc",

                   "Parapulviator", "Sorella-Parapulviator", "Helden-Pulviator Replik", "Camp-Pulviator",
                   "Sorella-Camp-Pulviator",
                   "UnderCover", "Sorella-UnderCover"]


        self.RUN = True
        self.Start = False
        self.TimeLeft = 0
        self.TimeLeftStart = 0
        self.TimeLeftC = TimerC()
        self.Rounds = 0
        self.Playtime = 0
        self.PlaytimeStart = 0
        self.PlaytimeC = TimerC()
        self.RoundOver = True
        self.Effect = None

        self.RoundTime = roundtime # Debug! std: 180

        self.WR = False
        self.WRthis = self.randomWP()
        self.WRnext = self.randomWP()

    def input(self, inpt):
        inpt = inpt.lower()
        if inpt == "wr":
            self.WRswitch()
        elif inpt == "exit" or inpt == "stop":
            self.stop()
        elif inpt == "reroll" or inpt == "rerol" or inpt == "rero" or inpt == "re" or inpt == "r":
            self.WRreroll()
        elif len(inpt) > 1:
            if inpt[0] == "e":
                try:
                    self.ChEffect(int(inpt.lstrip("e")))
                except ValueError:
                    self.RoundOverF()
            else:
                self.RoundOverF()
        else:
            self.RoundOverF()

    def randomWP(self, printweapon=False):
        number = random.randint(0, len(self.weapons) - 1)
        if printweapon:
            print("Your Weapon:\n%s" % self.weapons[number])
        return self.weapons[number]

    def WRswitch(self):
        if self.WR:
            self.WR = False
        else:
            self.WR = True

    def stop(self):
        self.RUN = False

    def WRreroll(self):
        WRnextTMP = self.WRnext
        self.WRnext = self.randomWP()

        while self.WRthis == self.WRnext or WRnextTMP == self.WRnext:
            self.WRnext = self.randomWP()

    def ChEffect(self, eff):
        self.Effect = eff

    def RoundOverF(self):
        if self.RoundOver:
            if not self.Start:
                self.PlaytimeC.start()
                self.PlaytimeStart = time.time()
            self.TimeLeftC.start()
            self.TimeLeftStart = time.time()
            self.Rounds += 1

            if self.Effect is not None and self.Effect != 0:
                self.Effect -= 1

            if self.Start:
                WRthisTMP = self.WRthis
                self.WRthis = self.WRnext
                self.WRnext = self.randomWP()

                while WRthisTMP == self.WRnext or self.WRthis == self.WRnext:
                    self.WRnext = self.randomWP()

            self.RoundOver = False
            self.Start = True

    def printIt(self):
        self.TimeLeft = self.RoundTime - self.TimeLeftC.getTime()
        self.TimeLeft = self.RoundTime - round(time.time() - self.TimeLeftStart)

        if self.Start:
            self.Playtime = self.PlaytimeC.getTime()
            self.Playtime = round(time.time() - self.PlaytimeStart)
        else:
            self.Playtime = 0

        if self.RoundOver:
            TimeLeftFor = "No Round Started"
        else:
            if (self.TimeLeft % 60) < 10:
                TimeLeftFor = "%s:%s%s" % (self.TimeLeft // 60, 0, self.TimeLeft % 60)
            else:
                TimeLeftFor = "%s:%s" % (self.TimeLeft // 60, self.TimeLeft % 60)

        if (self.Playtime % 60) < 10:
            PlaytimeFor = "%s:%s%s" % (self.Playtime // 60, 0, self.Playtime % 60)
        else:
            PlaytimeFor = "%s:%s" % (self.Playtime // 60, self.Playtime % 60)

        if self.TimeLeft <= 0:
            self.RoundOver = True


        print("Splatoon 2\n")
        print("Time:\t\t %s" % TimeLeftFor)
        print("Round:\t\t %s" % self.Rounds)

        if self.Effect is not None and self.Effect != 0:
            print("Effect:\t\t %s" % self.Effect)
        elif self.Effect == 0:
            print("Effect:\t\t No Effect Active")

        print("Playtime:\t %s" % PlaytimeFor)
        if self.WR:
            print("\nWeapon Randomizer:")
            print("This Round:\t %s" % self.WRthis)
            print("Next Round:\t %s" % self.WRnext)

        if self.WR:
            print("\nWeapon Randomizer (WR), Effect ('E'+number), Reroll Next Weapon(REROLL)")
        else:
            print("\nWeapon Randomizer (WR), Effect ('E'+number)")

        if self.RoundOver:
            print("\nStart Next Round?")

def Search(searchkeyU, searchlistU, exact=False):

    if len(searchkeyU) == 0:
        return None

    if not exact:
        searchkey = searchkeyU.lower()
        searchlist = []
        for x in searchlistU:
            searchlist.append(x.lower())
    else:
        searchkey = searchkeyU
        searchlist = []
        for x in searchlistU:
            searchlist.append(x)

    OutputNum = []

    for sListNum in range(len(searchlist)): # wort aus der liste
        if len(searchkey) > len(searchlist[sListNum]):
            continue  # suchwort größer als anderes wort

        for letterNum in range(len(searchlist[sListNum])): # buchstabe aus wort
            if searchlist[sListNum][letterNum] == searchkey[0]: # wahr=
                test = True

                for keyNum in range(len(searchkey)):
                    if test:
                        test = False
                        if keyNum == len(searchkey) - 1:
                            OutputNum.append(sListNum)
                            break
                        continue
                    if len(searchlist[sListNum]) - 1 < keyNum + letterNum:
                        break

                    if searchlist[sListNum][keyNum + letterNum] == searchkey[keyNum]:
                        if keyNum == len(searchkey) - 1:
                            OutputNum.append(sListNum)
                            break
                    else:
                        break

                break

    return OutputNum

def SearchStr(searchkeyU: str, searchStrU: str, exact=False):

    if len(searchkeyU) == 0:
        return None

    if not exact:
        searchkey = searchkeyU.lower()
        searchlist = searchStrU.lower()
    else:
        searchkey = searchkeyU
        searchlist = searchStrU

    OutputNum = []


    for letterNum in range(len(searchlist)):
        if searchlist[letterNum] == searchkey[0]:
            test = False

            for keyNum in range(len(searchkey)):
                if test:
                    test = False
                    if keyNum == len(searchkey) - 1:
                        OutputNum.append(keyNum)
                        break
                    continue
                if len(searchlist) - 1 < keyNum + letterNum:
                    break

                if searchlist[keyNum + letterNum] == searchkey[keyNum]:
                    if keyNum == len(searchkey) - 1:
                        OutputNum.append(letterNum)
                        break
                else:
                    break

    return OutputNum


def gerPartStr(word: str, begin: int, end: int):
    part = ""
    if len(word) <= end or len(word) <= begin or begin >= end:
        return False
    end -= 1
    for x in range(end):
        if x < begin:
            continue
        part += word[x]
    return part

def gerPartStrToStr(word: str, endkey: str, beginkey="", exact=False):
    if exact:
        word = word.lower()
        endkey = endkey.lower()
    part = ""
    x = 0
    end = False
    beginskip = False
    beginover = False
    while True:
        if beginkey != "" and not beginover:
            z = 0
            for y in range(len(beginkey)):
                if word[x + y] == beginkey[y]:
                    z += 1
                else:
                    beginskip = True
                if z == len(beginkey):
                    beginover = True
                    x += z
            if beginskip:
                beginskip = False
                x += 1
                continue
        z = 0
        for y in range(len(endkey)):
            if word[x + y] == endkey[y]:
                z += 1
            else:
                break
            if z == len(endkey):
                end = True
                break
        if end:
            break
        part += word[x]
        x += 1

    return part

def MusicType(mType, exact=False):
    if rsame(mType, "mp3"):
        if exact:
            return "mp3"
        else:
            return True
    elif rsame(mType, "mp4"):
        if exact:
            return "mp4"
        else:
            return True
    else:
        return False

def MusicEncode(musicname):
    if MusicType(musicname):
        name = musicname.rstrip("." + MusicType(musicname, True))
    else:
        name = musicname

    title = gerPartStrToStr(name, " by ")
    interpreter = gerPartStrToStr(name, beginkey=title + " by ", endkey= " (")
    musictype = turnStr(gerPartStrToStr(turnStr(name), endkey= turnStr(") - ")))

    part = gerPartStrToStr(name, beginkey=title + " by " + interpreter + " (From ", endkey=") - " + musictype)

    x = SearchStr(" S", part, exact = True)
    animeSeason = True
    if len(x) > 1:
        x = x[len(x) - 1] + 1
    elif len(x) == 0:
        animeSeason = None
    else:
        x = x[0]  + 1

    if animeSeason:
        try:
            animeSeason = int(part[x + 1] + part[x + 2])
        except ValueError:
            animeSeason = int(part[x + 1])
        except IndexError:
            animeSeason = int(part[x + 1])

    y = SearchStr(" OP", part, exact = True)
    animeTypeNum = True
    if len(y) > 1:
        y = y[len(y) - 1] + 2
        animeType = "OP"
    elif len(y) == 0:
        y = SearchStr(" EN", part, exact=True)
        if len(y) > 1:
            y = y[len(y) - 1] + 2
            animeType = "EN"
        elif len(y) == 0:
            animeType = None
            animeTypeNum = None
        else:
            y = y[0] + 2
            animeType = "EN"
    else:
        y = y[0] + 2
        animeType = "OP"

    if animeTypeNum:
        try:
            animeTypeNum = int(part[y + 1] + part[y + 2])
        except ValueError:
            animeTypeNum = int(part[y + 1])
        except IndexError:
            animeTypeNum = int(part[y + 1])

    if animeSeason is not None:
        #animeName = gerPartStrToStr(part, endkey=" " + part[x] + part[x + 1])
        animeName = gerPartStr(part, 0, x - 1)
    elif animeTypeNum is not None:
        #animeName = gerPartStrToStr(part, endkey=" " + part[y] + part[y + 1])
        animeName = gerPartStr(part, 0, y - 1)
    else:
        animeName = part

    return [title, interpreter, musictype, animeName, animeSeason, animeType, animeTypeNum]

class WindowsBalloonTipC:
    def __init__(self):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        wc = win32gui.WNDCLASS()
        self.hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map
        self.classAtom = win32gui.RegisterClass(wc)
        self.hwnd = None
        self.normList = []
    def ShowWindow(self, title, msg):
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow( self.classAtom, "Taskbar", style, 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0, self.hinst, None)
        win32gui.UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        # noinspection PyBroadException
        try:
           hicon = win32gui.LoadImage(self.hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
          hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, (self.hwnd, 0, win32gui.NIF_INFO, win32con.WM_USER+20, hicon, "Balloon  tooltip", msg, 200, title))
        win32gui.DestroyWindow(self.hwnd)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        self.normList.append(hwnd)
        self.normList.append(msg)
        self.normList.append(wparam)
        self.normList.append(lparam)

        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32api.PostQuitMessage(0)

WindowsBalloonTip = WindowsBalloonTipC()

def balloon_tip(title, msg):
    class tip(threading.Thread):
        def run(self):
            WindowsBalloonTip.ShowWindow(title, msg)
    tipp = tip()
    tipp.start()



class SysTrayIcon(object):
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]

    FIRST_ID = 1023

    def __init__(self,
                 icon,
                 hover_text,
                 menu_options,
                 on_quit=None,
                 default_menu_index=None,
                 window_class_name=None,):
        self.unerror = 0

        self.icon = icon
        self.hover_text = hover_text
        self.on_quit = on_quit

        menu_options = menu_options + (('Quit', None, self.QUIT),)
        self._next_action_id = self.FIRST_ID
        self.menu_actions_by_id = set()
        self.menu_options = self._add_ids_to_menu_options(list(menu_options))
        self.menu_actions_by_id = dict(self.menu_actions_by_id)
        del self._next_action_id


        self.default_menu_index = (default_menu_index or 0)
        self.window_class_name = window_class_name or "SysTrayIconPy"

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.restart,
                       win32con.WM_DESTROY: self.destroy,
                       win32con.WM_COMMAND: self.command,
                       win32con.WM_USER+20 : self.notify}
        window_class = win32gui.WNDCLASS()
        hinst = window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map
        classAtom = win32gui.RegisterClass(window_class)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(classAtom,
                                          self.window_class_name,
                                          style,
                                          0,
                                          0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0,
                                          0,
                                          hinst,
                                          None)
        win32gui.UpdateWindow(self.hwnd)
        self.notify_id = None
        self.refresh_icon()

        win32gui.PumpMessages()

    def _add_ids_to_menu_options(self, menu_options):
        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in self.SPECIAL_ACTIONS:
                self.menu_actions_by_id.add((self._next_action_id, option_action))
                result.append(menu_option + (self._next_action_id,))
            elif non_string_iterable(option_action):
                result.append((option_text,
                               option_icon,
                               self._add_ids_to_menu_options(option_action),
                               self._next_action_id))
            else:
                print('Unknown item', option_text, option_icon, option_action)
            self._next_action_id += 1
        return result

    def refresh_icon(self):
        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(self.icon):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst,
                                       self.icon,
                                       win32con.IMAGE_ICON,
                                       0,
                                       0,
                                       icon_flags)
        else:
            print("Can't find icon file - using default.")
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id: message = win32gui.NIM_MODIFY
        else: message = win32gui.NIM_ADD
        self.notify_id = (self.hwnd,
                          0,
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                          win32con.WM_USER+20,
                          hicon,
                          self.hover_text)
        win32gui.Shell_NotifyIcon(message, self.notify_id)

    def restart(self, hwnd, msg, wparam, lparam):
        self.refresh_icon()

    def destroy(self, hwnd, msg, wparam, lparam):
        if self.on_quit: self.on_quit(self)
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)

    def notify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONDBLCLK:
            self.execute_menu_option(self.default_menu_index + self.FIRST_ID)
        elif lparam==win32con.WM_RBUTTONUP:
            self.show_menu()
        elif lparam==win32con.WM_LBUTTONUP:
            pass
        return True

    def show_menu(self):
        menu = win32gui.CreatePopupMenu()
        self.create_menu(menu, self.menu_options)

        pos = win32gui.GetCursorPos()
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                self.hwnd,
                                None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

    def create_menu(self, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_icon:
                option_icon = self.prep_menu_icon(option_icon)

            if option_id in self.menu_actions_by_id:
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui.CreatePopupMenu()
                self.create_menu(submenu, option_action)
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(self, icon):
        self.unerror += 1
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm

    def command(self, hwnd, msg, wparam, lparam):
        idt = win32gui.LOWORD(wparam)
        self.execute_menu_option(idt)

    def execute_menu_option(self, idt):
        menu_action = self.menu_actions_by_id[idt]
        if menu_action == self.QUIT:
            win32gui.DestroyWindow(self.hwnd)
        else:
            menu_action(self)

def non_string_iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return not isinstance(obj, str)


class SysTray(threading.Thread):
    def __init__(self, icon: str, hover_text: str, menu: dict, sub_menu_name1: str=None, sub_menu1: dict=None,
                 sub_menu_name2: str=None, sub_menu2: dict=None,
                 sub_menu_name3: str=None, sub_menu3: dict=None,
                 sub_menu_name4: str=None, sub_menu4: dict=None,
                 sub_menu_name5: str=None, sub_menu5: dict=None, quitFunc=None):
        super().__init__()
        self.End = False
        self.icon = icon
        self.icons = itertools.cycle(glob.glob(self.icon))
        self.hover_text = hover_text

        if quitFunc is None:
            def quitFuncT(sysTrayIcon):
                pass
            self.quitFunc = quitFuncT
        else:
            self.quitFunc = quitFunc

        menu_options = []
        for x in menu:
            menu_options.append((x, next(self.icons), menu[x]))

        if sub_menu1 is not None:
            sub_menu_list = []
            for x in sub_menu1:
                sub_menu_list.append((x, next(self.icons), sub_menu1[x]))
            menu_options.append((sub_menu_name1, next(self.icons), tuple(sub_menu_list)))

        if sub_menu2 is not None:
            sub_menu_list = []
            for x in sub_menu2:
                sub_menu_list.append((x, next(self.icons), sub_menu2[x]))
            menu_options.append((sub_menu_name2, next(self.icons), tuple(sub_menu_list)))

        if sub_menu3 is not None:
            sub_menu_list = []
            for x in sub_menu3:
                sub_menu_list.append((x, next(self.icons), sub_menu3[x]))
            menu_options.append((sub_menu_name3, next(self.icons), tuple(sub_menu_list)))

        if sub_menu4 is not None:
            sub_menu_list = []
            for x in sub_menu4:
                sub_menu_list.append((x, next(self.icons), sub_menu4[x]))
            menu_options.append((sub_menu_name4, next(self.icons), tuple(sub_menu_list)))

        if sub_menu5 is not None:
            sub_menu_list = []
            for x in sub_menu5:
                sub_menu_list.append((x, next(self.icons), sub_menu5[x]))
            menu_options.append((sub_menu_name5, next(self.icons), tuple(sub_menu_list)))

        self.menu_options = tuple(menu_options)

    def run(self):
        SysTrayIcon(next(self.icons), self.hover_text, self.menu_options, on_quit=self.quitFunc, default_menu_index=1)
        self.End = True



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
        if (self.Time % 60) < 10:
            TimeFor = "%s:%s%s" % (round(self.Time) // 60, 0, round(self.Time) % 60)
        else:
            TimeFor = "%s:%s" % (round(self.Time) // 60, round(self.Time) % 60)
        return TimeFor
