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
