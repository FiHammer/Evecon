import ctypes
import socket
import pycaw
import pycaw.pycaw
import getpass
import comtypes
import random
import simplecrypt
import configparser
import webbrowser
import pyglet
import click
import queue
#import time from EveconTools
#import os from EveconTools
#import sys from EveconTools
#import datetime
#import threading from EveconTools
#import EveconExceptions from EveconLibBoth
#import EveconMiniDebug from EveconLibBoth

from EveconTools import *

if sys.platform == "win32":
    from EveconLibWin import *

    path_seg = "\\"
    firefox_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    vivaldi_path = "C:\\Program Files (x86)\\Vivaldi\\Application\\vivaldi.exe"

elif sys.platform == "linux":
    from EveconLibLin import *
    import subprocess
    import psutil
    import datetime

    path_seg = "/"
    firefox_path = ""
    vivaldi_path = ""

else:
    path_seg = "/"
    firefox_path = ""
    vivaldi_path = ""


if os.getcwd() == "C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\!Evecon\\dev":
    os.chdir("..")
    os.chdir("..")


ss_active = False
exitnow = 0
pausetime = 180
musicrun = False
thisIP = None
StartupServer = None
browser = "vivaldi"
MusicDir = None
startmain = False
Alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
musicrandom = True
enable_foxi = True
cores = 2
console_data = {"lenx": 120, "leny": 30, "posx": 0, "posy": 0, "pixx": 120, "pixy": 30}
thisHWND = 0


if sys.platform == "win32":
    ctypes.windll.kernel32.SetConsoleTitleW("EVECON: Loading HWND")
    loadHWND("EVECON: Loading HWND")
    ctypes.windll.kernel32.SetConsoleTitleW("EVECON: Loading...")

    szip = szipCWin("Programs\\7z")
    Megacmd = MegacmdCWin("Programs\\MEGAcmd")

else:

    szip = szipCLin()
    Megacmd = MegacmdCLin()



def killme():
    subprocess.call(["taskkill", "/F", "/PID", str(os.getpid())])
    os.system("taskkill /PID /F %s" % str(os.getpid()))

def readConfig():
    config = configparser.ConfigParser()
    config.read("data"+path_seg+"config.ini")

    global browser, musicrandom, enable_foxi

    try:
        enable_foxi_tmp = config["Notepad"]["enable_foxi"]
        if enable_foxi_tmp == "True":
            enable_foxi = True
        elif enable_foxi_tmp == "False":
            enable_foxi = False

        musicrandom_tmp = config["Music"]["random"]
        if musicrandom_tmp == "True":
            musicrandom = True
        elif musicrandom_tmp == "False":
            musicrandom = False

        browser = config["Notepad"]["browser"]

    except KeyError:
        pass


readConfig()

def Log(functioni, info, typei = "Normal"):
    log_file = open("data"+path_seg+"Log.txt", "a+")
    part_time = "[" + datetime.datetime.now().strftime("%H:%M:%S") + "]"
    if typei == "Normal":
        part_type = "[Info]"
    elif typei == "Warning":
        part_type = "[Warning]"
    elif typei == "Error":
        part_type = "[Error]"
    else:
        part_type = ""
    part_func = "[" + functioni + "]"

    log_write = part_time + " " + part_type + " " + part_func + ": " + info + "\n"

    log_file.write(log_write)
    log_file.close()




class Scanner(threading.Thread):
    def __init__(self, action, raw=False):
        """
        :type action: object
        react
        """
        super().__init__()
        self.action = action


        self.running = True
        self.raw = raw

    def run(self):
        while self.running:
            char = click.getchar()
            if self.raw:
                self.action(char)
            else:
                if char == "\x1b":
                    self.action("escape")
                elif char == "\x00;":
                    self.action("F1")
                elif char == "\x00<":
                    self.action("F2")
                elif char == "\x00=":
                    self.action("F3")
                elif char == "\x00>":
                    self.action("F4")
                elif char == "\x00?":
                    self.action("F5")
                elif char == "\x00@":
                    self.action("F6")
                elif char == "\x00A":
                    self.action("F7")
                elif char == "\x00B":
                    self.action("F8")
                elif char == "\x00C":
                    self.action("F9")
                elif char == "\x00D":
                    self.action("F10")
                elif char == 'à\x85':
                    self.action("F11")
                elif char == 'à\x86':
                    self.action("F12")
                elif char == "\x08":
                    self.action("backspace")
                elif char == "àR":
                    self.action("insert")
                elif char == "àG":
                    self.action("home") #pos1
                elif char == "àI":
                    self.action("pageup")
                elif char == "àS":
                    self.action("del")
                elif char == "àO":
                    self.action("end")
                elif char == "àQ":
                    self.action("pagedown")
                elif char == "àH":
                    self.action("arrowup")
                elif char == "àK":
                    self.action("arrowleft")
                elif char == "àP":
                    self.action("arrowdown")
                elif char == "àM":
                    self.action("arrowright")
                elif char.encode() == b'\xc3\xa0\xc2\x8d':
                    self.action("strg_arrowup")
                elif char == "às":
                    self.action("strg_arrowleft")
                elif char.encode() == b'\xc3\xa0\xc2\x91':
                    self.action("strg_arrowdown")
                elif char == "àt":
                    self.action("strg_arrowright")
                elif char == "\x00R":
                    self.action("num0")
                elif char == "\x00O":
                    self.action("num1")
                elif char == "\x00P":
                    self.action("num2")
                elif char == "\x00Q":
                    self.action("num3")
                elif char == "\x00K":
                    self.action("num4")
                elif char == "\x00M":
                    self.action("num6")
                elif char == "\x00G":
                    self.action("num7")
                elif char == "\x00H":
                    self.action("num8")
                elif char == "\x00I":
                    self.action("num9")
                elif char == "\r":
                    self.action("enter")
                else:
                    self.action(char)


def MusicEncode(musicname):
    if MusicType(musicname):
        name = musicname.rstrip("." + MusicType(musicname, True))
    else:
        name = musicname

    try:
        title = getPartStrToStr(name, " by ")
        interpreter = getPartStrToStr(name, beginkey=title + " by ", endkey=" (")
        musictype = turnStr(getPartStrToStr(turnStr(name), endkey= turnStr(") - ")))

        part = getPartStrToStr(name, beginkey=title + " by " + interpreter + " (From ", endkey=") - " + musictype)

        x = SearchStr(" S", part, exact = True)
    except IndexError:
        return False


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

        animeName = getPartStr(part, 0, x - 1)
    elif animeTypeNum is not None:
        #animeName = gerPartStrToStr(part, endkey=" " + part[y] + part[y + 1])

        animeName = getPartStr(part, 0, y - 1)
    else:
        animeName = part

    output = {"title": title, "interpreter": interpreter, "musictype": musictype, "animeName": animeName,
              "animeSeason": animeSeason, "animeType": animeType, "animeTypeNum": animeTypeNum}
    return output



