
import time
#from cls import *
import ctypes
import os
import sys
import datetime
import socket
import threading
import subprocess
import webbrowser
#from IPython.core.autocall import ExitAutocall
import shutil
import EveconExceptions
import psutil
import random
import win32process
import pyglet

#import win32api
#import win32gui
#import win32con

def cls():
    os.system("cls")


exitnow = 0
def exit_now(killmex = False):
    global ttime_stop, ttime_pause, ttime_pt
    ttime_stop = False
    ttime_pause = False
    ttime_pt = False

    ttime.deac()
    global exitnow
    exitnow = 1
    if version_PC != 1:
        exit()

    if killmex:
        time.sleep(0.5)
        killme()

    #sys.exit()

def killme():
    subprocess.call(["taskkill", "/PID", str(os.getpid())])



musicrun = False
ss_active = False
thisIP = None
StartupServer = None

cdir = os.getcwd()
os.chdir("..")
os.chdir("..")



Alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

def Log(functioni, info, typei = "Normal"):
    log_file = open("data\\Log.txt", "a+")
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


title_oldstatus = "Loading"
title_oldstart = "Error"
title_oldpc = "Error"
title_dead = False

def title(status="OLD", something="OLD", pc="OLD", deac=False):
    global title_dead
    if deac:
        title_dead = True
    global title_oldstatus, title_oldstart, title_oldpc
    if status == "OLD":
        status = title_oldstatus
    else:
        title_oldstatus = status

    if something == "OLD":
        something = title_oldstart
    else:
        title_oldstart = something

    if pc == "OLD":
        pc = title_oldpc
    else:
        title_oldpc = pc

    nowtime = datetime.datetime.now().strftime("%H:%M:%S")

    space_status = (60 - len(status) * 2) * " "
    space_pc = (64 - len(pc) * 2) * " "
    space_something = (40 - len(something) * 2) * " "
    space_time = 55 * " "

    if musicrun:
        space_status = 7 * " " # old: abs(60 - len(status) * 2 - 30)
        space_pc = 10 * " " # old: abs(64 - len(pc) * 2 - 30)
        space_something = (175 - (len(status + pc + space_status + space_pc) + round(len(something) * 1.5) + 1)) * " "
        if len(space_something) < 20:
            space_something = (160 - (len(status + pc + space_status + space_pc) + round(len(something) * 1.5) + 1)) * " "
        space_time = 1 * " "

    if not title_dead:
        ctypes.windll.kernel32.SetConsoleTitleW("EVECON: %s%s%s%s%s%s%sTime: %s" %
        (status, space_status, pc, space_pc, something, space_something, space_time, nowtime))

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
        self.path = path
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

                os.chdir(self.path)

                if switches is None:
                    command = ["7za.exe", "a", "-t" + archive_type, archive] + list(filenames)
                else:
                    command = ["7za.exe", "a", "-t" + archive_type] + list(switches) + [archive] + list(filenames)

                subprocess.call(command)

                time.sleep(0.25)
                os.chdir(dir_tmp)

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

            os.chdir(self.path)

            if switches is None:
                if output is None:
                    command = ["7za.exe", "x", archive]
                else:
                    command = ["7za.exe", "x", "-o" + output, archive]
            else:
                if output is None:
                    command = ["7za.exe", "x"] + list(switches) + [archive]
                else:
                    command = ["7za.exe", "x", "-o" + output] + list(switches) + [archive]


            subprocess.call(command)

            time.sleep(0.25)
            os.chdir(dir_tmp)
        else:
            print("error archive not found")

szip = szipC("Programs\\7z")


class MegacmdC:
    def __init__(self, path):
        self.path = path
        self.MegacmdServer = False
        self.Running = False
        self.LoggedIn = False
        self.email = None
        self.pw = None
    def __start__(self, command):
        if self.Running:
            dir_tmp = os.getcwd()
            os.chdir(self.path)
            subprocess.call(["MEGAclient.exe"] + list(command))
            time.sleep(0.25)
            os.chdir(dir_tmp)
        else:
            self.startServer()
            time.sleep(0.25)
            dir_tmp = os.getcwd()
            os.chdir(self.path)
            subprocess.call(["MEGAclient.exe"] + list(command))
            time.sleep(0.25)
            os.chdir(dir_tmp)
    def startServer(self):
        if not self.Running:
            if "MEGAcmdServer.exe" in (p.name() for p in psutil.process_iter()):
                raise EveconExceptions.MegaIsRunning(True)
            else:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                dir_tmp = os.getcwd()
                os.chdir(self.path)
                self.MegacmdServer = subprocess.Popen(["MEGAcmdServer.exe"], startupinfo=startupinfo, shell=False)
                self.Running = True
                time.sleep(1)
                os.chdir(dir_tmp)

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


def title_time_now():
    return datetime.datetime.now().strftime("%H:%M:%S")

title("Loading Light")

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


title("Loading Title Time")


class title_time(threading.Thread):

    def __init__(self, freq):
        threading.Thread.__init__(self)
        self.stop = 0
        self.freq = freq

    def run(self):
        global ttime_stop, ttime_pause, ttime_pt
        ttime_pause = True
        ttime_stop = True
        ttime_pt = False
        while ttime_stop:
            while ttime_pause:
                title()
                # wenn man hier kein old title mitgibt geht es nicht! warum? Versuch lösche über mir weg
                time.sleep(self.freq)
            time.sleep(0.1)
            while ttime_pt:
                first = time.time()
                pausetime = 180
                while ttime_pt:
                    time.sleep(0.25)

                    if (round(time.time() - first) % 60) < 10 :
                        sstime = str(round(time.time() + pausetime - first) // 60) + ":0" + str(round(time.time() + pausetime - first) % 60)
                    else:
                        sstime = str(round(time.time() + pausetime - first) // 60) + ":" + str(round(time.time() + pausetime - first) % 60)

                    title("OLD", "OLD", sstime)


    def deac(self):
        global ttime_stop, ttime_pause
        ttime_pause = False
        ttime_stop = False
    def pt(self):
        global ttime_stop, ttime_pause, ttime_pt
        if ttime_pt:
            ttime_pause = True
            ttime_pt = False
        else:
            ttime_pause = False
            ttime_pt = True


ttime = title_time(2.5)
ttime.start()

def killConsole():
    ttime.deac()
    title(deac=True)
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(hwnd, 0)

    # Why?
    ctypes.windll.kernel32.CloseHandle(hwnd)
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    #print(pid)
    #os.system('taskkill /PID ' + str(pid) + ' /f')
    #input()

    # tmp:
    #subprocess.call(["taskkill", "/IM", "conhost.exe", "/f"])

title("Loading: Finding Computers")


def computerconfig_schoolpc():
    color.change("F0")

def computerconfig_minipc():
    global MusicDir, thisIP
    MusicDir = "C:\\Users\\Mini-Pc Nutzer\\Desktop\\Musik\\Musik\\!Fertige Musik"
    thisIP = "192.168.2.102"



def computerconfig_bigpc():
    global thisIP
    thisIP = "192.168.2.101"


def computerconfig_aldi():
    nircmd("setsize", 1000, 520)


def computerconfig_laptop():
    global thisIP
    thisIP = "192.168.2.106" # Lan .104 = WLAN


Computername = socket.gethostname()

if Computername[0] == "P":
    if os.environ.get("USERNAME") == "NEUHOF":
        if os.getlogin() == "albingerl":
            title("OLD", "OLD", "albingerl@SchoolPC")
            Computerfind_SchoolPC_alb = 1
            Computerfind_SchoolPC = 1
            computerconfig_schoolpc()
        else:
            Computerfind_SchoolPC_alb = 0
            Computerfind_SchoolPC = 1
            computerconfig_schoolpc()
    else:
        Computerfind_SchoolPC_alb = 0
        Computerfind_SchoolPC = 0
else:
    Computerfind_SchoolPC_alb = 0
    Computerfind_SchoolPC = 0

if Computername == "Computer-Testet":
    title("OLD", "OLD", "somebody@Mini-PC")
    Computerfind_MiniPC = 1
    Computerfind_BigPC = 0
    Computerfind_PapaAldi = 0
    Computerfind_Laptop = 0
    computerconfig_minipc()

    HomePC = True

elif Computername == "XX":  # Todo BIG PC EINFÜGEN
    title("OLD", "OLD", "somebody@BigPC")
    Computerfind_MiniPC = 0
    Computerfind_BigPC = 1
    Computerfind_PapaAldi = 0
    Computerfind_Laptop = 0
    computerconfig_bigpc()

    HomePC = True

elif Computername == "Test":
    title("OLD", "OLD", "somebody@Aldi-Laptop")
    Computerfind_MiniPC = 0
    Computerfind_BigPC = 0
    Computerfind_PapaAldi = 1
    Computerfind_Laptop = 0
    computerconfig_aldi()

elif Computername == "Luis":
    title("OLD", "OLD", "somebody@Luis-Laptop")
    Computerfind_MiniPC = 0
    Computerfind_BigPC = 0
    Computerfind_PapaAldi = 0
    Computerfind_Laptop = 1
    computerconfig_laptop()

else:
    title("OLD", "OLD", "No Computer found")
    Computerfind_MiniPC = 0
    Computerfind_BigPC = 0
    Computerfind_PapaAldi = 0
    Computerfind_Laptop = 0


file_proversion_raw = open("data\\Info\\ProgramVersion", "r")
ProVersion = file_proversion_raw.readline()
file_proversion_raw.close()


def normaltitle():
    global ss_active
    if ss_active:
        title("Screensaver", "")
    else:
        if ProVersion == "PC-Version":
            title("OLD", "PC-Version")

        elif ProVersion == "MainStick-Version":
            title("OLD", "Stick-Version")
        elif ProVersion == "MiniStick-Version":
            title("OLD", "Stick-Version")
        else:
            title("OLD", "OLD")

normaltitle()

if ProVersion == "PC-Version":
    if Computerfind_MiniPC == 1:
        normaltitle()
        version_PC = 1
        version_MiniPC = 1
        version_BigPC = 0
        version_MainStick = 0
        version_MiniStick = 0
    if Computerfind_BigPC == 1:
        normaltitle()
        version_PC = 1
        version_MiniPC = 0
        version_BigPC = 1
        version_MainStick = 0
        version_MiniStick = 0
elif ProVersion == "MainStick-Version":
    normaltitle()
    version_PC = 0
    version_MiniPC = 0
    version_BigPC = 0
    version_MainStick = 1
    version_MiniStick = 0
elif ProVersion == "MiniStick-Version":
    normaltitle()
    version_PC = 0
    version_MiniPC = 0
    version_BigPC = 0
    version_MainStick = 0
    version_MiniStick = 1
else:
    title("Loading")
    version_PC = 0
    version_MiniPC = 0
    version_BigPC = 0
    version_MainStick = 0
    version_MiniStick = 0


from win32api import *
from win32gui import *
import win32con


class WindowsBalloonTip:
    def __init__(self, title, msg):
        message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map  # could also specify a wndproc.
        classAtom = RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow(classAtom, "Taskbar", style, 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join(sys.path[0], "balloontip.ico"))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            hicon = LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO, win32con.WM_USER + 20, hicon, "Balloon  tooltip", msg, 200, title))
        # self.show_balloon(title, msg)
        time.sleep(10)
        DestroyWindow(self.hwnd)
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.

def balloon_tip(title, msg):
    class tip(threading.Thread):
        def run(self):
            w = WindowsBalloonTip(title, msg)
    tipp = None
    tipp = tip()
    tipp.start()



title("Load first Programs")

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

class ServerC:
    def __init__(self, host, port, reac = None, reacSendData = False, mess = False):
        super().__init__()
        self.host = host
        self.port = port
        self.Running = False
        self.Connected = False
        self.End = False
        self.allDataSend = []
        self.allDataRec = []
        self.s = socket.socket()
        self.conAddress = None
        self.con = None

        self.mess = mess
        self.reac = reac
        self.reacSData = reacSendData

    def start(self):
        self.run()
    def stop(self):
        self.Running = False
        self.End = True
        self.Connected = False
        self.con.close()
    def send(self, data):
        if self.Running and self.Connected and not self.End:
            if type(data) == str:
                data = data.encode()
            elif type(data) == int:
                data = str(data).encode()
            self.con.send(data)
            self.allDataSend.append(data)
    def react(self, curData):
        if self.reac is not None:
            if self.reacSData:
                self.reac(curData)
            else:
                self.reac()
    def run(self):
        self.Running = True
        self.bind()
        while self.Running:
            self.s.listen(1)
            self.con, self.conAddress = self.s.accept()
            self.Connected = True
            print("Connected with", self.conAddress)
            balloon_tip("Coonected", "Connected with " + str(self.conAddress[0]))
            while self.Connected:
                try:
                    data = self.con.recv(1024)
                except ConnectionResetError:
                    self.Connected = False
                    break
                if not data:
                    break
                self.allDataRec.append(data)
                self.react(data)
                if data == b"stop_server" or data == b"stopserver":
                    self.Connected = False
                    self.Running = False
            print("Disconneted")
            balloon_tip("Disconneted", "Connected fron " + str(self.conAddress[0]))

        self.stop()

    def bind(self):
        self.s.bind((self.host, self.port))

class ServerThC(threading.Thread):
    def __init__(self, host, port, reac = None, reacSendData = False, mess = False):
        super().__init__()
        self.host = host
        self.port = port
        self.Running = False
        self.Connected = False
        self.End = False
        self.allDataSend = []
        self.allDataRec = []
        self.s = socket.socket()
        self.conAddress = None
        self.con = None

        self.mess = mess
        self.reac = reac
        self.reacSData = reacSendData

    def stop(self):
        self.Running = False
        self.End = True
        self.Connected = False
        self.con.close()
    def send(self, data):
        if self.Running and self.Connected and not self.End:
            if type(data) == str:
                data = data.encode()
            elif type(data) == int:
                data = str(data).encode()
            self.con.send(data)
            self.allDataSend.append(data)
    def react(self, curData):
        if self.reac is not None:
            if self.reacSData:
                self.reac(curData)
            else:
                self.reac()
    def run(self):
        self.Running = True
        self.bind()
        while self.Running:
            self.s.listen(1)
            self.con, self.conAddress = self.s.accept()
            self.Connected = True
            print("Connected with", self.conAddress)
            balloon_tip("Coonected", "Connected with " + str(self.conAddress[0]))
            while self.Connected:
                try:
                    data = self.con.recv(1024)
                except ConnectionResetError:
                    self.Connected = False
                    break
                if not data:
                    break
                self.allDataRec.append(data)
                self.react(data)
            print("Disconneted")
            balloon_tip("Disconneted", "Connected fron " + str(self.conAddress[0]))

        self.stop()

    def bind(self):
        self.s.bind((self.host, self.port))


