import EveconLib.Config
import EveconLib.Tools.Tools
import datetime
import os
import sys

if sys.platform == "win32":
    #import win32process
    from win32process import GetWindowThreadProcessId as win32process_GetWindowThreadProcessId

    #import win32gui
    from win32gui import GetWindowRect as win32gui_GetWindowRect
    from win32gui import GetWindowText as win32gui_GetWindowText
    from win32gui import EnumWindows as win32gui_EnumWindows
    #import ctypes
    from ctypes import windll as ctypes_windll

#import getpass
from getpass import getuser as getpass_getuser


def exit_now(killmex = False):
    try:
        EveconLib.Config.title_time.deac()
    except AttributeError:
        pass

    EveconLib.Config.exitnow = 1 # make to bool
    EveconLib.Config.startmain = False

    #if EveconLib.Config.myType = "python_file":
    #    exit()

    if killmex:
        time.sleep(0.5)
        EveconLib.Tools.Tools.killme()

    #sys.exit()
    #os.close(0)
    os._exit(0)

def killConsoleWin():
    if sys.platform == "win32":
        EveconLib.Config.title_time.deac()
        title(deac=True)
        hwnd = ctypes_windll.kernel32.GetConsoleWindow() # another HWND?
        ctypes_windll.user32.ShowWindow(hwnd, 0)

        # Why?
        ctypes_windll.kernel32.CloseHandle(hwnd)
        _, pid = win32process_GetWindowThreadProcessId(hwnd)
        #print(pid)
        #os.system('taskkill /PID ' + str(pid) + ' /f')
        #input()

        # tmp:
        #subprocess.call(["taskkill", "/IM", "conhost.exe", "/f"])





def loadHWND(newTitle=None):
    if sys.platform == "win32":
        def findIT(hwnd, extra):
            rect = win32gui_GetWindowRect(hwnd)

            EveconLib.Config.console_data["posx"] = x = rect[0]
            EveconLib.Config.console_data["posy"] = y = rect[1]
            EveconLib.Config.console_data["lenx"] = rect[2] - x
            EveconLib.Config.console_data["leny"] = rect[3] - y

            if newTitle is None and EveconLib.Tools.Tools.lsame(win32gui_GetWindowText(hwnd), gettitle("left")):
                EveconLib.Config.thisHWND = win32gui_GetWindowText(hwnd)
            elif newTitle is not None and win32gui_GetWindowText(hwnd) == newTitle:
                EveconLib.Config.thisHWND = win32gui_GetWindowText(hwnd)

        win32gui_EnumWindows(findIT, None)


def gettitle(part="all"):
    if sys.platform == "win32":
        something = EveconLib.Config.title_oldstart
        status = EveconLib.Config.title_oldstatus
        versionX = EveconLib.Config.title_oldversion

        nowtime = datetime.datetime.now().strftime("%H:%M:%S")

        space_status = (60 - len(status) * 2) * " "
        space_pc = (64 - len(versionX) * 2) * " "
        space_something = (40 - len(something) * 2) * " "
        space_time = 55 * " "

        if EveconLib.Config.musicrun:
            space_status = 7 * " "  # old: abs(60 - len(status) * 2 - 30)
            space_pc = 10 * " "  # old: abs(64 - len(pc) * 2 - 30)
            space_something = (175 - (
                        len(status + versionX + space_status + space_pc) + round(len(something) * 1.5) + 1)) * " "
            if len(space_something) < 20:
                space_something = (160 - (
                            len(status + versionX + space_status + space_pc) + round(len(something) * 1.5) + 1)) * " "
            space_time = 1 * " "
        if part == "all":
            return "EVECON: %s%s%s%s%s%s%sTime: %s" % (status, space_status, versionX, space_pc, something, space_something, space_time, nowtime)
        elif part == "left":
            return "EVECON: %s%s" % (status, space_status)


def title(status="OLD", something="OLD", version="OLD", deac=False):
    if sys.platform == "win32":
        if deac:
            EveconLib.Config.title_dead = True
            return

        if status == "OLD":
            status = EveconLib.Config.title_oldstatus
        else:
            EveconLib.Config.title_oldstatus = status

        if something == "OLD":
            something = EveconLib.Config.title_oldstart
        else:
            EveconLib.Config.title_oldstart = something

        if version == "OLD":
            version = EveconLib.Config.title_oldversion
        else:
            EveconLib.Config.title_oldversion = version

        nowtime = datetime.datetime.now().strftime("%H:%M:%S")

        space_status = (60 - len(status) * 2) * " "
        space_pc = (64 - len(version) * 2) * " "
        space_something = (40 - len(something) * 2) * " "
        space_time = 55 * " "

        if EveconLib.Config.musicrun:
            space_status = 7 * " " # old: abs(60 - len(status) * 2 - 30)
            space_pc = 10 * " " # old: abs(64 - len(pc) * 2 - 30)
            space_something = (175 - (len(status + version + space_status + space_pc) + round(len(something) * 1.5) + 1)) * " "
            if len(space_something) < 20:
                space_something = (160 - (len(status + version + space_status + space_pc) + round(len(something) * 1.5) + 1)) * " "
            space_time = 1 * " "

        if not EveconLib.Config.title_dead:
            ctypes_windll.kernel32.SetConsoleTitleW("EVECON: %s%s%s%s%s%s%sTime: %s" %
                                                    (status, space_status, version, space_pc, something, space_something, space_time, nowtime))

def normaltitle():
    if EveconLib.Config.ss_active:
        title("Screensaver", "")

    else:
        title("OLD", "Version: " + EveconLib.Config.code_version[2])


def Status(printit=True):
    if printit:
        EveconLib.Tools.cls()
        print("Status\n")

        print("Time: " + datetime.datetime.now().strftime("%H:%M:%S"))
        print("Date: " + datetime.datetime.now().strftime("%d.%m.%Y"))

        print("\nEvecon:\n")
        print("Version: " + EveconLib.Config.file_version)
        print("Code-Version: " + EveconLib.Config.code_version)
        print("Versionnummber: " + EveconLib.Config.file_versions[0])
        print("PID: " + str(os.getpid()))

        print("\nComputer:\n")
        print("Computername: " + EveconLib.Config.Computername)
        print("Username: " + getpass_getuser())
        print("Computer synonymous: " + EveconLib.Config.computer)
        if EveconLib.Config.thisIP:
            print("IP address: " + str(EveconLib.Config.thisIP))
        print("Homepc: " + str(EveconLib.Config.HomePC))

        input()

    status = {
        "version": {"version": EveconLib.Config.file_version, "codeversion": EveconLib.Config.code_version, "versionnumber": EveconLib.Config.file_versions[0]},
        "pid": os.getpid(), "computername": EveconLib.Config.Computername, "username": getpass_getuser(),
        "computersyn": EveconLib.Config.computer, "ip": EveconLib.Config.thisIP, "homepc": EveconLib.Config.HomePC}

    return status #[versionFind()[1], versionFind()[2], versionFind()[0], version, os.getpid(),Computername, getpass.getuser(), computer, thisIP, HomePC]