# noinspection PyTypeChecker
class MusicPlayerC(threading.Thread):
    def __init__(self, systray=True, random=True, expandRange=2):
        super().__init__()


        self.music = {"all_files": 0, "all_dirs": 0, "active": []}
        self.find_music_out = {}

        self.systray = None
        self.systrayon = systray

        self.volume = Volume.getVolume()
        self.volumep = 1

        self.randomizer = random
        # noinspection PyGlobalUndefined
        global musicrun
        musicrun = True

        self.musicrun = True
        self.playlist = []
        self.pershuffel = False

        self.running = False
        self.playing = False
        self.exitn = False
        self.allowPrint = False

        self.player = pyglet.media.Player()
        self.timer = TimerC()
        self.scanner = Scanner(self.react)
        self.spl = SplatoonC()

        self.skip_del = False
        self.paused = False
        self.pause_type = ""
        self.muted = False
        self.mute_vol = 1
        self.con_main = "pl"
        self.con_cont = "set"
        self.change = ""

        self.cur_Input = ""
        self.cur_Pos = 0
        self.expandRange = expandRange

        self.playlists = ["LiS", "Anime", "Phunk", "Caravan Palace", "Electro Swing", "Parov Stelar", "jPOP & etc", "OMFG"]
        self.playlists_key = ["lis", "an", "phu", "cp", "es", "ps", "jpop", "omfg"]

        self.musiclist = {}
        with open("data"+path_seg+"Music.txt") as musicfile:
            for line in musicfile:
                if lsame(line, "["):
                    self.musiclist[getPartStrToStr(line, "]", "[", True)] = getPartStrToStr(line, "'", " '", True)

    def findMusic(self, path, reset=True):
        if reset:
            self.find_music_out = {"all_files": 0, "all_dirs": 0}

        for file in os.listdir(path):
            fullname = path + path_seg + file
            if os.path.isdir(path + path_seg + file):
                self.music["all_dirs"] += 1
                self.music["dir" + str(self.music["all_dirs"])] = {"file": file, "path": path, "fullname": fullname}

                self.find_music_out["all_dirs"] += 1
                self.find_music_out["dir" + str(self.find_music_out["all_dirs"])] = {"file": file, "path": path, "fullname": fullname}

                self.findMusic(fullname, False)
            elif os.path.isfile(fullname) and MusicType(file):
                name = file.rstrip(MusicType(file, True)).rstrip(".")

                self.music["all_files"] += 1
                self.find_music_out["all_files"] += 1

                me = MusicEncode(file)
                if me:
                    antype = True
                    andata = me
                else:
                    antype = False
                    andata = None

                self.music["file" + str(self.music["all_files"])] = {"name": name, "file": file, "path": path, "fullname": fullname,
                                                                       "antype": antype, "andata": andata}

                self.find_music_out["file" + str(self.music["all_files"])] = {"name": name, "file": file, "path": path, "fullname": fullname,
                                                                               "antype": antype, "andata": andata}

    def addMusic(self, key, custom=None):  # key (AN, LIS)
        self.read_musiclist()
        if computer == "MiniPC":
            cls()
            print("Loading... (On Mini-PC)")
            musicDirLoad = MusicDir

        elif computer == "BigPC":
            cls()
            print("Loading... (On Big-PC)")
            musicDirLoad = MusicDir

        else:
            cls()
            print("Loading...")
            musicDirLoad = "Music"+path_seg+"Presets"

        old_Num = self.music["all_files"]
        key = key.lower()

        if custom:
            key = "cus"

        done = False
        for x in self.musiclist:
            if x == key:
                self.findMusic(musicDirLoad + path_seg + self.musiclist[key])
                done = True
                break

        if done:
            pass
        elif key == "us":
            self.findMusic("Music"+path_seg+"User")
        elif key == "cus" and custom: # custom
            self.findMusic(custom)
        else:
            return False


        q = queue.Queue()
        num_workers = cores*2

        def do_work(data):
            #cls()
            #print("Loading (%s/%s)" % (data[0], self.find_music_out["all_files"]))
            self.music["file" + str(data[1] + data[0])]["loaded"] = pyglet.media.load(
                self.music["file" + str(data[1] + data[0])]["fullname"])

        def worker():
            while True:
                data = q.get()
                if data is None:
                    break
                do_work(data)
                q.task_done()

        threads_used = []

        for i in range(num_workers):
            t = threading.Thread(target=worker)
            t.start()
            threads_used.append(t)

        for numfile in range(1, self.find_music_out["all_files"] + 1):
            q.put((numfile, old_Num))

        for i in range(num_workers):
            q.put(None)

        for i in threads_used:
            i.join()

        #for numfile in range(1, self.find_music_out["all_files"] + 1):
        #    cls()
        #    print("Loading (%s/%s)" % (numfile, self.find_music_out["all_files"]))
        #    self.music["file" + str(old_Num + numfile)]["loaded"] = pyglet.media.load(self.music["file" + str(old_Num + numfile)]["fullname"])

        #self.music_playlists_active.append(key)
        self.music["active"].append(key)
        print("Finished")
        return True

    def read_musiclist(self):
        with open("data"+path_seg+"Music.txt") as musicfile:
            for line in musicfile:
                if not lsame(line, "#") and lsame(line, "["):
                    self.musiclist[getPartStrToStr(line, "]", "[", True)] = getPartStrToStr(line, "'", " '", True)

    def reloadMusic(self, tracknum):
        if type(tracknum) == int:
            self.music["file" + str(tracknum)]["loaded"] = pyglet.media.load(self.music["file" + str(tracknum)]["fullname"])
        elif type(tracknum) == str:
            self.music[tracknum]["loaded"] = pyglet.media.load(self.music[tracknum]["fullname"])

    def make_playlist(self):
        self.playlist = []
        for x in range(1, self.music["all_files"] + 1):
            self.playlist.append("file" + str(x))

    def shufflePL(self, first=False):
        if first:
            random.shuffle(self.playlist)
        else:
            oldPL = self.playlist.copy()
            del oldPL[0]
            random.shuffle(oldPL)
            self.playlist = [self.playlist[0]] + oldPL

    def refreshTitle(self):
        if self.getCur()["antype"]:
            title("OLD", self.getCur()["andata"]["title"], "Now Playing")
        else:
            title("OLD", self.getCur()["name"], "Now Playing")

    def getCur(self):
        return self.music[self.playlist[0]]

    def rerollThis(self):
        oldPL = self.playlist.copy()
        del oldPL[self.cur_Pos]
        self.playlist = oldPL + [self.playlist[self.cur_Pos]]
        if self.cur_Pos == 0:
            self.next(True)

    def sortPL(self):
        self.playlist.sort()

    def sortPL_name(self):
        pl_names = []
        for fileX in self.playlist:
            pl_names.append(self.music[fileX]["name"])
        pl_names.sort()

        new_playlist = []
        for name in pl_names:
            for num_file in range(1, self.music["all_files"] + 1):
                if name == self.music["file" + str(num_file)]["name"]:
                    ok = True
                    for x in new_playlist:
                        if x == "file" + str(num_file):
                            ok = False
                    if ok:
                        new_playlist.append("file" + str(num_file))


        self.playlist = new_playlist.copy()

    def sortPL_an(self):
        pl_an_file = []
        pl_nonan_file = []

        for fileX in self.playlist:
            if self.music[fileX]["antype"]:
                pl_an_file.append(fileX)
            else:
                pl_nonan_file.append(fileX)

        pl_an_file.sort()
        pl_nonan_file.sort()

        new_playlist = []
        pl_an_name = []

        for an_file in pl_an_file:
            ok = True
            for x in pl_an_name:
                if x == self.music[an_file]["andata"]["animeName"]:
                    ok = False
            if ok:
                pl_an_name.append(self.music[an_file]["andata"]["animeName"])
        pl_an_name.sort()


        for an_name in pl_an_name:
            this_an = [] # files unsortiert
            this_an_name = [] # name unsortiert & sortiert
            new_pl = [] # files sortiert

            for num_file in range(1, self.music["all_files"] + 1):
                if self.music["file" + str(num_file)]["antype"] and an_name == self.music["file" + str(num_file)]["andata"]["animeName"]:
                    this_an.append("file" + str(num_file))
                    this_an_name.append(self.music["file" + str(num_file)]["name"])


            this_an_name.sort()
            for this_an_name2 in this_an_name:
                for file in this_an:
                    if this_an_name2 == self.music[file]["name"]:
                        new_pl.append(file)
                        break

            new_playlist += new_pl


        pl_nonan_name = []
        for fileX in pl_nonan_file:
            pl_nonan_name.append(self.music[fileX]["name"])
        pl_nonan_name.sort()

        for name in pl_nonan_name:
            for num_file in range(1, self.music["all_files"] + 1):
                if name == self.music["file" + str(num_file)]["name"]:
                    new_playlist.append("file" + str(num_file))


        self.playlist = new_playlist.copy()

    #Options

    def play(self):
        self.paused = False
        self.player.play()
    def pause(self):
        self.paused = True
        self.player.pause()
    def switch(self):
        if self.paused:
            self.play()
        else:
            self.pause()
    def switchmute(self):
        if self.muted:
            self.unmute()
        else:
            self.mute()
    def mute(self):
        self.muted = True
        self.mute_vol = self.volumep
        self.volp(0)
    def unmute(self):
        self.muted = False
        self.volp(self.mute_vol)
    def stop(self):
        # noinspection PyGlobalUndefined
        global musicrun
        musicrun = True

        self.musicrun = False
        self.playing = False
        self.paused = False
        self.running = False
        if self.systrayon:
            time.sleep(1)
            killme()
    def next(self, skipthis=False):
        if skipthis:
            self.skip_del = True
        self.playing = False
        if self.paused:
            self.paused = False
            self.player.play()
    def Del(self, plfile):
        num = Search(plfile, self.playlist)[0]
        if num == 0:
            self.stop()

        if self.cur_Pos >= len(self.playlist) - 1:
            self.cur_Pos -= 1

        del self.playlist[num]

        if self.cur_Pos == 0:
            self.next(True)
    def vol(self, vol):
        self.volume = vol
        Volume.change(vol)
    def volp(self, vol):
        self.volumep = vol
        self.player.volume = self.volumep


    def run(self):
        if self.systrayon and sys.platform == "win32":
            def quitFunc(x):
                self.stop()
            def unp_p(x):
                self.switch()
            def nextm(x):
                self.next()
            def delm(x):
                self.Del(self.playlist[0])
                self.playing = False
                if self.paused:
                    self.play()
            def reroll(x):
                self.shufflePL()

            def vol01(x):
                self.volp(0.1)
            def vol025(x):
                self.volp(0.25)
            def vol05(x):
                self.volp(0.5)
            def vol1(x):
                self.volp(1)

            sub_menu1 = {"0.1": vol01, "0.25": vol025, "0.5": vol05, "1": vol1}

            self.systray = SysTray("data"+path_seg+"Ico"+path_seg+"Radio.ico", "Evecon: MusicPlayer",
                                   {"Pause/Unpause": unp_p, "Next": nextm,
                                    "Del": delm, "Reroll": reroll},
                                   sub_menu1=sub_menu1, sub_menu_name1="Volume", quitFunc=quitFunc)
            self.systray.start()

        self.make_playlist()


        if self.randomizer:
            self.shufflePL(True)

        self.scanner.start()
        while self.musicrun:

            if self.music[self.playlist[0]]["loaded"].is_queued:
                self.reloadMusic(self.playlist[0])
            self.player.queue(self.music[self.playlist[0]]["loaded"])
            self.player.play()

            self.timer.start()

            self.player.volume = self.volumep

            self.running = True
            self.playing = True

            self.allowPrint = True
            self.refreshTitle()

            self.printit()
            while self.playing:

                time.sleep(0.15)
                for x in range(5):
                    if self.player.time == 0:
                        self.playing = False
                    elif round(self.getCur()["loaded"].duration) <= round(self.timer.getTime()):
                        self.playing = False
                    time.sleep(0.1)

                while self.paused:
                    self.timer.pause()
                    # Vll. hier spl pause command einfügen
                    #self.splmp.
                    while self.paused:
                        time.sleep(0.25)

                    self.timer.unpause()
                    self.refreshTitle()

                    #if self.spl:
                    #    self.splmp.PlaytimeStart += time.time() - music_time_wait
                    #    self.splmp.TimeLeftStart += time.time() - music_time_wait

            self.player.next()

            if self.skip_del:
                self.skip_del = False
            else:
                self.playlist += [self.playlist[0]]
                del self.playlist[0]


            if self.pershuffel:
                self.shufflePL()

            self.running = False

            if self.exitn:
                self.stop()

    def printit(self):
        cls()

        # Info-Container

        print("Musicplayer:\n")

        if self.getCur()["antype"]:
            print("Playing: \n%s \nFrom %s" % (self.getCur()["andata"]["title"], self.getCur()["andata"]["animeName"]))
        else:
            print("Playing: \n%s" % self.getCur()["name"])

        print("Time: %s\\%s" % (self.timer.getTimeFor(), TimeFor(self.getCur()["loaded"].duration)))
        if self.muted:
            #print(int((console_data["pixx"]/2)-3)*"|"+"Muted"+int((console_data["pixx"]/2)-2)*"|")
            l1 = ""
            l2 = ""
            pre = ""
            print(pre + int((console_data["pixx"] / 2) - 3) * l1 + "Muted" + int((console_data["pixx"] / 2) - 2) * l2)


        print("\n" + console_data["pixx"]*"-" + "\n")
        #sys.stdout.write(console_data[0]*"-")

        # Main-Container

        if self.con_main == "pl":
            print("Playlist: (%s)\n" % str(len(self.playlist)))

            debug = False

            search_done = False
            for now in range(self.expandRange):
                if not search_done:
                    if self.cur_Pos  == now:
                        if self.expandRange >= len(self.playlist) - 1:
                            for word_num in range(0, len(self.playlist)):
                                if word_num + 1 < 10:
                                    word_num_str = str(word_num + 1) + "  "
                                elif word_num + 1 < 100:
                                    word_num_str = str(word_num + 1) + " "
                                else:
                                    word_num_str = str(word_num + 1)

                                if self.cur_Pos  == word_num:
                                    if not debug:
                                        print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"])
                                    else:
                                        print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"], 0, self.playlist[word_num])
                                else:
                                    if not debug:
                                        print(" " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"])
                                    else:
                                        print(" " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"], 1, self.playlist[word_num])
                        elif 2 * self.expandRange + 1 >= len(self.playlist):
                            for word_num in range(0, 2 * self.expandRange + 1):  # + 1?
                                if word_num + 1 < 10:
                                    word_num_str = str(word_num + 1) + "  "
                                elif word_num + 1 < 100:
                                    word_num_str = str(word_num + 1) + " "
                                else:
                                    word_num_str = str(word_num + 1)

                                if self.cur_Pos  == word_num:
                                    try:
                                        if not debug:
                                            print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"])
                                        else:
                                            print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"], 2, self.playlist[word_num])
                                    except IndexError:
                                        pass
                                else:
                                    try:
                                        if not debug:
                                            print(" " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"])
                                        else:
                                            print(" " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"], 3, self.playlist[word_num])
                                    except IndexError:
                                        pass
                        else:
                            for word_num in range(0, 2 * self.expandRange + 1):  # + 1? # Anfang
                                if word_num + 1 < 10:
                                    word_num_str = str(word_num + 1) + "  "
                                elif word_num + 1 < 100:
                                    word_num_str = str(word_num + 1) + " "
                                else:
                                    word_num_str = str(word_num + 1)
                                if self.cur_Pos == word_num:
                                    if not debug:
                                        print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"])
                                    else:
                                        print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"], 4, self.playlist[word_num])
                                else:
                                    if not debug:
                                        print(" " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"])
                                    else:
                                        print(" " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"], 5, self.playlist[word_num])
                        search_done = True
                        break

                    elif self.cur_Pos == len(self.playlist) - now - 1 and self.cur_Pos >= self.expandRange: # Ende
                        for word_num in range(self.cur_Pos - self.expandRange - 2 + now, self.cur_Pos + 1 + now):
                            if word_num < 0:
                                continue
                            #print(word_num, self.cur_Pos, now, self.expandRange)
                            if word_num + 1 < 10:
                                word_num_str = str(word_num + 1) + "  "
                            elif word_num + 1 < 100:
                                word_num_str = str(word_num + 1) + " "
                            else:
                                word_num_str = str(word_num + 1)
                            if self.cur_Pos == word_num:
                                if not debug:
                                    print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"])
                                else:
                                    print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"], 6, self.playlist[word_num])
                            else:
                                if not debug:
                                    print(" " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"])
                                else:
                                    print(" " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"], 7, self.playlist[word_num])
                        search_done = True
                        break

            if not search_done: # Mitte
                for word_num in range(self.cur_Pos - self.expandRange, self.cur_Pos + self.expandRange + 1):
                    if word_num + 1 < 10:
                        word_num_str = str(word_num + 1) + "  "
                    elif word_num + 1 < 100:
                        word_num_str = str(word_num + 1) + " "
                    else:
                        word_num_str = str(word_num + 1)
                    if self.cur_Pos == word_num:
                        if not debug:
                            print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"])
                        else:
                            print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"], 10, self.playlist[word_num])
                    else:
                        if not debug:
                            print(" " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"])
                        else:
                            print(" " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"], 11, self.playlist[word_num])

        elif self.con_main == "details":
            print("Details:\n")
            if self.music[self.playlist[self.cur_Pos]]["antype"]:
                print("Title: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["title"]))
                print("Interpreter: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["interpreter"]))
                print("Musictype: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["musictype"]))
                print("Animename: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["animeName"]))
                print("Season: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["animeSeason"]))
                print("Type: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["animeType"]) +
                      str(self.music[self.playlist[self.cur_Pos]]["andata"]["animeTypeNum"]))
            else:
                print("Filename: " + self.music[self.playlist[self.cur_Pos]]["name"])
                print("Album: " + self.music[self.playlist[self.cur_Pos]]["loaded"].info.album.decode())
                print("Author: " + self.music[self.playlist[self.cur_Pos]]["loaded"].info.author.decode())
                print("Comment: " + self.music[self.playlist[self.cur_Pos]]["loaded"].info.comment.decode())
                print("Copyright: " + self.music[self.playlist[self.cur_Pos]]["loaded"].info.copyright.decode())
                print("Genre: " + self.music[self.playlist[self.cur_Pos]]["loaded"].info.genre.decode())
                print("Title: " + self.music[self.playlist[self.cur_Pos]]["loaded"].info.title.decode())
                print("Track: " + str(self.music[self.playlist[self.cur_Pos]]["loaded"].info.track))
                print("Year: " + str(self.music[self.playlist[self.cur_Pos]]["loaded"].info.year))

        elif self.con_main == "spl":
            self.spl.printit(False)

        # Control-Container

        print("\n" + console_data["pixx"]*"-" + "\n")

        if self.con_cont == "set":
            print("Commands:\n")

            if not self.paused:
                print("Pause (P), Delthis (DEL), Next (N), Reroll all (RE), Reroll this (RT), Details (DEA)")
            elif self.paused:
                print("Play (P), Delthis (DEL), Next (N), Reroll all (RE), Reroll this (RT), Details (DEA)")

            if self.con_main == "spl":
                self.spl.printcom()

            print("\nInput:\n%s" % self.cur_Input)

        elif self.con_cont == "conf":
            print("Confirm\n")
            print("Y/N")

        elif self.con_cont == "volp":
            print("Change Volume (Player):\n")
            print("Current: " + str(self.volumep))

            print("\n" + self.cur_Input)

        elif self.con_cont == "volw":
            self.volume = Volume.getVolume()
            print("Change Volume (Windows):\n")
            print("Current: " + str(self.volume))

            print("\n" + self.cur_Input)

        elif self.con_cont == "spe":
            print("Change Effectduration (Spl):\n")
            print("Current: " + str(self.spl.Effect))

            print("\n" + self.cur_Input)

    def react(self, inp):

        if self.con_main == "details":
            self.con_main = "pl"

        elif inp == " ":
            self.switch()

        elif len(inp) == 1:
            self.cur_Input += inp
            if self.input(self.cur_Input):
                self.cur_Input = ""

        elif inp == "backspace":
            if len(self.cur_Input) > 0:
                new_Input = ""
                for x in range(len(self.cur_Input) - 1):
                    new_Input += self.cur_Input[x]
                self.cur_Input = new_Input

        elif self.change and inp == "escape":
            self.cur_Input = ""
            self.change = ""
            self.con_cont = "set"


        elif self.change == "volp":
            if inp == "enter":
                self.volp(float(self.cur_Input))
                self.cur_Input = ""
                self.change = ""
                self.con_cont = "set"


        elif self.change == "volw":
            if inp == "enter":
                if len(self.cur_Input) > 4:
                    self.cur_Input = getPartStr(self.cur_Input, begin=0, end=4)
                self.vol(float(self.cur_Input))
                self.cur_Input = ""
                self.change = ""
                self.con_cont = "set"

        elif self.change == "spe":
            if inp == "enter":
                self.spl.ChEffect(self.cur_Input)
                self.cur_Input = ""
                self.change = ""
                self.con_cont = "set"

        elif inp == "arrowup" and self.cur_Pos > 0 and self.con_main == "pl":
            self.cur_Pos -= 1
        elif inp == "arrowdown" and self.cur_Pos < len(self.playlist) - 1 and self.con_main == "pl":
            self.cur_Pos += 1

        elif inp == "strg_arrowup" and self.cur_Pos > 0 and self.con_main == "pl" or \
                inp == "num8" and self.cur_Pos > 0 and self.con_main == "pl":
            newPL = []
            skipnext = False
            for x in range(len(self.playlist)):
                if x == self.cur_Pos - 1:
                    newPL.append(self.playlist[x + 1])
                    newPL.append(self.playlist[x])
                    skipnext = True
                elif skipnext:
                    skipnext = False
                else:
                    newPL.append(self.playlist[x])

            self.playlist = newPL.copy()

            if self.cur_Pos == 1:
                self.next(True)

            self.cur_Pos -= 1

        elif inp == "strg_arrowdown" and self.cur_Pos < len(self.playlist) - 1 and self.con_main == "pl" or \
                inp == "num2" and self.cur_Pos < len(self.playlist) - 1 and self.con_main == "pl":
            newPL = []
            skipnext = False
            for x in range(len(self.playlist)):
                if x == self.cur_Pos:
                    newPL.append(self.playlist[x + 1])
                    newPL.append(self.playlist[x])
                    skipnext = True
                elif skipnext:
                    skipnext = False
                else:
                    newPL.append(self.playlist[x])

            self.playlist = newPL.copy()

            if self.cur_Pos == 0:
                self.next(True)

            self.cur_Pos += 1

        elif inp == "del" and self.con_main == "pl":
            self.Del(self.playlist[self.cur_Pos])

        elif inp == "enter" and self.con_main == "pl":
            oldPL = self.playlist.copy()
            del oldPL[self.cur_Pos]
            self.playlist = [self.playlist[self.cur_Pos]] + oldPL
            self.next(True)
        else:
            return False

        self.printit()

    def input(self, i):
        i = i.lower()
        if i ==  "play" or i == "pau" or i == "pause" or i == "p":
            self.switch()
        elif i == "next" or i == "n":
            self.next()
        elif i == "m":
            self.switchmute()
        elif i == "stop" or i == "exit":
            self.stop()
        #elif i == "del":
        #    self.playing = False
        #    if self.paused:
        #        self.play()
        #    time.sleep(0.5)
        #    self.Del(self.playlist[-1])
        elif i == "del":
            self.Del(self.playlist[self.cur_Pos])
            if self.cur_Pos == 0:

                self.next()
        elif i == "volw":
            self.cur_Input = ""
            self.change = "volw"
            self.con_cont = "volw"
        elif i == "volp":
            self.cur_Input = ""
            self.change = "volp"
            self.con_cont = "volp"
        elif i == "re":
            self.shufflePL()
        elif i == "rt":
            self.rerollThis()
        elif i == "exin":
            self.exitn = True
        elif i == "dea":
            self.con_main = "details"
        elif i == "sortfile":
            self.sortPL()
            self.next(True)
        elif i == "sortname":
            self.sortPL_name()
            self.next(True)
        elif i == "sortan":
            self.sortPL_an()
            self.next(True)

        elif i == "spl":
            if self.con_main == "spl":
                self.con_main = "pl"
            else:
                self.con_main = "spl"

        elif lsame(i, "sp") and not i == "sp" and self.con_main == "spl":
            if lsame(i, "spe"):
                self.cur_Input = ""
                self.change = "spe"
                self.con_cont = "spe"
            elif i == "spn":
                self.spl.RoundOverF()
            elif i == "spwr":
                self.spl.WRswitch()
            elif i == "spr":
                self.spl.WRreroll()
            else:
                return False

        else:
            return False
        return True



class RadioC:
    def __init__(self, systray=True):
        super().__init__()

        self.streampause = False
        self.streamrun = True
        self.streamvolume = Volume.getVolume()

        if sys.platform == "win32":
            self.streamplayer = MPlayerCWin("Programs\\MPlayer")
        else:
            self.streamplayer = MPlayerCLin()

        self.streamPrintOth = False
        self.streamPrintCh = False
        self.streamPrintVol = False

        self.systrayon = systray
        self.systray = None

        self.stream_playlists = ["EgoFM", "HR1", "HR3", "Bayern3", "ByteFM"]
        self.stream_playlists_key = ["egofm", "hr1", "hr3", "br3", "bytefm"]
        self.stream_playlists_name = {"egofm" : "EgoFM",
                                      "hr1" : "HR1",
                                      "hr3" : "HR3",
                                      "br3" : "BR3",
                                      "bytefm" : "ByteFM"}
        self.stream_playlists_link = {"egofm" : "https://egofm-live.cast.addradio.de/egofm/live/mp3/high/stream.mp3",
                                      "hr1" : "http://hr-hr1-live.cast.addradio.de/hr/hr1/live/mp3/128/stream.mp3",
                                      "hr3" : "http://hr-hr3-live.cast.addradio.de/hr/hr3/live/mp3/128/stream.mp3",
                                      "br3" : "https://br-br3-live.sslcast.addradio.de/br/br3/live/mp3/128/stream.mp3",
                                      "bytefm" : "https://dg-ice-eco-https-fra-eco-cdn.cast.addradio.de/bytefm/main/mid/stream.mp3"}

        self.streamplaying = self.stream_playlists_key[random.randint(0, len(self.stream_playlists_key) - 1)]

    def Unpause(self):
        self.streamplayer.unpause()
        self.streampause = False
        title("Radio", self.stream_playlists_name[self.streamplaying], "Now Playing")
    def Pause(self):
        self.streamplayer.pause()
        self.streampause = True
        title("Radio", self.stream_playlists_name[self.streamplaying], "Paused")
    def Switch(self):
        if not self.streampause:
            self.Pause()
        else:
            self.Unpause()
        #self.streamplayer.switch()
        #self.streampause = self.streamplayer.Paused
    def Change(self, key):
        self.streamplayer.stop()
        self.streamplaying = key
        self.streamplayer.start(self.stream_playlists_link[key])
        title("Radio", self.stream_playlists_name[self.streamplaying], "Now Playing")
    def vol(self, vol):
        self.streamvolume = vol
        Volume.change(vol)
        #nircmd("volume", self.streamvolume)
    def Stop(self):
        self.streamplaying = None
        self.streampause = False
        self.streamrun = False
        self.streamplayer.stop()
        if self.systrayon:
            time.sleep(1)
            killme()
    def input(self, inpt):
        inpt = inpt.lower()
        if inpt == "play" or inpt == "pau" or inpt == "pause" or inpt == "p":
            self.Switch()
            self.printit()
        elif inpt == "change" or inpt == "ch" or inpt == "c":
            self.streamPrintOth = True
            self.streamPrintCh = True
            self.printit()
            self.Change(input("Change to:"))
            self.streamPrintOth = False
            self.streamPrintCh = False
            self.printit()
        elif inpt == "stop" or inpt == "exit":
            self.Stop()
            self.printit()
        elif inpt == "vol":
            self.streamPrintOth = True
            self.streamPrintVol = True
            self.printit()
            self.vol(float(input("Volume (Now: %s)\n" % Volume.getVolume())))
            self.streamPrintOth = False
            self.streamPrintVol = False
            self.printit()

    # noinspection PyStatementEffect
    def start(self):

        title("Radio", self.stream_playlists_name[self.streamplaying], "Now Playing")
        self.streamplayer.start(self.stream_playlists_link[self.streamplaying])
        # pause/unpause , submenu mit allen sendern

        def unp_p(x):
            self.Switch()


        if self.systrayon and sys.platform == "win32":


            def x0(x):
                self.Change(self.stream_playlists_key[0])
            def x1(x):
                self.Change(self.stream_playlists_key[1])
            def x2(x):
                self.Change(self.stream_playlists_key[2])
            def x3(x):
                self.Change(self.stream_playlists_key[3])
            def x4(x):
                self.Change(self.stream_playlists_key[4])
            def x5(x):
                self.Change(self.stream_playlists_key[5])
            def x6(x):
                self.Change(self.stream_playlists_key[6])
            def x7(x):
                self.Change(self.stream_playlists_key[7])
            def x8(x):
                self.Change(self.stream_playlists_key[8])
            def x9(x):
                self.Change(self.stream_playlists_key[9])
            def x10(x):
                self.Change(self.stream_playlists_key[10])
            def x11(x):
                self.Change(self.stream_playlists_key[11])
            def x12(x):
                self.Change(self.stream_playlists_key[12])
            def x13(x):
                self.Change(self.stream_playlists_key[13])
            def x14(x):
                self.Change(self.stream_playlists_key[14])
            def x15(x):
                self.Change(self.stream_playlists_key[15])

            if len(self.stream_playlists) == 1:
                sub_menu1 = {self.stream_playlists[0]: x0}
            elif len(self.stream_playlists) == 2:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1}
            elif len(self.stream_playlists) == 3:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2}
            elif len(self.stream_playlists) == 4:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3}
            elif len(self.stream_playlists) == 5:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4}
            elif len(self.stream_playlists) == 6:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5}
            elif len(self.stream_playlists) == 7:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6}
            elif len(self.stream_playlists) == 8:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7}
            elif len(self.stream_playlists) == 9:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8}
            elif len(self.stream_playlists) == 10:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                            self.stream_playlists[9]: x9}
            elif len(self.stream_playlists) == 11:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                            self.stream_playlists[9]: x9, self.stream_playlists[10]: x10}
            elif len(self.stream_playlists) == 12:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                            self.stream_playlists[9]: x9, self.stream_playlists[10]: x10,
                            self.stream_playlists[11]: x11}
            elif len(self.stream_playlists) == 13:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                            self.stream_playlists[9]: x9, self.stream_playlists[10]: x10,
                            self.stream_playlists[11]: x11,
                            self.stream_playlists[12]: x12}
            elif len(self.stream_playlists) == 14:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                            self.stream_playlists[9]: x9, self.stream_playlists[10]: x10,
                            self.stream_playlists[11]: x11,
                            self.stream_playlists[12]: x12, self.stream_playlists[13]: x13}
            elif len(self.stream_playlists) == 15:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                            self.stream_playlists[9]: x9, self.stream_playlists[10]: x10,
                            self.stream_playlists[11]: x11,
                            self.stream_playlists[12]: x12, self.stream_playlists[13]: x13,
                            self.stream_playlists[14]: x14}
            elif len(self.stream_playlists) == 16:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                            self.stream_playlists[9]: x9, self.stream_playlists[10]: x10,
                            self.stream_playlists[11]: x11,
                            self.stream_playlists[12]: x12, self.stream_playlists[13]: x13,
                            self.stream_playlists[14]: x14,
                            self.stream_playlists[15]: x15}
            else:
                def nothing(x):
                    print("nothing")

                sub_menu1 = {"Nothing": nothing}

            def quitFunc(x):
                self.Stop()

            self.systray = SysTray("data\\Ico\\Radio.ico", "Evecon: Radio", {"Pause/Unpause": unp_p},
                                   sub_menu1=sub_menu1, sub_menu_name1="Change Radio", quitFunc=quitFunc)
            self.systray.start()
            self.printit()

    def printit(self):
        cls()
        if not self.streampause:
            print("Radio:\n\nPlaying:")
        else:
            print("Radio:\n\nPaused:")

        print(self.streamplaying)
        print("\n")
        if not self.streamPrintOth:
            if not self.streampause:
                print("Pause (PAU), Stop (STOP), Change (CH), Volume (VOL)")
            else:
                print("Unpause (PAU), Stop (STOP), Change (CH), Volume (VOL)")
        elif self.streamPrintVol:
            print("Volume (Now: %s)\n" % Volume.getVolume())

        elif self.streamPrintCh:

            for xl, x2 in zip(self.stream_playlists, self.stream_playlists_key):
                print(x2 + " (" + x2.upper() + ")")

            print("Change to:\n")