class ClientC(threading.Thread):
    def __init__(self, host, port, reac=None, reacSendData=False):
        super().__init__()
        self.host = host
        self.port = port
        self.Running = False
        self.Connected = False
        self.End = False
        self.allDataSend = []
        self.allDataRec = []
        self.s = socket.socket()

        self.reac = reac
        self.reacSData = reacSendData

    def stop(self):
        self.Running = False
        self.End = True
        self.Connected = False
        self.s.close()

    def send(self, data):
        if self.Running and self.Connected and not self.End:
            if type(data) == str:
                data = data.encode()
            elif type(data) == int:
                data = str(data).encode()
            self.s.send(data)
            self.allDataSend.append(data)

    def react(self, curData):
        if self.reac is not None:
            if self.reacSData:
                self.reac(curData)
            else:
                self.reac()

    def run(self):
        self.Running = True
        self.connect()
        data = None
        if self.Connected:
            while self.Running:
                try:
                    data = self.s.recv(1024)
                except ConnectionResetError:
                    self.Running = False

                self.allDataRec.append(data)
                self.react(data)

        self.stop()

    def connect(self):
        try:
            self.s.connect((self.host, self.port))
            print("Connected")
        except TimeoutError:
            # wrong ip
            return False
        except ConnectionRefusedError:
            # wrong port
            return False

        self.Connected = True
        return True

def InteractiveClient(host, port):
    def x(data):
        print("[Server] " + data.decode())

    cl = ClientC(host, port, x, True)
    cl.start()

    x = input("-> ")
    while x != "q":
        cl.send(x)
        x = input("-> ")

    cl.stop()

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
                    pass
                    if searchlist[sListNum][keyNum + letterNum] == searchkey[keyNum]:
                        if keyNum == len(searchkey) - 1:
                            OutputNum.append(sListNum)
                            break
                    else:
                        break

                break

    return OutputNum

def StartupServerTasks(data_un):
    data = data_un.decode("utf-8")
    global SST_mp, SST_mp_Ac, StartupServer

    if data == "shutdown":
        print("Evecon Server", "Shutdown")
        #balloon_tip("Evecon Server", "Shutdown")
        Tools.Shutdown()
    elif data == "sleep":
        print("Evecon Server", "sleep")
        #balloon_tip("Evecon Server", "sleep")
        Tools.Sleep()
    elif data == "ep_energysave":
        print("Evecon Server", "ep_energysave")
        #balloon_tip("Evecon Server", "ep_energysave")
        Tools.EnergyPlan.Change(1)
    elif data == "reboot":
        print("Evecon Server", "reboot")
        #balloon_tip("Evecon Server", "reboot")
        Tools.Reboot()
    elif data == "mp_setup":
        print("Evecon Server", "mp_setup")
        #balloon_tip("Evecon Server", "mp_setup")
        SST_mp = MusicPlayerC()
        SST_mp_Ac = True
    elif data[0] == "m" and data[1] == "p" and data[2] == "_" and data[3] == "a" and data[4] == "d" and data[5] == "d" and SST_mp_Ac:
        print("Evecon Server", "mp_add " + data.lstrip("mp_").lstrip("add").lstrip("_"))
        #balloon_tip("Evecon Server", "mp_add " + data.lstrip("mp_add_"))
        x = SST_mp.addMusic(data.lstrip("mp_").lstrip("add").lstrip("_"))
        if x:
            StartupServer.send("Done Loading")
        else:
            StartupServer.send("Error")
    elif data == "mp_start" and SST_mp_Ac:
        print("Evecon Server", "mp_start")
        #balloon_tip("Evecon Server", "mp_start")
        SST_mp.start()
    elif data == "mp_stop" and SST_mp_Ac:
        print("Evecon Server", "mp_stop")
        #balloon_tip("Evecon Server", "mp_stop")
        SST_mp.Stop()
    elif data == "mp_getsong" and SST_mp_Ac:
        StartupServer.send(SST_mp.musiclistname[SST_mp.thismusicnumber])

def np(preset="Man"):
    title("Loading Notepad")

    def shota():
        file_shota_raw = open("data\\Notepad\\Notiespez\\NotieFoxishota.txt", "r")
        file_shota = []
        for y in file_shota_raw:
            file_shota.append(y.strip())
        file_shota_raw.close()

        for y in range(len(file_shota)):  # Open in Browser
            if y == 0:
                if "firefox.exe" in (p.name() for p in psutil.process_iter()):
                    dir_tmp = os.getcwd()
                    os.chdir("C:\\Program Files\\Mozilla Firefox")
                    subprocess.call(["firefox.exe", "-new-window", file_shota[y]])
                    time.sleep(0.25)
                    os.chdir(dir_tmp)
                    continue
                else:
                    webbrowser.open(file_shota[y])
            time.sleep(2.5)
            webbrowser.open(file_shota[y])

    def now():
        cls()
        now_name = input("Name:\n\n")
        cls()
        now_name_link = input("Name (Link):\n\n")
        cls()
        now_page = input("Page:\n\n")
        cls()

        file_counter_raw = open("data\\Notepad\\Notiespez\\NotieCounter.txt", "r")
        file_counter_old = file_counter_raw.readline()
        file_counter_raw.close()
        file_counter_raw = open("data\\Notepad\\Notiespez\\NotieCounter.txt", "w")
        file_counter = int(file_counter_old) + 1
        file_counter_raw.write(str(file_counter))
        file_counter_raw.close()

        file_oldpage_raw = open("data\\Notepad\\Notiespez\\NotieFoxiNOWpage.txt", "r")
        file_oldpage = file_oldpage_raw.readline()
        pagedif = int(file_oldpage) - int(now_page)
        file_oldpage_raw.close()

        file_counterext_raw = open("data\\Notepad\\Notiespez\\Notiecounterlog.txt", "a+")
        file_counterext_raw.write(
            "       %s         %s                   %s                     %s                %s    %s" % (
            str(file_counter), str(file_oldpage), str(now_page), str(pagedif),
            datetime.datetime.now().strftime("%d.%m.%Y"), datetime.datetime.now().strftime("%H:%M")))
        file_counterext_raw.close()

        file_name_raw = open("data\\Notepad\\Notiespez\\NotieFoxiNOWname.txt", "w")
        file_name_raw.write(now_name)
        file_name_raw.close()

        file_name_raw = open("data\\Notepad\\Notiespez\\NotieFoxiNOWnamelink.txt", "w")
        file_name_raw.write(now_name_link)
        file_name_raw.close()

        file_name_raw = open("data\\Notepad\\Notiespez\\NotieFoxiNOWpage.txt", "w")
        file_name_raw.write(now_page)
        file_name_raw.close()

        file_name_raw = open("data\\Notepad\\Notiespez\\NotieFoxiNOWpagelink.txt", "w")
        file_name_raw.write("https://hentaifox.com/pag/%s/" % now_page)
        file_name_raw.close()

    def fox():

        file_foxpage_raw = open("data\\Notepad\\Notiespez\\NotieFoxinowpagelink.txt", "r")
        file_foxpage = file_foxpage_raw.readline()
        file_foxpage_raw.close()

        file_foxname_raw = open("data\\Notepad\\Notiespez\\NotieFoxinownamelink.txt", "r")
        file_foxname = file_foxname_raw.readline()
        file_foxname_raw.close()

        if "firefox.exe" in (p.name() for p in psutil.process_iter()):
            dir_tmp = os.getcwd()
            os.chdir("C:\\Program Files\\Mozilla Firefox")
            subprocess.call(["firefox.exe", "-url", file_foxpage, file_foxname])
            time.sleep(0.25)
            os.chdir(dir_tmp)
        else:
            webbrowser.open(file_foxpage)
            time.sleep(5)
            webbrowser.open(file_foxname)

    def foxname():

        file_foxname_raw = open("data\\Notepad\\Notiespez\\NotieFoxinownamelink.txt", "r")
        file_foxname = file_foxname_raw.readline()
        file_foxname_raw.close()

        if "firefox.exe" in (p.name() for p in psutil.process_iter()):
            dir_tmp = os.getcwd()
            os.chdir("C:\\Program Files\\Mozilla Firefox")
            subprocess.call(["firefox.exe", "-new-window", file_foxname])
            time.sleep(0.25)
            os.chdir(dir_tmp)
        else:
            webbrowser.open(file_foxname)

    def foxpage():

        file_foxpage_raw = open("data\\Notepad\\Notiespez\\NotieFoxinowpagelink.txt", "r")
        file_foxpage = file_foxpage_raw.readline()
        file_foxpage_raw.close()

        if "firefox.exe" in (p.name() for p in psutil.process_iter()):
            dir_tmp = os.getcwd()
            os.chdir("C:\\Program Files\\Mozilla Firefox")
            subprocess.call(["firefox.exe", "-new-window", file_foxpage])
            time.sleep(0.25)
            os.chdir(dir_tmp)
        else:
            webbrowser.open(file_foxpage)

    def gr():
        new_name = input("What do you want to add?")
        file_gr = open("data\\Notepad\\Notiespez\\NotieFoxigoodread.txt", "a+")
        file_gr.write(new_name)
        file_gr.close()

    def gnr():
        new_name = input("What do you want to add?")
        file_gnr = open("data\\Notepad\\Notiespez\\NotieFoxigoodnotread.txt", "a+")
        file_gnr.write(new_name)
        file_gnr.close()

    def lr():
        new_name = input("What do you want to add?")
        file_lr = open("data\\Notepad\\Notiespez\\NotieFoxilongread.txt", "a+")
        file_lr.write(new_name)
        file_lr.close()

    def lnr():
        new_name = input("What do you want to add?")
        file_lnr = open("data\\Notepad\\Notiespez\\NotieFoxilongnotread.txt", "a+")
        file_lnr.write(new_name)
        file_lnr.close()

    def counter():
        file_counter_raw = open("data\\Notepad\\Notiespez\\NotieCounter.txt", "r")
        file_counter = file_counter_raw.readline()
        file_counter_raw.close()
        cls()
        print("You have %s flaps! Nice!\n" % file_counter)
        np_ex = input("Extended?\n")
        if np_ex.lower() == "y":
            cls()
            file_counterex_raw = open("data\\Notepad\\Notiespez\\Notiecounterlog.txt", "r")
            file_counterex_list = []
            for x in file_counterex_raw:
                file_counterex_list.append(x.strip())
            file_counterex_raw.close()
            for x in file_counterex_list:
                print(x)
            input()

    def count():
        file_counter_raw = open("data\\Notepad\\Notiespez\\NotieCounter.txt", "r")
        file_counter_old = file_counter_raw.readline()
        file_counter_raw.close()
        file_counter_raw = open("data\\Notepad\\Notiespez\\NotieCounter.txt", "w")
        file_counter = int(file_counter_old) + 1
        file_counter_raw.write(str(file_counter))
        file_counter_raw.close()

        file_counterext_raw = open("data\\Notepad\\Notiespez\\Notiecounterlog.txt", "a+")
        file_counterext_raw.write(
            "       %s         %s                   %s                     %s                %s    %s\n" % (
            str(file_counter), "un", "un", "un", datetime.datetime.now().strftime("%d.%m.%Y"),
            datetime.datetime.now().strftime("%H:%M")))
        file_counterext_raw.close()

    if preset == "shota":
        shota()
    if preset == "now":
        now()
    if preset == "fox":
        fox()
    if preset == "foxpage":
        foxpage()
    if preset == "foxname":
        foxname()
    if preset == "Man":

        file_foxname_raw = open("data\\Notepad\\Notiespez\\NotieFoxinowname.txt", "r")
        file_foxname = file_foxname_raw.readline()
        file_foxname_raw.close()

        file_foxpage_raw = open("data\\Notepad\\Notiespez\\NotieFoxinowpage.txt", "r")
        file_foxpage = file_foxpage_raw.readline()
        file_foxpage_raw.close()

        file_gr_raw = open("data\\Notepad\\Notiespez\\NotieFoxigoodread.txt", "r")
        file_gr_list = []
        for x in file_gr_raw:
            file_gr_list.append(x.strip())
        file_gr_raw.close()

        file_gnr_raw = open("data\\Notepad\\Notiespez\\NotieFoxigoodnotread.txt", "r")
        file_gnr_list = []
        for x in file_gnr_raw:
            file_gnr_list.append(x.strip())
        file_gnr_raw.close()

        file_lr_raw = open("data\\Notepad\\Notiespez\\NotieFoxilongread.txt", "r")
        file_lr_list = []
        for x in file_lr_raw:
            file_lr_list.append(x.strip())
        file_lr_raw.close()

        file_lnr_raw = open("data\\Notepad\\Notiespez\\NotieFoxilongnotread.txt", "r")
        file_lnr_list = []
        for x in file_lnr_raw:
            file_lnr_list.append(x.strip())
        file_lnr_raw.close()

        cls()
        print("Notie\n the best Notepad\n")
        print("Foxi:\n")
        print("You read: '%s' at the page '%s'\n" % (file_foxname, file_foxpage))

        print("Too good:\n\n")
        print("You read: (GR)\n")
        for x in file_gr_list:
            print(x)
        print("\nYou have not read: (GNR)\n")
        for x in file_gnr_list:
            print(x)

        print("\nToo long:\n\n")
        print("You read: (LNR)\n")
        for x in file_lr_list:
            print(x)
        print("\nYou have not read: (LNR)\n")
        for x in file_lnr_list:
            print(x)

        np_user_input = input("\n\nWhat to do now?\n\n")

        if np_user_input.lower() == "shota":
            shota()
        if np_user_input.lower() == "now":
            now()
        if np_user_input.lower() == "fox":
            fox()
        if np_user_input.lower() == "foxpage":
            foxpage()
        if np_user_input.lower() == "foxname":
            foxname()
        if np_user_input.lower() == "gr":
            gr()
        if np_user_input.lower() == "gnr":
            gnr()
        if np_user_input.lower() == "lr":
            lr()
        if np_user_input.lower() == "lnr":
            lnr()
        if np_user_input.lower() == "count":
            count()
        if np_user_input.lower() == "counter":
            counter()



title("Loading Arguments")

