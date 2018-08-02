import time
#from cls import *
import ctypes
import os
import sys
import datetime
import socket
import subprocess
import shutil
#from IPython.core.autocall import ExitAutocall
import EveconExceptions
import psutil
import threading

def cls():
    os.system("cls")

def exit_now():
    global ttime_stop
    ttime_stop = 1
    global exitnow
    exitnow = 1
    if version_PC != 1:
        exit()

WORK = True

class ddbug(threading.Thread):
    def run(self):
        global WORK
        while WORK:
            time.sleep(1)

ddbugger = ddbug()
ddbugger.start()

cdir = os.getcwd()
if cdir == "C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\Programs\\Evecon\\Updater":
    os.chdir("..")
    os.chdir("..")
    os.chdir("..")
else:
    os.chdir("..")

title_oldstatus = "Loading"
title_oldstart = ""
exitnow = 0
Alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z", ]


def title(status="OLD", something="OLD"):
    global title_oldstatus, title_oldstart
    if status == "OLD":
        status = title_oldstatus
    else:
        title_oldstatus = status

    if something == "OLD":
        something = title_oldstart
    else:
        title_oldstart = something

    space_status = (60 - len(status) * 2) * " "

    ctypes.windll.kernel32.SetConsoleTitleW("EVECON Updater: %s%s%s" %
                                            (status, space_status, something))


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

def computerconfig_schoolpc():
    pass


def computerconfig_minipc():
    pass


def computerconfig_bigpc():
    pass


def computerconfig_aldi():
    pass


def computerconfig_laptop():
    pass


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
    title("OLD", "OLD")
    Computerfind_MiniPC = 1
    Computerfind_BigPC = 0
    Computerfind_PapaAldi = 0
    Computerfind_Laptop = 0

elif Computername == "XX":
    title("OLD", "OLD")
    Computerfind_MiniPC = 0
    Computerfind_BigPC = 1
    Computerfind_PapaAldi = 0
    Computerfind_Laptop = 0

elif Computername == "Test":
    title("OLD", "OLD")
    Computerfind_MiniPC = 0
    Computerfind_BigPC = 0
    Computerfind_PapaAldi = 1
    Computerfind_Laptop = 0

elif Computername == "Luis":
    title("OLD", "OLD")
    Computerfind_MiniPC = 0
    Computerfind_BigPC = 0
    Computerfind_PapaAldi = 0
    Computerfind_Laptop = 1

else:
    title("OLD", "OLD")
    Computerfind_MiniPC = 0
    Computerfind_BigPC = 0
    Computerfind_PapaAldi = 0
    Computerfind_Laptop = 0

file_proversion_raw = open("data\\Info\\ProgramVersion", "r")
ProVersion = file_proversion_raw.readline()
file_proversion_raw.close()

if ProVersion == "PC-Version":
    if Computerfind_MiniPC == 1:
        version_PC = 1
        version_MiniPC = 1
        version_BigPC = 0
        version_MainStick = 0
        version_MiniStick = 0
    if Computerfind_BigPC == 1:
        version_PC = 1
        version_MiniPC = 0
        version_BigPC = 1
        version_MainStick = 0
        version_MiniStick = 0
elif ProVersion == "MainStick-Version":
    version_PC = 0
    version_MiniPC = 0
    version_BigPC = 0
    version_MainStick = 1
    version_MiniStick = 0
elif ProVersion == "MiniStick-Version":
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

title("Loading Arguments")