def title_time_now():
    return datetime.datetime.now().strftime("%H:%M:%S")

#title("Loading Light")

class colorC:
    def __init__(self):
        self.CurColor = "07"
        self.colors = {"0" : "black", "1" : "blue", "2" : "green", "3" : "cyan", "4" : "red", "5" : "purple",
                       "6" : "yellow", "7" : "light gray", "8" : "gray", "9" : "light blue", "A" : "light green",
                       "B" : "light cyan", "C" : "light red", "D" : "light purple", "E" : "light yellow", "F" : "white"}
        self.colorsinv = {"black" : "0", "blue" : "1", "green" : "2", "cyan": "3", "red": "4", "purple": "5",
                       "yellow": "6", "light gray": "7", "gray": "8", "light blue" : "9", "light green": "A",
                       "light cyan": "B", "light red": "C", "light purple": "D", "light yellow": "E", "white": "F"}
        self.colorKeys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

    def encode(self, code, printit=False):
        background = self.colors[code[0]]
        foreground = self.colors[code[1]]
        if printit:
            print("Color:\n")
            print("Background: " + background)
            print("Foreground: " + foreground)
        return background, foreground

    def decode(self, background, foreground, printit=False):
        code = ""
        code += self.colorsinv[background]
        code += self.colorsinv[foreground]
        if printit:
            print("Code: " + code)
        return code

    def change(self, code):
        self.CurColor = code
        #subprocess.call(["color", code])
        os.system("color " + code)

    def switch(self):
        if self.CurColor == "07":
            self.change("F0")
        elif self.CurColor == "F0":
            self.change("07")

    def Man(self):
        cls()
        print("Color change")
        print("First is background")
        print("Second is foreground")
        print("Standard: 07 (White on black)\n")
        print("    0 = Schwarz     8 = Grau")
        print("    1 = Blau        9 = Hellblau")
        print("    2 = Gruen       A = Hellgruen")
        print("    3 = Tuerkis     B = Helltuerkis")
        print("    4 = Rot         C = Hellrot")
        print("    5 = Lila        D = Helllila")
        print("    6 = Gelb        E = Hellgelb")
        print("    7 = Hellgrau    F = Weiss")

        code = input("\n")
        self.CurColor = code
        os.system("color %s" % code)