def Evecons(findversions=0):
    global Evecons_multi, Evecons_mainstick, Evecons_mainstick_path, Evecons_mainstick_pathkey, Evecons_PC, Evecons_PC_path, Evecons_ministick, Evecons_ministick_path, Evecons_ministick_pathkey
    global version_PC, version_MiniPC, version_BigPC, version_MainStick, version_MiniStick
    global mainstickversion, ministickversion, PCversion

    Eveconss = []
    Evecons_multi = 0
    Evecons_mainstick = 0
    Evecons_mainstick_path = 0
    Evecons_mainstick_pathkey = 0
    Evecons_PC = 0

    mainstickversion = []
    ministickversion = []
    PCversion = []

    if os.path.isfile("C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\data\\Info\\exist"):
        Evecons_PC_path = "C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon"
    elif  os.path.isfile(""):   # BigPC noch einfügen
        Evecons_PC_path = ""
    Evecons_ministick = 0
    Evecons_ministick_path = 0
    Evecons_ministick_pathkey = 0

    for Alpha in Alphabet:
        if os.path.isfile("%s:\\Evecon\\data\\Info\\exist" % Alpha):
            file_proversionstick_raw = open("data\\Info\\ProgramVersion", "r")
            proversionunkownstick = file_proversionstick_raw.readline()
            file_proversionstick_raw.close()

            if proversionunkownstick == "MainStick-Version" and version_MainStick == 0:

                Eveconss.append("MainStick")
                Evecons_mainstick = 1
                Evecons_mainstick_pathkey = Alpha
                Evecons_mainstick_path = ("%s:\\Evecon" % Alpha)

                def mainstick_version():
                    file_mainstick_version_raw = open("%s:\\Evecon\\data\\Info\\version" % Evecons_mainstick_pathkey, "r")

                    for x in file_mainstick_version_raw:
                        mainstickversion.append(x.strip())
                    file_mainstick_version_raw.close()

                if findversions == 1:
                    mainstick_version()

            elif proversionunkownstick == "MiniStick-Version" and version_MiniStick == 0:

                Eveconss.append("MiniStick")
                Evecons_ministick = 1
                Evecons_ministick_pathkey = Alpha
                Evecons_ministick_path = ("%s:\\Evecon" % Alpha)

                def ministick_version():
                    file_ministick_version_raw = open("%s:\\Evecon\\data\\Info\\version" % Evecons_ministick_pathkey, "r")

                    for x in file_ministick_version_raw:
                        ministickversion.append(x.strip())
                    file_ministick_version_raw.close()

                if findversions == 1:
                    ministick_version()

    if version_MainStick == 1:
        if os.path.isfile("C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\data\\Info\\exist"):

            Eveconss.append("PC")
            Evecons_PC = 1

            def pc_version():
                file_pc_version_raw = open("C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\data\\Info\\version", "r")

                for x in file_pc_version_raw:
                    PCversion.append(x.strip())
                file_pc_version_raw.close()

            if findversions == 1:
                pc_version()

        elif os.path.isfile(""):  # BigPC einfügen

            Eveconss.append("PC")
            Evecons_PC = 1

            def pc_version():
                file_pc_version_raw = open("", "r") # BigPC einfügen
                for x in file_pc_version_raw:
                    PCversion.append(x.strip())
                file_pc_version_raw.close()

            if findversions == 1:
                pc_version()

    if version_MiniStick == 1:
        if os.path.isfile("C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\data\\Info\\exist"):

            Eveconss.append("PC")
            Evecons_PC = 1

            def pc_version():
                file_pc_version_raw = open("C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\data\\Info\\version", "r")
                for x in file_pc_version_raw:
                    PCversion.append(x.strip())
                file_pc_version_raw.close()

            if findversions == 1:
                pc_version()

        elif os.path.isfile(""): # BigPC einfügen

            Eveconss.append("PC")
            Evecons_PC = 1

            def pc_version():
                file_pc_version_raw = open("", "r")
                for x in file_pc_version_raw:
                    PCversion.append(x.strip())
                    file_pc_version_raw.close()

            if findversions == 1:
                pc_version()


    if len(Eveconss) >= 2:
        Evecons_multi = 1


def version():
    file_version_raw = open("data\\Info\\version", "r")
    global this_version
    this_version = []
    for x in file_version_raw:
        this_version.append(x.strip())
    file_version_raw.close()


def update():
    version()
    global this_version
    Evecons(1)
    global mainstickversion, ministickversion, PCversion
    global Evecons_multi, Evecons_mainstick, Evecons_PC, Evecons_ministick
    if Evecons_multi == 0:
        if Evecons_PC == 1:
            if this_version[0] > PCversion[0]:
                title("Updating another Program")
                dir_tmp = os.getcwd()
                os.chdir("Programs\\Evecon\\Updater")
                subprocess.call(["updater.exe", "-update"])
                time.sleep(0.25)
                os.chdir(dir_tmp)
            elif this_version[0] < PCversion[0]:
                title("Updating this Program", "Closing")
                dir_tmp = os.getcwd()
                os.chdir("Programs\\Evecon\\Updater")
                subprocess.call(["updater.exe", "-update"])
                time.sleep(0.25)
                os.chdir(dir_tmp)
                exit_now()
        elif Evecons_mainstick == 1:
            if this_version[0] > mainstickversion[0]:
                title("Updating another Program")
                dir_tmp = os.getcwd()
                os.chdir("Programs\\Evecon\\Updater")
                subprocess.call(["updater.exe", "-update"])
                time.sleep(0.25)
                os.chdir(dir_tmp)
            elif this_version[0] < mainstickversion[0]:
                title("Updating this Program", "Closing")
                dir_tmp = os.getcwd()
                os.chdir("Programs\\Evecon\\Updater")
                subprocess.call(["updater.exe", "-update"])
                time.sleep(0.25)
                os.chdir(dir_tmp)
                exit_now()
        elif Evecons_ministick == 1:
            if this_version[0] > ministickversion[0]:
                title("Updating another Program")
                dir_tmp = os.getcwd()
                os.chdir("Programs\\Evecon\\Updater")
                subprocess.call(["updater.exe", "-update"])
                time.sleep(0.25)
                os.chdir(dir_tmp)
            elif this_version[0] < ministickversion[0]:
                title("Updating this Program", "Closing")
                dir_tmp = os.getcwd()
                os.chdir("Programs\\Evecon\\Updater")
                subprocess.call(["updater.exe", "-update"])
                time.sleep(0.25)
                os.chdir(dir_tmp)
                exit_now()
    else:                                   # Wenn mehr als drei Programme gleichzeitig dies umprogrammieren!
        if version_PC == 1:
            if mainstickversion[0] > ministickversion[0]:
                highestversion = mainstickversion[0]
                mustupdateanother = 1
            elif mainstickversion[0] < ministickversion[0]:
                highestversion = ministickversion[0]
                mustupdateanother = 1
            else:
                highestversion = mainstickversion[0]
                mustupdateanother = 0

            if this_version[0] > highestversion:
                title("Updating other Programs")
                dir_tmp = os.getcwd()
                os.chdir("Programs\\Evecon\\Updater")
                subprocess.call(["updater.exe", "-update"])
                time.sleep(0.25)
                os.chdir(dir_tmp)
            elif this_version[0] < highestversion:
                title("Updating this Program", "Closing")
                dir_tmp = os.getcwd()
                os.chdir("Programs\\Evecon\\Updater")
                subprocess.call(["updater.exe", "-update"])
                time.sleep(0.25)
                os.chdir(dir_tmp)
                exit_now()
            elif this_version[0] == highestversion:
                if mustupdateanother == 1:
                    title("Updating another Program")
                    dir_tmp = os.getcwd()
                    os.chdir("Programs\\Evecon\\Updater")
                    subprocess.call(["updater.exe", "-update"])
                    time.sleep(0.25)
                    os.chdir(dir_tmp)
        elif version_MainStick == 1:
            if PCversion[0] > ministickversion[0]:
                highestversion = PCversion[0]
                mustupdateanother = 1
            elif PCversion[0] < ministickversion[0]:
                highestversion = ministickversion[0]
                mustupdateanother = 1
            else:
                highestversion = PCversion[0]
                mustupdateanother = 0

            if this_version[0] > highestversion:
                title("Updating other Programs")
                dir_tmp = os.getcwd()
                os.chdir("Programs\\Evecon\\Updater")
                subprocess.call(["updater.exe", "-update"])
                time.sleep(0.25)
                os.chdir(dir_tmp)
            elif this_version[0] < highestversion:
                title("Updating this Program", "Closing")
                dir_tmp = os.getcwd()
                os.chdir("Programs\\Evecon\\Updater")
                subprocess.call(["updater.exe", "-update"])
                time.sleep(0.25)
                os.chdir(dir_tmp)
                exit_now()
            elif this_version[0] == highestversion:
                if mustupdateanother == 1:
                    title("Updating another Program")
                    dir_tmp = os.getcwd()
                    os.chdir("Programs\\Evecon\\Updater")
                    subprocess.call(["updater.exe", "-update"])
                    time.sleep(0.25)
                    os.chdir(dir_tmp)
        elif version_MiniStick == 1:
            if PCversion[0] > mainstickversion[0]:
                highestversion = PCversion[0]
                mustupdateanother = 1
            elif PCversion[0] < mainstickversion[0]:
                highestversion = mainstickversion[0]
                mustupdateanother = 1
            else:
                highestversion = PCversion[0]
                mustupdateanother = 0

            if this_version[0] > highestversion:
                title("Updating other Programs")
                dir_tmp = os.getcwd()
                os.chdir("Programs\\Evecon\\Updater")
                subprocess.call(["updater.exe", "-update"])
                time.sleep(0.25)
                os.chdir(dir_tmp)
            elif this_version[0] < highestversion:
                title("Updating this Program", "Closing")
                dir_tmp = os.getcwd()
                os.chdir("Programs\\Evecon\\Updater")
                subprocess.call(["updater.exe", "-update"])
                time.sleep(0.25)
                os.chdir(dir_tmp)
                exit_now()
            elif this_version[0] == highestversion:
                if mustupdateanother == 1:
                    title("Updating another Program")
                    dir_tmp = os.getcwd()
                    os.chdir("Programs\\Evecon\\Updater")
                    subprocess.call(["updater.exe", "-update"])
                    time.sleep(0.25)
                    os.chdir(dir_tmp)

def upgrade():
    title("Updating this Program", "")
    dir_tmp = os.getcwd()
    os.chdir("Programs\\Evecon\\Updater")
    subprocess.call(["updater.exe", "-upgrade"])

    exit_now()



def debug():
    cls()
    while True:
        exec(input())