def Evecons(findversions=0):
    global Evecons_multi, Evecons_mainstick, Evecons_mainstick_path, Evecons_mainstick_pathkey, Evecons_PC, Evecons_PC_path, Evecons_ministick, Evecons_ministick_path, Evecons_ministick_pathkey

    global mainstickversion, ministickversion, PCversion

    Eveconss = []
    Evecons_multi = 0
    Evecons_mainstick = 0
    Evecons_mainstick_path = 0
    Evecons_mainstick_pathkey = 0
    Evecons_PC = 0
    if os.path.isfile("C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\data\\Info\\exist"):
        Evecons_PC_path = "C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon"
    elif os.path.isfile(""):  # BigPC noch einfügen
        Evecons_PC_path = ""
    Evecons_ministick = 0
    Evecons_ministick_path = 0
    Evecons_ministick_pathkey = 0

    mainstickversion = []
    ministickversion = []
    PCversion = []

    for Alpha in Alphabet:
        if os.path.isfile("%s:\\Evecon\\data\\Info\\exist" % Alpha):
            file_proversionstick_raw = open("data\\Info\\ProgramVersion", "r")
            proversionunkownstick = file_proversionstick_raw.readline()
            file_proversionstick_raw.close()

            if proversionunkownstick == "MainStick-Version":

                Eveconss.append("MainStick")
                Evecons_mainstick = 1
                Evecons_mainstick_pathkey = Alpha
                Evecons_mainstick_path = ("%s:\\Evecon" % Alpha)

                def mainstick_version():
                    file_mainstick_version_raw = open("%s:\\Evecon\\data\\Info\\version" % Evecons_mainstick_pathkey,
                                                      "r")
                    for x in file_mainstick_version_raw:
                        mainstickversion.append(x.strip())
                    file_mainstick_version_raw.close()

                if findversions == 1:
                    mainstick_version()

            if proversionunkownstick == "MiniStick-Version":

                Eveconss.append("MiniStick")
                Evecons_ministick = 1
                Evecons_ministick_pathkey = Alpha
                Evecons_ministick_path = ("%s:\\Evecon" % Alpha)

                def ministick_version():
                    file_ministick_version_raw = open("%s:\\Evecon\\data\\Info\\version" % Evecons_ministick_pathkey,
                                                      "r")
                    for x in file_ministick_version_raw:
                        ministickversion.append(x.strip())
                    file_ministick_version_raw.close()

                if findversions == 1:
                    ministick_version()

    if version_MainStick == 1:
        if os.path.isfile("C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\data\\Info\\exist"):

            Eveconss.append("PC")
            Evecons_PC = 1

            def PC_version():
                file_PC_version_raw = open("C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\data\\Info\\version", "r")
                for x in file_PC_version_raw:
                    PCversion.append(x.strip())
                file_PC_version_raw.close()

            if findversions == 1:
                PC_version()

        elif os.path.isfile(""):  # BigPC einfügen

            Eveconss.append("PC")
            Evecons_PC = 1

            def PC_version():
                file_PC_version_raw = open("", "r")
                for x in file_PC_version_raw:
                    PCversion.append(x.strip())
                file_PC_version_raw.close()

            if findversions == 1:
                PC_version()

    if version_MiniStick == 1:
        if os.path.isfile("C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\data\\Info\\exist"):

            Eveconss.append("PC")
            Evecons_PC = 1

            def PC_version():
                file_PC_version_raw = open("C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\data\\Info\\version", "r")
                for x in file_PC_version_raw:
                    PCversion.append(x.strip())
                file_PC_version_raw.close()

            if findversions == 1:
                PC_version()

        elif os.path.isfile(""):  # BigPC einfügen

            Eveconss.append("PC")
            Evecons_PC = 1

            def PC_version():
                file_PC_version_raw = open("", "r")
                for x in file_PC_version_raw:
                    PCversion.append(x.strip())
                file_PC_version_raw.close()

            if findversions == 1:
                PC_version()

    if len(Eveconss) >= 2:
        Evecons_multi = 1


def version():
    file_version_raw = open("data\\Info\\version", "r")
    global this_version
    this_version = []
    for xcc in file_version_raw:
        this_version.append(xcc.strip())
    file_version_raw.close()