color = colorC()

class VolumeC:
    def __init__(self):
        self.devices = pycaw.pycaw.AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(pycaw.pycaw.IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
        self.volume = ctypes.cast(self.interface, ctypes.POINTER(pycaw.pycaw.IAudioEndpointVolume))

        self.volumes = {0: -65.25, 0.01: -56.992191314697266, 0.02: -51.671180725097656, 0.03: -47.73759078979492,
                        0.04: -44.61552047729492, 0.05: -42.026729583740234, 0.06: -39.81534194946289,
                        0.07: -37.88519287109375, 0.08: -36.17274856567383, 0.09: -34.63383865356445,
                        0.1: -33.23651123046875, 0.11: -31.956890106201172, 0.12: -30.77667808532715,
                        0.13: -29.681535720825195, 0.14: -28.66002082824707, 0.15: -27.70285415649414,
                        0.16: -26.80240821838379, 0.17: -25.95233154296875, 0.18: -25.147287368774414,
                        0.19: -24.38274574279785, 0.2: -23.654823303222656, 0.21: -22.960174560546875,
                        0.22: -22.295886993408203, 0.23: -21.6594181060791, 0.24: -21.048532485961914,
                        0.25: -20.461252212524414, 0.26: -19.895822525024414, 0.27: -19.350669860839844,
                        0.28: -18.824398040771484, 0.29: -18.315736770629883, 0.3: -17.82354736328125,
                        0.31: -17.3467960357666, 0.32: -16.884546279907227, 0.33: -16.435937881469727,
                        0.34: -16.000192642211914, 0.35: -15.576590538024902, 0.36: -15.164472579956055,
                        0.37: -14.763236045837402, 0.38: -14.372318267822266, 0.39: -13.991202354431152,
                        0.4: -13.61940860748291, 0.41: -12.902039527893066, 0.42: -12.902039527893066,
                        0.43: -12.555663108825684, 0.44: -12.217005729675293, 0.45: -11.88572883605957,
                        0.46: -11.561516761779785, 0.47: -11.2440767288208, 0.48: -10.933131217956543,
                        0.49: -10.62841796875, 0.5: -10.329694747924805, 0.51: -10.036728858947754,
                        0.52: -9.749302864074707, 0.53: -9.46721076965332, 0.54: -9.190258026123047,
                        0.55: -8.918261528015137, 0.56: -8.651047706604004, 0.57: -8.388449668884277,
                        0.58: -8.130311965942383, 0.59: -7.876484394073486, 0.6: -7.626824855804443,
                        0.61: -7.381200790405273, 0.62: -7.1394829750061035, 0.63: -6.901548862457275,
                        0.64: -6.6672821044921875, 0.65: -6.436570644378662, 0.66: -6.209307670593262,
                        0.67: -5.98539400100708, 0.68: -5.764730453491211, 0.69: -5.547224998474121,
                        0.7: -5.33278751373291, 0.71: -5.121333599090576, 0.72: -4.912779808044434,
                        0.73: -4.707049369812012, 0.74: -4.5040669441223145, 0.75: -4.3037590980529785,
                        0.76: -4.1060566902160645, 0.77: -3.9108924865722656, 0.78: -3.718202590942383,
                        0.79: -3.527923583984375, 0.8: -3.339998245239258, 0.81: -3.1543679237365723,
                        0.82: -2.970977306365967, 0.83: -2.7897727489471436, 0.84: -2.610703229904175,
                        0.85: -2.4337174892425537, 0.86: -2.2587697505950928, 0.87: -2.08581280708313,
                        0.88: -1.9148017168045044, 0.89: -1.7456932067871094, 0.9: -1.5784454345703125,
                        0.91: -1.4130167961120605, 0.92: -1.2493702173233032, 0.93: -1.0874667167663574,
                        0.94: -0.9272695183753967, 0.95: -0.768743097782135, 0.96: -0.6118528842926025,
                        0.97: -0.4565645754337311, 0.98: -0.30284759402275085, 0.99: -0.15066957473754883, 1.0: 0.0}

        self.curVol = self.getVolume()
        self.curVoldirect = self.getVolumedirect()
    def change(self, vol: float):
        self.setdirect(self.convertToDirect(vol))
        self.refresh()

    def setdirect(self, vol: float):
        self.volume.SetMasterVolumeLevel(vol, None)
        self.refresh()

    def getVolume(self):
        return self.convertFromDirect(self.getVolumedirect())

    def getVolumedirect(self):
        return self.volume.GetMasterVolumeLevel()

    def convertToDirect(self, normal):
        return self.volumes[round(normal, 2)]

    def convertFromDirect(self, direct):
        for x in self.volumes:
            if self.volumes[x] == direct:
                return x

    def refresh(self):
        self.curVol = self.getVolume()
        self.curVoldirect = self.getVolumedirect()

Volume = VolumeC()

class Client(threading.Thread):
    def __init__(self, ip: str, port: int, react, buffersize=1024, loginName=None, loginPW=None, Seculevel=0, showLog=False):
        """
        port
        the port where the server schould listen on

        reac
        the function with will be executed when the client sent data

        ip
        normaly the ip of your pc
        ip of your pc

        buffersize
        normaly 1024
        byte limit of your get data

        loginName
        if you want the client should login in the server you should define here the username

        loginPW
        if you want the client should login in the server you should define here the password

        Seculevel
        normaly 0 if both uses 0 no secu will be used
        -2: the encryption will be deactivated, but if the client has enabled Secu, the connection will be refuesd
        -1: the encryption will be deactivated
        0:  the client decide if the encryption is enabled
        1:  you force the client to generate a encryption code, but if the client has deactivated Secu, no Secu will be used
        2:  you force the client to generate a encryption code, but if the client has deactivated Secu, the connection will be refuesd

        BigServerBuffersize
        normaly 536870912 (maybe 512MB)
        if this Buffersize is less then the normal buffersize the BigServer will be deactivated
        you can set the Buffersize of the Bigserver

        BigServerPort
        set the Port of the BigServer if it is 0 the port is the normal port+1

        showLog
        show Log entries

        Keywords:
        #C! for a command
        #T! do not use, this will be used to talk to the client directly, like login in

        """
        super().__init__()


        self.port = port
        self.react = react
        self.ip = ip
        self.buffersize = buffersize
        self.showLog = showLog


        if loginName and loginPW:
            self.login = True
        else:
            self.login = False
        self.loginName = loginName
        self.loginPW = loginPW

        self.Seculevel = Seculevel

        self.Logsend = []
        self.Logrece = []

        self.s = socket.socket()

        self.Running = False # between start and end
        self.Connected = False # while connected

        self.conAddress = None
        self.conInfo = {}

        self.Info = {"login" : {"status" : self.login, "name" : self.loginName, "password" : self.loginPW},
                     "secu" : {"level" : self.Seculevel}}

        self.Log = []
        self.Status = "Starting"

    def run(self):
        self.Running = True

        self.Status = "Setup"
        self.writeLog("Status:")
        self.writeLog("Ip: " + str(self.ip))
        self.writeLog("Port: " + str(self.port))
        self.writeLog("Login: " + str(self.login))
        self.writeLog("LoginName: " + str(self.loginName))
        self.writeLog("LoginPW: " + str(self.loginPW))
        self.writeLog("Seculevel: " + str(self.Seculevel))

        self.Status = "Connecting"

        try:
            self.s.connect((self.ip, self.port))

        except TimeoutError:
            # wrong ip
            self.writeLog("Can not find IP, Timeout")
            raise EveconExceptions.ClientWrongPort

        except ConnectionRefusedError:
            # wrong port
            self.writeLog("Can not connect to port, ConnectionRefused")
            raise EveconExceptions.ClientWrongPort

        self.Connected = True
        self.Status = "Connected"
        self.writeLog("Connected with Server")

        try:
            InfoServer_raw = self.s.recv(1024)
        except ConnectionResetError:
            self.writeLog("Server disconnected without warning")
            raise EveconExceptions.ClientConnectionLost()

        InfoServer = InfoServer_raw.decode("UTF-8").split("!")

        if not InfoServer[0] == "#T":
            self.writeLog("Server send wrong Infoconnection")
            raise EveconExceptions.ClientWrongServer()

        elif InfoServer[0] == "#T" and InfoServer[1] == "Test":
            self.conInfo = {"secu": {"status": -1}, "key": "None"}
            self.writeLog("== uses the 'Test'-Version")

        else:
            if InfoServer[1] == "True":
                # noinspection PyTypeChecker
                InfoServer[1] = True
            else:
                # noinspection PyTypeChecker
                InfoServer[1] = False
            if InfoServer[2] == "True":
                # noinspection PyTypeChecker
                InfoServer[2] = True
            else:
                # noinspection PyTypeChecker
                InfoServer[2] = False
            self.conInfo = {"login": {"status" : InfoServer[1]},
                            "bigserver" : {"status" : InfoServer[2], "port" : int(InfoServer[3])},
                            "secu": {"level" : int(InfoServer[4])}}

        S = int(self.conInfo["secu"]["level"])
        C = int(self.Seculevel)

        if not -3 < S < 3:
            self.writeLog("Server send a wrong Seculevel")
            raise EveconExceptions.ClientWrongServer

        elif S == -2:
            if C == 2:
                self.Info["secu"]["status"] = 0
            else:
                self.Info["secu"]["status"] = -1
        elif S == -1:
            if C == 2:
                self.Info["secu"]["status"] = 1
            else:
                self.Info["secu"]["status"] = -1
        elif S == 0:
            if C < 1:
                self.Info["secu"]["status"] = -1
            else:
                self.Info["secu"]["status"] = 1
        elif S == 1:
            if C == -2:
                self.Info["secu"]["status"] = -1
            else:
                self.Info["secu"]["status"] = 1
        elif S == 2:
            if C == -2:
                self.Info["secu"]["status"] = 0
            else:
                self.Info["secu"]["status"] = 1

        if self.Info["secu"]["status"] == 1:
            self.Info["secu"]["key"] = randompw(returnpw=True, printpw=False, exclude=["#", "!"])
        else:
            self.Info["secu"]["key"] = None

        InfoSend = b'#T!' + str(self.Info["login"]["status"]).encode() + b'!' + \
                   str(self.Info["login"]["name"]).encode() + b'!' + \
                   str(self.Info["login"]["password"]).encode() + b'!' + \
                   str(self.Info["secu"]["status"]).encode() + b'!' + \
                   str(self.Info["secu"]["level"]).encode() + b'!' + \
                   str(self.Info["secu"]["key"]).encode()

        self.send(InfoSend, encrypt=False)

        try:
            conAccept = self.s.recv(self.buffersize).decode("UTF-8")
        except ConnectionResetError:
            self.writeLog("Server disconnected without warning")
            raise EveconExceptions.ClientConnectionLost()
        #print(conAccept, InfoSend)

        if conAccept:

            if self.Info["secu"]["status"] == 1:
                self.writeLog("Started Connection with Server. Decryption Key: " + self.Info["secu"]["key"])

                while self.Running and self.Connected and self.Status != "Ended" and self.Status == "Connected":
                    try:
                        data_en = self.s.recv(self.buffersize)
                    except ConnectionResetError:
                        self.writeLog("Server disconnected without warning")
                        break
                    except ConnectionAbortedError:
                        self.writeLog("Connection aborted")
                        break
                    #print(data_en)
                    data = simplecrypt.decrypt(self.Info["secu"]["key"], data_en)

                    self.receive(data)

            elif self.Info["secu"]["status"] == -1:
                self.writeLog("Started Connection with Server. No Decryption")

                while self.Running and self.Connected and self.Status != "Ended" and self.Status == "Connected":
                    try:
                        data = self.s.recv(self.buffersize)
                    except ConnectionResetError:
                        self.writeLog("Server disconnected without warning")
                        break
                    except ConnectionAbortedError:
                        self.writeLog("Connection aborted")
                        break

                    self.receive(data)
            else:
                self.writeLog("Wrong status")
        else:
            self.writeLog("Wrong Password")

        self.s.close()
        self.Running = False
        self.Connected = False
        self.Status = "Ended"


    def send(self, data, encrypt=None):
        if self.Running and self.Connected and self.Status != "Ended" and self.Status == "Connected":
            if type(data) == str:
                data_send = data.encode()
            elif type(data) == int:
                data_send = str(data).encode()
            elif type(data) == bool:
                data_send = str(data).encode()
            else:
                data_send = data

            if encrypt is None:
                if self.Info["secu"]["status"] == 1:
                    data_send_de = simplecrypt.encrypt(self.Info["secu"]["key"], data_send)
                else:
                    data_send_de = data_send
            elif encrypt:
                data_send_de = simplecrypt.encrypt(self.Info["secu"]["key"], data_send)
            else:
                data_send_de = data_send

            self.Logsend.append(data)
            self.s.send(data_send_de)

    def receive(self, data):
        if self.Running and self.Connected and self.Status != "Ended" and self.Status == "Connected":
            data_form = data.decode("UTF-8")
            data_form_split = data_form.split("!")

            self.Logrece.append(data)
            self.writeLog("Receive: " + data_form)

            if data_form_split[0] == "#C" and len(data_form_split) > 1:
                if data_form_split[1] == "exit":
                    self.exit()
            elif data_form_split[0] == "#T" and len(data_form_split) > 1:
                if data_form_split[1] == "exit":
                    if data_form_split[1] == "exit":
                        self.exit(sendM=False)
                        self.writeLog("Server disconnected")

            else:
                self.react(data_form)

    def save(self, directory:str):
        file_log_raw = open("Log.txt", "w")
        for x in self.Log:
            file_log_raw.write(x)
        file_log_raw.close()

        file_logsend_raw = open("LogSend.txt", "w")
        for x in self.Logsend:
            file_logsend_raw.write(x)
        file_logsend_raw.close()

        file_logrece_raw = open("LogReceive.txt", "w")
        for x in self.Logrece:
            file_logrece_raw.write(x)
        file_logrece_raw.close()

    def writeLog(self, data):
        write = "(" + datetime.datetime.now().strftime("%H:%M:%S:%f") + ") " + "(" + self.Status + ") " + data
        self.Log.append(write)
        if self.showLog:
            print("[Log] " + write)

    def exit(self, sendM=True):
        if sendM:
            self.send("#T!exit")
        self.s.close()

    def getStatus(self):
        curStatus = {"status" : {"status" : self.Status, "running" : self.Running, "connected" : self.Connected},
                     "log": self.Log, "info" : self.Info}
        return curStatus


class Server(threading.Thread):
    def __init__(self, port: int, react, ip=socket.gethostbyname(socket.gethostname()), buffersize=1024,
                 loginName=None, loginPW=None, maxConnections=1, Seculevel=0, BigServerBuffersize=536870912,
                 BigServerPort=0, welcomeMessage="Welcome to Evecon Server!", thisBig=False):
        """
        ip
        ip of the server

        port
        the port where the server listen on

        reac
        the function with will be executed when the server sent data

        buffersize
        normaly 1024
        byte limit of your get data

        loginName
        if enabled in the server the loginName is defined here

        loginPW
        if enabled in the server the loginPW is defined here

        Seculevel
        normaly 0 if both uses 0 no secu will be used
        -2: the encryption will be deactivated so you can not connect with server with seculevel 2
        -1: the encryption will be deactivated, but if the client has enabled Secu, Secu will be used
        0:  the client decide if the encryption is enabled
        1:  you force the client to generate a encryption code, but if the client has deactivated Secu, no Secu will be used
        2:  the encryption will be deactivated so you can not connect with server with seculevel -2

        S   C   Y=Encryption N=No Encryption E=No Connection
        -2  -2  N
        -2  -1  N
        -2  0   N
        -2  1   N
        -2  2   E

        -1  -2  N
        -1  -1  N
        -1  0   N
        -1  1   N
        -1  2   Y

        0  -2   N
        0  -1   N
        0  0    N
        0  1    Y
        0  2    Y

        1  -2   N
        1  -1   Y
        1  0    Y
        1  1    Y
        1  2    Y

        2  -2   E
        2  -1   Y
        2  0    Y
        2  1    Y
        2  2    Y

        BigServerBuffersize
        normaly 536870912 (maybe 512MB)
        if this Buffersize is less then the normal buffersize the BigServer will be deactivated
        you can set the Buffersize of the Bigserver

        BigServerPort
        set the Port of the BigServer if it is 0 the port is the normal port+1

        Keywords:
        #C! for a command
        #T! do not use, this will be used to talk to the client directly, like login in
        #R! for receiving some return infomation
        #B! for travel through bigserver

        """
        super().__init__()

        self.version = "1.0.0"

        self.thisBigServer = thisBig
        self.port = port
        self.react = react
        self.ip = ip
        self.buffersize = buffersize
        self.maxConnections = maxConnections
        self.welcomeMessage = welcomeMessage

        if loginName and loginPW:
            self.login = True
        else:
            self.login = False
        self.loginName = loginName
        self.loginPW = loginPW

        self.Seculevel = Seculevel

        self.Timer = TimerC()

        self.BigServerBuffersize = BigServerBuffersize
        if not BigServerPort:
            self.BigServerPort = port + 1

        if BigServerBuffersize > self.buffersize:
            self.BigServerEnabled = True
            self.BigServer = Server(port=BigServerPort, react=self.receive, buffersize=self.BigServerBuffersize,
                                    loginName=self.loginName, loginPW=self.loginPW, Seculevel=self.Seculevel,
                                    BigServerBuffersize=0, thisBig=True)
        else:
            self.BigServerEnabled = False
            self.BigServer = None

        self.Logsend = []
        self.Logrece = []

        self.s = socket.socket()
        try:
            self.s.bind((self.ip, self.port))
        except OSError:
            raise EveconExceptions.ServerPortUsed(self.port)

        self.Running = False  # between start and end
        self.Connected = False  # while connected

        self.connects = []

        self.conAddress = None
        self.con = None
        self.conInfo = None

        self.Info = {"ip": self.ip, "port": self.port, "buffersize": self.buffersize,
                     "maxconnections": self.maxConnections, "welcomeMessage": self.welcomeMessage,
                     "login": {"status": self.login, "name": self.loginName, "password": self.loginPW},
                     "bigserver": {"status": self.BigServerEnabled, "ip": self.ip, "port": self.BigServerPort},
                     "secu": {"level": self.Seculevel}}

        self.Log = []
        self.Status = "Starting"

    def run(self):
        self.Running = True
        self.Timer.start()

        self.Status = "Setup"
        self.writeLog("Status:")
        self.writeLog("Ip: " + str(self.ip))
        self.writeLog("Port: " + str(self.port))
        self.writeLog("Login: " + str(self.login))
        self.writeLog("LoginName: " + str(self.loginName))
        self.writeLog("LoginPW: " + str(self.loginPW))
        self.writeLog("BigServer: " + str(self.BigServerEnabled))
        self.writeLog("BigServerPort: " + str(self.BigServerPort))
        self.writeLog("Seculevel: " + str(self.Seculevel))

        while self.Running:

            self.Status = "Listening..."
            self.writeLog("Listening...")

            self.s.listen(self.maxConnections)

            self.con, self.conAddress = self.s.accept()

            self.writeLog("Found Client with IP: %s, Port: %s" % (self.conAddress[0], self.conAddress[1]))

            self.Connected = True
            self.Status = "Connected"
            self.connects.append(self.conAddress)

            InfoSend = b'#T!' + str(self.Info["login"]["status"]).encode() + b'!' + \
                       str(self.Info["bigserver"]["status"]).encode() + b'!' + \
                       str(self.Info["bigserver"]["port"]).encode() + b'!' + \
                       str(self.Info["secu"]["level"]).encode()

            # self.Log.append(InfoSend)
            self.send(InfoSend, encrypt=False)

            try:
                InfoClient_raw = self.con.recv(1024)
            except ConnectionResetError:
                self.writeLog("Client disconnected while logging in")
                continue

            InfoClient = InfoClient_raw.decode("UTF-8").split("!")

            if not InfoClient[0] == "#T":
                self.writeLog("Client send wrong Infoconnection")
                continue

            elif InfoClient[0] == "#T" and InfoClient[1] == "Test":
                self.conInfo = {"secu": {"status": -1}, "key": "None"}
                self.writeLog("Client uses the 'Test'-Version")

            else:
                if InfoClient[1] == "True":
                    # noinspection PyTypeChecker
                    InfoClient[1] = True
                else:
                    # noinspection PyTypeChecker
                    InfoClient[1] = False

                self.conInfo = {"login": {"status": InfoClient[1], "name": InfoClient[2], "password": InfoClient[3]},
                                "secu": {"status": int(InfoClient[4]), "level": int(InfoClient[5]),
                                         "key": InfoClient[6]}}

            self.writeLog("Client:")
            self.writeLog("Login: " + str(InfoClient[1]))
            self.writeLog("LoginName: " + InfoClient[2])
            self.writeLog("LoginPW: " + InfoClient[3])
            self.writeLog("Secu: " + str(InfoClient[4]))
            self.writeLog("Seculevel: " + str(InfoClient[5]))
            self.writeLog("Secukey: " + self.conInfo["secu"]["key"])

            # print(self.Info, self.conInfo)

            if self.login:
                if self.conInfo["login"]["status"]:
                    if self.loginName == self.conInfo["login"]["name"] and self.loginPW == self.conInfo["login"][
                        "password"]:
                        conAccept = True
                    else:
                        conAccept = False
                else:
                    conAccept = False
            elif self.conInfo["login"]["status"]:
                conAccept = False
            else:
                conAccept = True

            self.send(conAccept, encrypt=False)
            if not conAccept:
                self.writeLog("Client sent wrong logindata")
                continue

            self.send(self.welcomeMessage)

            if self.conInfo["secu"]["status"] == 1:  # yes
                self.writeLog("Started Connection with Client. Decryption")

                while self.Running and self.Connected and self.Status != "Ended" and self.Status == "Connected":
                    try:
                        data_en = self.con.recv(1024)
                    except ConnectionResetError:
                        self.writeLog("Client disconnected without warning")
                        break
                    except ConnectionAbortedError:
                        self.writeLog("Connection aborted")
                        break
                    except OSError:
                        break

                    data = simplecrypt.decrypt(self.conInfo["secu"]["key"], data_en)

                    if not data:
                        self.writeLog("Client disconnected. If this happens the Client send something courious")
                        break

                    self.receive(data)

            elif self.conInfo["secu"]["status"] == -1:  # no
                self.writeLog("Started Connection with Client. No Decryption")

                while self.Running and self.Connected and self.Status != "Ended" and self.Status == "Connected":
                    try:
                        data = self.con.recv(1024)
                    except ConnectionResetError:
                        self.writeLog("Client disconnected without warning")
                        break
                    except ConnectionAbortedError:
                        self.writeLog("Connection aborted")
                        break
                    except OSError:
                        break

                    if not data:
                        self.writeLog("Client disconnected. If this happens the Client send something courious")
                        break

                    self.receive(data)

            elif self.conInfo["secu"]["status"] == 0:  # no connection
                self.writeLog("Can not establish a connection. Seclevels: Server: %s, Client: %s" % (
                    self.Seculevel, self.conInfo["secu"]["level"]))

            else:
                self.writeLog("The Client sent: " + str(self.conInfo["secu"]["status"]) + ". Error")

            self.Connected = False
            self.con.close()
            # reset
            self.conAddress = None
            self.con = None
            self.conInfo = None

        self.Running = False
        self.Status = "Ended"

    def send(self, data, encrypt=None):
        if self.Running and self.Connected and self.Status != "Ended" and self.Status == "Connected" or not encrypt:

            if type(data) == str:
                data_send = data.encode()
            elif type(data) == int:
                data_send = str(data).encode()
            elif type(data) == bool:
                data_send = str(data).encode()
            else:
                data_send = data

            if encrypt is None:
                if self.conInfo["secu"]["status"] == 1:
                    data_send_de = simplecrypt.encrypt(self.conInfo["secu"]["key"], data_send)
                else:
                    data_send_de = data_send
            elif encrypt:
                data_send_de = simplecrypt.encrypt(self.conInfo["secu"]["key"], data_send)
            else:
                data_send_de = data_send

            # print(encrypt, self.conInfo["secu"]["status"])
            # print(data, data_send, data_send_de)
            self.Logsend.append(data)
            self.writeLog("Sended: " + data_send.decode("UTF-8"))
            self.con.send(data_send_de)

    def receive(self, data):
        if self.Running and self.Connected and self.Status != "Ended" and self.Status == "Connected":
            data_form = data.decode("UTF-8")
            data_form_split = data_form.split("!")

            self.Logrece.append(data)
            self.writeLog("Receive: " + data_form)

            if data_form_split[0] == "#C" and len(data_form_split) > 1:
                if data_form_split[1] == "getTimeRaw":
                    self.send("#R!" + str(self.getRunTime()))
                elif data_form_split[1] == "getTime":
                    self.send("#R!" + str(self.getRunTime(False)))
                elif data_form_split[1] == "exit":
                    self.exit()
            elif data_form_split[0] == "#T" and len(data_form_split) > 1:
                if data_form_split[1] == "exit":
                    self.exit(sendM=False)
                    self.writeLog("Client disconnected")
            elif data_form_split[0] == "#B" and len(data_form_split) > 1:
                pass
            else:
                self.react(data_form)

    def writeLog(self, data):
        write = "(" + datetime.datetime.now().strftime("%H:%M:%S:%f") + ") " + "(" + self.Status + ") " + data
        self.Log.append(write)
        print("[Log] " + write)

    def save(self, directory: str):
        file_log_raw = open("Log.txt", "w")
        for x in self.Log:
            file_log_raw.write(x)
        file_log_raw.close()

        file_logsend_raw = open("LogSend.txt", "w")
        for x in self.Logsend:
            file_logsend_raw.write(x)
        file_logsend_raw.close()

        file_logrece_raw = open("LogReceive.txt", "w")
        for x in self.Logrece:
            file_logrece_raw.write(x)
        file_logrece_raw.close()

    def exit(self, sendM=True):
        if sendM:
            self.send("#T!exit")
        self.con.close()

    def getStatus(self):
        curStatus = {"status": {"status": self.Status, "running": self.Running, "connected": self.Connected},
                     "log": self.Log, "info": self.Info, "connects": self.connects}
        return curStatus

    def getRunTime(self, raw=True):
        if raw:
            return self.Timer.getTime()
        else:
            return self.Timer.getTimeFor()


class Browser:
    def __init__(self, path):
        self.path = path
        self.bro = None

        self.name = self.path.split(path_seg)[-1]
        if self.name in (p.name() for p in psutil.process_iter()):
            self.running = True
        else:
            self.running = False

    def open(self, url: list, new_type=2):
        if type(url) != list:
            url = [url]
        for x in url:
            self.bro.open(url=x, new=new_type)

    def open_win(self, url: list):
        self.open(url=url, new_type=1)

    def open_tab(self, url: list):
        self.open(url=url, new_type=2)

    def refresh(self):
        if self.name in (p.name() for p in psutil.process_iter()):
            self.running = True
        else:
            self.running = False

class Firefox(Browser):
    def __init__(self, path=firefox_path):
        super().__init__(path)

        self.bro = webbrowser.Mozilla(self.path)


class Vivaldi(Browser):
    def __init__(self, path=vivaldi_path):
        super().__init__(path)

        self.bro = webbrowser.Chrome(self.path)


title("Loading Title Time")



def computerconfig_schoolpc():
    color.change("F0")

def computerconfig_minipc():
    global MusicDir, thisIP, cores#, browser
    MusicDir = "C:\\Users\\Mini-Pc Nutzer\\Desktop\\Musik\\Musik\\!Fertige Musik"
    thisIP = "192.168.2.102"
    #browser = "vivaldi"
    cores = 2

def computerconfig_bigpc():
    global MusicDir, thisIP, cores
    MusicDir = "D:\\Musik\\!Fertige Musik"
    thisIP = "192.168.2.101"
    cores = 4

def computerconfig_aldi():
    nircmd("setsize", 1000, 520)
    thisIP = "192.168.2.110"


def computerconfig_laptop():
    global thisIP
    thisIP = "192.168.2.106" # Lan __ .104 = WLAN
    cores = 4


Computername = socket.gethostname()

if Computername == "Computer-Testet":
    title("OLD", "OLD", "somebody@Mini-PC")
    computer = "MiniPC"
    computerconfig_minipc()
    HomePC = True

elif Computername == "Bigger-PC":
    title("OLD", "OLD", "somebody@BigPC")
    computer = "BigPC"
    computerconfig_bigpc()

    HomePC = True

elif Computername == "Test":
    title("OLD", "OLD", "somebody@Aldi-Laptop")
    computer = "AldiPC"
    computerconfig_aldi()

elif Computername == "Luis":
    title("OLD", "OLD", "somebody@Luis-Laptop")
    computer = "Laptop"
    computerconfig_laptop()

else:
    title("OLD", "OLD", "No Computer found")
    computer = None

file_proversion_raw = open("data"+path_seg+"Info"+path_seg+"ProgramVersion", "r")
ProVersion = file_proversion_raw.readline()
file_proversion_raw.close()

def versionFind():
    file_version_raw = open("data"+path_seg+"Info"+path_seg+"version", "r")
    global this_version
    this_version = []
    for x in file_version_raw:
        this_version.append(x.strip())
    file_version_raw.close()
    return this_version

def normaltitle():
    #global ss_active
    if ss_active:
        title("Screensaver", "")

    else:
        title("OLD", "Version: " + str(versionFind()[1]))

normaltitle()

if ProVersion == "PC-Version":
    if computer == "MiniPC":
        normaltitle()
        version = "MiniPC"
    elif computer == "BigPC":
        normaltitle()
        version = "BigPC"
    elif computer == "Laptop":
        normaltitle()
        version = "Laptop"
    else:
        title("Loading")
        version = None
elif ProVersion == "MainStick-Version":
    normaltitle()
    version = "MainStick"
elif ProVersion == "MiniStick-Version":
    normaltitle()
    version = "MiniStick"
else:
    title("Loading")
    version = None



def Status(printit=True):
    if printit:
        cls()
        print("Status\n")

        print("Time: " + datetime.datetime.now().strftime("%H:%M:%S"))
        print("Date: " + datetime.datetime.now().strftime("%d.%m.%Y"))

        print("\nEvecon:\n")
        print("Version: " + versionFind()[1])
        print("Versionnummber: " + versionFind()[0])
        print("Evecon Type: " + version)
        print("PID: " + str(os.getpid()))

        print("\nComputer:\n")
        print("Computername: " + Computername)
        print("Username: " + getpass.getuser())
        print("Computer synonymous: " + computer)
        if thisIP:
            print("IP address: " + str(thisIP))
        print("Homepc: " + str(HomePC))


        input()

    return [versionFind()[1], versionFind()[0], version, os.getpid(),Computername, getpass.getuser(), computer, thisIP, HomePC]


def randompw(returnpw=False, length=150, printpw=True, exclude=None):
    if exclude is None:
        exclude = []
    listx = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
             "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
             "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!",
             "§", "$", "%", "&", "/", "(", ")", "=", "?", "ß", "#", "'", "+", "*", "~", "ü", "ö", "ä", "-", "_", ".",
             ":", ",", ";", "{", "[", "]", "}", ">", "<", "|"]

    for x in exclude:
        for y in range(len(listx) - 1):
            if x == listx[y]:
                del listx[y]

    pw = ""

    for rx in range(length):
        pw += listx[random.randint(0, len(listx) - 1)]

    if returnpw:
        return pw

    if printpw:
        cls()
        print("Password: (length: %s) \n\n%s" % (length, pw))

        input()