def games(preset="Man"):


    def snake():
        import random, click

        global nothing, me, food, max_x, max_y, lastthing, Title_run, lockMe, test, testx, testy, ttime_stop, paused, Thingyou, Things, now, special, direction, sleep, restart

        nothing = " "
        me = "X"
        food = "O"
        max_x = 120
        max_y = 30
        ttime_stop = False

        global Titledeac

        Titledeac = False

        for testy in range(1, max_y):
            for testx in range(1, max_x):
                exec("global pos%s_%s; pos%s_%s = '%s'" % (testx, testy, testx, testy, nothing))


        exec("pos%s_%s = '%s'" % (int(max_x / 2), int(max_y / 2), me))
        now = {"x": int(max_x / 2), "y": int(max_y / 2)}
        lastthing = {"x": int(max_x / 2), "y": int(max_y / 2)}
        direction = "up"
        sleep = 0.2
        restart = True


        class Titleclass(threading.Thread):

            def run(self):
                global Title_run, nowtime, beginn, score, moves, Things
                Title_run = False

                while True:

                    Title_run = False
                    nowtime = 0
                    beginn = time.time()
                    score = 0
                    ctypes.windll.kernel32.SetConsoleTitleW("Snake: Time: %s    Score: %s" %
                                                            (nowtime, score))
                    while not Title_run:
                        time.sleep(0.5)
                    beginn = time.time()
                    time.sleep(0.25)
                    while Title_run:
                        while not paused:
                            nowtime = int(time.time()) - int(beginn)
                            score = moves * 50 + (Things - 1) * 1000

                            ctypes.windll.kernel32.SetConsoleTitleW("Snake: Time: %s    Score: %s" %
                                                                    (nowtime, score))
                            time.sleep(0.5)
                        time.sleep(0.5)
                        beginn += 0.5


        if not Titledeac:
            titles = Titleclass()
            titles.start()


        class Direc(threading.Thread):

            def run(self):
                while True:
                    first = click.getchar()
                    time.sleep(0.01)
                    second = click.getchar()
                    global direction
                    if first == b'\xe0':
                        if second == b'H':
                            if direction != "down":
                                direction = "up"
                        elif second == b'P':
                            if direction != "up":
                                direction = "down"
                        elif second == b'M':
                            if direction != "left":
                                direction = "right"
                        elif second == b'K':
                            if direction != "right":
                                direction = "left"
                    if first == b'W':
                        if direction != "down":
                            direction = "up"
                    elif first == b'S':
                        if direction != "up":
                            direction = "down"
                    elif first == b'D':
                        if direction != "left":
                            direction = "right"
                    elif first == b'A':
                        if direction != "right":
                            direction = "left"
                    elif first == b' ':
                        direction = "wait"


        direct = Direc()
        direct.start()

        global Thing

        class Thing:
            def __init__(self, beforex, beforey):
                global OurThing
                #	exec("global pos%s_%s; pos%s_%s = '%s'" % (abs(beforex), abs(beforey), abs(beforex), abs(beforey), me))
                self.lastdirection = "wait"
                self.beforex = beforex
                self.beforey = beforey
                OurThing.append("")


            def move(self, thisdirect):  # braucht mann nowx und nowy?
                global Thingyou, Things, lastthing
                temp = False
                if self.lastdirection == "wait":
                    exec("global pos%s_%s; pos%s_%s = '%s'" % (self.beforex, self.beforey, self.beforex, self.beforey, me))
                    lastthing['x'] = self.beforex
                    lastthing['y'] = self.beforey
                elif self.lastdirection == "up":
                    self.beforey -= 1
                    exec("global pos%s_%s; pos%s_%s = '%s'" % (
                    self.beforex, self.beforey, self.beforex, self.beforey, me))  # hier werte überprüfen
                    OurThing[Thingyou] = ("pos%s_%s" % (self.beforex, self.beforey))
                    if Things > Thingyou:
                        Thingyou += 1
                        exec("Thing%s.move('up')" % Thingyou)
                    else:
                        lastthing['x'] = self.beforex
                        lastthing['y'] = self.beforey

                elif self.lastdirection == "down":
                    self.beforey += 1
                    exec("global pos%s_%s; pos%s_%s = '%s'" % (self.beforex, self.beforey, self.beforex, self.beforey, me))
                    OurThing[Thingyou] = ("pos%s_%s" % (self.beforex, self.beforey))
                    if Things > Thingyou:
                        Thingyou += 1
                        exec("Thing%s.move('down')" % Thingyou)
                    else:
                        lastthing['x'] = self.beforex
                        lastthing['y'] = self.beforey

                elif self.lastdirection == "right":
                    self.beforex += 1
                    exec("global pos%s_%s; pos%s_%s = '%s'" % (self.beforex, self.beforey, self.beforex, self.beforey, me))
                    OurThing[Thingyou] = ("pos%s_%s" % (self.beforex, self.beforey))
                    if Things > Thingyou:
                        Thingyou += 1
                        exec("Thing%s.move('right')" % Thingyou)
                    else:
                        lastthing['x'] = self.beforex
                        lastthing['y'] = self.beforey

                elif self.lastdirection == "left":
                    self.beforex -= 1
                    exec("global pos%s_%s; pos%s_%s = '%s'" % (self.beforex, self.beforey, self.beforex, self.beforey, me))
                    OurThing[Thingyou] = ("pos%s_%s" % (self.beforex, self.beforey))
                    if Things > Thingyou:
                        Thingyou += 1
                        exec("Thing%s.move('left')" % Thingyou)
                    else:
                        lastthing['x'] = self.beforex
                        lastthing['y'] = self.beforey

                self.lastdirection = thisdirect


        def move():
            global direction, restart, Things, Thingyou, now, special, paused
            temp = False
            temp2 = False
            Thingyou = 1

            for testy in range(1, max_y):
                for testx in range(1, max_x):
                    exec("global pos%s_%s" % (testx, testy))

            if direction == "wait":
                paused = True
                exec("global pos%s_%s; pos%s_%s = '%s'" % (now["x"], now["y"], now["x"], now["y"], me))
                time.sleep(sleep)
                pass

            if direction == "up":
                paused = False

                for testm in range(1, len(OurThing)):
                    if ("pos%s_%s" % (now["x"], now["y"] - 1)) == OurThing[testm]:
                        restart = False
                if restart:
                    if now["y"] == 1:
                        restart = False
                    else:

                        exec("global pos%s_%s; pos%s_%s = '%s'" % (now["x"], now["y"], now["x"], now["y"], nothing))
                        now["y"] -= 1
                        exec("global pos%s_%s; pos%s_%s = '%s'" % (now["x"], now["y"], now["x"], now["y"], me))

                        if Things > Thingyou:
                            Thingyou += 1
                            exec("Thing%s.move('up')" % Thingyou)
                        else:
                            lastthing['x'] = now['x']
                            lastthing['y'] = now['y']

                        for test1 in range(len(special)):
                            if ("pos%s_%s" % (now["x"], now["y"])) == special[test1]:
                                temp = True
                                special[test1] = ("pos%s_%s" % (random.randint(1, max_x), random.randint(1, max_y)))
                                Things += 1
                                exec("global Thing%s; Thing%s = Thing(lastthing['x'], lastthing['y'])" % (Things, Things))

            if direction == "down":
                paused = False
                for testm in range(1, len(OurThing)):
                    if ("pos%s_%s" % (now["x"], now["y"] + 1)) == OurThing[testm]:
                        print(now, OurThing)
                        restart = False
                if restart:
                    if now["y"] == max_y - 1:
                        restart = False
                    else:

                        exec("global pos%s_%s; pos%s_%s = '%s'" % (now["x"], now["y"], now["x"], now["y"], nothing))
                        now["y"] += 1
                        exec("global pos%s_%s; pos%s_%s = '%s'" % (now["x"], now["y"], now["x"], now["y"], me))

                        if Things > Thingyou:
                            Thingyou += 1
                            exec("Thing%s.move('down')" % Thingyou)
                        else:
                            lastthing['x'] = now['x']
                            lastthing['y'] = now['y']

                        for test1 in range(len(special)):
                            if ("pos%s_%s" % (now["x"], now["y"])) == special[test1]:
                                temp = True
                                special[test1] = ("pos%s_%s" % (random.randint(1, max_x), random.randint(1, max_y)))
                                Things += 1
                                exec("global Thing%s; Thing%s = Thing(lastthing['x'], lastthing['y'])" % (Things, Things))

            if direction == "right":
                paused = False
                for testm in range(1, len(OurThing)):
                    if ("pos%s_%s" % (now["x"] + 1, now["y"])) == OurThing[testm]:
                        restart = False
                if restart:
                    if now["x"] == max_x - 1:
                        restart = False
                    else:

                        exec("global pos%s_%s; pos%s_%s = '%s'" % (now["x"], now["y"], now["x"], now["y"], nothing))
                        now["x"] += 1
                        exec("global pos%s_%s; pos%s_%s = '%s'" % (now["x"], now["y"], now["x"], now["y"], me))

                        if Things > Thingyou:
                            Thingyou += 1
                            exec("Thing%s.move('right')" % Thingyou)
                        else:
                            lastthing['x'] = now['x']
                            lastthing['y'] = now['y']

                        for test1 in range(len(special)):
                            if ("pos%s_%s" % (now["x"], now["y"])) == special[test1]:
                                temp = True
                                special[test1] = ("pos%s_%s" % (random.randint(1, max_x), random.randint(1, max_y)))
                                Things += 1
                                exec("global Thing%s; Thing%s = Thing(lastthing['x'], lastthing['y'])" % (Things, Things))

            if direction == "left":
                paused = False

                for testm in range(1, len(OurThing)):
                    if ("pos%s_%s" % (now["x"] - 1, now["y"])) == OurThing[testm]:
                        restart = False
                if restart:
                    if now["x"] <= 1:
                        restart = False
                    else:

                        exec("global pos%s_%s; pos%s_%s = '%s'" % (now["x"], now["y"], now["x"], now["y"], nothing))
                        now["x"] -= 1
                        exec("global pos%s_%s; pos%s_%s = '%s'" % (now["x"], now["y"], now["x"], now["y"], me))

                        if Things > Thingyou:
                            Thingyou += 1
                            exec("Thing%s.move('left')" % Thingyou)
                        else:
                            lastthing['x'] = now['x']
                            lastthing['y'] = now['y']

                        for test1 in range(len(special)):
                            if ("pos%s_%s" % (now["x"], now["y"])) == special[test1]:
                                temp = True
                                special[test1] = ("pos%s_%s" % (random.randint(1, max_x), random.randint(1, max_y)))
                                Things += 1
                                exec("global Thing%s; Thing%s = Thing(lastthing['x'], lastthing['y'])" % (Things, Things))


        while True:
            global Title_run, beginn
            Title_run = False
            beginn = time.time()
            for testy in range(1, max_y):
                for testx in range(1, max_x):
                    exec("global pos%s_%s" % (testx, testy))

            for testy in range(1, max_y):
                for testx in range(1, max_x):
                    exec("pos%s_%s = '%s'" % (testx, testy, nothing))

            now = {"x": int(max_x / 2), "y": int(max_y / 2)}
            exec("global pos%s_%s; pos%s_%s = '%s'" % (int(max_x / 2), int(max_y / 2), int(max_x / 2), int(max_y / 2), me))

            special = ["pos%s_%s" % (random.randint(1, max_x), random.randint(1, max_y)),
                       "pos%s_%s" % (random.randint(1, max_x), random.randint(1, max_y)),
                       "pos%s_%s" % (random.randint(1, max_x), random.randint(1, max_y)),
                       "pos%s_%s" % (random.randint(1, max_x), random.randint(1, max_y)),
                       "pos%s_%s" % (random.randint(1, max_x), random.randint(1, max_y)),
                       "pos%s_%s" % (random.randint(1, max_x), random.randint(1, max_y)),
                       "pos%s_%s" % (random.randint(1, max_x), random.randint(1, max_y)),
                       "pos%s_%s" % (random.randint(1, max_x), random.randint(1, max_y))]
            global Things, OurThing, Thingyou, moves
            direction = "wait"
            sleep = 0.1
            restart = True
            Things = 1
            OurThing = ["", ""]
            Thingyou = 0
            moves = 0

            for test in range(len(special)):
                exec("%s = '%s'" % (special[test], food))


            class printy(threading.Thread):
                def __init__(self, printx):
                    super().__init__()  # was ist das?
                    self.printx = printx

                def run(self):
                    lockMe.acquire()
                    for testyp in range(1, max_y):
                        exec("sys.stdout.write(pos%s_%s)" % (self.printx, testyp))
                    print("")
                    lockMe.release()


            lockMe = threading.Lock()
            # for testy in range(1, max_y):
            #    exec("printer%s = printy(testy)" % testy)
            # for testy in range(1, max_y):
            #    exec("printer%s.start()" % testy)


            while restart:
                Title_run = True

                # for testy in range(1, max_y):
                #    exec("printer%s.join()" % testy)

                for testy in range(1, max_y):
                    for testx in range(1, max_x):
                        exec("global pos%s_%s" % (testx, testy))

                for testy in range(1, max_y):
                    for testx in range(1, max_x):
                        exec("global pos%s_%s; sys.stdout.write(pos%s_%s)" % (testx, testy, testx, testy))
                    print("")

                for testy in range(1, max_y):
                    for testx in range(1, max_x):
                        exec("global pos%s_%s; pos%s_%s = '%s'" % (testx, testy, testx, testy, nothing))

                for test in range(len(special)):
                    exec("global %s; %s = '%s'" % (special[test], special[test], food))

                time.sleep(sleep / (Things / 2))

                move()
                moves += 1
                cls()

    if preset == "snake":
        snake()

    if preset == "Man":
        cls()
        games_user_input = input("What to do now?\n\n")

        if games_user_input.lower() == "snake":
            global ttime_stop
            ttime_stop = False
            snake()



class MusicPlayerC(threading.Thread):
    def __init__(self):
        super().__init__()
        self.unerror = 0

        self.musiclist = []
        self.musiclistname = []
        self.musiclistpath = []
        self.musiclistdirname = []
        self.musiclistdirnamefull = []

        global musicrun
        musicrun = True

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

        self.lastmusicnumber = 0
        self.thismusicnumber = 0
        self.nextmusicnumber = 0

        self.music_playlists = ["LiS", "Anime", "Phunk", "Caravan Palace", "Electro Swing", "Parov Stelar", "jPOP & etc", "OMFG"]
        self.music_playlists_key = ["lis", "an", "phu", "cp", "es", "ps", "jpop", "omfg"]

        self.spl = False
        self.splmp = SplatoonC()

    def addMusic(self, key, loadMu=True): # key (AN, LIS)
        if not Computerfind_MiniPC:
            cls()
            print("Loading...")

            if key == "us":
                self.searchMusic("Music\\User", loadMu)
                print("Finished")
                return True
            elif key == "lis":
                self.searchMusic("Music\\Presets\\Life is Strange", loadMu)
                print("Finished")
                return True
            elif key == "an":
                self.searchMusic("Music\\Presets\\Anime", loadMu)
                print("Finished")
                return True
            elif key == "phu":
                self.searchMusic("Music\\Presets\\Phunk", loadMu)
                print("Finished")
                return True
            elif key == "cp":
                self.searchMusic("Music\\Presets\\Caravan Palace", loadMu)
                print("Finished")
                return True
            elif key == "es":
                self.searchMusic("Music\\Presets\\Electro Swing", loadMu)
                print("Finished")
                return True
            elif key == "ud":
                cls()
                self.searchMusic(input("Your path:\n"), loadMu)
                print("Finished")
                return True
            elif key == "ps":
                self.searchMusic("Music\\Presets\\Parov Stelar", loadMu)
                print("Finished")
                return True
            elif key == "jpop":
                self.searchMusic("Music\\Presets\\jPOP-etc", loadMu)
                print("Finished")
                return True
            elif key == "omfg":
                self.searchMusic("Music\\Presets\\OMFG", loadMu)
                print("Finished")
                return True

            else:
                return False

        else:
            cls()
            print("Loading... (On Mini-PC)")

            if key == "us":
                self.searchMusic("Music\\User", loadMu)
                print("Finished")
                return True
            elif key == "lis":
                self.searchMusic(MusicDir + "\\Games\\Life is Strange", loadMu)
                print("Finished")
                return True
            elif key == "an":
                self.searchMusic(MusicDir + "\\Anime", loadMu)
                print("Finished")
                return True
            elif key == "phu":
                self.searchMusic(MusicDir + "\\Phunk", loadMu)
                print("Finished")
                return True
            elif key == "cp":
                self.searchMusic(MusicDir + "\\Caravan Palace", loadMu)
                print("Finished")
                return True
            elif key == "es":
                self.searchMusic(MusicDir + "\\Electro Swing", loadMu)
                print("Finished")
                return True
            elif key == "ud":
                cls()
                self.searchMusic(input("Your path:\n"), loadMu)
                print("Finished")
                return "ul"
            elif key == "ps":
                self.searchMusic(MusicDir + "\\Parov Stelar", loadMu)
                print("Finished")
                return True
            elif key == "jpop":
                self.searchMusic(MusicDir + "\\jPOP-etc", loadMu)
                print("Finished")
                return True
            elif key == "omfg":
                self.searchMusic(MusicDir + "\\OMFG" ,loadMu)
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

    def istype(self, mType, exact=False):
        self.unerror += 1
        if mType[len(mType) - 3] == "m" and mType[len(mType) - 2] == "p" and mType[len(mType) - 1] == "3":
            if exact:
                return "mp3"
            else:
                return True
        elif mType[len(mType) - 3] == "m" and mType[len(mType) - 2] == "p" and mType[len(mType) - 1] == "4":
            if exact:
                return "mp4"
            else:
                return True
        else:
            return False

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
        self.musicplaying = False
        self.musicpause = False
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
        else:
            if self.spl:
                self.splmp.input(inpt=inpt)

         # play, next, stop, pause, last, del, deln, vol, volp, mute, mutep, jump (to 0), reroll
         # SPL: spl (On/Off), wr, reroll, start (""), effect (E--)
    def run(self):

        self.thismusicnumber = random.randint(0, len(self.musiclist) - 1)
        self.nextmusicnumber = random.randint(0, len(self.musiclist) - 1)

        global musicrun
        while musicrun:


            if self.musiclist[self.thismusicnumber].is_queued:
                self.reloadMusic(self.thismusicnumber)

            self.musicplayer = pyglet.media.Player()
            self.musicplayer.queue(self.musiclist[self.thismusicnumber])
            self.musicplayer.play()
            self.musicplayer.volume = self.musicvolumep
            self.music_time = time.time()

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


    def printIt(self):
        cls()
        print("Musicplayer\n\nNow Playing:")
        if self.istype(self.musiclistname[self.thismusicnumber], True) == "mp3":
            print(self.musiclistname[self.thismusicnumber].rstrip(".mp3"))
        elif self.istype(self.musiclistname[self.thismusicnumber], True) == "mp4":
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
        if self.istype(self.musiclistname[self.nextmusicnumber], True) == "mp3":
            print(self.musiclistname[self.nextmusicnumber].rstrip(".mp3"))
        elif self.istype(self.musiclistname[self.nextmusicnumber], True) == "mp4":
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
            print(self.musiclistname[self.thismusicnumber])
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



def Music():

    def Play():
        class Printerr(threading.Thread):
            def run(self):
                global musicrun
                while musicrun:
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

        global musicrun
        while musicrun:
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