def update():
    cls()
    version()
    global this_version
    global mainstickversion, ministickversion, PCversion

    Evecons(1)

    global Evecons_multi, Evecons_mainstick, Evecons_mainstick_path, Evecons_PC, Evecons_PC_path, Evecons_ministick, Evecons_ministick_path, restart

    def this_to_PC():
        backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_PC_path, "w")  # von diesem auf PC
        backuptime.write("Backup:\nFrom: %s\nTo: Mini-PC\nDate: %s\nTime: %s\nVersion: %s" % (
            ProVersion.rstrip("-Version"), datetime.datetime.now().strftime("%d.%m.%Y"),
            datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
        backuptime.close()
        shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_PC_path)
        shutil.copytree("%s\\!Evecon" % Evecons_PC_path, "%s\\data\\Backup\\!Evecon" % Evecons_PC_path)
        shutil.rmtree("%s\\!Evecon" % Evecons_PC_path)
        shutil.copytree("!Evecon", "%s" % Evecons_PC_path)
        shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_PC_path)
        shutil.copytree("%s\\data\\Notepad" % Evecons_PC_path, "%s\\data\\Backup\\data\\Notepad" % Evecons_PC_path)
        shutil.rmtree("%s\\data\\Notepad" % Evecons_PC_path)
        shutil.copytree("data\\Notepad", "%s\\data\\Notepad" % Evecons_PC_path)

        os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_PC_path)
        shutil.copy("%s\\data\\Info\\version" % Evecons_PC_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_PC_path)
        os.remove("%s\\data\\Info\\version" % Evecons_PC_path)
        shutil.copy("data\\Info\\version", "%s\\data\\Info" % Evecons_PC_path)
        os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_PC_path)
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_PC_path)
        os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path)
        shutil.copy("data\\Info\\Changelog.txt", "%s\\data\\Info" % Evecons_PC_path)

    def PC_to_this():
        backuptime = open("data\\Backup\\backup.txt", "w")  # von PC auf diesen
        backuptime.write("Backup:\nFrom: Mini-PC\nTo: %s\nDate: %s\nTime: %s\nVersion: %s" % (
            ProVersion.rstrip("-Version"), datetime.datetime.now().strftime("%d.%m.%Y"),
            datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
        backuptime.close()
        shutil.rmtree("data\\Backup\\!Evecon")
        shutil.copytree("!Evecon", "data\\Backup\\!Evecon")
        shutil.rmtree("!Evecon")
        shutil.copytree("%s\\!Evecon" % Evecons_PC_path, "!Evecon")
        shutil.rmtree("data\\Backup\\data\\Notepad")
        shutil.copytree("data\\Notepad", "data\\Backup\\data\\Notepad")
        shutil.rmtree("data\\Notepad")
        shutil.copytree("%s\\data\\Notepad" % Evecons_PC_path, "data\\Notepad")

        os.remove("data\\Backup\\data\\Info\\version")
        shutil.copy("data\\Info\\version", "data\\Backup\\data\\Info")
        os.remove("data\\Info\\version")
        shutil.copy("%s\\data\\Info\\version" % Evecons_PC_path, "data\\Info")
        os.remove("data\\Backup\\data\\Info\\Changelog.txt")
        shutil.copy("data\\Info\\Changelog.txt", "data\\Backup\\data\\Info")
        os.remove("data\\Info\\Changelog.txt")
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path, "data\\Info")

    def this_to_Mainstick():
        backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_mainstick_path, "w")  # von diesem auf Mainstick
        backuptime.write("Backup:\nFrom: %s\nTo: Mainstick\nDate: %s\nTime: %s\nVersion: %s" % (
            ProVersion.rstrip("-Version"), datetime.datetime.now().strftime("%d.%m.%Y"),
            datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
        backuptime.close()
        shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_mainstick_path)
        shutil.copytree("%s\\!Evecon" % Evecons_mainstick_path,
                        "%s\\data\\Backup\\!Evecon" % Evecons_mainstick_path)
        shutil.rmtree("%s\\!Evecon" % Evecons_mainstick_path)
        shutil.copytree("!Evecon", "%s\\!Evecon" % Evecons_mainstick_path)
        shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_mainstick_path)
        shutil.copytree("%s\\data\\Notepad" % Evecons_mainstick_path,
                        "%s\\data\\Backup\\data\\Notepad" % Evecons_mainstick_path)
        shutil.rmtree("%s\\data\\Notepad" % Evecons_mainstick_path)
        shutil.copytree("data\\Notepad", "%s\\data\\Notepad" % Evecons_mainstick_path)

        os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_mainstick_path)
        shutil.copy("%s\\data\\Info\\version" % Evecons_mainstick_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_mainstick_path)
        os.remove("%s\\data\\Info\\version" % Evecons_mainstick_path)
        shutil.copy("data\\Info\\version", "%s\\data\\Info" % Evecons_mainstick_path)
        os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_mainstick_path)
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_mainstick_path)
        os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path)
        shutil.copy("data\\Info\\Changelog.txt", "%s\\data\\Info" % Evecons_mainstick_path)

    def Mainstick_to_this():
        backuptime = open("data\\Backup\\backup.txt", "w")  # von Mainstick auf diesen
        backuptime.write("Backup:\nFrom: Mainstick\nTo: %s\nDate: %s\nTime: %s\nVersion: %s" % (
            ProVersion.rstrip("-Version"), datetime.datetime.now().strftime("%d.%m.%Y"),
            datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
        backuptime.close()
        shutil.rmtree("data\\Backup\\!Evecon")
        shutil.copytree("!Evecon", "data\\Backup\\!Evecon")
        shutil.rmtree("!Evecon")
        shutil.copytree("%s\\!Evecon" % Evecons_mainstick_path, "!Evecon")
        shutil.rmtree("data\\Backup\\data\\Notepad")
        shutil.copytree("data\\Notepad", "data\\Backup\\data\\Notepad")
        shutil.rmtree("data\\Notepad")
        shutil.copytree("%s\\data\\Notepad" % Evecons_mainstick_path, "data\\Notepad")

        os.remove("data\\Backup\\data\\Info\\version")
        shutil.copy("data\\Info\\version", "data\\Backup\\data\\Info")
        os.remove("data\\Info\\version")
        shutil.copy("%s\\data\\Info\\version" % Evecons_mainstick_path, "data\\Info")
        os.remove("data\\Backup\\data\\Info\\Changelog.txt")
        shutil.copy("data\\Info\\Changelog.txt", "data\\Backup\\data\\Info")
        os.remove("data\\Info\\Changelog.txt")
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path, "data\\Info")

    def this_to_Ministick():
        backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_ministick_path, "w")  # von diesem auf Ministick
        backuptime.write("Backup:\nFrom: %s\nTo: Ministick-PC\nDate: %s\nTime: %s\nVersion: %s" % (
            ProVersion.rstrip("-Version"), datetime.datetime.now().strftime("%d.%m.%Y"),
            datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
        backuptime.close()
        shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_ministick_path)
        shutil.copytree("%s\\!Evecon" % Evecons_ministick_path,
                        "%s\\data\\Backup\\!Evecon" % Evecons_ministick_path)
        shutil.rmtree("%s\\!Evecon" % Evecons_ministick_path)
        shutil.copytree("!Evecon", "%s\\!Evecon" % Evecons_ministick_path)
        shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_ministick_path)
        shutil.copytree("%s\\data\\Notepad" % Evecons_ministick_path,
                        "%s\\data\\Backup\\data\\Notepad" % Evecons_ministick_path)
        shutil.rmtree("%s\\data\\Notepad" % Evecons_ministick_path)
        shutil.copytree("data\\Notepad", "%s\\data\\Notepad" % Evecons_ministick_path)

        os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_ministick_path)
        shutil.copy("%s\\data\\Info\\version" % Evecons_ministick_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_ministick_path)
        os.remove("%s\\data\\Info\\version" % Evecons_ministick_path)
        shutil.copy("data\\Info\\version", "%s\\data\\Info" % Evecons_ministick_path)
        os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_ministick_path)
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_ministick_path)
        os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path)
        shutil.copy("data\\Info\\Changelog.txt", "%s\\data\\Info" % Evecons_ministick_path)

    def Ministick_to_this():
        backuptime = open("data\\Backup\\backup.txt", "w")  # von Ministick auf diesen
        backuptime.write("Backup:\nFrom: Ministick\nTo: %s\nDate: %s\nTime: %s\nVersion: %s" % (
            ProVersion.rstrip("-Version"), datetime.datetime.now().strftime("%d.%m.%Y"),
            datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
        backuptime.close()
        shutil.rmtree("data\\Backup\\!Evecon")
        shutil.copytree("!Evecon", "data\\Backup\\!Evecon")
        shutil.rmtree("!Evecon")
        shutil.copytree("%s\\!Evecon" % Evecons_ministick_path, "!Evecon")
        shutil.rmtree("data\\Backup\\data\\Notepad")
        shutil.copytree("data\\Notepad", "data\\Backup\\data\\Notepad")
        shutil.rmtree("data\\Notepad")
        shutil.copytree("%s\\data\\Notepad" % Evecons_ministick_path, "data\\Notepad")

        os.remove("data\\Backup\\data\\Info\\version")
        shutil.copy("data\\Info\\version", "data\\Backup\\data\\Info")
        os.remove("data\\Info\\version")
        shutil.copy("%s\\data\\Info\\version" % Evecons_ministick_path, "data\\Info")
        os.remove("data\\Backup\\data\\Info\\Changelog.txt")
        shutil.copy("data\\Info\\Changelog.txt", "data\\Backup\\data\\Info")
        os.remove("data\\Info\\Changelog.txt")
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path, "data\\Info")

    def PC_to_Mainstick():
        backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_mainstick_path, "w")  # von PC auf Mainstick
        backuptime.write("Backup:\nFrom: PC\nTo: Mainstick\nDate: %s\nTime: %s\nVersion: %s" % (
            datetime.datetime.now().strftime("%d.%m.%Y"),
            datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
        backuptime.close()
        shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_mainstick_path)
        shutil.copytree("%s\\!Evecon" % Evecons_mainstick_path,
                        "%s\\data\\Backup\\!Evecon" % Evecons_mainstick_path)
        shutil.rmtree("%s\\!Evecon" % Evecons_mainstick_path)
        shutil.copytree("%s\\!Evecon" % Evecons_PC_path, "%s\\!Evecon" % Evecons_mainstick_path)
        shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_mainstick_path)
        shutil.copytree("%s\\data\\Notepad" % Evecons_mainstick_path,
                        "%s\\data\\Backup\\data\\Notepad" % Evecons_mainstick_path)
        shutil.rmtree("%s\\data\\Notepad" % Evecons_mainstick_path)
        shutil.copytree("%s\\data\\Notepad" % Evecons_PC_path, "%s\\data\\Notepad" % Evecons_mainstick_path)

        os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_mainstick_path)
        shutil.copy("%s\\data\\Info\\version" % Evecons_mainstick_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_mainstick_path)
        os.remove("%s\\data\\Info\\version" % Evecons_mainstick_path)
        shutil.copy("%s\\data\\Info\\version" % Evecons_PC_path, "%s\\data\\Info" % Evecons_mainstick_path)
        os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_mainstick_path)
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_mainstick_path)
        os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path)
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path, "%s\\data\\Info" % Evecons_mainstick_path)

    def PC_to_Ministick():
        backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_ministick_path, "w")  # von PC auf Ministick
        backuptime.write("Backup:\nFrom: PC\nTo: Ministick\nDate: %s\nTime: %s\nVersion: %s" % (
            datetime.datetime.now().strftime("%d.%m.%Y"),
            datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
        backuptime.close()
        shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_ministick_path)
        shutil.copytree("%s\\!Evecon" % Evecons_ministick_path,
                        "%s\\data\\Backup\\!Evecon" % Evecons_ministick_path)
        shutil.rmtree("%s\\!Evecon" % Evecons_ministick_path)
        shutil.copytree("%s\\!Evecon" % Evecons_PC_path, "%s\\!Evecon" % Evecons_ministick_path)
        shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_ministick_path)
        shutil.copytree("%s\\data\\Notepad" % Evecons_ministick_path,
                        "%s\\data\\Backup\\data\\Notepad" % Evecons_ministick_path)
        shutil.rmtree("%s\\data\\Notepad" % Evecons_ministick_path)
        shutil.copytree("%s\\data\\Notepad" % Evecons_PC_path, "%s\\data\\Notepad" % Evecons_ministick_path)

        os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_ministick_path)
        shutil.copy("%s\\data\\Info\\version" % Evecons_ministick_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_ministick_path)
        os.remove("%s\\data\\Info\\version" % Evecons_ministick_path)
        shutil.copy("%s\\data\\Info\\version" % Evecons_PC_path, "%s\\data\\Info" % Evecons_ministick_path)
        os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_ministick_path)
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_ministick_path)
        os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path)
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path, "%s\\data\\Info" % Evecons_ministick_path)

    def Mainstick_to_Ministick():
        backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_ministick_path, "w")  # von Mainstick auf Ministick
        backuptime.write("Backup:\nFrom: Mainstick\nTo: Ministick\nDate: %s\nTime: %s\nVersion: %s" % (
            datetime.datetime.now().strftime("%d.%m.%Y"),
            datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
        backuptime.close()
        shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_ministick_path)
        shutil.copytree("%s\\!Evecon" % Evecons_ministick_path, "%s\\data\\Backup\\!Evecon" % Evecons_ministick_path)
        shutil.rmtree("%s\\!Evecon" % Evecons_ministick_path)
        shutil.copytree("%s\\!Evecon" % Evecons_mainstick_path, "%s\\!Evecon" % Evecons_ministick_path)
        shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_ministick_path)
        shutil.copytree("%s\\data\\Notepad" % Evecons_ministick_path,
                        "%s\\data\\Backup\\data\\Notepad" % Evecons_ministick_path)
        shutil.rmtree("%s\\data\\Notepad" % Evecons_ministick_path)
        shutil.copytree("%s\\data\\Notepad" % Evecons_mainstick_path, "%s\\data\\Notepad" % Evecons_ministick_path)

        os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_ministick_path)
        shutil.copy("%s\\data\\Info\\version" % Evecons_ministick_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_ministick_path)
        os.remove("%s\\data\\Info\\version" % Evecons_ministick_path)
        shutil.copy("%s\\data\\Info\\version" % Evecons_mainstick_path, "%s\\data\\Info" % Evecons_ministick_path)
        os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_ministick_path)
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_ministick_path)
        os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path)
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path, "%s\\data\\Info" % Evecons_ministick_path)

    def Ministick_to_Mainstick():
        backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_mainstick_path, "w")  # von Ministick auf Mainstick
        backuptime.write("Backup:\nFrom: Mainstick\nTo: Ministick\nDate: %s\nTime: %s\nVersion: %s" % (
            datetime.datetime.now().strftime("%d.%m.%Y"),
            datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
        backuptime.close()
        shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_mainstick_path)
        shutil.copytree("%s\\!Evecon" % Evecons_mainstick_path, "%s\\data\\Backup\\!Evecon" % Evecons_mainstick_path)
        shutil.rmtree("%s\\!Evecon" % Evecons_mainstick_path)
        shutil.copytree("%s\\!Evecon" % Evecons_ministick_path, "%s\\!Evecon" % Evecons_mainstick_path)
        shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_mainstick_path)
        shutil.copytree("%s\\data\\Notepad" % Evecons_mainstick_path,
                        "%s\\data\\Backup\\data\\Notepad" % Evecons_mainstick_path)
        shutil.rmtree("%s\\data\\Notepad" % Evecons_mainstick_path)
        shutil.copytree("%s\\data\\Notepad" % Evecons_ministick_path, "%s\\data\\Notepad" % Evecons_mainstick_path)

        os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_mainstick_path)
        shutil.copy("%s\\data\\Info\\version" % Evecons_mainstick_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_mainstick_path)
        os.remove("%s\\data\\Info\\version" % Evecons_mainstick_path)
        shutil.copy("%s\\data\\Info\\version" % Evecons_ministick_path, "%s\\data\\Info" % Evecons_mainstick_path)
        os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_mainstick_path)
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_mainstick_path)
        os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path)
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path, "%s\\data\\Info" % Evecons_mainstick_path)

    def Ministick_to_PC():
        backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_PC_path,
                          "w")
        backuptime.write("Backup:\nFrom: Mainstick\nTo: Ministick\nDate: %s\nTime: %s\nVersion: %s" % (
            datetime.datetime.now().strftime("%d.%m.%Y"),
            datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
        backuptime.close()
        shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_PC_path)
        shutil.copytree("%s\\!Evecon" % Evecons_PC_path,
                        "%s\\data\\Backup\\!Evecon" % Evecons_PC_path)
        shutil.rmtree("%s\\!Evecon" % Evecons_PC_path)
        shutil.copytree("%s\\!Evecon" % Evecons_ministick_path,
                        "%s\\!Evecon" % Evecons_PC_path)
        shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_PC_path)
        shutil.copytree("%s\\data\\Notepad" % Evecons_PC_path,
                        "%s\\data\\Backup\\data\\Notepad" % Evecons_PC_path)
        shutil.rmtree("%s\\data\\Notepad" % Evecons_PC_path)
        shutil.copytree("%s\\data\\Notepad" % Evecons_ministick_path,
                        "%s\\data\\Notepad" % Evecons_PC_path)

        os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_PC_path)
        shutil.copy("%s\\data\\Info\\version" % Evecons_PC_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_PC_path)
        os.remove("%s\\data\\Info\\version" % Evecons_PC_path)
        shutil.copy("%s\\data\\Info\\version" % Evecons_ministick_path,
                    "%s\\data\\Info" % Evecons_PC_path)
        os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_PC_path)
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_PC_path)
        os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path)
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path,
                    "%s\\data\\Info" % Evecons_PC_path)

    def Mainstick_to_PC():
        backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_PC_path, "w")  # von Mainstick auf Ministick
        backuptime.write("Backup:\nFrom: Mainstick\nTo: Ministick\nDate: %s\nTime: %s\nVersion: %s" % (
            datetime.datetime.now().strftime("%d.%m.%Y"),
            datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
        backuptime.close()
        shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_PC_path)
        shutil.copytree("%s\\!Evecon" % Evecons_PC_path, "%s\\data\\Backup\\!Evecon" % Evecons_PC_path)
        shutil.rmtree("%s\\!Evecon" % Evecons_PC_path)
        shutil.copytree("%s\\!Evecon" % Evecons_mainstick_path, "%s\\!Evecon" % Evecons_PC_path)
        shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_PC_path)
        shutil.copytree("%s\\data\\Notepad" % Evecons_PC_path,
                        "%s\\data\\Backup\\data\\Notepad" % Evecons_PC_path)
        shutil.rmtree("%s\\data\\Notepad" % Evecons_PC_path)
        shutil.copytree("%s\\data\\Notepad" % Evecons_mainstick_path, "%s\\data\\Notepad" % Evecons_PC_path)

        os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_PC_path)
        shutil.copy("%s\\data\\Info\\version" % Evecons_PC_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_PC_path)
        os.remove("%s\\data\\Info\\version" % Evecons_PC_path)
        shutil.copy("%s\\data\\Info\\version" % Evecons_mainstick_path, "%s\\data\\Info" % Evecons_PC_path)
        os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_PC_path)
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path,
                    "%s\\data\\Backup\\data\\Info" % Evecons_PC_path)
        os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path)
        shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path, "%s\\data\\Info" % Evecons_PC_path)

    if Evecons_multi == 0:
        if Evecons_PC == 1:
            if this_version[0] > PCversion[0]:
                this_to_PC()

            elif this_version[0] < PCversion[0]:
                PC_to_this()
                restart = True

        elif Evecons_mainstick == 1:
            if this_version[0] > mainstickversion[0]:
                this_to_Mainstick()

            elif this_version[0] < mainstickversion[0]:
                Mainstick_to_this()
                restart = True

        elif Evecons_ministick == 1:
            if this_version[0] > ministickversion[0]:
                this_to_Ministick()

            elif this_version[0] < ministickversion[0]:
                Ministick_to_this()
                restart = True

    else:  # Wenn mehr als drei Programme gleichzeitig dies umprogrammieren!
        if version_PC == 1:
            if mainstickversion[0] > ministickversion[0]:
                highestversion = mainstickversion[0]
                highestversionname = "Mainstick"
                mustupdateanother = 1
            elif mainstickversion[0] < ministickversion[0]:
                highestversion = ministickversion[0]
                highestversionname = "Ministick"
                mustupdateanother = 1
            else:
                highestversion = mainstickversion[0]
                highestversionname = "Mainstick"
                mustupdateanother = 0

            if this_version[0] > highestversion:

                this_to_Mainstick()
                this_to_Ministick()


            elif this_version[0] < highestversion:
                if mustupdateanother == 1:  # beide update
                    if highestversionname == "Mainstick":

                        Mainstick_to_this()
                        Mainstick_to_Ministick()
                        restart = True


                    elif highestversionname == "Ministick":

                        Ministick_to_this()
                        Ministick_to_Mainstick()
                        restart = True

                else:

                    Mainstick_to_this()
                    restart = True

            elif this_version[0] == highestversion:
                if mustupdateanother == 1:
                    if highestversionname == "Mainstick":
                        # von diesem (PC) auf Ministick
                        this_to_Ministick()

                    elif highestversionname == "Ministick":
                        # von diesem (PC) auf Mainstick
                        this_to_Mainstick()

        elif version_MainStick == 1:
            if PCversion[0] > ministickversion[0]:
                highestversion = PCversion[0]
                highestversionname = "PC"
                mustupdateanother = 1
            elif PCversion[0] < ministickversion[0]:
                highestversion = ministickversion[0]
                highestversionname = "Ministick"
                mustupdateanother = 1
            else:
                highestversion = PCversion[0]
                highestversionname = "Mainstick"
                mustupdateanother = 0

            if this_version[0] > highestversion:

                this_to_PC()
                this_to_Ministick()

            elif this_version[0] < highestversion:
                if mustupdateanother == 1:  # beide update
                    if highestversionname == "PC":

                        # von PC auf diesen (Mainstick)
                        PC_to_this()

                        # von PC auf Ministick
                        PC_to_Ministick()
                        restart = True

                    elif highestversionname == "Ministick":

                        # von Ministick auf diesen (Mainstick)
                        Ministick_to_this()

                        # von Ministick auf PC
                        Ministick_to_PC()
                        restart = True

                else:
                    # PC auf diesen (Mainstick)
                    PC_to_Mainstick()


            elif this_version[0] == highestversion:
                if mustupdateanother == 1:
                    if highestversionname == "PC":

                        # von PC auf Ministick
                        PC_to_Ministick()

                    elif highestversionname == "Ministick":

                        # von diesem (Mainstick) auf PC
                        this_to_PC()

        elif version_MiniStick == 1:
            if PCversion[0] > mainstickversion[0]:
                highestversion = PCversion[0]
                highestversionname = "PC"
                mustupdateanother = 1
            elif PCversion[0] < mainstickversion[0]:
                highestversion = mainstickversion[0]
                highestversionname = "Mainstick"
                mustupdateanother = 1
            else:
                highestversion = PCversion[0]
                highestversionname = "Mainstick"
                mustupdateanother = 0

            if this_version[0] > highestversion:

                # von diesem (MiniStick) auf PC
                this_to_PC()

                # von diesem (MiniStick) auf Mainstick
                this_to_Mainstick()

            elif this_version[0] < highestversion:
                if mustupdateanother == 1:  # beide update
                    if highestversionname == "PC":

                        # von PC auf diesen (MiniStick)
                        PC_to_this()

                        # von PC auf Mainstick
                        PC_to_Mainstick()
                        restart = True

                    elif highestversionname == "Mainstick":

                        # von Mainstick auf diesen (MiniStick)
                        Mainstick_to_this()
                        # von Mainstick auf PC
                        Mainstick_to_PC()
                        restart = True

                else:

                    # von PC auf diesen (MiniStick)
                    PC_to_this()
                    restart = True

            elif this_version[0] == highestversion:

                if mustupdateanother == 1:

                    if highestversionname == "PC":

                        # von PC auf Mainstick
                        PC_to_Mainstick()

                    elif highestversionname == "Mainstick":

                        # von Mainstick auf PC
                        Mainstick_to_PC()