class SplatoonC:
    def __init__(self, roundtime = 180, weaponlang="Eng"):

        self.weaponsGer = ["Disperser", "Disperser Neo", "Junior-Klechser", "Junior-Klechser Plus", "Fein-Disperser",
                           "Fein-Disperser Neo", "Airbrush MG", "Airbrush RG", "Klechser", "Tentatek-Klechser",
                           "Kensa-Kleckser", "Heldenwaffe Replik (Klechser)", "Okto-Klechser Replik", ".52 Gallon",
                           ".52 Gallon Deko", "N-ZAP85", "N-ZAP89", "Profi-Klechser", "Focus-Profi-Kleckser",
                           "Kensa-Profi-Kleckser", ".96 Gallon", ".96 Gallon Deko", "Platscher", "Platscher SE",

                           "Luna-Blaster", "Luna-Blaster Neo", "Kensa-Luna-Blaster", "Blaster", "Blaster SE",
                           "Helden-Blaster Replik", "Fern-Blaster", "Fern-Blaster SE", "Kontra-Blaster",
                           "Kontra-Blaster Neo", "Turbo-Blaster", "Turbo-Blaster Deko", "Turbo-Blaster Plus",
                           "Turbo-Blaster Plus Deko",

                           "L3 Tintenwerfer", "L3 Tintenwerfer D", "S3 Tintenwerfer", "S3 Tintenwerfer D", "Quetscher",
                           "Quetscher Fol",

                           "Karbonroller", "Karbonroller Deko", "Klecksroller", "Medusa-Klecksroller",
                           "Kensa-Klecksroller", "Helden-Roller Replik", "Dynaroller", "Dynaroller Tesla",
                           "Kensa-Dynaroller", "Flex-Roller", "Flex-Roller Fol",
                           "Quasto", "Quasto Fresco", "Kalligraf", "Kalligraf Fresco", "Helden-Pinsel Replik",

                           "Sepiator Alpha", "Sepiator Beta", "Klecks-Konzentrator", "Rilax-Klecks-Konzentrator",
                           "Kensa-Klecks-Konzentrator", "Helden-Konzentrator Replik", "Ziel-Konzentrator",
                           "Rilax-Ziel-Konzentrator", "Kensa-Ziel-Konzentrator", "E-liter 4K", "E-liter 4K SE",
                           "Ziel-E-liter 4K", "Ziel-E-liter 4K SE", "Klotzer 14-A", "Klotzer 14-B", "T-Tuber",
                           "T-Tuber SE",

                           "Schwapper", "Schwapper Deko", "Helden-Schwapper Replik", "3R-Schwapper",
                           "3R-Schwapper Fresco", "Knall-Schwapper", "Trommel-Schwapper", "Trommel-Schwapper Neo",
                           "Kensa-Trommel-Schapper", "Wannen-Schwapper",

                           "Klecks-Splatling", "Sagitron-Klecks-Splatling", "Splatling", "Splatling Deko",
                           "Helden-Splatling Replik", "Hydrant", "Hydrant SE", "Kuli-Splatling", "Nautilus 47",

                           "Sprenkler", "Sprenkler Fresco", "Klecks-Doppler", "Enperry-Klecks-Doppler",
                           "Kensa-Klecks-Doppler", "Helden-Doppler Replik", "Kelvin 525", "Kelvin 525 Deko",
                           "Dual-Platscher", "Dual-Platscher SE", "Quadhopper Noir", "Quadhopper Blanc",

                           "Parapulviator", "Sorella-Parapulviator", "Helden-Pulviator Replik", "Camp-Pulviator",
                           "Sorella-Camp-Pulviator", "UnderCover", "Sorella-UnderCover"]

        self.weaponsEng = ["Sploosh-o-matic", "Neo Sploosh-o-matic", "Splattershot Jr.", "Custom Splattershot Jr.",
                           "Splash-o-matic", "Neo Splash-o-matic", "Aerospray MG", "Aerospray RG", "Splattershot",
                           "Tentatek Splattershot", "Kensa Splattershot", "Hero Shot Replica", "Octo Shot Replica",
                           ".52 Gal", ".52 Gal Deco", "N-ZAP '85", "N-ZAP '89", "Splattershot Pro",
                           "Forge Splattershot Pro", "Kensa Splattershot Pro", ".96 Gal", ".96 Gal Deco",
                           "Jet Squelcher", "Custom Jet Squelcher",

                           "Luna Blaster", "Luna Blaster Neo", "Kensa Luna Blaster", "Blaster", "Custom Blaster",
                           "Hero Blaster Replica", "Range Blaster", "Custom Range Blaster", "Clash Blaster",
                           "Clash Blaster Neo", "Rapid Blaster", "Rapid Blaster Deco", "Rapid Blaster Pro",
                           "Rapid Blaster Pro Deco",

                           "L-3 Nozzlenose", "L-3 Nozzlenose D", "H-3 Nozzlenose", "H-3 Nozzlenose D", "Squeezer",
                           "Foil Squeezer",

                           "Carbon Roller", "Carbon Roller Deco", "Splat Roller", "Krak-On Splat Roller",
                           "Kensa Splat Roller", "Hero Roller Replica", "Dynamo Roller", "Gold Dynamo Roller",
                           "Kensa Dynamo Roller", "Flingza Roller", "Foil Flingza Roller",
                           "Inkbrush", "Inkbrush Nouveau", "Octobrush", "Octobrush Nouveau", "Herobrush Replica",

                           "Classic Squiffer", "New Squiffer", "Splat Charger", "Firefin Splat Charger",
                           "Kensa Charger", "Hero Charger Replica", "Splatterscope", "Firefin Splatterscope",
                           "Kensa Splatterscope", "E-liter 4K", "Custom E-liter 4K", "E-liter 4K Scope",
                           "Custom E-liter 4K Scope", "Bamboozler 14 MK I", "Bamboozler 14 MK II", "Goo Tuber",
                           "Custom Goo Tuber",

                           "Slosher", "Slosher Deco", "Hero Slosher Replica", "Tri-Slosher", "Tri-Slosher Nouverau",
                           "Sloshing Machine", "Sloshing Machine Neo", "Kensa Sloshing Machine", "Bloblobber",
                           "Explosher",

                           "Mini Splatling", "Zink Mini Splatling", "Heavy Splatling", "Heavy Splatling Deco",
                           "Hero Splatling Replica", "Hydra Splatling", "Custom Hydra Splatling", "Ballpoint Splatling",
                           "Nautilus 47",

                           "Bapple Dualies", "Bapple Dualies Nouveau", "Splat Dualies", "Enperry Splat Dualies",
                           "Kensa Splat Dualies", "Hero Dualie Replicas", "Glooga Dualies", "Glooga Dualies Deco",
                           "Dualie Squelchers", "Custom Dualie Squelchers", "Dark Tetra Dualies", "Light Tetra Dualies",

                           "Splat Brella", "Sorella Brella", "Hero Brella Replica", "Tenta Brella",
                           "Tenta Sorella Brella", "Undercover Brella", "Undercover Sorella Brella"]

        self.lang = weaponlang
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
        self.WRthis = self.randomWP(lang="both")
        self.WRnext = self.randomWP(lang="both")

    def input(self, inpt):
        inpt = inpt.lower()
        if inpt == "wr":
            self.WRswitch()
            return True
        elif inpt == "exit" or inpt == "stop":
            self.stop()
            return True
        elif inpt == "reroll" or inpt == "rerol" or inpt == "rero" or inpt == "re" or inpt == "r":
            self.WRreroll()
            return True
        elif len(inpt) > 1:
            if inpt[0] == "e":
                try:
                    self.ChEffect(int(inpt.lstrip("e")))
                    return True
                except ValueError:
                    return self.RoundOverF()
            else:
                return self.RoundOverF()
        else:
            return self.RoundOverF()

    def randomWP(self, printweapon=False, lang=None):
        number = random.randint(0, len(self.weaponsEng) - 1)

        if not lang:
            if self.lang == "eng":
                weapon = self.weaponsEng[number]
            else:  # German
                weapon = self.weaponsGer[number]
        else:
            if lang == "eng":
                weapon = self.weaponsEng[number]
            elif lang == "both":
                weapon = (self.weaponsEng[number], self.weaponsGer[number])
            else:  # German
                weapon = self.weaponsGer[number]

        if printweapon:
            if lang == "both":
                print("Your Weapon:\n%s (%s)" % (weapon[0], weapon[1]))
            else:
                print("Your Weapon:\n%s" % weapon)
        return weapon

    def WRswitch(self):
        if self.WR:
            self.WR = False
        else:
            self.WR = True

    def stop(self):
        self.RUN = False

    def WRreroll(self):
        WRnextTMP = self.WRnext
        self.WRnext = self.randomWP(lang="both")

        while self.WRthis == self.WRnext or WRnextTMP == self.WRnext:
            self.WRnext = self.randomWP(lang="both")

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
                self.WRnext = self.randomWP(lang="both")

                while WRthisTMP == self.WRnext or self.WRthis == self.WRnext:
                    self.WRnext = self.randomWP(lang="both")

            self.RoundOver = False
            self.Start = True
            return True
        else:
            return False

    def printit(self, printcom=True):
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
            print("This Round:\t %s (%s)" % self.WRthis)
            print("Next Round:\t %s (%s)" % self.WRnext)
        if printcom:
            if self.WR:
                print("\nWeapon Randomizer (WR), Effect ('E'+number), Reroll Next Weapon(REROLL)")
            else:
                print("\nWeapon Randomizer (WR), Effect ('E'+number)")

        if self.RoundOver:
            print("\nStart Next Round?")

    def printcom(self):
        if self.WR:
            print("Weapon Randomizer (spWR), Effect (spE), Next Round (spN), Reroll Next Weapon(spR)")
        else:
            print("Weapon Randomizer (spWR), Effect (spE), Next Round (spN)")




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