def screensaver(preset = None):
    #   thread für time zähler,
    #   dann background time printer
    #   dann zur input console (main())

    #   light funktion machen
    def deacss():
        if os.path.exists("data\\tmp\\Screensaver\\deac"):
            os.remove("data\\tmp\\Screensaver\\deac")
        else:
            file = open("data\\tmp\\Screensaver\\deac", "w")
            file.write("deactivated")
            file.close()

    def ss():
        global color, ss_active, killmem

        title("Screensaver", "")

        oldEP = Tools.EnergyPlan.getEP()
        Tools.EnergyPlan.Change(1)

        ttime.pt()

        killmem = False
        sleeps = True
        ss_active = True
        color = "dark"

        class Timecount(threading.Thread):
            def run(self):
                global ss_pause

                ss_start = time.time()
                while sleeps:
                    time.sleep(0.1)

                ss_pause = time.time() - ss_start


        backtime = Timecount()

        ss_start = time.time()

        #dir_tmp = os.getcwd()
        #os.chdir("Programs\\Evecon\\Screensaver_time")
        #os.system("start ss_time.exe")
        #subprocess.call("ss_time.exe") # time printer
        #os.chdir(dir_tmp)
        #time.sleep(1)

        nircmd("foreground")
        nircmd("setsize")

        def screensavertime():

            dir_tmp = os.getcwd()
            os.chdir("Programs\\Evecon\\Screensaver_time")
            subprocess.call("ss_time.exe")
            os.chdir(dir_tmp)

        def lightss():
            global color
            if color != "dark":
                os.system("color 07")
                color_data = open("data\\tmp\\sscolor", "w")
                color_data.write("dark")
                color_data.close()
                color = "dark"
            elif color != "bright":
                os.system("color F0")
                color_data = open("data\\tmp\\sscolor", "w")
                color_data.write("bright")
                color_data.close()
                color = "bright"

        def deac():
            if os.path.exists("data\\tmp\\Screensaver\\deac"):
                os.remove("data\\tmp\\Screensaver\\deac")
            else:
                file = open("data\\tmp\\Screensaver\\deac", "w")
                file.write("deactivated")
                file.close()

        while sleeps:
            cls()
            user_input = input("Screensaver\n\nWhat to do?\nLight (L), Deac (DEAC)\n\n")

            if user_input.lower() == "l":
                lightss()
            elif user_input.lower() == "deac":
                deac()
            elif user_input.lower() == "time":
                screensavertime()
            elif user_input.lower() == "debug":
                debug()
            elif user_input.lower() == "games":
                games()
            elif user_input.lower() == "snake":
                games("snake")
            elif user_input.lower() == "music":
                Music()
                killmem = True
            elif user_input.lower() == "main":
                main()
            else:
                sleeps = False


        subprocess.call(["taskkill", "/IM", "ss_time.exe"])

        # schreibe in die Datei ...
        ss_pause = time.time() - ss_start
        Tools.EnergyPlan.Change(oldEP)
        exit_now(killmem)

    if preset is None:
        ss()
    elif preset == "deac":
        deacss()

def Timeprint():
    cls()

    print("Preset:\nRight (R)")
    user_input = input()

    if user_input.lower() == "r":

        nircmd("maxi")

        space = "\t" * 24

        def printerIT():
            cls()
            for x in range(len(hour1)):
                print(space + hour1[x] + empty + hour2[x])
            for x in range(len(minu1)):
                print(space + minu1[x] + empty + minu2[x])
            for x in range(len(sec1)):
                print(space + sec1[x] + empty + sec2[x])

    else:
        print("ERROR") # hier standart wenn es es gibt
        def printerIT():
            cls()
            for x in range(len(hour1)):
                print(space + hour1[x] + empty + hour2[x])
            for x in range(len(minu1)):
                print(space + minu1[x] + empty + minu2[x])
            for x in range(len(sec1)):
                print(space + sec1[x] + empty + sec2[x])



    empty = " "
    nothingit = "-"  # nothing in time
    iss = "X"  # ist was oder so


    blockempty = nothingit * 19
    blockfull = nothingit * 2 + iss * 15 + nothingit * 2
    blockside = nothingit * 2 + iss + nothingit * 13 + iss + nothingit * 2
    blockemptyfull = nothingit * 16 + iss + nothingit * 2
    blockfullempty = nothingit * 2 + iss + nothingit * 16

    global hour1, hour2, minu1, minu2, sec1, sec2

    hour1 = [blockempty, blockfull,
             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
             blockfull,
             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
             blockfull]
    hour2 = [blockempty, blockfull,
             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
             blockfull,
             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
             blockfull]
    minu1 = [blockempty, blockfull,
             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
             blockfull,
             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
             blockfull]
    minu2 = [blockempty, blockfull,
             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
             blockfull,
             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
             blockfull]
    sec1 = [blockempty, blockfull,
            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
            blockfull,
            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
            blockfull, blockempty]
    sec2 = [blockempty, blockfull,
            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
            blockfull,
            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
            blockfull, blockempty]

    def refreshtime():
        global lasthour, lastminu, lastsec, hour1, hour2, minu1, minu2, sec1, sec2
        hour = datetime.datetime.now().strftime("%H")
        minu = datetime.datetime.now().strftime("%M")
        sec = datetime.datetime.now().strftime("%S")
        if lasthour != hour:
            if lasthour[0] != hour[0]:
                if hour[0] == "0":
                    hour1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[0] == "1":
                    hour1 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[0] == "2":
                    hour1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull]
                if hour[0] == "3":
                    hour1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if hour[0] == "4":
                    hour1 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[0] == "5":
                    hour1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if hour[0] == "6":
                    hour1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[0] == "7":
                    hour1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[0] == "8":
                    hour1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[0] == "9":
                    hour1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
            if lasthour[1] != hour[1]:
                if hour[1] == "0":
                    hour2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[1] == "1":
                    hour2 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[1] == "2":
                    hour2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull]
                if hour[1] == "3":
                    hour2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if hour[1] == "4":
                    hour2 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[1] == "5":
                    hour2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if hour[1] == "6":
                    hour2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[1] == "7":
                    hour2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[1] == "8":
                    hour2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[1] == "9":
                    hour2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
            lasthour = hour
        if lastminu != minu:
            if lastminu[0] != minu[0]:
                if minu[0] == "0":
                    minu1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[0] == "1":
                    minu1 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[0] == "2":
                    minu1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull]
                if minu[0] == "3":
                    minu1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if minu[0] == "4":
                    minu1 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[0] == "5":
                    minu1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if minu[0] == "6":
                    minu1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[0] == "7":
                    minu1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[0] == "8":
                    minu1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[0] == "9":
                    minu1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
            if lastminu[1] != minu[1]:
                if minu[1] == "0":
                    minu2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[1] == "1":
                    minu2 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[1] == "2":
                    minu2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull]
                if minu[1] == "3":
                    minu2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if minu[1] == "4":
                    minu2 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[1] == "5":
                    minu2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if minu[1] == "6":
                    minu2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[1] == "7":
                    minu2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[1] == "8":
                    minu2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[1] == "9":
                    minu2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
            lastminu = minu
        if lastsec != sec:
            if lastsec[0] != sec[0]:
                if sec[0] == "0":
                    sec1 = [blockempty, blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockside,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull, blockempty]
                if sec[0] == "1":
                    sec1 = [blockempty, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockempty]
                if sec[0] == "2":
                    sec1 = [blockempty, blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull,
                            blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                            blockfullempty, blockfullempty, blockfullempty,
                            blockfull, blockempty]
                if sec[0] == "3":
                    sec1 = [blockempty, blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull, blockempty]
                if sec[0] == "4":
                    sec1 = [blockempty, blockside,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockempty]
                if sec[0] == "5":
                    sec1 = [blockempty, blockfull,
                            blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                            blockfullempty, blockfullempty, blockfullempty,
                            blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull, blockempty]
                if sec[0] == "6":
                    sec1 = [blockempty, blockfull,
                            blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                            blockfullempty, blockfullempty, blockfullempty,
                            blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull, blockempty]
                if sec[0] == "7":
                    sec1 = [blockempty, blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockempty]
                if sec[0] == "8":
                    sec1 = [blockempty, blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull, blockempty]
                if sec[0] == "9":
                    sec1 = [blockempty, blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull, blockempty]
            if lastsec[1] != sec[1]:
                if sec[1] == "0":
                    sec2 = [blockempty, blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockside,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull, blockempty]
                if sec[1] == "1":
                    sec2 = [blockempty, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockempty]
                if sec[1] == "2":
                    sec2 = [blockempty, blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull,
                            blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                            blockfullempty, blockfullempty, blockfullempty,
                            blockfull, blockempty]
                if sec[1] == "3":
                    sec2 = [blockempty, blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull, blockempty]
                if sec[1] == "4":
                    sec2 = [blockempty, blockside,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockempty]
                if sec[1] == "5":
                    sec2 = [blockempty, blockfull,
                            blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                            blockfullempty, blockfullempty, blockfullempty,
                            blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull, blockempty]
                if sec[1] == "6":
                    sec2 = [blockempty, blockfull,
                            blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                            blockfullempty, blockfullempty, blockfullempty,
                            blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull, blockempty]
                if sec[1] == "7":
                    sec2 = [blockempty, blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockempty]
                if sec[1] == "8":
                    sec2 = [blockempty, blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull, blockempty]
                if sec[1] == "9":
                    sec2 = [blockempty, blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull, blockempty]
            lastsec = sec

    global lasthour, lastminu, lastsec
    lasthour = "EE"
    lastminu = "EE"
    lastsec = "EE"


    global ttime_stop
    ttime_stop = False

    while True:
        refreshtime()
        printerIT()
        time.sleep(1)



def Timerprint(hourT, minuT, secT):

    # insgesamter Block: 135x60
    empty = " "
    nothingit = "-" # nothing in time
    iss = "X" # ist was oder so

    space = "\t" * 24
    blockempty = nothingit * 19
    blockfull = nothingit * 2 + iss * 15 + nothingit * 2
    blockside = nothingit * 2 + iss + nothingit * 13 + iss + nothingit * 2
    blockemptyfull = nothingit * 16 + iss + nothingit * 2
    blockfullempty = nothingit * 2 + iss + nothingit * 16

    global hour1, hour2, minu1, minu2, sec1, sec2

    hour1 = [blockempty, blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull]
    hour2 = [blockempty, blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull]
    minu1 = [blockempty, blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull]
    minu2 = [blockempty, blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull]
    sec1 = [blockempty, blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull, blockempty]
    sec2 = [blockempty, blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull, blockempty]

    waittime = hourT * 3600 +  minuT * 60 + secT

    def printtime():
        cls()
        for x in range(len(hour1)):
            print(space + hour1[x] + empty + hour2[x])
        for x in range(len(minu1)):
            print(space + minu1[x] + empty + minu2[x])
        for x in range(len(sec1)):
            print(space + sec1[x] + empty + sec2[x])


    def refreshtime():
        global lasthour, lastminu, lastsec, hour1, hour2, minu1, minu2, sec1, sec2
        nonlocal waittime


        hour = str(waittime // 3600)
        if len(hour) == 1:
            hour = "0" + hour

        minu = str((waittime % 3600) // 60)
        if len(minu) == 1:
            minu = "0" + minu

        sec = str((waittime % 3600) % 60)
        if len(sec) == 1:
            sec = "0" + sec

        if lasthour != hour:
            if lasthour[0] != hour[0]:
                if hour[0] == "0":
                    hour1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[0] == "1":
                    hour1 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[0] == "2":
                    hour1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfull]
                if hour[0] == "3":
                    hour1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if hour[0] == "4":
                    hour1 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[0] == "5":
                    hour1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if hour[0] == "6":
                    hour1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[0] == "7":
                    hour1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[0] == "8":
                    hour1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[0] == "9":
                    hour1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
            if lasthour[1] != hour[1]:
                if hour[1] == "0":
                    hour2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[1] == "1":
                    hour2 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[1] == "2":
                    hour2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfull]
                if hour[1] == "3":
                    hour2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if hour[1] == "4":
                    hour2 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[1] == "5":
                    hour2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if hour[1] == "6":
                    hour2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[1] == "7":
                    hour2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[1] == "8":
                    hour2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[1] == "9":
                    hour2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
            lasthour = hour
        if lastminu != minu:
            if lastminu[0] != minu[0]:
                if minu[0] == "0":
                    minu1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[0] == "1":
                    minu1 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[0] == "2":
                    minu1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull]
                if minu[0] == "3":
                    minu1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if minu[0] == "4":
                    minu1 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[0] == "5":
                    minu1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if minu[0] == "6":
                    minu1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[0] == "7":
                    minu1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[0] == "8":
                    minu1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[0] == "9":
                    minu1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
            if lastminu[1] != minu[1]:
                if minu[1] == "0":
                    minu2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[1] == "1":
                    minu2 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[1] == "2":
                    minu2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull]
                if minu[1] == "3":
                    minu2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if minu[1] == "4":
                    minu2 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[1] == "5":
                    minu2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if minu[1] == "6":
                    minu2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[1] == "7":
                    minu2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[1] == "8":
                    minu2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[1] == "9":
                    minu2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
            lastminu = minu
        if lastsec != sec:
            if lastsec[0] != sec[0]:
                if sec[0] == "0":
                    sec1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull, blockempty]
                if sec[0] == "1":
                    sec1 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockempty]
                if sec[0] == "2":
                    sec1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull, blockempty]
                if sec[0] == "3":
                    sec1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull, blockempty]
                if sec[0] == "4":
                    sec1 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockempty]
                if sec[0] == "5":
                    sec1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull, blockempty]
                if sec[0] == "6":
                    sec1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull, blockempty]
                if sec[0] == "7":
                    sec1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockempty]
                if sec[0] == "8":
                    sec1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull, blockempty]
                if sec[0] == "9":
                    sec1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull, blockempty]
            if lastsec[1] != sec[1]:
                if sec[1] == "0":
                    sec2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull, blockempty]
                if sec[1] == "1":
                    sec2 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockempty]
                if sec[1] == "2":
                    sec2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull, blockempty]
                if sec[1] == "3":
                    sec2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull, blockempty]
                if sec[1] == "4":
                    sec2 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockempty]
                if sec[1] == "5":
                    sec2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull, blockempty]
                if sec[1] == "6":
                    sec2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull, blockempty]
                if sec[1] == "7":
                    sec2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockempty]
                if sec[1] == "8":
                    sec2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull, blockempty]
                if sec[1] == "9":
                    sec2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull, blockempty]
            lastsec = sec



    global lasthour, lastminu, lastsec, RUN
    lasthour = "EE"
    lastminu = "EE"
    lastsec = "EE"
    RUN = True

    class runner(threading.Thread):
        def run(self):
            global RUN
            nonlocal waittime
            while RUN:
                waittime -= 1
                time.sleep(1)
                if waittime == 0:
                    RUN = False

    runer = runner()
    runer.start()

    while RUN:
        refreshtime()
        printtime()
        time.sleep(1)