def zipme():
    title("Upgrade", "Zipping")
    version()
    global this_version
    newarchive = "data\\Update\\Evecon-" + this_version[1] + ".zip"
    allfiles = ["!Evecon\\dev\\!Console.py", "!Evecon\\dev\\updater.py",
                "data\\Info\\Changelog.txt", "data\\Info\\version"]
    alldic = ["!Evecon\\!Console"]

    szip.create_archive(newarchive, allfiles + alldic)

    if os.path.isfile(newarchive):
        print("Success")
    else:
        print("ERROR")
        raise EveconExceptions.UpdateZip


def upload():
    #
    # aktuelles Evecon in eine Zipfile komprimieren! (7-Zip) (FIN)
    # dazu gehört: '!Console', 'dev' bzw darin NUR *.py und 'dll', 'data\Info\Changelog.txt + version' (FIN)
    # diese zip-File dann auf Mega.nz mit dem Konto -------@*.com und PW -------- hochladen.
    # bzw. auf Mega einige Ordner erstellen UND die aktuelle Versions-Datei ersetzen! (die normale 'version')

    zipme()
    title("Upgrade", "Uploading")
    version()
    global this_version


    logindata = open("data\\Info\\updater_megalogin", "r")
    email = logindata.readline().rstrip()
    pw = logindata.readline().rstrip()
    logindata.close()

    Megacmd.login(email, pw)
    Megacmd.rm("/Evecon/version")
    Megacmd.upload("data\\Info\\version", "/Evecon")
    Megacmd.mkdir("/Evecon/Versions/%s" % this_version[1])
    Megacmd.upload("data\\Update\\Evecon-" + this_version[1] + ".zip", "/Evecon/Versions/%s" % this_version[1])
    Megacmd.exit()
    time.sleep(0.5)
    cls()
    os.remove("data\\Update\\Evecon-" + this_version[1] + ".zip")