def unge(zahl):
    if type(zahl) != int:
        pass
    elif zahl/2 == int(zahl/2):
        return 0
    else:
        return 1

def getPartStr(word: str, begin: int, end: int):
    part = ""
    if len(word) < end or len(word) <= begin or begin >= end:
        return False

    for x in range(end):
        if x < begin:
            continue
        part += word[x]
    return part

def getPartStrToStr(word: str, endkey: str, beginkey="", exact=False):
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


class ToolsC:
    def __init__(self):
        self.EnergyPlan = self.EnergyPlanC()
        self.Run = True
    class EnergyPlanC:
        def __init__(self):
            self.cEP = None
            self.cEP_code = None
            self.cEP_id = None
            self.getEP()
            self.Plans = ["381b4222-f694-41f0-9685-ff5bb260df2e", "a1841308-3541-4fab-bc81-f71556f20b4a", "472405ce-5d19-4c83-94d7-a473c87dedad"]
            self.Plans_Dic = {"Ausbalanciert" : "381b4222-f694-41f0-9685-ff5bb260df2e", "Energiesparmodus" : "a1841308-3541-4fab-bc81-f71556f20b4a",
                              "0Sys" : "472405ce-5d19-4c83-94d7-a473c87dedad"}

        def getEP(self, printit=False):
            p = subprocess.Popen(["powercfg", "/GETACTIVESCHEME"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            output, err = p.communicate(b"input data that is passed to subprocess' stdin")
            try:
                eplan_tmp = output.decode("utf-8")
            except UnicodeDecodeError:
                eplan_tmp = 'GUID des Energieschemas: a1841308-3541-4fab-bc81-f71556f20b4a  (Energiesparmodus)'

            eplan_tmp2 = eplan_tmp.lstrip("GUID des Energieschemas").lstrip(": ")
            eplan_code = ""
            for x in range(36):
                eplan_code += eplan_tmp2[x]

            self.cEP_code = eplan_code

            if eplan_code == '381b4222-f694-41f0-9685-ff5bb260df2e':
                self.cEP = "Ausbalanciert"
                self.cEP_id = 0
            elif eplan_code == 'a1841308-3541-4fab-bc81-f71556f20b4a':
                self.cEP = "Energiesparmodus"
                self.cEP_id = 1
            elif eplan_code == '472405ce-5d19-4c83-94d7-a473c87dedad':
                self.cEP = "0Sys"
                self.cEP_id = 2
            else:
                raise EveconExceptions.EnergyPlanNotFound

            if printit:
                print("Current Plan:")
                print(self.cEP)
                print("Code: " + self.cEP_code)

            return self.cEP_id

        def Change(self, ID):
            subprocess.call(["powercfg", "/s", str(self.Plans[ID])])
        def Switch(self):
            self.getEP()
            if self.cEP_id == 0:
                self.Change(1)
            elif self.cEP_id == 1:
                self.Change(0)
            elif self.cEP_id == 2:
                self.Change(1)

    def Shutdown(self, wait=0):
        self.Run = False
        subprocess.call(["shutdown", "/s", "/f", "/t", str(wait)])
    def Sleep(self, wait=0):
        self.Run = False
        subprocess.call(["shutdown", "/h", "/t", str(wait)])
    def Reboot(self, wait=0):
        self.Run = False
        subprocess.call(["shutdown", "/r", "/t", str(wait)])

Tools = ToolsC()


def exit_now(killmex = False):
    ttime.deac()
    # noinspection PyGlobalUndefined
    global exitnow, startmain
    exitnow = 1
    startmain = False
    #if version_PC != 1:
    #    exit()

    if killmex:
        time.sleep(0.5)
        killme()

    sys.exit()