def Alarmprint(x=230, y=65, colorCh=False):
    # insgesamter Block: 135x60

    def randi(x):
        randlist = ["1", "2", " "]
        key = random.randint(0, 100)
        if key == 0:
            randlist.append("X")
        elif key == 1:
            randlist = ["/", "\\", "_"]
        elif key == 2:
            listx = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                     "U",
                     "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
                     "p",
                     "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                     "!",
                     "§", "$", "%", "&", "/", "(", ")", "=", "?", "ß", "#", "'", "+", "*", "~", "ü", "ö", "ä", "-", "_",
                     ".",
                     ":", ",", ";", "{", "[", "]", "}", ">", "<", "|"]
            randlist = [listx[random.randint(0, len(listx) - 1)], listx[random.randint(0, len(listx) - 1)], listx[random.randint(0, len(listx) - 1)]]
        for z in range(random.randint(1, 5)):
            randlist.append(randlist[random.randint(0, len(randlist) - 1)])

        block = ""
        for z in range(x):
            block += str(randlist[random.randint(0, len(randlist) - 1)])
        return block


    afk = True

    oldColor = color.CurColor

    class printre(threading.Thread):
        def __init__(self, x, y, colorCh):
            super().__init__()

            self.x = x
            self.y = y
            self.colorCh = colorCh

        def run(self):
            nonlocal afk
            while afk:

                if self.colorCh:
                    randcolor = ""
                    randcolor += color.colorKeys[random.randint(0, len(color.colorKeys) - 1)]
                    randcolor += "0"
                    color.change(randcolor)
                cls()
                for x in range(self.y):
                    print(randi(self.x))
                time.sleep(0.75)

    printri = printre(x, y, colorCh)
    printri.start()

    input()
    afk = False
    color.change(oldColor)

def randompw(returnpw = False, length = 150):
    import random
    listx = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
            "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!",
            "§", "$", "%", "&", "/", "(", ")", "=", "?", "ß", "#", "'", "+", "*", "~", "ü", "ö", "ä", "-", "_", ".",
            ":", ",", ";", "{", "[", "]", "}", ">", "<", "|"]

    pw = ""

    for rx in range(length):
        pw += listx[random.randint(0, len(listx) - 1)]

    if returnpw:
        return pw
    cls()
    print("Password: (length: %s) \n\n%s" % (length, pw))

    input()