def upgrade():
    cls()
    if version_PC == 1:
        title("Upgrade", "Changelog")
        version()
        global this_version
        print("Changelog\n\nOld Version: %s" % this_version[1])
        newversion = input("\nNew Version: ")
        newupdate = []
        newupdate_firstinput = False
        while True:
            cls()
            print("Updates:\n")
            if newupdate_firstinput:
                print("In this Update:")
                for x in range(len(newupdate)):
                    print(newupdate[x])
            newupdate_input = input("\nType 'END' to exit\n\n")
            if newupdate_input.lower() == "end":
                break
            newupdate.append(newupdate_input)
            newupdate_firstinput = True
        cls()
        title("Upgrade", "Backup")

        backuptime = open("data\\Backup\\backup.txt", "w")
        backuptime.write("Backup while Upgrading:\nDate: %s\nTime: %s\nVersion: %s" % (
            datetime.datetime.now().strftime("%d.%m.%Y"),
            datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
        backuptime.close()

        shutil.rmtree("data\\Backup\\!Evecon")

        shutil.copytree("!Evecon\\!Console", "data\\Backup\\!Evecon\\!Console")
        os.mkdir("data\\Backup\\!Evecon\\dev")
        shutil.copy("!Evecon\\dev\\!Console.py", "data\\Backup\\!Evecon\\dev")
        shutil.copy("!Evecon\\dev\\EveconExceptions.py", "data\\Backup\\!Evecon\\dev")
        shutil.copy("!Evecon\\dev\\ss_time.py", "data\\Backup\\!Evecon\\dev")
        shutil.copy("!Evecon\\dev\\updater.py", "data\\Backup\\!Evecon\\dev")

        os.remove("data\\Backup\\data\\Info\\version")
        shutil.copy("data\\Info\\version", "data\\Backup\\data\\Info")
        os.remove("data\\Backup\\data\\Info\\Changelog.txt")
        shutil.copy("data\\Info\\Changelog.txt", "data\\Backup\\data\\Info")

        title("Upgrade", "Change Version")

        this_version_1 = int(this_version[0]) + 1
        file_change_version_raw = open("data\\Info\\version", "w")
        file_change_version_raw.write("%s\n%s" % (str(this_version_1), newversion))
        file_change_version_raw.close()

        title("Upgrade", "Change Changelog")

        file_changelog_raw = open("data\\Info\\Changelog.txt", "a+")
        file_changelog_raw.write(
            "Version: %s\nNumber: %s\nDate: %s\nTime: %s\nChanges:\n" % (newversion, str(this_version_1),
                                                                         datetime.datetime.now().strftime("%d.%m.%Y"),
                                                                         datetime.datetime.now().strftime("%H:%M:%S")))
        for x in range(len(newupdate)):
            file_changelog_raw.write(newupdate[x])
            file_changelog_raw.write("\n")
        file_changelog_raw.write("\n\n")
        file_changelog_raw.close()

        version()

        title("Upgrade", "Deleting")

        dir_tmp = os.getcwd()
        os.chdir("!Evecon\\dev")
        shutil.rmtree("build\\!Console")
        shutil.rmtree("dist\\!Console")

        title("Upgrade", "Installing")

        os.system("pyinstaller !Console.py")
        time.sleep(1)
        os.chdir(dir_tmp)
        shutil.rmtree("!Evecon\\!Console")
        shutil.copytree("!Evecon\\dev\\dist\\!Console", "!Evecon\\!Console")
        shutil.copy("!Evecon\\dev\\dll\\avbin64.dll", "!Evecon\\!Console")

        upload()

    # 2. Changelog und neue version abfragen mit alte zeigen (version) 3. backup 4. os.system("pyinstaller x") 5. kopieren 6. neustart wenn mit arg -re mit !Evecon.bat
    else:
        print("Only at a PC with PyInstaller!")
        time.sleep(3)


skiparg = []

for x in range(3):
    try:
        sys.argv[x]
    except IndexError:
        sys.argv.append(None)
        skiparg.append(x)
test = []
if not skiparg:
    skiparg.append(2)

for x in range(1, 2):
    if x >= skiparg[0]:
        break
    if sys.argv[x] == "-update":
        title("Updating", "Self-start")
        update()
        if restart:
            subprocess.call(["!Evecon.bat"])
        exit_now()
    if sys.argv[x] == "-upgrade":
        title("Upgrading", "Self-start")
        upgrade()
        subprocess.call(["!Evecon.bat"])
        exit_now()


def main():
    title("Waiting for Input")

    cls()
    user_input = input("What to do?\nUpdate (UD), Upgrade (UG)\n\n")

    if user_input.lower() == "ud":
        update()
    if user_input.lower() == "ug":
        upgrade()


if exitnow == 0:
    if __name__ == "__main__":
        main()
        time.sleep(0)

        exit_now()
        WORK = False