def passwordmanager():
    import simplecrypt
    title("Passwordmanager")

    def start():

        global pw0, pw1, pw2, pw3
        pw0 = None
        pw1 = None
        pw2 = None
        pw3 = None

        def unlock(lvl=None):


            def lvl0():
                global pw0

                cls()
                print("Loading...")

                mpw0 = "$sQHB<~aws7!w3,§4t)1köBc_,dtid>ümMU?m>tlG>GD+l%/KjKIb0U%gK§j<bU]R?W§;z|r9s|bE>.t,?MjC+u1t)DV_!E(IqW?vpy8Vd&kw§ißäYTc%g}U3xKM_}ZxI}Zr)agk_|-nJeü*.):(~7"

                pw0_raw = open("data\\Password\\MPwds\\pw0", "rb")
                pw0_lock = pw0_raw.read()

                pw0 = simplecrypt.decrypt(mpw0, pw0_lock).decode("utf-8")
                pw0_raw.close()

            def lvl1():
                global pw1

                cls()
                mpw1 = input("Master Password No.1:\n")
                cls()
                print("Loading...")

                pw1_raw = open("data\\Password\\MPwds\\pw1", "rb")
                pw1_lock = pw1_raw.read()
                try:
                    pw1 = simplecrypt.decrypt(mpw1, pw1_lock).decode("utf-8")
                except simplecrypt.DecryptionException:
                    print("Wrong Masterpassword")
                    time.sleep(1.5)
                pw1_raw.close()

            def lvl2():
                global pw2
                cls()
                mpw2 = input("Master Password No.2:\n")
                cls()
                print("Loading...")

                pw2_raw = open("data\\Password\\MPwds\\pw2", "rb")
                pw2_lock = pw2_raw.read()

                try:
                    pw2 = simplecrypt.decrypt(mpw2, pw2_lock).decode("utf-8")
                except simplecrypt.DecryptionException:
                    print("Wrong Masterpassword")
                    time.sleep(1.5)
                pw2_raw.close()

            def lvl3():
                global pw3
                cls()
                mpw3 = input("Master Password No.3:\n")
                cls()
                print("Loading...")

                pw3_raw = open("data\\Password\\MPwds\\pw3", "rb")
                pw3_lock = pw3_raw.read()

                try:
                    pw3 = simplecrypt.decrypt(mpw3, pw3_lock).decode("utf-8")
                except simplecrypt.DecryptionException:
                    print("Wrong Masterpassword")
                    time.sleep(1.5)
                pw3_raw.close()

            if lvl == 0:
                lvl0()
            elif lvl == 1:
                lvl1()
            elif lvl == 2:
                lvl2()
            elif lvl == 3:
                lvl3()
            elif lvl is None:
                cls()
                print("Unlock lvl 1/2/3")
                lvlu = input()
                if lvlu == 1:
                    lvl1()
                elif lvlu == 2:
                    lvl2()
                elif lvlu == 3:
                    lvl3()

        def creapw(): # vergess nicht hier kein crea, del, mpw liste erstellen lassen!
            title("Create a PW")
            cls()

            def start_input():

                pwlvl = None
                pwfullname = None
                pwemail = None
                pwnumber = None
                pwbdate = None
                pwgender = None
                pwresidence = None
                pwpassword = None
                pwsq1 = None
                pwsq1a = None
                pwsq2 = None
                pwsq2a = None
                pwsq3 = None
                pwsq3a = None

                cls()
                print("%s:\n\nPassword (RAN):" % pwname)
                pwpassword = input().rstrip("\n")
                if pwpassword.lower() == "ran":
                    pwpassword = randompw(True)
                    cls()
                    print("Your random Password:\n\n%s" % pwpassword)
                    input()
                cls()
                print("%s:\n\nPassword Level (1/2/3):" % pwname)
                pwlvl = input().rstrip("\n")

                if int(pwlvl) == 1:
                    unlock(1)
                elif int(pwlvl) == 2:
                    unlock(2)
                elif int(pwlvl) == 3:
                    unlock(3)

                cls()
                print("%s:\n\nWebsite:" % pwname)
                pwwebsite = input().rstrip("\n")
                cls()
                print("%s:\n\nType:" % pwname)
                pwtype = input().rstrip("\n")
                cls()
                print("%s:\n'None' for nothing, today (NOW)\n\nDate:" % pwname)
                pwdate = input().rstrip("\n")
                if pwdate.lower() == "none" or pwdate.lower() == "":
                    pwdate = None
                elif pwdate.lower() == "now":
                    pwdate = datetime.datetime.now().strftime("%d.%m.%Y")
                cls()
                print("%s:\n'None' for nothing\n\nNickname:" % pwname)
                pwnick = input().rstrip("\n")
                if pwnick.lower() == "none" or pwnick.lower() == "":
                    pwnick = None
                cls()
                print("%s:\n'None' for nothing\n\nFull name:" % pwname)
                pwfullname = input().rstrip("\n")
                if pwfullname.lower() == "none" or pwfullname.lower() == "":
                    pwfullname = None
                cls()
                print("%s:\n'None' for nothing, lualbi11@aol.de (REAL)\n\nE-Mail:" % pwname)
                pwemail = input().rstrip("\n")
                if pwemail.lower() == "none" or pwemail.lower() == "":
                    pwemail = None
                elif pwemail.lower() == "real":
                    pwemail = "lualbi11@aol.de"
                cls()
                print("%s:\n'None' for nothing\n\nPhonenumber:" % pwname)
                pwnumber = input().rstrip("\n")
                if pwnumber.lower() == "none" or pwnumber.lower() == "":
                    pwnumber = None
                cls()
                print("%s:\n'None' for nothing\n\nBirthdate:" % pwname)
                pwbdate = input().rstrip("\n")
                if pwbdate.lower() == "none" or pwbdate.lower() == "":
                    pwbdate = None
                cls()
                print("%s:\n'None' for nothing\n\nGender:" % pwname)
                pwgender = input().rstrip("\n")
                if pwgender.lower() == "none" or pwgender.lower() == "":
                    pwgender = None
                cls()
                print("%s:\n'None' for nothing\n\nResidence:" % pwname)
                pwresidence = input().rstrip("\n")
                if pwresidence.lower() == "none" or pwresidence.lower() == "":
                    pwresidence = None
                cls()
                print("%s:\n'None' for nothing\n\nSecurity Question:" % pwname)
                pwsq1 = input().rstrip("\n")
                if pwsq1.lower() == "none" or pwsq1.lower() == "":
                    pwsq1 = None
                cls()
                if pwsq1 is not None:
                    print("%s:\n\nSecurity Question answer:" % pwname)
                    pwsq1a = input().rstrip("\n")
                    cls()
                    print("%s:\n'None' for nothing\n\nSecurity Question 2:" % pwname)
                    pwsq2 = input().rstrip("\n")
                    if pwsq2.lower() == "none" or pwsq2.lower() == "":
                        pwsq2 = None
                    cls()
                    if pwsq2 is not None:
                        print("%s:\n\nSecurity Question 2 answer:" % pwname)
                        pwsq2a = input().rstrip("\n")
                        cls()
                        print("%s:\n'None' for nothing\n\nSecurity Question 3:" % pwname)
                        pwsq3 = input().rstrip("\n")
                        if pwsq3.lower() == "none" or pwsq3.lower() == "":
                            pwsq3 = None
                        cls()
                        if pwsq3 is not None:
                            print("%s:\n\nSecurity Question 3 answer:" % pwname)
                            pwsq3a = input().rstrip("\n")
                            cls()

                print("%s:\n'None' for nothing\n\nComment:" % pwname)
                pwcomment = input().rstrip("\n")
                if pwcomment.lower() == "none" or pwcomment.lower() == "":
                    pwcomment = None
                cls()


                title("Encrypting")

                os.mkdir("data\\Password\\Pwds\\%s" % pwname)
                os.mkdir("data\\Password\\Pwds\\%s\\pwd" % pwname)
                os.mkdir("data\\Password\\Pwds\\%s\\personaldata" % pwname)


                pwlist.append(pwname + "\n")
                pwlist.sort()

                chpwlist_raw = open("data\\Password\\list.txt", "w")
                for xcl in pwlist:
                    chpwlist_raw.write(xcl)
                chpwlist_raw.close()


                pwinfo = [pwname + "\n", pwwebsite + "\n", pwtype + "\n"]

                if pwdate is not None:
                    pwinfo.append(pwdate)

                pwinfo_raw = open("data\\Password\\Pwds\\%s\\info.txt" % pwname, "w")

                for xcl in pwinfo:
                    pwinfo_raw.write(xcl)
                pwinfo_raw.close()

                if pwnick is not None:
                    pwnick_raw = open("data\\Password\\Pwds\\%s\\personaldata\\nickname.txt" % pwname, "w")
                    pwnick_raw.write(pwnick)
                    pwinfo_raw.close()

                if pwfullname is not None:
                    pwfullname_raw = open("data\\Password\\Pwds\\%s\\personaldata\\name" % pwname, "wb")
                    if int(pwlvl) == 0:
                        pwfullname_raw.write(simplecrypt.encrypt(pw0, pwfullname))
                    elif int(pwlvl) == 1:
                        pwfullname_raw.write(simplecrypt.encrypt(pw1, pwfullname))
                    elif int(pwlvl) == 2:
                        pwfullname_raw.write(simplecrypt.encrypt(pw2, pwfullname))
                    elif int(pwlvl) == 3:
                        pwfullname_raw.write(simplecrypt.encrypt(pw3, pwfullname))

                    pwfullname_raw.close()

                if pwemail is not None:
                    pwemail_raw = open("data\\Password\\Pwds\\%s\\personaldata\\email" % pwname, "wb")
                    if int(pwlvl) == 0:
                        pwemail_raw.write(simplecrypt.encrypt(pw0, pwemail))
                    elif int(pwlvl) == 1:
                        pwemail_raw.write(simplecrypt.encrypt(pw1, pwemail))
                    elif int(pwlvl) == 2:
                        pwemail_raw.write(simplecrypt.encrypt(pw2, pwemail))
                    elif int(pwlvl) == 3:
                        pwemail_raw.write(simplecrypt.encrypt(pw3, pwemail))

                    pwemail_raw.close()


                if pwnumber is not None:
                    pwnumber_raw = open("data\\Password\\Pwds\\%s\\personaldata\\pnumber" % pwname, "wb")
                    if int(pwlvl) == 0:
                        pwnumber_raw.write(simplecrypt.encrypt(pw0, pwnumber))
                    elif int(pwlvl) == 1:
                        pwnumber_raw.write(simplecrypt.encrypt(pw1, pwnumber))
                    elif int(pwlvl) == 2:
                        pwnumber_raw.write(simplecrypt.encrypt(pw2, pwnumber))
                    elif int(pwlvl) == 3:
                        pwnumber_raw.write(simplecrypt.encrypt(pw3, pwnumber))

                    pwnumber_raw.close()


                if pwbdate is not None:
                    pwbdate_raw = open("data\\Password\\Pwds\\%s\\personaldata\\bdate" % pwname, "wb")
                    if int(pwlvl) == 0:
                        pwbdate_raw.write(simplecrypt.encrypt(pw0, pwbdate))
                    elif int(pwlvl) == 1:
                        pwbdate_raw.write(simplecrypt.encrypt(pw1, pwbdate))
                    elif int(pwlvl) == 2:
                        pwbdate_raw.write(simplecrypt.encrypt(pw2, pwbdate))
                    elif int(pwlvl) == 3:
                        pwbdate_raw.write(simplecrypt.encrypt(pw3, pwbdate))

                    pwbdate_raw.close()

                if pwgender is not None:
                    pwgender_raw = open("data\\Password\\Pwds\\%s\\personaldata\\gender" % pwname, "wb")
                    if int(pwlvl) == 0:
                        pwgender_raw.write(simplecrypt.encrypt(pw0, pwgender))
                    elif int(pwlvl) == 1:
                        pwgender_raw.write(simplecrypt.encrypt(pw1, pwgender))
                    elif int(pwlvl) == 2:
                        pwgender_raw.write(simplecrypt.encrypt(pw2, pwgender))
                    elif int(pwlvl) == 3:
                        pwgender_raw.write(simplecrypt.encrypt(pw3, pwgender))

                    pwgender_raw.close()

                if pwresidence is not None:
                    pwresidence_raw = open("data\\Password\\Pwds\\%s\\personaldata\\residence" % pwname, "wb")
                    if int(pwlvl) == 0:
                        pwresidence_raw.write(simplecrypt.encrypt(pw0, pwresidence))
                    elif int(pwlvl) == 1:
                        pwresidence_raw.write(simplecrypt.encrypt(pw1, pwresidence))
                    elif int(pwlvl) == 2:
                        pwresidence_raw.write(simplecrypt.encrypt(pw2, pwresidence))
                    elif int(pwlvl) == 3:
                        pwresidence_raw.write(simplecrypt.encrypt(pw3, pwresidence))

                    pwresidence_raw.close()

                pwlvl_raw = open("data\\Password\\Pwds\\%s\\pwd\\pwdlvl" % pwname, "wb")
                pwlvl_raw.write(simplecrypt.encrypt(pw0, pwlvl))
                pwlvl_raw.close()

                pwpassword_raw = open("data\\Password\\Pwds\\%s\\pwd\\pwd" % pwname, "wb")
                if int(pwlvl) == 0:
                    pwpassword_raw.write(simplecrypt.encrypt(pw0, pwpassword))
                elif int(pwlvl) == 1:
                    pwpassword_raw.write(simplecrypt.encrypt(pw1, pwpassword))
                elif int(pwlvl) == 2:
                    pwpassword_raw.write(simplecrypt.encrypt(pw2, pwpassword))
                elif int(pwlvl) == 3:
                    pwpassword_raw.write(simplecrypt.encrypt(pw3, pwpassword))

                pwpassword_raw.close()


                if pwsq1 is not None:
                    pwsq1_raw = open("data\\Password\\Pwds\\%s\\pwd\\sq1" % pwname, "w")
                    pwsq1_raw.write(pwsq1)
                    pwsq1_raw.close()

                    pwsq1a_raw = open("data\\Password\\Pwds\\%s\\pwd\\sq1a" % pwname, "wb")
                    if int(pwlvl) == 0:
                        pwsq1a_raw.write(simplecrypt.encrypt(pw0, pwsq1a))
                    elif int(pwlvl) == 1:
                        pwsq1a_raw.write(simplecrypt.encrypt(pw1, pwsq1a))
                    elif int(pwlvl) == 2:
                        pwsq1a_raw.write(simplecrypt.encrypt(pw2, pwsq1a))
                    elif int(pwlvl) == 3:
                        pwsq1a_raw.write(simplecrypt.encrypt(pw3, pwsq1a))

                        pwsq1a_raw.close()

                    if pwsq2 is not None:
                        pwsq2_raw = open("data\\Password\\Pwds\\%s\\pwd\\sq2" % pwname, "w")
                        pwsq2_raw.write(pwsq2)
                        pwsq2_raw.close()

                        pwsq2a_raw = open("data\\Password\\Pwds\\%s\\pwd\\sq2a" % pwname, "wb")
                        if int(pwlvl) == 0:
                            pwsq2a_raw.write(simplecrypt.encrypt(pw0, pwsq2a))
                        elif int(pwlvl) == 1:
                            pwsq2a_raw.write(simplecrypt.encrypt(pw1, pwsq2a))
                        elif int(pwlvl) == 2:
                            pwsq2a_raw.write(simplecrypt.encrypt(pw2, pwsq2a))
                        elif int(pwlvl) == 3:
                            pwsq2a_raw.write(simplecrypt.encrypt(pw3, pwsq2a))

                            pwsq2a_raw.close()

                        if pwsq3 is not None:
                            pwsq3_raw = open("data\\Password\\Pwds\\%s\\pwd\\sq3" % pwname, "w")
                            pwsq3_raw.write(pwsq2)
                            pwsq3_raw.close()

                            pwsq3a_raw = open("data\\Password\\Pwds\\%s\\pwd\\sq3a" % pwname, "wb")
                            if int(pwlvl) == 0:
                                pwsq3a_raw.write(simplecrypt.encrypt(pw0, pwsq3a))
                            elif int(pwlvl) == 1:
                                pwsq3a_raw.write(simplecrypt.encrypt(pw1, pwsq3a))
                            elif int(pwlvl) == 2:
                                pwsq3a_raw.write(simplecrypt.encrypt(pw2, pwsq3a))
                            elif int(pwlvl) == 3:
                                pwsq3a_raw.write(simplecrypt.encrypt(pw3, pwsq3a))

                            pwsq3a_raw.close()

                if pwcomment is not None:
                    pwcomment_raw = open("data\\Password\\Pwds\\%s\\comment.txt" % pwname, "w")
                    pwcomment_raw.write(pwcomment)
                    pwcomment_raw.close()


                cls()
                title("Created PW")
                time.sleep(1)
                print("Success")




            startin = True

            print("Name:")
            pwname = input().rstrip("\n")

            for xn in pwlist:
                if pwname == xn:
                    startin = False


            if pwname.lower() == "del":
                startin = False
            elif pwname.lower() == "mpw":
                startin = False
            elif pwname.lower() == "crea":
                startin = False

            if startin:
                start_input()



        def delpw():
            pass
        def chmpw():
            cls()
            print("Change lvl 1/2/3")
            changelvl = int(input())
            if changelvl == 1:
                cls()
                oldmpw = input("Old Masterpw:\n")
                cls()
                newmpw = input("New Masterpw:\n")

                if newmpw == input("Reapeat new Masterpw:\n"):
                    cls()
                    print("Loading...")
                    oldpw_raw = open("data\\Password\\MPwds\\pw1", "rb")
                    oldpw_lock = oldpw_raw.read()
                    oldpw = simplecrypt.decrypt(oldmpw, oldpw_lock).decode("utf-8")
                    oldpw_raw.close()

                    pw_raw = open("data\\Password\\MPwds\\pw1", "wb")
                    pw_raw.write(simplecrypt.encrypt(newmpw, oldpw))
                    pw_raw.close()

                else:
                    cls()
                    print("Error")


            elif changelvl == 2:
                cls()
                oldmpw = input("Old Masterpw:\n")
                cls()
                newmpw = input("New Masterpw:\n")

                if newmpw == input("Reapeat new Masterpw:\n"):
                    cls()
                    print("Loading...")
                    oldpw_raw = open("data\\Password\\MPwds\\pw2", "rb")
                    oldpw_lock = oldpw_raw.read()
                    oldpw = simplecrypt.decrypt(oldmpw, oldpw_lock).decode("utf-8")
                    oldpw_raw.close()

                    pw_raw = open("data\\Password\\MPwds\\pw2", "wb")
                    pw_raw.write(simplecrypt.encrypt(newmpw, oldpw))
                    pw_raw.close()

                else:
                    cls()
                    print("Error")

            elif changelvl == 3:
                cls()
                oldmpw = input("Old Masterpw:\n")
                cls()
                newmpw = input("New Masterpw:\n")

                if newmpw == input("Reapeat new Masterpw:\n"):
                    cls()
                    print("Loading...")
                    oldpw_raw = open("data\\Password\\MPwds\\pw3", "rb")
                    oldpw_lock = oldpw_raw.read()
                    oldpw = simplecrypt.decrypt(oldmpw, oldpw_lock).decode("utf-8")
                    oldpw_raw.close()

                    pw_raw = open("data\\Password\\MPwds\\pw3", "wb")
                    pw_raw.write(simplecrypt.encrypt(newmpw, oldpw))
                    pw_raw.close()

                else:
                    cls()
                    print("Error")

        def pw(listname):
            global pw0, pw1, pw2, pw3, userdata, securityquestion

            title("PW: decoding %s" % listname)
            cls()
            print("Loading...")

            userdata = False
            securityquestion = False

            userdataskip = False
            passwordskip = False
            securityquestionskip = False

            pwlvl = None
            pwfullname = None
            pwemail = None
            pwnumber = None
            pwbdate = None
            pwgender = None
            pwresidence = None
            pwpassword = None
            pwsq1 = None
            pwsq1a = None
            pwsq2 = None
            pwsq2a = None
            pwsq3 = None
            pwsq3a = None

            def userdataac():
                global userdata
                userdata = True

            def securityquestionac():
                global securityquestion
                securityquestion = True

            while True:



                pw_info_raw = open("data\\Password\\Pwds\\%s\\info.txt" % listname, "r")
                pw_info = []
                for pwi in  pw_info_raw:
                    pw_info.append(pwi)
                pw_info_raw.close()
                pwname = pw_info[0]
                pwwebsite = pw_info[1]
                pwtype = pw_info[2]
                try:
                    pwdate = pw_info[3]
                except IndexError:
                    pwdate = None

                if os.path.exists("data\\Password\\Pwds\\%s\\personaldata\\nickname.txt" % listname):
                    pwnick_raw = open("data\\Password\\Pwds\\%s\\personaldata\\nickname.txt" % listname, "r")
                    pwnick = pwnick_raw.read()
                    pwnick_raw.close()
                else:
                    pwnick = None

                if not passwordskip:

                    pwlvl_raw = open("data\\Password\\Pwds\\%s\\pwd\\pwdlvl" % listname, "rb")
                    pwlvl_lock = pwlvl_raw.read()
                    pwlvl_raw.close()

                    pwlvl = int(simplecrypt.decrypt(pw0, pwlvl_lock).decode("utf-8"))

                    if pwlvl == 0:
                        pwpassword_raw = open("data\\Password\\Pwds\\%s\\pwd\\pwd" % listname, "rb")
                        pwpassword_lock = pwpassword_raw.read()
                        pwpassword_raw.close()

                        pwpassword = simplecrypt.decrypt(pw0, pwpassword_lock).decode("utf-8")

                    elif pwlvl == 1:
                        if pw1 is not None:
                            pwpassword_raw = open("data\\Password\\Pwds\\%s\\pwd\\pwd" % listname, "rb")
                            pwpassword_lock = pwpassword_raw.read()
                            pwpassword_raw.close()

                            pwpassword = simplecrypt.decrypt(pw1, pwpassword_lock).decode("utf-8")
                        else:
                            pwpassword = "*locked, please unlock lvl 1*"

                    elif pwlvl == 2:
                        if pw2 is not None:
                            pwpassword_raw = open("data\\Password\\Pwds\\%s\\pwd\\pwd" % listname, "rb")
                            pwpassword_lock = pwpassword_raw.read()
                            pwpassword_raw.close()

                            pwpassword = simplecrypt.decrypt(pw2, pwpassword_lock).decode("utf-8")
                        else:
                            pwpassword = "*locked, please unlock lvl 2*"

                    elif pwlvl == 3:
                        if pw3 is not None:
                            pwpassword_raw = open("data\\Password\\Pwds\\%s\\pwd\\pwd" % listname, "rb")
                            pwpassword_lock = pwpassword_raw.read()
                            pwpassword_raw.close()

                            pwpassword = simplecrypt.decrypt(pw3, pwpassword_lock).decode("utf-8")
                        else:
                            pwpassword = "*locked, please unlock lvl 3*"

                    else:
                        pwpassword = "*Error: lvl not found*"

                    passwordskip = True

                if pwlvl == 1:
                    if pw1 is not None:
                        pwlvlunlock = True
                        a1 = True

                    else:
                        pwlvlunlock = False
                elif pwlvl == 2:
                    if pw2 is not None:
                        pwlvlunlock = True
                    else:
                        pwlvlunlock = False
                elif pwlvl == 3:
                    if pw3 is not None:
                        pwlvlunlock = True
                    else:
                        pwlvlunlock = False

                if not userdataskip:
                    if userdata:
                        if os.path.exists("data\\Password\\Pwds\\%s\\personaldata\\name" % listname):
                            pwfullname_raw = open("data\\Password\\Pwds\\%s\\personaldata\\name" % listname, "rb")
                            pwfullname_lock = pwfullname_raw.read()
                            pwfullname_raw.close()
                            if pwlvl == 0:
                                pwfullname = simplecrypt.decrypt(pw0, pwfullname_lock).decode("utf-8")
                            elif pwlvl == 1:
                                if pw1 is not None:
                                    pwfullname = simplecrypt.decrypt(pw1, pwfullname_lock).decode("utf-8")
                                else:
                                    pwfullname = "*locked, please unlock lvl 1*"
                            elif pwlvl == 2:
                                if pw2 is not None:
                                    pwfullname = simplecrypt.decrypt(pw2, pwfullname_lock).decode("utf-8")
                                else:
                                    pwfullname = "*locked, please unlock lvl 2*"
                            elif pwlvl == 3:
                                if pw3 is not None:
                                    pwfullname = simplecrypt.decrypt(pw3, pwfullname_lock).decode("utf-8")
                                else:
                                    pwfullname = "*locked, please unlock lvl 3*"
                        else:
                            pwfullname = None

                        if os.path.exists("data\\Password\\Pwds\\%s\\personaldata\\email" % listname):
                            pwemail_raw = open("data\\Password\\Pwds\\%s\\personaldata\\email" % listname, "rb")
                            pwemail_lock = pwemail_raw.read()
                            pwemail_raw.close()
                            if pwlvl == 0:
                                pwemail = simplecrypt.decrypt(pw0, pwemail_lock).decode("utf-8")
                            elif pwlvl == 1:
                                if pw1 is not None:
                                    pwemail = simplecrypt.decrypt(pw1, pwemail_lock).decode("utf-8")
                                else:
                                    pwemail = "*locked, please unlock lvl 1*"
                            elif pwlvl == 2:
                                if pw2 is not None:
                                    pwemail = simplecrypt.decrypt(pw2, pwemail_lock).decode("utf-8")
                                else:
                                    pwemail = "*locked, please unlock lvl 2*"
                            elif pwlvl == 3:
                                if pw3 is not None:
                                    pwemail = simplecrypt.decrypt(pw3, pwemail_lock).decode("utf-8")
                                else:
                                    pwemail = "*locked, please unlock lvl 3*"
                        else:
                            pwemail = None

                        if os.path.exists("data\\Password\\Pwds\\%s\\personaldata\\pnumber" % listname):
                            pwnumber_raw = open("data\\Password\\Pwds\\%s\\personaldata\\pnumber" % listname, "rb")
                            pwnumber_lock = pwnumber_raw.read()
                            pwnumber_raw.close()

                            if pwlvl == 0:
                                pwnumber = simplecrypt.decrypt(pw0, pwnumber_lock).decode("utf-8")
                            elif pwlvl == 1:
                                if pw1 is not None:
                                    pwnumber = simplecrypt.decrypt(pw1, pwnumber_lock).decode("utf-8")
                                else:
                                    pwnumber = "*locked, please unlock lvl 1*"
                            elif pwlvl == 2:
                                if pw2 is not None:
                                    pwnumber = simplecrypt.decrypt(pw2, pwnumber_lock).decode("utf-8")
                                else:
                                    pwnumber = "*locked, please unlock lvl 3*"
                            elif pwlvl == 3:
                                if pw3 is not None:
                                    pwnumber = simplecrypt.decrypt(pw3, pwnumber_lock).decode("utf-8")
                                else:
                                    pwnumber = "*locked, please unlock lvl 3*"
                        else:
                            pwnumber = None

                        if os.path.exists("data\\Password\\Pwds\\%s\\personaldata\\bdate" % listname):
                            pwbdate_raw = open("data\\Password\\Pwds\\%s\\personaldata\\bdate" % listname, "rb")
                            pwbdate_lock = pwbdate_raw.read()
                            pwbdate_raw.close()

                            if pwlvl == 0:
                                pwbdate = simplecrypt.decrypt(pw0, pwbdate_lock).decode("utf-8")
                            elif pwlvl == 1:
                                if pw1 is not None:
                                    pwbdate = simplecrypt.decrypt(pw1, pwbdate_lock).decode("utf-8")
                                else:
                                    pwbdate = "*locked, please unlock lvl 1*"
                            elif pwlvl == 2:
                                if pw2 is not None:
                                    pwbdate = simplecrypt.decrypt(pw2, pwbdate_lock).decode("utf-8")
                                else:
                                    pwbdate = "*locked, please unlock lvl 2*"
                            elif pwlvl == 3:
                                if pw3 is not None:
                                    pwbdate = simplecrypt.decrypt(pw3, pwbdate_lock).decode("utf-8")
                                else:
                                    pwbdate = "*locked, please unlock lvl 3*"
                        else:
                            pwbdate = None

                        if os.path.exists("data\\Password\\Pwds\\%s\\personaldata\\gender" % listname):
                            pwgender_raw = open("data\\Password\\Pwds\\%s\\personaldata\\gender" % listname, "rb")
                            pwgender_lock = pwgender_raw.read()
                            pwgender_raw.close()

                            if pwlvl == 0:
                                pwgender = simplecrypt.decrypt(pw0, pwgender_lock).decode("utf-8")
                            elif pwlvl == 1:
                                if pw1 is not None:
                                    pwgender = simplecrypt.decrypt(pw1, pwgender_lock).decode("utf-8")
                                else:
                                    pwgender = "*locked, please unlock lvl 1*"
                            elif pwlvl == 2:
                                if pw2 is not None:
                                    pwgender = simplecrypt.decrypt(pw2, pwgender_lock).decode("utf-8")
                                else:
                                    pwgender = "*locked, please unlock lvl 2*"
                            elif pwlvl == 3:
                                if pw3 is not None:
                                    pwgender = simplecrypt.decrypt(pw3, pwgender_lock).decode("utf-8")
                                else:
                                    pwgender = "*locked, please unlock lvl 3*"
                        else:
                            pwgender = None

                        if os.path.exists("data\\Password\\Pwds\\%s\\personaldata\\residence" % listname):
                            pwresidence_raw = open("data\\Password\\Pwds\\%s\\personaldata\\residence" % listname, "rb")
                            pwresidence_lock = pwresidence_raw.read()
                            pwresidence_raw.close()

                            if pwlvl == 0:
                                pwresidence = simplecrypt.decrypt(pw0, pwresidence_lock).decode("utf-8")
                            elif pwlvl == 1:
                                if pw1 is not None:
                                    pwresidence = simplecrypt.decrypt(pw1, pwresidence_lock).decode("utf-8")
                                else:
                                    pwresidence = "*locked, please unlock lvl 1*"
                            elif pwlvl == 2:
                                if pw2 is not None:
                                    pwresidence = simplecrypt.decrypt(pw2, pwresidence_lock).decode("utf-8")
                                else:
                                    pwresidence = "*locked, please unlock lvl 2*"
                            elif pwlvl == 3:
                                if pw3 is not None:
                                    pwresidence = simplecrypt.decrypt(pw3, pwresidence_lock).decode("utf-8")
                                else:
                                    pwresidence = "*locked, please unlock lvl 3*"
                        else:
                            pwresidence = None

                        userdataskip = True

                    else:
                        pwfullname = None
                        pwemail = None
                        pwnumber = None
                        pwbdate = None
                        pwgender = None
                        pwresidence = None





                if not securityquestionskip:
                    if os.path.exists("data\\Password\\Pwds\\%s\\pwd\\sq1.txt" % listname):
                        pwsq1_raw = open("data\\Password\\Pwds\\%s\\personaldata\\sq1.txt" % listname, "r")
                        pwsq1 = pwsq1_raw.read()
                        pwsq1_raw.close()


                        pwsq1a_raw = open("data\\Password\\Pwds\\%s\\personaldata\\sq1a" % listname, "rb")
                        pwsq1a_lock = pwsq1a_raw.read()
                        pwsq1a_raw.close()

                        if pwlvl == 0:
                            pwsq1a = simplecrypt.decrypt(pw0, pwsq1a_lock).decode("utf-8")
                        elif pwlvl == 1:
                            pwsq1a = simplecrypt.decrypt(pw1, pwsq1a_lock).decode("utf-8")
                        elif pwlvl == 2:
                            pwsq1a = simplecrypt.decrypt(pw2, pwsq1a_lock).decode("utf-8")
                        elif pwlvl == 3:
                            pwsq1a = simplecrypt.decrypt(pw3, pwsq1a_lock).decode("utf-8")
                        else:
                            pwsq1a = "*Error: lvl not found*"


                        if os.path.exists("data\\Password\\Pwds\\%s\\pwd\\sq2.txt" % listname):
                            pwsq2_raw = open("data\\Password\\Pwds\\%s\\personaldata\\sq2.txt" % listname, "r")
                            pwsq2 = pwsq2_raw.read()
                            pwsq2_raw.close()

                            pwsq2a_raw = open("data\\Password\\Pwds\\%s\\personaldata\\sq2a" % listname, "rb")
                            pwsq2a_lock = pwsq2a_raw.read()
                            pwsq2a_raw.close()

                            if pwlvl == 0:
                                pwsq2a = simplecrypt.decrypt(pw0, pwsq2a_lock).decode("utf-8")
                            elif pwlvl == 1:
                                pwsq2a = simplecrypt.decrypt(pw1, pwsq2a_lock).decode("utf-8")
                            elif pwlvl == 2:
                                pwsq2a = simplecrypt.decrypt(pw2, pwsq2a_lock).decode("utf-8")
                            elif pwlvl == 3:
                                pwsq2a = simplecrypt.decrypt(pw3, pwsq2a_lock).decode("utf-8")
                            else:
                                pwsq2a = "*Error: lvl not found*"

                            if os.path.exists("data\\Password\\Pwds\\%s\\pwd\\sq3.txt" % listname):
                                pwsq3_raw = open("data\\Password\\Pwds\\%s\\personaldata\\sq3.txt" % listname, "r")
                                pwsq3 = pwsq3_raw.read()
                                pwsq3_raw.close()

                                pwsq3a_raw = open("data\\Password\\Pwds\\%s\\personaldata\\sq3a" % listname, "rb")
                                pwsq3a_lock = pwsq3a_raw.read()
                                pwsq3a_raw.close()

                                if pwlvl == 0:
                                    pwsq3a = simplecrypt.decrypt(pw0, pwsq3a_lock).decode("utf-8")
                                elif pwlvl == 1:
                                    pwsq3a = simplecrypt.decrypt(pw1, pwsq3a_lock).decode("utf-8")
                                elif pwlvl == 2:
                                    pwsq3a = simplecrypt.decrypt(pw2, pwsq3a_lock).decode("utf-8")
                                elif pwlvl == 3:
                                    pwsq3a = simplecrypt.decrypt(pw3, pwsq3a_lock).decode("utf-8")
                                else:
                                    pwsq3a = "*Error: lvl not found*"





                    securityquestionskip = True

                if os.path.exists("data\\Password\\Pwds\\%s\\comment.txt" % listname):
                    pwcomment_raw = open("data\\Password\\Pwds\\%s\\comment.txt" % listname, "r")
                    pwcomment = pwcomment_raw.read()
                    pwcomment_raw.close()
                else:
                    pwcomment = None


                title("PW: %s" % listname)

                cls()


                print("%s:\n" % pwname.rstrip("\n"))
                print("Website:\t  %s" % pwwebsite.rstrip("\n"))
                print("Type:\t\t  %s" % pwtype)
                if pwdate is not None:
                    print("Date of sign up:  %s\n" % pwdate)
                if pwnick is not None:
                    print("Nickname:\t  %s" % pwnick)
                if pwfullname is not None:
                    print("Fullname:\t  %s" % pwfullname)
                if pwemail is not None:
                    print("E-Mail:\t\t  %s" % pwemail)
                if pwnumber is not None:
                    print("Phonenummber:\t  %s" % pwnumber)
                if pwbdate is not None:
                    print("Birthdate:\t  %s" % pwbdate)
                if pwgender is not None:
                    print("Gender:\t\t  %s" % pwgender)
                if pwresidence is not None:
                    print("Residence:\t  %s" % pwresidence)

                print("\nPassword:\n%s\n" % pwpassword)

                if pwsq1 is not None:
                    print("Security Question 1:\n%s" % pwsq1)
                    print("Security Question 1 answer:\n%s" % pwsq1a)
                if pwsq2 is not None:
                    print("Security Question 2:\n%s" % pwsq2)
                    print("Security Question 2 answer:\n%s" % pwsq2a)
                if pwsq3 is not None:
                    print("Security Question 3:\n%s" % pwsq3)
                    print("Security Question 3 answer:\n%s" % pwsq3a)
                if pwcomment is not None:
                    print("Comment:\n%s" % pwcomment)

                user_input_pw = input("\n\n")

                if user_input_pw.lower() == "unlock":
                    unlock()
                    passwordskip = False
                    userdataskip = False
                    securityquestionskip = False
                elif user_input_pw.lower() == "unlock1":
                    unlock(1)
                    passwordskip = False
                    userdataskip = False
                    securityquestionskip = False
                elif user_input_pw.lower() == "unlock2":           
                    unlock(2)                                      
                    passwordskip = False
                    userdataskip = False
                    securityquestionskip = False
                elif user_input_pw.lower() == "unlock3":           
                    unlock(3)                                      
                    passwordskip = False
                    userdataskip = False
                    securityquestionskip = False
                elif user_input_pw.lower() == "ud":                
                    userdataac()                                   
                    cls()                                          
                    print("Loading...")
                    userdataskip = False                           
                elif user_input_pw.lower() == "sq":                
                    securityquestionac()                           
                    cls()
                    print("Loading...")
                    securityquestionskip = False
                else:
                    break


        unlock(0)

        pwlist_raw = open("data\\Password\\list.txt", "r")
        pwlist = []
        for xl in pwlist_raw:
            pwlist.append(xl)
        pwlist_raw.close()

        cls()
        print("Commands:\nCreate a new password (CREA), Delete a password (DEL), Unlock pw (UNLOCK)\n\nPasswords:\n") # geheim: change masterpw (mpw)
        for xl in pwlist:
            print(xl.rstrip("\n"))

        user_input_p = input("\n")

        if user_input_p.lower() == "crea":
            creapw()
        elif user_input_p.lower() == "del":
            delpw()
        elif user_input_p.lower() == "mpw":
            chmpw()
        elif user_input_p.lower() == "unlock":
            unlock()
        elif user_input_p.lower() == "unlock1":
            unlock(1)
        elif user_input_p.lower() == "unlock2":
            unlock(2)
        elif user_input_p.lower() == "unlock3":
            unlock(3)

        for xl in pwlist:
            if user_input_p == xl.rstrip("\n"):
                pw(user_input_p)
    cls()

    print("Password:\n")

    if input() == "Luis":
        start()




class SplatoonC:
    def __init__(self):
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
        self.TimeLeft = 180 - self.TimeLeftC.getTime()
        self.TimeLeft = 180 - round(time.time() - self.TimeLeftStart)

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

        if self.TimeLeft == 0:
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



def Splatoon():
    spl = SplatoonC()

    class Printerr(threading.Thread):
        def run(self):
            while spl.RUN:
                cls()
                spl.printIt()
                time.sleep(1)

    Printer = Printerr()
    Printer.start()

    while spl.RUN:
        user_input = input()
        spl.input(user_input)

def main():
    version()
    title("Waiting for Input")

    cls()
    user_input = input("What to do?\nNotepad (NP), Light (L), Upgrade (UG)\n\n")

    if user_input.lower() == "np":
        np()
    if user_input.lower() == "npnow":
        np("now")
    if user_input.lower() == "npfox":
        np("fox")
    if user_input.lower() == "npfoxpage":
        np("foxpage")
    if user_input.lower() == "npfoxname":
        np("foxname")
    if user_input.lower() == "npshota":
        np("shota")
    if user_input.lower() == "l":
        color.Man()
    if user_input.lower() == "ug":
        upgrade()
    if user_input.lower() == "debug":
        debug()
    if user_input.lower() == "games":
        games()
    if user_input.lower() == "snake":
        games("snake")
    if user_input.lower() == "music":
        Music()
    if user_input.lower() == "time":
        Timeprint()
    if user_input.lower() == "randpw":
        randompw()
    if user_input.lower() == "pw":
        passwordmanager()


def Arg():
    global ttime_stop

    skiparg = []

    for x in range(5):
        try:
            sys.argv[x]
        except IndexError:
            sys.argv.append(None)
            skiparg.append(x)
    test = []
    if not skiparg:
        skiparg.append(4)

    for x in range(1, 4):
        if x >= skiparg[0]:
            break
        if sys.argv[x] == "-l_dark":
            title("Load Argument", "Argument: Dark")
            color.change("07")
        if sys.argv[x] == "-l_bright":
            title("Load Argument", "Argument: Bright")
            color.change("F0")
        if sys.argv[x] == "-np_fox":
            title("Load Argument", "Notie: FOX")
            ttime_stop = False
            np("fox")
            exit_now()
        if sys.argv[x] == "-np_foxpage":
            title("Load Argument", "Notie: FOXPAGE")
            ttime_stop = False
            np("foxpage")
            exit_now()
        if sys.argv[x] == "-np_foxname":
            title("Load Argument", "Notie: FOXNAME")
            ttime_stop = False
            np("foxname")
            exit_now()
        if sys.argv[x] == "-np_notie":
            title("Load Argument", "Notie: Notie")
            np("Man")
        if sys.argv[x] == "-np_now":
            title("Load Argument", "Notie: NOW")
            ttime_stop = False
            np("now")
            exit_now()
        if sys.argv[x] == "-np_shota":
            title("Load Argument", "Notie: SHOTA")
            ttime_stop = False
            np("shota")
            exit_now()
        if sys.argv[x] == "-nc_stdsize":
            title("Load Argument", "Nircmd: Standard size")
            nircmd("setsize", 1000, 520)
        if sys.argv[x] == "-tt_freq":
            title("Load Argument", "TTime: Change Freq")
            title_time.freq = float(sys.argv[x + 1])
        if sys.argv[x] == "-tt_deac":
            title("Load Argument", "TTime: Deactivate")
            ttime_stop = False
        if sys.argv[x] == "-update":
            title("Load Argument", "Updater: Updating")
            update()
        if sys.argv[x] == "-upgrade":
            title("Load Argument", "Updater: Upgrading")
            upgrade()
        if sys.argv[x] == "-screensaver":
            title("Load Argument", "Screensaver")
            screensaver()
        if sys.argv[x] == "-ep_switch":
            title("Load Argument", "Switch Energy Plan")
            ttime_stop = False
            Tools.EnergyPlan.Switch()
            Tools.EnergyPlan.getEP(True)
            time.sleep(2)
            exit_now()
        if sys.argv[x] == "-shutdown":
            title("Load Argument", "Shutdown")
            ttime_stop = False
            Tools.Shutdown()
            exit_now()
        if sys.argv[x] == "-reboot":
            title("Load Argument", "Shutdown")
            ttime_stop = False
            Tools.Reboot()
            exit_now()
        if sys.argv[x] == "-start_server":
            global StartupServer
            title("Server", " ", " ")
            ttime_stop = False
            serverport = int(sys.argv[x + 1])
            if not sys.argv[x + 2] == "-app":
                killConsole()
            StartupServer = ServerC(thisIP, serverport, reac=StartupServerTasks, reacSendData=True, mess=True)
            StartupServer.start()


if sys.argv:
    Arg()


if exitnow == 0:
    if __name__ == "__main__":
        title("Search for Updates")
        update()
        title("Start Enviroment")
        main()
        time.sleep(0)

        exit_now()


