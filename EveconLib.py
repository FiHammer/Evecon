from EveconTools import *
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
import json

import win32api
import win32gui
import win32con
import win32gui_struct
import win32process

import itertools
import glob
import datetime
import subprocess
import psutil

import EveconMiniDebug
import EveconExceptions


path_seg = "\\"
firefox_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
vivaldi_path = "C:\\Program Files (x86)\\Vivaldi\\Application\\vivaldi.exe"

if os.getcwd() == "C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\!Evecon\\dev":
    os.chdir("..")
    os.chdir("..")


code_version = "0.9.4.1"

pyglet.options['search_local_libs'] = True

ss_active = False
exitnow = 0
pausetime = 180
musicrun = False
thisIP = None
StartupServer = None
browser = "vivaldi"
startmain = False
Alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
musicrandom = True
enable_foxi = True
cores = 2
console_data = {"lenx": 120, "leny": 30, "posx": 0, "posy": 0, "pixx": 120, "pixy": 30}
thisHWND = 0

title_oldstatus = "Loading"
title_oldstart = "Error"
title_oldversionX = "Error"
title_dead = False

def loadHWND(newTitle=None):
    def findIT(hwnd, extra):
        rect = win32gui.GetWindowRect(hwnd)
        global thisHWND, console_data
        console_data["posx"] = x = rect[0]
        console_data["posy"] = y = rect[1]
        console_data["lenx"] = rect[2] - x
        console_data["leny"] = rect[3] - y

        if newTitle is None and lsame(win32gui.GetWindowText(hwnd), gettitle("left")):
            thisHWND = win32gui.GetWindowText(hwnd)
        elif newTitle is not None and win32gui.GetWindowText(hwnd) == newTitle:
            thisHWND = win32gui.GetWindowText(hwnd)

    win32gui.EnumWindows(findIT, None)

ctypes.windll.kernel32.SetConsoleTitleW("EVECON: Loading HWND")
loadHWND("EVECON: Loading HWND")
ctypes.windll.kernel32.SetConsoleTitleW("EVECON: Loading...")


def killme():
    subprocess.call(["taskkill", "/F", "/PID", str(os.getpid())])
    os.system("taskkill /PID /F %s" % str(os.getpid()))

def readConfig():
    config = configparser.ConfigParser()
    config.read("data"+path_seg+"Config"+path_seg+"config.ini")

    global browser, musicrandom, enable_foxi, thisIP, cores

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

        thisIP = config["PC"]["thisIP"]
        cores = int(config["PC"]["cores"])


    except KeyError:
        pass


readConfig()

def Log(functioni, info, typei = "Normal"):
    log_file = open("data"+path_seg+"Log"+"Log.txt", "a+")
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



class Printer(threading.Thread):
    def __init__(self, printit, waitTime=1.5, refreshTime=1, waitUntil=0):
        """
        An easy printer, which will print every some secons the function(s)

        :param printit: the function(s) to print
        :type printit: list
        :type printit: function

        :param waitTime: time between every print
        :type waitTime: float
        :type printit: double

        :param refreshTime: time between pause
        :type refreshTime: int
        :type refreshTime: float
        :type refreshTime: double

        :param waitUntil: this should be a time from time.time(); the printer will wait until the time is over
        :type waitUntil: int
        :type waitUntil: float
        :type waitUntil: double

        running: started/stopped
        printing: printing loop
        waiting: waiting loop
        """
        super().__init__()

        if isinstance(printit, list):
            self.printitS = printit
        else:
            self.printitS = [printit]

        self.waitTime = waitTime
        self.refreshTime = refreshTime

        self.running = False
        self.printing = False
        self.waiting = False
        self.waitUntil = waitUntil


    def run(self):
        """
        script
        """
        self.running = True
        self.printing = True
        self.waiting = True

        while self.running:
            while self.printing and self.waitUntil < time.time():
                cls()
                for printFunc in self.printitS:
                    printFunc()
                time.sleep(self.waitTime)
            while self.waiting:
                time.sleep(self.refreshTime)
            time.sleep(0.1)

    def pause(self):
        """
        pause the printer

        :return: True if success
        """

        if self.printing:
            self.printing = False
            self.waiting = True

            return True
        else:
            return False

    def unpause(self):
        """
        unpause the printer

        :return: True if success
        """

        if self.waiting:
            self.printing = True
            self.waiting = False

            return True
        else:
            return False

    def switch(self):
        """
        switch between pause

        :return: if True pause, False unpause
        """

        if self.printing:
            self.pause()
            return True
        else:
            self.unpause()
            return False

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
            if self.running:
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
                    elif char == "\x7f":
                        self.action("strg_backspace")
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
                        self.action("return")
                    else:
                        self.action(char)



class Findus:
    def __init__(self, workList: list, reactUser=None, prefix=None, suffix=None, startPos=0, expandRange=2, scanner=None, autoPrint=False, afterPrint=True, autoSearch=False, onlyReturn=True, autoSort=False, enableCommands=False):
        """
        :param workList: the list with the content with witch the user can play
        :type workList: list

        :param reactUser: Findus will send the input of the user to this function if it is NOT NONE
        :type reactUser: function
        :type reactUser: NoneType

        :param prefix: will be printed(returned) before the word; str for all word; dict ('content of list': prefix in str) for singel; none for none
        :type prefix: str
        :type prefix: dict
        :type prefix: NoneType

        :param suffix: will be printed(returned) after the word; str for all word; dict ('content of list': prefix in str) for singel; none for none
        :type suffix: str
        :type suffix: dict
        :type suffix: NoneType

        :param startPos: sets the startposition of the curser
        :type startPos: int

        :param expandRange: sets the range of shown entries of the list above and under the curser
        :type expandRange: int

        :param scanner: use your own scanner
        :type scanner: Scanner

        :param autoPrint: enables the autoPrint function: will print every 1.5
        :type autoPrint: bool

        :param afterPrint: automaticly prints after every action
        :type afterPrint: bool

        :param autoSearch: the user can activate the search and can search in this
        :type autoSearch: bool

        :param onlyReturn: with this the react function will only get Returns. No more keypushes!
        :type onlyReturn: bool

        :param autoSort: enables autoSorting after 'every' (with enableInput) keypus
        :type autoSort: bool

        :param enableCommands: enables (other) commands (than search (is active with autoSerach))
        :type enableCommands: bool
        """

        if startPos >= len(workList):
            startPos = 0

        self._orgList = workList
        self.normList = workList
        self.searchList = workList
        self.workList = self._orgList.copy()

        self.curPos = startPos
        self.expandRange = expandRange
        self.enableInput = autoSearch
        self.onlyReturn = onlyReturn
        self.autoSort = autoSort
        self.afterPrint = afterPrint
        self.enableCommands = enableCommands

        self.prefix = {}
        if isinstance(prefix, str):
            self.prefixEnabled = True
            for x in self.workList:
                self.prefix[x] = prefix

        elif isinstance(prefix, dict):
            self.prefixEnabled = True

            self.prefix = prefix
            alreadyLoaded = []
            for x in prefix:
                alreadyLoaded.append(x)

            for x in self.workList:
                if not Search(x, alreadyLoaded, exact=True, lower=False):
                    self.prefix[x] = ""

        else: # None or other
            self.prefixEnabled = False
            for x in self.workList:
                self.prefix[x] = ""

        self.suffix = {}
        if isinstance(suffix, str):
            self.suffixEnabled = True
            for x in self.workList:
                self.suffix[x] = suffix

        elif isinstance(suffix, dict):
            self.suffixEnabled = True

            self.suffix = suffix
            alreadyLoaded = []
            for x in suffix:
                alreadyLoaded.append(x)

            for x in self.workList:
                if not Search(x, alreadyLoaded, exact=True, lower=False):
                    self.suffix[x] = ""

        else:  # None or other
            self.suffixEnabled = False
            for x in self.workList:
                self.suffix[x] = ""

        self.debug = False
        self.started = False

        self.lastInput = ""
        self.Input = ""
        self.reactUser = reactUser

        if scanner:
            self.scanner = scanner
        else:
            self.scanner = Scanner(self.react)

        self.autoPrint = autoPrint
        if autoPrint:
            self.printer = Printer(self.printit, refreshTime=2)
        else:
            self.printer = None

        self.outputMode = "normal"
        self.searching = False
        self.searchWord = ""




    def sort(self, allLists=False):
        """
        sorts the list (workList & norm-/searchList) by the name of the content

        :param allLists: all lists will be sorted
        :type allLists: bool
        """

        self.workList.sort()

        if self.searching:
            self.searchList.sort()
            if allLists:
                self.normList.sort()
        else:
            self.normList.sort()
            if allLists:
                self.searchList.sort()

    def setCurPos(self, pos: int):
        """
        this method will set the position of the curser (and check if it is posible)

        :param pos: the new position of the curser
        :type pos: int

        :return: if new position was set
        """

        if len(self.workList) - 1 >= pos:
            self.curPos = pos
            return True
        else:
            return False

    def setNewList(self, workList: list, prefix=None, suffix=None, resetSearch=True):
        """
        deletes the old workList and overwrites it with the param

        :param resetSearch: if true it resets the searchWord
        :type resetSearch: bool

        :param workList: the new workList
        :type workList: list

        :param prefix: will be printed(returned) before the word; str for all word; dict ('content of list': prefix in str) for singel; none for none
        :type prefix: str
        :type prefix: dict
        :type prefix: NoneType

        :param suffix: will be printed(returned) after the word; str for all word; dict ('content of list': prefix in str) for singel; none for none
        :type suffix: str
        :type suffix: dict
        :type suffix: NoneType
        """

        self._orgList = workList
        self.normList = workList
        self.searchList = workList
        self.workList = workList

        self.prefix = {}
        if isinstance(prefix, str):
            self.prefixEnabled = True
            for x in self.workList:
                self.prefix[x] = prefix

        elif isinstance(prefix, dict):
            self.prefixEnabled = True

            self.prefix = prefix
            alreadyLoaded = []
            for x in prefix:
                alreadyLoaded.append(x)

            for x in self.workList:
                if not Search(x, alreadyLoaded, exact=True, lower=False):
                    self.prefix[x] = ""

        else:  # None or other
            self.prefixEnabled = False
            for x in self.workList:
                self.prefix[x] = ""

        self.suffix = {}
        if isinstance(suffix, str):
            self.suffixEnabled = True
            for x in self.workList:
                self.suffix[x] = suffix

        elif isinstance(suffix, dict):
            self.suffixEnabled = True

            self.suffix = suffix
            alreadyLoaded = []
            for x in suffix:
                alreadyLoaded.append(x)

            for x in self.workList:
                if not Search(x, alreadyLoaded, exact=True, lower=False):
                    self.suffix[x] = ""

        else:  # None or other
            self.suffixEnabled = False
            for x in self.workList:
                self.suffix[x] = ""

        if resetSearch:
            self.searchWord = ""
        else:
            self.search("", overwrite=False)

    def setPrefix(self, prefix, directName=""):
        """
        sets the prefix

        :param prefix: will be printed(returned) before the word; str for all word; dict ('content of list': prefix in str) for singel; none for none
        :type prefix: dict
        :type prefix: str
        :type prefix: NoneType

        :param directName: with this you can specify which one you want to change; var is the name/content of the workList; only works with prefix: str
        :type directName: str

        :return: success
        """

        if directName:
            if isinstance(prefix, str) and isinstance(directName, str) and directName in self.prefix:
                self.prefix[directName] = prefix
            else:
                return False
        else:
            self.prefix = {}
            if isinstance(prefix, str):
                self.prefixEnabled = True
                for x in self.workList:
                    self.prefix[x] = prefix

            elif isinstance(prefix, dict):
                self.prefixEnabled = True

                self.prefix = prefix
                alreadyLoaded = []
                for x in prefix:
                    alreadyLoaded.append(x)

                for x in self.workList:
                    if not Search(x, alreadyLoaded, exact=True, lower=False):
                        self.prefix[x] = ""

            else:  # None or other
                self.prefixEnabled = False
                for x in self.workList:
                    self.prefix[x] = ""

        return True

    def setSuffix(self, suffix, directName=""):
        """
        sets the suffix

        :param suffix: will be printed(returned) after the word; str for all word; dict ('content of list': prefix in str) for singel; none for none
        :type suffix: dict
        :type suffix: str
        :type suffix: NoneType

        :param directName: with this you can specify which one you want to change; var is the name/content of the workList; only works with prefix: str
        :type directName: str

        :return: success
        """
        if directName:
            if isinstance(suffix, str) and isinstance(directName, str) and directName in self.prefix:
                self.prefix[directName] = suffix
            else:
                return False
        else:
            self.suffix = {}
            if isinstance(suffix, str):
                self.suffixEnabled = True
                for x in self.workList:
                    self.suffix[x] = suffix

            elif isinstance(suffix, dict):
                self.suffixEnabled = True

                self.suffix = suffix
                alreadyLoaded = []
                for x in suffix:
                    alreadyLoaded.append(x)

                for x in self.workList:
                    if not Search(x, alreadyLoaded, exact=True, lower=False):
                        self.suffix[x] = ""

            else:  # None or other
                self.suffixEnabled = False
                for x in self.workList:
                    self.suffix[x] = ""

        return True

    def switchSearch(self):
        """
        switch the outputMode between search or normal
        switch the var searching
        sets the CurPos to 0
        changes the workList

        :return: returns True when switched to search, false for normal
        """
        if self.outputMode == "normal":
            self.workList = self.searchList.copy()
            self.Input = ""

            self.setCurPos(0)
            self.outputMode = "search"
            self.searching = True
            return True

        else:
            self.workList = self.normList.copy()
            self.Input = ""

            self.setCurPos(0)
            self.outputMode = "normal"
            self.searching = False
            return False


    def search(self, word: str, overwrite=True, refresh=True):
        """
        changes the searchword
        refreshs the workList (if searching or refresh)

        :param word: the new (part of the) searching word
        :type word: str

        :param overwrite: if true the old word will be overridden, else it will be append
        :type overwrite: bool

        :param refresh: if not only the searchWord will be changed, else it will be searched
        :type refresh: bool

        :return: the search word
        """

        if overwrite:
            self.searchWord = word
        else:
            self.searchWord += word

        if refresh:

            solutions = Search(self.searchWord, self._orgList)

            newList = []
            if solutions:
                for x in solutions:
                    newList.append(self._orgList[x])
            else:
                newList = self._orgList.copy()

            if self.curPos > len(newList) - 1:
                self.curPos = 0

            self.searchList = newList.copy()

        if self.searching:
            self.workList = self.searchList.copy()

        return self.searchWord


    def start(self):
        """
        starts the scanner

        :return: success
        """

        if not self.started and not self.scanner.is_alive():
            self.started = True
            self.scanner.start()

            if self.autoPrint:
                self.printer.start()

            return True
        else:
            return False


    def react(self, inpt: str):
        """
        :param inpt: the input that comes form the Scanner-object
        :type inpt: str

        :return: success
        """
        self.lastInput = inpt
        if inpt == "arrowup" and self.curPos > 0:  # down
            self.curPos -= 1

        elif inpt == "arrowdown" and self.curPos < len(self.workList) - 1:  # up
            self.curPos += 1

        elif self.enableInput and not lsame(inpt, "arrow"):
            if inpt == "escape" and self.searching:
                self.switchSearch()

            elif len(inpt) == 1:
                self.Input += inpt

            elif inpt == "backspace":
                if len(self.Input) > 0:
                    new_Input = ""
                    for x in range(len(self.Input) - 1):
                        new_Input += self.Input[x]
                    self.Input = new_Input

            elif inpt == "strg_backspace":  # del
                self.Input = ""

            else:
                self.sendToUser(inpt)

            if self.searching: # if in search, search for it
                self.search(self.Input)
            else:              # if no search, command
                if self.enableCommands:
                    self.commands(self.Input)
                else:
                    self.sendToUser(inpt)

        elif self.reactUser and not lsame(inpt, "arrow"):
            self.sendToUser(inpt)
        else:
            return False

        if self.autoSort:
            self.sort()
        if self.afterPrint:
            self.printit()
        print(inpt)
        return True

    def sendToUser(self, inpt):
        """
        mini-method, for shrinking

        :param inpt: data
        :return:
        """
        if self.reactUser:
            if self.onlyReturn:
                if inpt == "return":
                    self.reactUser(inpt)
            else:
                self.reactUser(inpt)

    def commands(self, inpt: str, sendToReact=False):
        """
        :param inpt: the command change
        :type inpt: str

        :param sendToReact: if unsuccess, send to UserReact
        :type sendToReact: bool

        :return: success
        """

        if inpt == "search":
            return self.switchSearch()
        else:
            if sendToReact:
                if self.onlyReturn:
                    if inpt == "return":
                        self.reactUser(inpt)
                else:
                    self.reactUser(inpt)
            return False
        #return True

    def printit(self):
        """
        prints all programm output, after clearing the screen
        """
        cls()
        self.printbody()
        self.printfoot()

    def printbody(self):
        """
        prints the programm body output
        """
        for x in self.returnbody():
            print(x)

    def printfoot(self):
        """
        prints the programm foot output
        """
        print("")
        for x in self.returnfoot():
            print(x)

    def returnit(self):
        """
        :return: returns all programm output (list)
        """
        return self.returnbody() + self.returnfoot()

    def returnbody(self):
        """
        :return: returns the programm body output (list)
        """

        outputList = []
        search_done = False
        for now in range(self.expandRange):
            if not search_done:
                if self.curPos == now:
                    if self.expandRange >= len(self.workList) - 1:
                        for word_num in range(0, len(self.workList)):
                            if word_num + 1 < 10:
                                word_num_str = str(word_num + 1) + "  "
                            elif word_num + 1 < 100:
                                word_num_str = str(word_num + 1) + " "
                            else:
                                word_num_str = str(word_num + 1)

                            if self.prefixEnabled and self.suffixEnabled:
                                prefix = self.prefix[self.workList[word_num]] + " "
                                suffix = " " + self.suffix[self.workList[word_num]] + " "
                            elif self.prefixEnabled:
                                prefix = self.prefix[self.workList[word_num]] + " "
                                suffix = ""
                            elif self.suffixEnabled:
                                prefix = ""
                                suffix = " " + self.suffix[self.workList[word_num]] + " "
                            else:
                                prefix = ""
                                suffix = ""

                            if self.curPos == word_num:
                                if not self.debug:
                                    if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                                        outputList.append(" " + word_num_str + " * " + prefix + getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                                    else:
                                        outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix)
                                else:
                                    outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix + "0")
                            else:
                                if not self.debug:
                                    if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                                        outputList.append(" " + word_num_str + "   " + prefix + getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                                    else:
                                        outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix)
                                else:
                                    outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix + "1")

                    elif 2 * self.expandRange + 1 >= len(self.workList):
                        for word_num in range(0, 2 * self.expandRange + 1):  # + 1?
                            if word_num + 1 < 10:
                                word_num_str = str(word_num + 1) + "  "
                            elif word_num + 1 < 100:
                                word_num_str = str(word_num + 1) + " "
                            else:
                                word_num_str = str(word_num + 1)

                            if self.prefixEnabled and self.suffixEnabled:
                                prefix = self.prefix[self.workList[word_num]] + " "
                                suffix = " " + self.suffix[self.workList[word_num]] + " "
                            elif self.prefixEnabled:
                                prefix = self.prefix[self.workList[word_num]] + " "
                                suffix = ""
                            elif self.suffixEnabled:
                                prefix = ""
                                suffix = " " + self.suffix[self.workList[word_num]] + " "
                            else:
                                prefix = ""
                                suffix = ""

                            if self.curPos == word_num:
                                try:
                                    if not self.debug:
                                        if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                                            outputList.append(" " + word_num_str + " * " + prefix + getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                                        else:
                                            outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix)
                                    else:
                                        outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix + "2")
                                except IndexError:
                                    pass
                            else:
                                try:
                                    if not self.debug:
                                        if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                                            outputList.append(" " + word_num_str + "   " + prefix + getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                                        else:
                                            outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix)
                                    else:
                                        outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix + "3")
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

                            if self.prefixEnabled and self.suffixEnabled:
                                prefix = self.prefix[self.workList[word_num]] + " "
                                suffix = " " + self.suffix[self.workList[word_num]] + " "
                            elif self.prefixEnabled:
                                prefix = self.prefix[self.workList[word_num]] + " "
                                suffix = ""
                            elif self.suffixEnabled:
                                prefix = ""
                                suffix = " " + self.suffix[self.workList[word_num]] + " "
                            else:
                                prefix = ""
                                suffix = ""

                            if self.curPos == word_num:
                                if not self.debug:
                                    if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                                        outputList.append(" " + word_num_str + " * " + prefix + getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                                    else:
                                        outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix)
                                else:
                                    outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix + "4")
                            else:
                                if not self.debug:
                                    if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                                        outputList.append(" " + word_num_str + "   " + prefix + getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                                    else:
                                        outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix)
                                else:
                                    outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix + "5")
                    search_done = True
                    break

                elif self.curPos == len(self.workList) - now - 1 and self.curPos >= self.expandRange:  # Ende
                    for word_num in range(self.curPos - self.expandRange - 2 + now, self.curPos + 1 + now):
                        if word_num < 0:
                            continue
                        # print(word_num, self.curPos, now, self.expandRange)
                        if word_num + 1 < 10:
                            word_num_str = str(word_num + 1) + "  "
                        elif word_num + 1 < 100:
                            word_num_str = str(word_num + 1) + " "
                        else:
                            word_num_str = str(word_num + 1)

                        if self.prefixEnabled and self.suffixEnabled:
                            prefix = self.prefix[self.workList[word_num]] + " "
                            suffix = " " + self.suffix[self.workList[word_num]] + " "
                        elif self.prefixEnabled:
                            prefix = self.prefix[self.workList[word_num]] + " "
                            suffix = ""
                        elif self.suffixEnabled:
                            prefix = ""
                            suffix = " " + self.suffix[self.workList[word_num]] + " "
                        else:
                            prefix = ""
                            suffix = ""

                        if self.curPos == word_num:
                            if not self.debug:
                                if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                                    outputList.append(" " + word_num_str + " * " + prefix + getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                                else:
                                    outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix)
                            else:
                                outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix + "6")
                        else:
                            if not self.debug:
                                if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                                    outputList.append(" " + word_num_str + "   " + prefix + getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                                else:
                                    outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix)
                            else:
                                outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix + "7")
                    search_done = True
                    break

        if not search_done:  # Mitte
            for word_num in range(self.curPos - self.expandRange, self.curPos + self.expandRange + 1):
                if word_num + 1 < 10:
                    word_num_str = str(word_num + 1) + "  "
                elif word_num + 1 < 100:
                    word_num_str = str(word_num + 1) + " "
                else:
                    word_num_str = str(word_num + 1)

                if self.prefixEnabled and self.suffixEnabled:
                    prefix = self.prefix[self.workList[word_num]] + " "
                    suffix = " " + self.suffix[self.workList[word_num]] + " "
                elif self.prefixEnabled:
                    prefix = self.prefix[self.workList[word_num]] + " "
                    suffix = ""
                elif self.suffixEnabled:
                    prefix = ""
                    suffix = " " + self.suffix[self.workList[word_num]] + " "
                else:
                    prefix = ""
                    suffix = ""

                if self.curPos == word_num:
                    if not self.debug:
                        if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                            outputList.append(" " + word_num_str + " * " + prefix + getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                        else:
                            outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix)
                    else:
                        outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix + "10")
                else:
                    if not self.debug:
                        if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                            outputList.append(" " + word_num_str + "   " + prefix + getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                        else:
                            outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix)
                    else:
                        outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix + "11")

        return outputList

    def returnfoot(self):
        """
        :return: returns the programm foot output (list)
        """
        outputList = []
        if self.enableInput:
            outputList.append("\nInput: " + self.Input)
        return outputList



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


# Imported from EveconLibWIN


def title(status="OLD", something="OLD", versionX="OLD", deac=False):
    global title_dead
    if deac:
        title_dead = True
    global title_oldstatus, title_oldstart, title_oldversionX
    if status == "OLD":
        status = title_oldstatus
    else:
        title_oldstatus = status

    if something == "OLD":
        something = title_oldstart
    else:
        title_oldstart = something

    if versionX == "OLD":
        versionX = title_oldversionX
    else:
        title_oldversionX = versionX

    nowtime = datetime.datetime.now().strftime("%H:%M:%S")

    space_status = (60 - len(status) * 2) * " "
    space_pc = (64 - len(versionX) * 2) * " "
    space_something = (40 - len(something) * 2) * " "
    space_time = 55 * " "

    if musicrun:
        space_status = 7 * " " # old: abs(60 - len(status) * 2 - 30)
        space_pc = 10 * " " # old: abs(64 - len(pc) * 2 - 30)
        space_something = (175 - (len(status + versionX + space_status + space_pc) + round(len(something) * 1.5) + 1)) * " "
        if len(space_something) < 20:
            space_something = (160 - (len(status + versionX + space_status + space_pc) + round(len(something) * 1.5) + 1)) * " "
        space_time = 1 * " "

    if not title_dead:
        ctypes.windll.kernel32.SetConsoleTitleW("EVECON: %s%s%s%s%s%s%sTime: %s" %
                                                (status, space_status, versionX, space_pc, something, space_something, space_time, nowtime))

class title_time(threading.Thread):

    def __init__(self, freq):
        threading.Thread.__init__(self)
        self.stop = 0
        self.freq = freq
        # self.stopped = False
        self.pause = False
        self.stop = False
        self.ss = False
        self.sstime = ""
        self.normrun = True

    def run(self):
        global pausetime
        while not self.stop:
            while self.normrun:
                title()
                time.sleep(self.freq)
            time.sleep(0.1)
            while self.ss:
                first = time.time()
                while self.ss:
                    time.sleep(0.25)

                    if (round(time.time() - first) % 60) < 10:
                        self.sstime = str(round(time.time() + pausetime - first) // 60) + ":0" + str(
                            round(time.time() + pausetime - first) % 60)
                    else:
                        self.sstime = str(round(time.time() + pausetime - first) // 60) + ":" + str(
                            round(time.time() + pausetime - first) % 60)

                    title("OLD", "OLD", self.sstime)

    def deac(self):
        self.stop = True
        self.normrun = False
        self.ss = False

    def ss_switch(self):
        if self.ss:
            self.pause = True
            self.ss = False
        else:
            self.pause = False
            self.ss = True

ttime = title_time(2.5)

def killConsoleWin():
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


def gettitle(part="all"):
    something = title_oldstart
    status = title_oldstatus
    versionX = title_oldversionX

    nowtime = datetime.datetime.now().strftime("%H:%M:%S")

    space_status = (60 - len(status) * 2) * " "
    space_pc = (64 - len(versionX) * 2) * " "
    space_something = (40 - len(something) * 2) * " "
    space_time = 55 * " "

    if musicrun:
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
        self.unerrorl = []
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

        self.unerrorl.append(hwnd)
        self.unerrorl.append(msg)
        self.unerrorl.append(wparam)
        self.unerrorl.append(lparam)

    def destroy(self, hwnd, msg, wparam, lparam):
        if self.on_quit: self.on_quit(self)
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)

        self.unerrorl.append(hwnd)
        self.unerrorl.append(msg)
        self.unerrorl.append(wparam)
        self.unerrorl.append(lparam)

    def notify(self, hwnd, msg, wparam, lparam):
        self.unerrorl.append(hwnd)
        self.unerrorl.append(msg)
        self.unerrorl.append(wparam)

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
        self.unerrorl.append(hwnd)
        self.unerrorl.append(msg)
        self.unerrorl.append(lparam)

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

class UsedPortsC:
    def __init__(self):
        self.ports = []
        self.programs = 0

        self.usePorts = []

        python = 0
        evecon = 0

        for x in psutil.process_iter():
            if x.name() == "!Console.exe":
                evecon += 1
            elif x.name() == "python.exe":
                python += 1

        if python + evecon == 1 or self.programs > python + evecon - 1:
            self.resetFile()

        else:
            with open("data" + path_seg + "tmp" + path_seg + "usedPorts.txt") as file:
                lines = file.readlines()
                for x in range(len(lines)):
                    if x == 0: # first Line
                        self.programs = int(lines[x].rstrip())
                    else:
                        try:
                            int(x)
                            self.ports.append(lines[x].rstrip())
                        except ValueError:
                            self.resetFile()
                            break

    def readFile(self):
        self.ports = []
        self.programs = 0
        python = 0
        evecon = 0

        for x in psutil.process_iter():
            if x.name() == "!Console.exe":
                evecon += 1
            elif x.name() == "python.exe":
                python += 1
        """
        if python + evecon == 1 or self.programs > python + evecon:
            self.resetFile()
        
        else:
        """
        with open("data" + path_seg + "tmp" + path_seg + "usedPorts.txt") as file:
            lines = file.readlines()
            for x in range(len(lines)):
                if x == 0: # first Line
                    self.programs = int(lines[x].rstrip())
                else:
                    try:
                        int(x)
                        self.ports.append(lines[x].rstrip())
                    except ValueError:
                        self.resetFile()
                        break
        if len(self.ports) < self.programs:
            self.resetFile()

    def writeFile(self):
        with open("data" + path_seg + "tmp" + path_seg + "usedPorts.txt", "w") as file:
            for x in range(len(self.ports) + 1):
                if x == 0:
                    file.write(str(self.programs) + "\n")
                elif x == len(self.ports):
                    file.write(self.ports[x - 1])
                else:
                    file.write(self.ports[x - 1] + "\n")
    def resetFile(self):
        self.programs = 0
        self.usePorts = []
        self.ports = []
        with open("data" + path_seg + "tmp" + path_seg + "usedPorts.txt", "w") as file:
            file.write(str(self.programs))

    def addPort(self, port):
        if Search(str(port), self.ports):
            return False
        self.ports.append(str(port))
        if not self.usePorts:
            self.programs += 1
        self.usePorts.append(str(port))
        self.writeFile()
    def remPort(self, port):
        found = Search(str(port), self.ports)
        del self.ports[found[0]]


        found = Search(str(port), self.usePorts)
        del self.usePorts[found[0]]
        if not self.usePorts:
            self.programs -= 1
        self.writeFile()
    def isAvalible(self, port):
        self.readFile()
        if Search(str(port), self.ports):
            return False
        else:
            return True
    def getNextPort(self, port):
        self.readFile()
        while True:
            port += 1
            if not Search(str(port), self.ports):
                return port
    def givePort(self, port=4000):
        if not self.isAvalible(port):
            port = self.getNextPort(port)
        self.addPort(port)
        return port

usedPorts = UsedPortsC()

class globalMPportsC:
    def __init__(self, file):
        self.file = file
        self.ports = []
        self.programs = 0

        self.usePorts = []

        python = 0
        evecon = 0

        for x in psutil.process_iter():
            if x.name() == "!Console.exe":
                evecon += 1
            elif x.name() == "python.exe":
                python += 1

        if python + evecon == 1 or self.programs > python + evecon:
            self.resetFile()

        else:
            with open("data" + path_seg + "tmp" + path_seg + self.file) as file:
                lines = file.readlines()
                for x in range(len(lines)):
                    if x == 0: # first Line
                        self.programs = int(lines[x].rstrip())
                    else:
                        try:
                            int(x)
                            self.ports.append(lines[x].rstrip())
                        except ValueError:
                            self.resetFile()
                            break

    def readFile(self):
        python = 0
        evecon = 0

        for x in psutil.process_iter():
            if x.name() == "!Console.exe":
                evecon += 1
            elif x.name() == "python.exe":
                python += 1

        if python + evecon == 1 or self.programs > python + evecon:
            self.resetFile()

        else:
            with open("data" + path_seg + "tmp" + path_seg + self.file) as file:
                lines = file.readlines()
                for x in range(len(lines)):
                    if x == 0: # first Line
                        self.programs = int(lines[x].rstrip())
                    else:
                        try:
                            int(x)
                            self.ports.append(lines[x].rstrip())
                        except ValueError:
                            self.resetFile()
                            break
            if len(self.ports) < self.programs:
                self.resetFile()

    def writeFile(self):
        with open("data" + path_seg + "tmp" + path_seg + self.file, "w") as file:
            for x in range(len(self.ports) + 1):
                if x == 0:
                    file.write(str(self.programs) + "\n")
                elif x == len(self.ports):
                    file.write(self.ports[x - 1])
                else:
                    file.write(self.ports[x - 1] + "\n")
    def resetFile(self):
        self.programs = 0
        with open("data" + path_seg + "tmp" + path_seg + self.file, "w") as file:
            file.write(str(self.programs))

    def addPort(self, port):
        if Search(str(port), self.ports):
            return False
        self.ports.append(str(port))
        if not self.usePorts:
            self.programs += 1
        self.usePorts.append(str(port))
        self.writeFile()
    def remPort(self, port):
        found = Search(str(port), self.ports)
        del self.ports[found[0]]

        found = Search(str(port), self.usePorts)
        del self.usePorts[found[0]]
        if not self.usePorts:
            self.programs -= 1
        self.writeFile()


globalMPports = globalMPportsC("mpPorts.txt")
globalMPportsJava = globalMPportsC("mpPortsJava.txt")


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
                debug = [sysTrayIcon]
                x = "ss"
                debug.append(x)

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
            #print(["put"] + localfiles + [remotepath])
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

                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                subP = subprocess.Popen(command, startupinfo=startupinfo, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                subP.wait()
                subP.communicate()

            else:
                print("error archive type is not supported")
        else:
            print("error archive type is not the same as the archive name")

    def extract_archive(self, archive, output=None, switches=None, EveconPath=True):
        if os.path.exists(archive):
            dir_tmp = os.getcwd()
            if EveconPath:
                archive = dir_tmp + "\\" + archive

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

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            subP = subprocess.Popen(command, startupinfo=startupinfo, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
            subP.wait()
            subP.communicate()
            #subprocess.call(command)

        else:
            print("error archive not found")

szip = szipC("Programs\\7z")

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



# noinspection PyTypeChecker
class MusicPlayerC(threading.Thread):
    def __init__(self, systray=True, random=True, expandRange=2, stop_del=False, scanner_active=True, balloonTip=True, killMeAfterEnd=True, remote=True, remotePort=4554):
        super().__init__()

        self.debug = False

        self.music = {"all_files": 0, "all_dirs": 0, "active": []}
        self.find_music_out = {}

        self.systray = None
        self.systrayon = systray
        self.balloonTip = balloonTip
        self.killMeAfterEnd = killMeAfterEnd
        self.remote = True
        self.remotePort = remotePort

        self.remoteAddress = ""
        self.remoteAction = ""
        if self.remote:
            self.server = Server(port=self.remotePort, ip="192.168.2.102", react=self.react_remote, welcomeMessage="", reactLogINOUT=True, printLog=False)
            self.server_java = ServerJava(port=self.remotePort + 1, ip="192.168.2.102", react=self.react_remote)
        else:
            self.server = None
            self.server_java = None

        self.volume = Volume.getVolume()
        self.volumep = 1

        # stop the musicplayer while hovering over file 1 and pressing 'del'-button
        self.stop_del = stop_del
        self.randomizer = random
        self.scanner_active = scanner_active
        # noinspection PyGlobalUndefined
        global musicrun
        musicrun = True

        self.starttime = 0
        self.hardworktime = 0
        self.musicrun = True
        self.playlist = []
        self.pershuffel = False

        self.running = False
        self.playing = False
        self.exitn = False
        self.allowPrint = False
        self.autorefresh = True

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
        self.con_main_last = None
        self.con_cont = "set"
        self.change = ""

        self.last_print = 0
        self.last_print_auto = 0

        self.cur_Input = ""
        self.cur_Pos = 0
        self.expandRange = expandRange

        self.searching = False
        self.searchlist = []
        self.cur_Search = ""


        self.tmp_pl_input_1 = []
        self.tmp_pl_input_2 = []
        self.tmp_pl_output_1 = []
        self.tmp_pl_output_2 = []


        self.musiclist = {"names": []}
        self.multiplaylists = {}
        self.genre = []
        self.musicDir = ""

        """
        with open("data" + path_seg + "Config" + path_seg + "Music.json") as jsonfile:
            data = json.load(jsonfile)

        if data["pc"] == computer:
            pass
        else:
            with open("data" + path_seg + "Backup" + path_seg + "Music_backup.json") as jsonfile:
                data = json.load(jsonfile)

        self.musicDir = data["musicDir"]

        #dirs

        musiclist = {}
        musiclist_ids = []
        multiplaylists = {}
        multiplaylist_ids = []

        for mpl_id in data["multiplaylists"]:
            if mpl_id == data["multiplaylists"][mpl_id]["id"]:
                multiplaylist_ids.append(mpl_id)

        for ml_id in data["directories"]:
            if ml_id == data["directories"][ml_id]["id"] and not Search(ml_id, multiplaylist_ids):
                musiclist_ids.append(ml_id)
                musiclist[ml_id] = data["directories"][ml_id]["path"]

        for mpl_id in multiplaylist_ids:
            cur_pl = []
            for x in range(data["multiplaylists"][mpl_id]["content"]["len"]):
                cur_pl.append(data["multiplaylists"][mpl_id]["content"][str(x)])

            new_cur_pl = []
            for x in range(len(cur_pl)):
                if Search(cur_pl[x], musiclist_ids):
                    new_cur_pl.append(cur_pl[x])

            if new_cur_pl:
                multiplaylists[mpl_id] = new_cur_pl

        self.musiclist = musiclist.copy()
        self.multiplaylists = multiplaylists.copy()

        self.multiplaylists_key = []
        for key in self.multiplaylists:
            self.multiplaylists_key.append(key)

        #self.playlists = ["LiS", "Anime", "Phunk", "Caravan Palace", "Electro Swing", "Parov Stelar", "jPOP & etc", "OMFG"]
        #self.playlists_key = ["lis", "an", "phu", "cp", "es", "ps", "jpop", "omfg"]

        self.playlists = [] # name NOW: self.musiclist["names"]
        self.playlists_key = [] # key NOW: self.musiclist["keys"]

        for key in self.musiclist:
            self.playlists.append(self.musiclist[key].split("\\")[-1].title())
            self.playlists_key.append(key)
        
        """

    def findMusic(self, path, reset=True):
        if reset:
            self.find_music_out = {"all_files": 0, "all_dirs": 0}
        content = []

        for file in os.listdir(path):
            fullname = path + path_seg + file
            if os.path.isdir(path + path_seg + file):
                self.music["all_dirs"] += 1
                self.music["dir" + str(self.music["all_dirs"])] = {"file": file, "path": path, "fullname": fullname}

                thisDirID = self.music["all_dirs"]

                self.find_music_out["all_dirs"] += 1
                self.find_music_out["dir" + str(self.find_music_out["all_dirs"])] = {"file": file, "path": path,
                                                                                     "fullname": fullname}
                dir_content = self.findMusic(fullname, False)

                self.music["dir" + str(thisDirID)]["content"] = dir_content
                self.find_music_out["dir" + str(thisDirID)]["content"] = dir_content

                content.append("dir" + str(thisDirID))  # ID of DIR

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

                self.music["file" + str(self.music["all_files"])] = {"name": name, "file": file, "path": path,
                                                                     "fullname": fullname,
                                                                     "antype": antype, "andata": andata}

                self.find_music_out["file" + str(self.music["all_files"])] = {"name": name, "file": file, "path": path,
                                                                              "fullname": fullname,
                                                                              "antype": antype, "andata": andata}

                content.append("file" + str(self.music["all_files"]))  # ID of FILE

        return content

    def addMusic(self, key, custom=False, genre=False):  # key (AN, LIS)
        self.read_musiclist()
        cls()
        if computer == "MiniPC":
            print("Loading... (On Mini-PC)")
        elif computer == "BigPC":
            print("Loading... (On Big-PC)")
        else:
            print("Loading...")

        old_Num = self.music["all_files"]
        if type(key) == str:
            key = key.lower()

        if custom:
            key = "cus"
        elif genre:
            if Search(key, self.genre, exact=True):
                if isinstance(key, str):
                    for aDir in self.musiclist["keys"]:
                        if Search(key, self.musiclist[aDir]["genre"], exact=True):
                            self.addMusic(aDir)
                elif isinstance(key, list):
                    for aGenre in key:
                        for aDir in self.musiclist["keys"]:
                            if Search(aGenre, self.musiclist[aDir]["genre"], exact=True):
                                self.addMusic(aDir)
                return True
            else:
                return False

        done = False
        if type(key) == str:
            for x in self.musiclist["keys"]:
                if x == key:
                    self.findMusic(self.musicDir + path_seg + self.musiclist[key]["path"])
                    done = True
                    break
        elif type(key) == list:
            for x in self.musiclist["keys"]:
                for y in key:
                    if x == y:
                        self.addMusic(x)
                        break
            return True

        if done:
            pass
        elif key == "us":
            self.findMusic("Music"+path_seg+"User")
        elif key == "cus" and custom: # custom
            self.findMusic(custom)
        elif key == "all":
            for x in self.musiclist["keys"]:
                self.addMusic(x)
            return True
        elif Search(key, list(self.multiplaylists.keys()), exact=True):
            self.addMusic(self.multiplaylists[key])
        elif Search(key, self.genre, exact=True):
            if isinstance(key, str):
                for aDir in self.musiclist["keys"]:
                    if Search(key, self.musiclist[aDir]["genre"], exact=True):
                        self.addMusic(aDir)
            elif isinstance(key, list):
                for aGenre in key:
                    for aDir in self.musiclist["keys"]:
                        if Search(aGenre, self.musiclist[aDir]["genre"], exact=True):
                            self.addMusic(aDir)
            else:
                pass
            return True

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
        print("Finished: " + key)
        return True

    def read_musiclist(self):
        def unvalid(error, key=False, remove=False):
            nonlocal data
            if not key:
                print("Musicfile is not valid:\n" + error)
            else:
                print("Musicfile is not valid:\nKey not found! (" + error + ")")

            if remove:
                with open("data" + path_seg + "Backup" + path_seg + "Music_backup.json") as jsonfile:
                    data = json.load(jsonfile)

            return False

        def parse(unvaild):
            version = "1.1"
            if data.get("pc") != computer or data.get("pc") == "global":
                unvaild("Wrong PC!", remove=True)
                return parse(unvalid)
            if data.get("version"):
                if not data["version"] == version:
                    unvaild("Wrong Version! (" + version + " required)")
                    return parse(unvalid)
            else:
                unvaild("version", True, remove=True)
                return parse(unvalid)

            if data.get("musicDir"):
                if os.path.exists(data["musicDir"]):
                    musicDir = data["musicDir"] + "\\"
                else:
                    unvaild("Wrong musicDir path", remove=True)
                    return parse(unvalid)
            else:
                unvaild("musicDir", True, remove=True)
                return parse(unvalid)

            if not data.get("directories"):
                unvaild("directories", True, remove=True)
                return parse(unvalid)
            if not data.get("multiplaylists"):
                unvaild("multiplaylists", True, remove=True)
                return parse(unvalid)


            musicDirs = {"names": []}
            musicDirs_direct = data["directories"].copy()
            multiPls = {}
            multiPls_direct = data["multiplaylists"].copy()

            dirIDs = []
            dirIDs_direct = list(musicDirs_direct.keys())
            mplIDs = []
            mplIDs_direct = list(multiPls_direct.keys())
            genre = []

            # generate the music directories and genre!

            for aDir in dirIDs_direct:
                if aDir == musicDirs_direct[aDir].get("id"):
                    if aDir.islower() and musicDirs_direct[aDir]["id"].islower():
                        if Search(aDir, dirIDs, exact=True):
                            unvalid("A Dir-ID was double (" + aDir + ")")
                            continue
                        if not os.path.exists(musicDir + musicDirs_direct[aDir].get("path")):
                            unvalid("A Dir-Path does not exist (" + musicDirs_direct[aDir].get("path") + ")")
                            continue
                        dirIDs.append(aDir)

                        musicDirs[aDir] = musicDirs_direct[aDir].copy()
                        if musicDirs_direct[aDir].get("genre"):
                            for aGenre in musicDirs_direct[aDir]["genre"]:
                                if aGenre.islower():
                                    if not Search(aGenre, genre, exact=True):
                                        genre.append(aGenre)
                                else:
                                    unvalid("Genre is not low (" + aGenre + ")")
                        else:
                            musicDirs[aDir]["genre"] = []
                        if not musicDirs_direct[aDir].get("name"):
                            musicDirs[aDir]["name"] = musicDirs[aDir]["path"].split("\\")[-1].title()
                        musicDirs["names"].append(musicDirs[aDir]["name"])
                    else:
                        unvalid("Dir-ID is not low (" + aDir + "/" + musicDirs_direct[aDir]["id"] + ")")
                else:
                    unvalid("Diffrent Dir-IDs (" + aDir + ")")

            musicDirs["keys"] = dirIDs

            # generate mpl
            for aMPl in mplIDs_direct:
                if aMPl == multiPls_direct[aMPl].get("id"):
                    if aMPl.islower():
                        if not Search(aMPl, dirIDs, exact=True):
                            if Search(aMPl, mplIDs, exact=True):
                                unvalid("A MPl-ID was double (" + aMPl + ")")
                                continue
                            mplIDs.append(aMPl)

                            multiPls[aMPl] = multiPls_direct[aMPl]["content"]["ids"].copy()

                            if multiPls_direct[aMPl]["content"].get("genre"):
                                for aGenre in multiPls_direct[aMPl]["content"]["genre"]:
                                    for aDir in dirIDs:
                                        if Search(aGenre, musicDirs[aDir]["genre"], exact=True) and not Search(aDir,
                                                                                                               multiPls[
                                                                                                                   aMPl],
                                                                                                               exact=True):
                                            multiPls[aMPl].append(aDir)

                        else:
                            unvalid("MPl-ID is used in the musicDirs (" + aMPl + ")")
                    else:
                        unvalid("MPl-ID is not low (" + aMPl + ")")
                else:
                    unvalid("Diffrent MPl-IDs (" + aMPl + ")")

            # deleting genre
            delGenre = []
            for aGenre_ID in range(len(genre)):
                for aID in dirIDs+mplIDs:
                    if aID == genre[aGenre_ID]:
                        delGenre.append(aGenre_ID)

            for x in delGenre:
                del genre[x]

            return musicDirs, multiPls, genre, musicDir

        with open("data" + path_seg + "Config" + path_seg+ "Music.json") as jsonfile:
            data = json.load(jsonfile)


        self.musiclist, self.multiplaylists, self.genre, self.musicDir = parse(unvalid)



        """
        #dirs

        musiclist = {}
        musiclist_ids = []
        multiplaylists = {}
        multiplaylist_ids = []

        for mpl_id in data["multiplaylists"]:
            if mpl_id == data["multiplaylists"][mpl_id]["id"]:
                multiplaylist_ids.append(mpl_id)

        for ml_id in data["directories"]:
            if ml_id == data["directories"][ml_id]["id"] and not Search(ml_id, multiplaylist_ids, exact=True):
                musiclist_ids.append(ml_id)
                musiclist[ml_id] = data["directories"][ml_id]["path"]

        for mpl_id in multiplaylist_ids:
            cur_pl = []
            for aDir in range(data["multiplaylists"][mpl_id]["content"]["len"]):
                cur_pl.append(data["multiplaylists"][mpl_id]["content"][str(aDir)])

            new_cur_pl = []
            for aDir in range(len(cur_pl)):
                if Search(cur_pl[aDir], musiclist_ids):
                    new_cur_pl.append(cur_pl[aDir])

            if new_cur_pl:
                multiplaylists[mpl_id] = new_cur_pl

        self.musiclist = musiclist.copy()
        self.multiplaylists = multiplaylists.copy()

        """


    def reloadMusic(self, tracknum):
        if type(tracknum) == int:
            self.music["file" + str(tracknum)]["loaded"] = pyglet.media.load(self.music["file" + str(tracknum)]["fullname"])
        elif type(tracknum) == str:
            self.music[tracknum]["loaded"] = pyglet.media.load(self.music[tracknum]["fullname"])

    def make_playlist(self):
        self.playlist = []
        for x in range(1, self.music["all_files"] + 1):
            self.playlist.append("file" + str(x))
        self.searchlist = self.playlist.copy()

    def shufflePL(self, first=False):
        if first:
            random.shuffle(self.playlist)
        else:
            oldPL = self.playlist.copy()
            del oldPL[0]
            random.shuffle(oldPL)
            self.playlist = [self.playlist[0]] + oldPL

        self.hardworktime = time.time() + 0.1

    def refreshTitle(self):
        if self.getCur()["antype"]:
            title("OLD", self.getCur()["andata"]["title"], "Now Playing")
        else:
            title("OLD", self.getCur()["name"], "Now Playing")

    def showBalloonTip(self):
        if self.getCur()["antype"]:
            name = self.getCur()["andata"]["title"]
        else:
            name = self.getCur()["name"]
        WindowsBalloonTip.ShowWindow("Evecon: MusicPlayer", "Now playing: " + name)

    def getCur(self):
        if len(self.playlist) == 0:
            self.stop()
        return self.music[self.playlist[0]]

    def rerollThis(self):
        oldPL = self.playlist.copy()
        del oldPL[self.cur_Pos]
        self.playlist = oldPL + [self.playlist[self.cur_Pos]]
        if self.cur_Pos == 0:
            self.next(True)

    def sortPL(self):
        self.playlist.sort()
        self.hardworktime = time.time() + 0.2

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
        self.hardworktime = time.time()

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
        self.hardworktime = time.time()


    #Options

    def play(self):
        self.paused = False
        self.player.play()
        self.hardworktime = time.time() + 0.2
    def pause(self):
        self.paused = True
        self.player.pause()
        self.hardworktime = time.time() + 0.2
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
        self.scanner.running = False

        if self.remote:
            self.server.close_connection()
            self.server_java.stop()
            globalMPports.remPort(self.server.port)
            globalMPportsJava.remPort(self.server_java.port)

        if self.systrayon and self.killMeAfterEnd:
            time.sleep(1)
            killme()
    def next(self, skipthis=False):
        if skipthis:
            self.skip_del = True
        self.playing = False
        if self.paused:
            self.paused = False
            self.player.play()
        self.hardworktime = time.time() + 0.2
    def Del(self, num):
        #num = Search(plfile, self.playlist)[0]
        if num == 0 and self.stop_del:
            self.stop()
        if num > len(self.playlist) - 1:
            return False

        if self.cur_Pos >= len(self.playlist) - 1:
            self.cur_Pos -= 1

        del self.playlist[num]

        if num == 0:
            self.next(True)

    def Del_plfile(self, plfile):
        num = Search(plfile, self.playlist)[0]
        if num == 0 and self.stop_del:
            self.stop()
        if num > len(self.playlist) - 1:
            return False

        file = self.playlist[0]
        file_del = self.playlist[num]

        if self.cur_Pos >= len(self.playlist) - 1:
            self.cur_Pos -= 1

        del self.playlist[num]

        if file == file_del:
            self.next(True)

    def vol(self, vol):
        self.volume = vol
        Volume.change(vol)
    def volp(self, vol):
        self.volumep = vol
        self.player.volume = self.volumep
    def queue(self, pos):
        oldPL = self.playlist.copy()
        del oldPL[pos]
        del oldPL[0]
        self.playlist = [self.playlist[0]] + [self.playlist[pos]] + oldPL
        self.hardworktime = time.time()
    def queue_plfile(self, plfile):
        oldPL = self.playlist.copy()
        del oldPL[Search(plfile, oldPL)[0]]
        del oldPL[0]
        self.playlist = [self.playlist[0], plfile] + oldPL
        self.hardworktime = time.time()

    def refreshSearch(self):


        self.cur_Pos = 0

        if self.cur_Search != "":
            namelist = []

            for x in self.playlist:
                namelist.append(self.music[x]["name"])

            found = Search(self.cur_Search, namelist)

            searchlist_name = []
            for x in found:
                searchlist_name.append(namelist[x])

            searchlist_name.sort()

            music_dir = self.music.copy()

        else:
            searchlist_name = []
            for fileX in self.playlist:
                searchlist_name.append(self.music[fileX]["name"])
            searchlist_name.sort()

        self.tmp_pl_input_1 = []
        self.tmp_pl_input_2 = []
        for name in searchlist_name:
            if len(searchlist_name)/2 > len(self.tmp_pl_input_1):
                self.tmp_pl_input_1.append(name)
            else:
                self.tmp_pl_input_2.append(name)


        """
        for num_file in range(1, music_dir["all_files"] + 1):
            try:
                if name == music_dir["file" + str(num_file)]["name"]:
                    new_playlist.append("file" + str(num_file))
                    del music_dir["file" + str(num_file)]
                    break
            except KeyError:
                pass
        """

        def work1():
            music_dir = self.music.copy()

            new_playlist = []
            for name in self.tmp_pl_input_1:
                for num_file in range(1, music_dir["all_files"] + 1):
                    try:
                        if name == music_dir["file" + str(num_file)]["name"]:
                            new_playlist.append("file" + str(num_file))
                            del music_dir["file" + str(num_file)]
                            break
                    except KeyError:
                        pass
            self.tmp_pl_output_1 = new_playlist

        def work2():
            music_dir = self.music.copy()

            new_playlist = []
            for name in self.tmp_pl_input_2:
                for num_file in range(1, music_dir["all_files"] + 1):
                    try:
                        if name == music_dir["file" + str(num_file)]["name"]:
                            new_playlist.append("file" + str(num_file))
                            del music_dir["file" + str(num_file)]
                            break
                    except KeyError:
                        pass
            self.tmp_pl_output_2 = new_playlist

        t1 = threading.Thread(target=work1)
        t2 = threading.Thread(target=work2)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        new_playlist = self.tmp_pl_output_1 + self.tmp_pl_output_2

        self.searchlist = new_playlist.copy()



    def run(self):
        if self.systrayon and sys.platform == "win32":
            def quitFunc(x):
                self.stop()
            def unp_p(x):
                self.switch()
            def nextm(x):
                self.next()
            def delm(x):
                self.Del(0)
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

        if not self.playlist:
            self.make_playlist()
        self.searchlist = self.playlist.copy()


        if self.randomizer:
            self.shufflePL(True)


        if self.remote:
            globalMPports.addPort(self.server.port)
            globalMPportsJava.addPort(self.server_java.port)
            self.server.start()
            self.server_java.start()

        self.starttime = time.time()
        self.hardworktime = time.time()
        if self.scanner_active:
            self.scanner.start()
        while self.musicrun:

            if self.music[self.playlist[0]]["loaded"].is_queued:
                self.reloadMusic(self.playlist[0])

            if self.balloonTip:
                self.showBalloonTip()

            self.player.queue(self.music[self.playlist[0]]["loaded"])
            self.player.play()

            self.timer.start()

            self.player.volume = self.volumep

            self.running = True
            self.playing = True

            self.allowPrint = True
            self.refreshTitle()

            self.printit()
            self.last_print_auto = time.time()
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

    def print_head(self):
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
        if self.remoteAddress:
            print("Remoteaccess: " + self.remoteAddress)
            print("Last remoteaction: " + self.remoteAction)


        #sys.stdout.write(console_data[0]*"-")


    def print_body(self):
        # Main-Container

        if self.con_main == "pl":
            print("Playlist: (%s)\n" % str(len(self.playlist)))


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
                                    if not self.debug:
                                        if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                            print(" " + word_num_str + " * " + getPartStr(self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                                        else:
                                            print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"])
                                    else:
                                        print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"], 0, self.playlist[word_num])
                                else:
                                    if not self.debug:
                                        if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                            print(" " + word_num_str + "   " + getPartStr(self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                                        else:
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
                                        if not self.debug:
                                            if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                                print(" " + word_num_str + " * " + getPartStr(self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                                            else:
                                                print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"])
                                        else:
                                            print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"], 2, self.playlist[word_num])
                                    except IndexError:
                                        pass
                                else:
                                    try:
                                        if not self.debug:
                                            if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                                print(" " + word_num_str + "   " + getPartStr(self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                                            else:
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
                                    if not self.debug:
                                        if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                            print(" " + word_num_str + " * " + getPartStr(self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                                        else:
                                            print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"])
                                    else:
                                        print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"], 4, self.playlist[word_num])
                                else:
                                    if not self.debug:
                                        if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                            print(" " + word_num_str + "   " + getPartStr(self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                                        else:
                                            print(" " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"])
                                    else:
                                        print(" " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"], 5, self.playlist[word_num])
                        search_done = True
                        break

                    elif self.cur_Pos == len(self.playlist) - now - 1 and self.cur_Pos >= self.expandRange: # Ende
                        for word_num in range(self.cur_Pos - self.expandRange - 2 + now, self.cur_Pos + 1 + now):
                            if word_num < 0:
                                continue
                            #print(word_num, self.curPos, now, self.expandRange)
                            if word_num + 1 < 10:
                                word_num_str = str(word_num + 1) + "  "
                            elif word_num + 1 < 100:
                                word_num_str = str(word_num + 1) + " "
                            else:
                                word_num_str = str(word_num + 1)
                            if self.cur_Pos == word_num:
                                if not self.debug:
                                    if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                        print(" " + word_num_str + " * " + getPartStr(self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                                    else:
                                        print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"])
                                else:
                                    print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"], 6, self.playlist[word_num])
                            else:
                                if not self.debug:
                                    if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                        print(" " + word_num_str + "   " + getPartStr(self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                                    else:
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
                        if not self.debug:
                            if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                print(
                                    " " + word_num_str + " * " + getPartStr(self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                            else:
                                print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"])
                        else:
                            print(" " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"], 10, self.playlist[word_num])
                    else:
                        if not self.debug:
                            if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                print(" " + word_num_str + "   " + getPartStr(self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                            else:
                                print(" " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"])
                        else:
                            print(" " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"], 11, self.playlist[word_num])

        elif self.con_main == "details":
            print("Details:\n")
            print("Duration: " + str(TimeFor(self.music["file1"]["loaded"].duration)))

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

            if self.debug:
                print("\nDebugging Details:\n")

                print("Cur-Pos: " + str(self.cur_Pos))
                print("Autorefresh: " + str(self.autorefresh))

                print("File:\n")
                print("Filename: " + self.music[self.playlist[self.cur_Pos]]["file"])
                print("Path: " + self.music[self.playlist[self.cur_Pos]]["path"])

                print("\nPlayer:\n")

                print("Vol: " + str(Volume.getVolume()))
                print("Volplayer: " + str(self.volumep))
                print("Muted: " + str(self.muted))
                print("Playing: " + str(self.playing))
                print("Paused: " + str(self.paused))
                print("Loaded-Key: " + str(self.music["active"]))

                print("\nOther:\n")

                print("Scanner-Status: " + str(self.scanner.is_alive()))
                print("Timer direct: " + str(self.timer.getTime()))
                print("Last print: " + str(self.last_print))

            if self.server:
                print("\nPort: " + str(self.server.port))
                print("Port-Java: " + str(self.server_java.port))

        elif self.con_main == "spl":
            self.spl.printit(False)


        elif self.con_main == "search":
            #print(self.searchlist)
            print("Search: (%s)\n" % str(len(self.searchlist)))

            search_done = False
            for now in range(self.expandRange):
                if not search_done:
                    if self.cur_Pos == now:
                        if self.expandRange >= len(self.searchlist) - 1:
                            for word_num in range(0, len(self.searchlist)):
                                if word_num + 1 < 10:
                                    word_num_str = str(word_num + 1) + "  "
                                elif word_num + 1 < 100:
                                    word_num_str = str(word_num + 1) + " "
                                else:
                                    word_num_str = str(word_num + 1)

                                if self.cur_Pos == word_num:
                                    if not self.debug:
                                        if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                            print(" " + word_num_str + " * " + getPartStr(
                                                self.music[self.searchlist[word_num]]["name"], 0, 108) + "...")
                                        else:
                                            print(" " + word_num_str + " * " + self.music[self.searchlist[word_num]][
                                                "name"])
                                    else:
                                        print(" " + word_num_str + " * " + self.music[self.searchlist[word_num]]["name"],
                                              0, self.searchlist[word_num])
                                else:
                                    if not self.debug:
                                        if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                            print(" " + word_num_str + "   " + getPartStr(
                                                self.music[self.searchlist[word_num]]["name"], 0, 108) + "...")
                                        else:
                                            print(" " + word_num_str + "   " + self.music[self.searchlist[word_num]][
                                                "name"])
                                    else:
                                        print(" " + word_num_str + "   " + self.music[self.searchlist[word_num]]["name"],
                                              1, self.searchlist[word_num])
                        elif 2 * self.expandRange + 1 >= len(self.searchlist):
                            for word_num in range(0, 2 * self.expandRange + 1):  # + 1?
                                if word_num + 1 < 10:
                                    word_num_str = str(word_num + 1) + "  "
                                elif word_num + 1 < 100:
                                    word_num_str = str(word_num + 1) + " "
                                else:
                                    word_num_str = str(word_num + 1)

                                if self.cur_Pos == word_num:
                                    try:
                                        if not self.debug:
                                            if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                                print(" " + word_num_str + " * " + getPartStr(
                                                    self.music[self.searchlist[word_num]]["name"], 0, 108) + "...")
                                            else:
                                                print(" " + word_num_str + " * " + self.music[self.searchlist[word_num]][
                                                    "name"])
                                        else:
                                            print(" " + word_num_str + " * " + self.music[self.searchlist[word_num]][
                                                "name"], 2, self.searchlist[word_num])
                                    except IndexError:
                                        pass
                                else:
                                    try:
                                        if not self.debug:
                                            if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                                print(" " + word_num_str + "   " + getPartStr(
                                                    self.music[self.searchlist[word_num]]["name"], 0, 108) + "...")
                                            else:
                                                print(" " + word_num_str + "   " + self.music[self.searchlist[word_num]][
                                                    "name"])
                                        else:
                                            print(" " + word_num_str + "   " + self.music[self.searchlist[word_num]][
                                                "name"], 3, self.searchlist[word_num])
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
                                    if not self.debug:
                                        if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                            print(" " + word_num_str + " * " + getPartStr(
                                                self.music[self.searchlist[word_num]]["name"], 0, 108) + "...")
                                        else:
                                            print(" " + word_num_str + " * " + self.music[self.searchlist[word_num]][
                                                "name"])
                                    else:
                                        print(" " + word_num_str + " * " + self.music[self.searchlist[word_num]]["name"],
                                              4, self.searchlist[word_num])
                                else:
                                    if not self.debug:
                                        if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                            print(" " + word_num_str + "   " + getPartStr(
                                                self.music[self.searchlist[word_num]]["name"], 0, 108) + "...")
                                        else:
                                            print(" " + word_num_str + "   " + self.music[self.searchlist[word_num]][
                                                "name"])
                                    else:
                                        print(" " + word_num_str + "   " + self.music[self.searchlist[word_num]]["name"],
                                              5, self.searchlist[word_num])
                        search_done = True
                        break

                    elif self.cur_Pos == len(self.searchlist) - now - 1 and self.cur_Pos >= self.expandRange:  # Ende
                        for word_num in range(self.cur_Pos - self.expandRange - 2 + now, self.cur_Pos + 1 + now):
                            if word_num < 0:
                                continue
                            # print(word_num, self.curPos, now, self.expandRange)
                            if word_num + 1 < 10:
                                word_num_str = str(word_num + 1) + "  "
                            elif word_num + 1 < 100:
                                word_num_str = str(word_num + 1) + " "
                            else:
                                word_num_str = str(word_num + 1)
                            if self.cur_Pos == word_num:
                                if not self.debug:
                                    if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                        print(" " + word_num_str + " * " + getPartStr(
                                            self.music[self.searchlist[word_num]]["name"], 0, 108) + "...")
                                    else:
                                        print(" " + word_num_str + " * " + self.music[self.searchlist[word_num]]["name"])
                                else:
                                    print(" " + word_num_str + " * " + self.music[self.searchlist[word_num]]["name"], 6,
                                          self.searchlist[word_num])
                            else:
                                if not self.debug:
                                    if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                        print(" " + word_num_str + "   " + getPartStr(
                                            self.music[self.searchlist[word_num]]["name"], 0, 108) + "...")
                                    else:
                                        print(" " + word_num_str + "   " + self.music[self.searchlist[word_num]]["name"])
                                else:
                                    print(" " + word_num_str + "   " + self.music[self.searchlist[word_num]]["name"], 7,
                                          self.searchlist[word_num])
                        search_done = True
                        break

            if not search_done:  # Mitte
                for word_num in range(self.cur_Pos - self.expandRange, self.cur_Pos + self.expandRange + 1):
                    if word_num + 1 < 10:
                        word_num_str = str(word_num + 1) + "  "
                    elif word_num + 1 < 100:
                        word_num_str = str(word_num + 1) + " "
                    else:
                        word_num_str = str(word_num + 1)
                    if self.cur_Pos == word_num:
                        if not self.debug:
                            if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                print(
                                    " " + word_num_str + " * " + getPartStr(self.music[self.searchlist[word_num]]["name"],
                                                                            0, 108) + "...")
                            else:
                                print(" " + word_num_str + " * " + self.music[self.searchlist[word_num]]["name"])
                        else:
                            print(" " + word_num_str + " * " + self.music[self.searchlist[word_num]]["name"], 10,
                                  self.searchlist[word_num])
                    else:
                        if not self.debug:
                            if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                print(
                                    " " + word_num_str + "   " + getPartStr(self.music[self.searchlist[word_num]]["name"],
                                                                            0, 108) + "...")
                            else:
                                print(" " + word_num_str + "   " + self.music[self.searchlist[word_num]]["name"])
                        else:
                            print(" " + word_num_str + "   " + self.music[self.searchlist[word_num]]["name"], 11,
                                  self.searchlist[word_num])






    def print_foot(self):


        if self.con_cont == "set":
            print("Commands:\n")

            if not self.paused:
                print("Pause (P), Delthis (DEL), Next (N), Reroll all (RE), Reroll this (RT), Queue this (QU), Details (DEA)")
            elif self.paused:
                print("Play (P), Delthis (DEL), Next (N), Reroll all (RE), Reroll this (RT), Queue this (QU), Details (DEA)")

            if self.con_main == "spl":
                self.spl.printcom()

            print("\nInput:\n%s" % self.cur_Input)

        elif self.con_cont == "search":
            print("Commands: (with UPPER LETTERs)\n")

            print("Play this (P), Delthis (DEL), Queue this (QU)")

            print("\nInput: %s" % self.cur_Input.upper())

            print("\nSearch: (with lower letters)\n")
            print("Input: %s" % self.cur_Search)

        elif self.con_cont == "conf":
            print("Confirm\n")
            print("Y/N")

        elif self.con_cont == "cont":
            print("Continue?\n")
            print("Press something")

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

    def printit(self):
        self.last_print = time.time()
        cls()

        # Info-Container
        self.print_head()

        print("\n" + console_data["pixx"]*"-" + "\n")
        # Main-Container
        self.print_body()


        print("\n" + console_data["pixx"]*"-" + "\n")
        # Control-Container
        self.print_foot()

    def react(self, inp):
        while self.starttime + 1.5 >= time.time() and self.hardworktime + 0.65 >= time.time():
            time.sleep(0.25)

        if self.con_main == "details":
            self.con_main = self.con_main_last
            self.con_cont = "set"

        # Search BLOCK

        elif inp == "escape" and self.searching:
            self.con_main = "pl"
            self.con_cont = "set"
            self.searching = False
            self.cur_Search = ""
            self.cur_Input = ""

        elif inp == " " and self.searching:
            self.cur_Search += " "
            self.refreshSearch()

        elif len(inp) == 1 and self.searching:
            if inp == inp.lower(): # SEARCH
                self.cur_Search += inp
                self.refreshSearch()

            else: # COMMANDS
                self.cur_Input += inp

                i = self.cur_Input.lower()

                # Search commands
                if i == "play" or i == "pau" or i == "pause" or i == "p":
                    oldPL = self.playlist.copy()
                    del oldPL[Search(self.searchlist[self.cur_Pos], self.playlist)[0]]
                    self.playlist = [self.searchlist[self.cur_Pos]] + oldPL
                    self.next(True)

                    self.con_main = "pl"
                    self.con_cont = "set"
                    self.searching = False
                    self.cur_Search = ""
                    self.cur_Pos = 0

                    self.cur_Input = ""

                elif i == "del":
                    self.Del_plfile(self.searchlist[self.cur_Pos])
                    self.refreshSearch()
                    self.cur_Input = ""

                elif i == "qu":
                    self.queue_plfile(self.searchlist[self.cur_Pos])
                    self.cur_Input = ""

                # Musicplayer commands
                elif i == "next" or i == "n":
                    self.next()
                    self.cur_Input = ""
                elif i == "m":
                    self.switchmute()
                    self.cur_Input = ""
                elif i == "stop" or i == "exit":
                    self.stop()
                    self.cur_Input = ""



        elif inp == "del" and self.searching:
            self.Del_plfile(self.searchlist[self.cur_Pos])
            self.refreshSearch()
            self.cur_Input = ""

        elif inp == "return" and self.searching:
            oldPL = self.playlist.copy()
            del oldPL[Search(self.searchlist[self.cur_Pos], self.playlist)[0]]
            self.playlist = [self.searchlist[self.cur_Pos]] + oldPL
            self.next(True)

            self.con_main = "pl"
            self.con_cont = "set"
            self.searching = False
            self.cur_Search = ""
            self.cur_Pos = 0

            self.cur_Input = ""


        elif inp == "backspace" and self.searching: # SEARCH
            if len(self.cur_Search) > 0:
                new_Search = ""
                for x in range(len(self.cur_Search) - 1):
                    new_Search += self.cur_Search[x]
                self.cur_Search = new_Search

                self.refreshSearch()

        elif inp == "strg_backspace" and self.searching: # COMMANDS
            if len(self.cur_Input) > 0:
                new_Input = ""
                for x in range(len(self.cur_Input) - 1):
                    new_Input += self.cur_Input[x]
                self.cur_Input = new_Input

        elif inp == "arrowup" and self.cur_Pos > 0 and self.searching:
            self.cur_Pos -= 1
        elif inp == "arrowdown" and self.cur_Pos < len(self.searchlist) - 1 and self.searching:
            self.cur_Pos += 1


        elif inp == " ":
            self.switch()

        elif len(inp) == 1 and not self.searching: #MAIN give to next method
            self.cur_Input += inp
            if self.input(self.cur_Input):
                self.cur_Input = ""


        elif inp == "backspace" and not self.searching:
            if len(self.cur_Input) > 0:
                new_Input = ""
                for x in range(len(self.cur_Input) - 1):
                    new_Input += self.cur_Input[x]
                self.cur_Input = new_Input

        elif inp == "strg_backspace" and not self.searching:
            self.cur_Input = ""


        elif self.change and inp == "escape":
            self.cur_Input = ""
            self.change = ""
            self.con_cont = "set"

        elif self.change == "volp":
            if inp == "return":
                self.volp(float(self.cur_Input))
                self.cur_Input = ""
                self.change = ""
                self.con_cont = "set"

        elif self.change == "volw":
            if inp == "return":
                if len(self.cur_Input) > 4:
                    self.cur_Input = getPartStr(self.cur_Input, begin=0, end=4)
                self.vol(float(self.cur_Input))
                self.cur_Input = ""
                self.change = ""
                self.con_cont = "set"

        elif self.change == "spe":
            if inp == "return":
                self.spl.ChEffect(int(self.cur_Input))
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
            self.Del(self.cur_Pos)

        elif inp == "return" and self.con_main == "pl":
            oldPL = self.playlist.copy()
            del oldPL[self.cur_Pos]
            self.playlist = [self.playlist[self.cur_Pos]] + oldPL
            self.next(True)
        else:
            return False

        self.printit()
        self.last_print_auto = time.time()

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
            self.Del(self.cur_Pos)

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
            self.con_main_last = self.con_main
            self.con_main = "details"
            self.con_cont = "cont"
        elif i == "sortfile":
            self.sortPL()
            self.next(True)
        elif i == "sortname":
            self.sortPL_name()
            self.next(True)
        elif i == "sortan":
            self.sortPL_an()
            self.next(True)
        elif i == "qu":
            self.queue(self.cur_Pos)
        elif i == "debug":
            if self.debug:
                self.debug = False
            else:
                self.debug = True
        elif i == "refresh":
            self.refreshTitle()
            self.printit()

        elif i == "autorefresh" and self.debug:
            if self.autorefresh:
                self.autorefresh = False
            else:
                self.autorefresh = True

        elif i == "search" and self.con_main == "pl":
            self.con_main = "search"
            self.con_cont = "search"
            self.searching = True
            self.cur_Search = ""
            self.cur_Input = "" # need this ?
            self.refreshSearch()


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

    def react_remote(self, i, java=False):
        if isinstance(i, tuple):
            self.remoteAddress = i[0]
        elif i is None:
            self.remoteAddress = ""
            self.remoteAction = ""
        else: # COMMANDS
            """
            HOW:
            
            type_what(_value)
            
            eg.: 
            set_pause_0
            get_pause
            """
            data = i.split("_")

            if data[0] == "set":
                if data[1] == "next":
                    self.next()
                    self.remoteAction = "Next"
                elif data[1] == "pause":
                    if len(data) == 3:
                        if data[2] == "0":
                            self.play()
                            self.remoteAction = "Unpause"
                        elif data[2] == "1":
                            self.pause()
                            self.remoteAction = "Pause"
                    else:
                        self.switch()
                        self.remoteAction = "Switch pause"
                elif data[1] == "mute":
                    if len(data) == 3:
                        if data[2] == "0":
                            self.unmute()
                            self.remoteAction = "Unmute"
                        elif data[2] == "1":
                            self.mute()
                            self.remoteAction = "Mute"
                    else:
                        self.switchmute()
                        self.remoteAction = "Switch mute"
                elif data[1] == "exit":
                    self.stop()
                elif data[1] == "volume" and len(data) == 3:
                    self.vol(float(data[2]))
                    self.remoteAction = "Volume to: " + str(self.volume)
                elif data[1] == "volumep" and len(data) == 3:
                    self.volp(float(data[2]))
                    self.remoteAction = "VolumeP to: " + str(self.volumep)


            elif data[0] == "get":
                data_send = ""
                if data[1] == "title":
                    data_send = self.getCur()["name"]
                elif data[1] == "time":
                    data_send = round(self.timer.getTime())
                elif data[1] == "duration":
                    data_send = round(self.getCur()["loaded"].duration)
                elif data[1] == "volume":
                    data_send = str(Volume.getVolume())
                #print(data_send)
                if data_send:
                    if not java:
                        self.server.send(data_send)
                    else:
                        self.server_java.send(data_send)





class RadioC:
    def __init__(self, systray=True):
        super().__init__()

        self.streampause = False
        self.streamrun = True
        self.streamvolume = Volume.getVolume()

        self.streamplayer = MPlayerC("Programs\\MPlayer")

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

        self.send(InfoSend, encrypt=False, direct=True)

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


    def send(self, data, encrypt=None, direct=False):
        if self.Running and self.Connected and self.Status != "Ended" and self.Status == "Connected" or direct:
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

            self.s.send(data_send_de)

            if type(data) == str:
                data_str = data
            elif type(data) == bytes:
                data_str = data.decode("UTF-8")
            else:
                data_str = str(data)

            self.Logsend.append(data_str)
            self.writeLog("Send: " + data_str)
        else:
            return False

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
            if type(x) == str:
                file_logsend_raw.write(x)
            elif type(x) == bytes:
                file_logsend_raw.write(x.decode("UTF-8"))
            elif type(x) == bool:
                file_logsend_raw.write(str(x))
        file_logsend_raw.close()

        file_logrece_raw = open("LogReceive.txt", "w")
        for x in self.Logrece:
            if type(x) == str:
                file_logrece_raw.write(x)
            elif type(x) == bytes:
                file_logrece_raw.write(x.decode("UTF-8"))
            elif type(x) == bool:
                file_logrece_raw.write(str(x))
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
        self.Connected = False
        self.Status = "Lost Connection"

    def getStatus(self):
        curStatus = {"status" : {"status" : self.Status, "running" : self.Running, "connected" : self.Connected},
                     "log": self.Log, "info" : self.Info}
        return curStatus


class Server(threading.Thread):
    def __init__(self, port: int, react, ip=socket.gethostbyname(socket.gethostname()), buffersize=1024,
                 loginName=None, loginPW=None, maxConnections=1, Seculevel=0, BigServerBuffersize=0,
                 BigServerPort=0, welcomeMessage="Welcome to Evecon Server!", thisBig=False, printLog=True, reactLogINOUT=False):
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

        reactLogINOUT
        if True the server will send a react with only the ip-address if the connection is succsessful
        at disconnet with None

        Keywords:
        #C! for a command
        #T! do not use, this will be used to talk to the client directly, like login in
        #R! for receiving some return infomation
        #B! for travel through bigserver

        """
        super().__init__()

        self.version = "1.0.0"

        self.port = usedPorts.givePort(port)

        self.thisBigServer = thisBig
        self.react = react
        self.ip = ip
        self.buffersize = buffersize
        self.maxConnections = maxConnections
        self.welcomeMessage = welcomeMessage
        self.printLog = printLog
        self.reactLogINOUT = reactLogINOUT

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
            self.send(InfoSend, encrypt=False, direct=True)

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

            if self.welcomeMessage:
                self.send(self.welcomeMessage)

            if self.reactLogINOUT:
                self.react(self.conAddress)

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


            if self.reactLogINOUT:
                self.react(None)

        self.Running = False
        self.Status = "Ended"

    def send(self, data, encrypt=None, direct=False):
        if self.Running and self.Connected and self.Status != "Ended" and self.Status == "Connected" or direct:

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
        if self.printLog:
            print("[Log] " + write)

    def save(self, directory: str):
        file_log_raw = open("Log.txt", "w")
        for x in self.Log:
            file_log_raw.write(x + "\n")
        file_log_raw.close()

        file_logsend_raw = open("LogSend.txt", "w")
        for x in self.Logsend:
            if type(x) == str:
                file_logsend_raw.write(x + "\n")
            elif type(x) == bytes:
                file_logsend_raw.write(x.decode("UTF-8") + "\n")
            elif type(x) == bool:
                file_logsend_raw.write(str(x) + "\n")
        file_logsend_raw.close()

        file_logrece_raw = open("LogReceive.txt", "w")
        for x in self.Logrece:
            if type(x) == str:
                file_logrece_raw.write(x + "\n")
            elif type(x) == bytes:
                file_logrece_raw.write(x.decode("UTF-8") + "\n")
            elif type(x) == bool:
                file_logrece_raw.write(str(x) + "\n")
        file_logrece_raw.close()

    def exit(self, sendM=True):
        if self.con:
            if sendM:
                self.send("#T!exit")
            self.con.close()
        self.Connected = False
        self.Running = False
        usedPorts.remPort(self.port)

    def close_connection(self):
        if self.con and self.Connected:
            self.send("#T!exit")
            self.con.close()
            self.Connected = False
            usedPorts.remPort(self.port)

    def getStatus(self):
        curStatus = {"status": {"status": self.Status, "running": self.Running, "connected": self.Connected},
                     "log": self.Log, "info": self.Info, "connects": self.connects}
        return curStatus

    def getRunTime(self, raw=True):
        if raw:
            return self.Timer.getTime()
        else:
            return self.Timer.getTimeFor()

class ServerJava(threading.Thread):
    def __init__(self, ip, port, react, allowPrint=False, giveJava=True, sendIP=True):
        super().__init__()
        self.host = ip
        self.allowPrint = allowPrint
        self.port = usedPorts.givePort(port)
        self.giveJava = giveJava
        self.sendIP = sendIP

        self.Running = False
        self.Connected = False
        self.End = False
        self.allDataSend = []
        self.allDataRec = []
        self.s = socket.socket()
        self.conAddress = None
        self.con = None

        self.reac = react

    def stop(self):
        self.Running = False
        self.End = True
        self.Connected = False
        self.con.close()

    def send(self, data):
        if self.Running and self.Connected and not self.End:
            if type(data) == str:
                data = data.encode()
            else:
                data = str(data).encode()
            data += b'\r\n'
            if self.allowPrint:
                print("[Log] Sending:" + str(data))
            self.con.send(data)
            self.allDataSend.append(data)

    def react(self, curData):
        if self.allowPrint:
            print("[Log] Recieving:" + str(curData))
        data = curData.decode("UTF-8").lstrip().rstrip()
        if self.giveJava:
            self.reac(data, java=True)
        else:
            self.reac(data)

    def run(self):
        self.Running = True
        self.bind()

        if self.allowPrint:
            print("[Log] Started!")
        while self.Running:
            self.s.listen(1)
            self.con, self.conAddress = self.s.accept()
            if self.allowPrint:
                print("[Log] Connected:" + str(self.conAddress))
            if self.sendIP:
                self.reac(self.conAddress)
            self.Connected = True
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

        self.stop()

    def bind(self):
        self.s.bind((self.host, self.port))


class BrowserOld:
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

"""
class Firefox(Browser):
    def __init__(self, path=firefox_path):
        super().__init__(path)

        self.bro = webbrowser.Mozilla(self.path)
"""

class Vivaldi(BrowserOld):
    def __init__(self, path=vivaldi_path):
        super().__init__(path)

        self.bro = webbrowser.Chrome(self.path)

class Browser:
    def __init__(self, path):
        self.path = path

        self.com_newWin = ""
        self.com_newTab = ""
        self.path_dir = ""
        for x in self.path.split(path_seg):
            if x == "C:":
                self.path_dir = x
            elif x != "firefox.exe":
                self.path_dir += path_seg + x

        self.name = self.path.split(path_seg)[-1]
        if self.name in (p.name() for p in psutil.process_iter()):
            self.running = True
        else:
            self.running = False


    def open(self, url: list, new_type=2):
        if type(url) != list:
            url = [url]
        for x in url:
            self.open_tab(url=str(x))

    def open_win(self, url: str):
        dir_tmp = os.getcwd()
        os.chdir(self.path_dir)
        subprocess.call([self.name, self.com_newWin, url])
        time.sleep(0.15)
        os.chdir(dir_tmp)

    def open_tab(self, url: str):
        dir_tmp = os.getcwd()
        os.chdir(self.path_dir)
        subprocess.call([self.name, self.com_newTab, url])
        time.sleep(0.15)
        os.chdir(dir_tmp)

    def refresh(self):
        if self.name in (p.name() for p in psutil.process_iter()):
            self.running = True
        else:
            self.running = False

class Firefox(Browser):
    def __init__(self, path=firefox_path):
        super().__init__(path)

        self.com_newWin = "-new-window"
        self.com_newTab = "-new-tab"


class MusicPlayerRemote:
    #TODO: HERE
    pass






title("Loading Title Time")


def computerconfig_schoolpc():
    color.change("F0")

def computerconfig_minipc():
    pass

def computerconfig_bigpc():
    pass

def computerconfig_aldi():
    nircmd("setsize", 1000, 520)

def computerconfig_laptop():
    pass


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
    this_version.append(code_version)
    return this_version

def normaltitle():
    #global ss_active
    if ss_active:
        title("Screensaver", "")

    else:
        title("OLD", "Version: " + str(versionFind()[2]))

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
        print("Code-Version: " + versionFind()[2])
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

    status = {
        "version": {"version": versionFind()[1], "codeversion": versionFind()[2], "versionnumber": versionFind()[0]},
        "evecontype": version, "pid": os.getpid(), "computername": Computername, "username": getpass.getuser(),
        "computersyn": computer, "ip": thisIP, "homepc": HomePC}

    return status #[versionFind()[1], versionFind()[2], versionFind()[0], version, os.getpid(),Computername, getpass.getuser(), computer, thisIP, HomePC]


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
                print("\nWeapon Randomizer (WR), Effect ('E'+number), Reroll Next Weapon (REROLL)")
            else:
                print("\nWeapon Randomizer (WR), Effect ('E'+number)")

        if self.RoundOver:
            print("\nStart Next Round?")

    def printcom(self):
        if self.WR:
            print("Weapon Randomizer (spWR), Effect (spE), Next Round (spN), Reroll Next Weapon (spR)")
        else:
            print("Weapon Randomizer (spWR), Effect (spE), Next Round (spN)")




def Search(searchkeyU, searchlistU, exact=False, lower=True, onlyOnce=True):

    if len(searchkeyU) == 0:
        return []

    if lower:
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
        if exact:
            if searchlist[sListNum] == searchkey:
                OutputNum.append(sListNum)
            else:
                continue
        if len(searchkey) > len(searchlist[sListNum]):
            continue  # suchwort größer als anderes wort (jetzt in der Liste)

        for letterNum in range(len(searchlist[sListNum])): # buchstabe aus wort aus der gesamt liste
            if searchlist[sListNum][letterNum] == searchkey[0]: # ist ein Buchstabe (aus der for-Schleife) auch in dem Suchwort[0] vorhanden?
                test = True

                for keyNum in range(len(searchkey)):
                    if test:
                        test = False
                        if keyNum == len(searchkey) - 1: # Fall: Wenn das Suchwort nur ein Buchstabe groß ist!
                            OutputNum.append(sListNum)
                            break
                        continue

                    # was macht das ?: wenn es der letzte buchstabe vom String ist ende
                    if len(searchlist[sListNum]) - 1 < keyNum + letterNum:
                        break
                    #if len(searchlist[sListNum]) - 1 < keyNum + letterNum:
                    #    print(OutputNum, sListNum, searchlist[sListNum], letterNum, searchlist[sListNum][letterNum], keyNum)

                    if searchlist[sListNum][keyNum + letterNum] == searchkey[keyNum]:
                        if keyNum == len(searchkey) - 1:

                            # if the keyword is two times in the fullword: this is a protect of duplication
                            doit = True
                            for NumOldList in OutputNum:
                                if NumOldList == sListNum:
                                    doit = False
                                    break

                            if doit:
                                OutputNum.append(sListNum)
                            break
                    else:
                        break

    if onlyOnce:
        OutputNum = DelDouble(OutputNum)


    return OutputNum


def DelDouble(workList: list):
    """
    deletes everything in the list which is multiple in the list

    :param workList: the list
    :return: new list
    """

    newList = []

    for x in workList:
        found=False
        for y in newList:
            if x == y:
                found=True
        if not found:
            newList.append(x)


    return newList


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


# Klakum.relays[0].set(2)


class KlakumC:
    class RelayC:
        def __init__(self, myid, connection):
            self.id = myid
            self.connetion = connection
            self.value = None

        def refresh(self):
            if self.connetion.Connected:
                self.connetion.send("relay_" + str(self.id) + "_get")

        def set(self, value):
            if self.connetion.Connected:
                self.value = value
                self.connetion.send("relay_" + str(self.id) + "_set_" + str(value))

        def switch(self):
            if self.connetion.Connected:
                self.connetion.send("relay_" + str(self.id) + "_switch")

    class SRelayC:
        def __init__(self, myid, connection):
            self.id = myid
            self.connetion = connection

        def switch(self):
            if self.connetion.Connected:
                self.connetion.send("srelay_" + str(self.id) + "_switch")

    def __init__(self):
        self.connection = Client(ip="192.168.2.107", port=1007, react=self.react)
        self.relays = [self.RelayC(0, self.connection), self.RelayC(1, self.connection), self.RelayC(2, self.connection),
                       self.RelayC(3, self.connection), self.RelayC(4, self.connection), self.RelayC(5, self.connection),
                       self.RelayC(6, self.connection)]

        self.srelays = [self.SRelayC(0, self.connection)]

        self.Connected = False


    def react(self, msg):
        msg_split = msg.split("_")

        if msg_split[0] == "relay":

            relay_id = int(msg_split[1])
            if msg_split[2] == "return":
                self.relays[relay_id].value = msg_split[3]

        elif msg_split[0] == "srelay":
            relay_id = int(msg_split[1])

    def connect(self):
        if not self.Connected:
            self.connection.start()
            while not self.connection.Connected:
                time.sleep(0.05)
            time.sleep(0.15)
            self.Connected = True
            self.refresh()
            time.sleep(0.05)
            return True
        else:
            return False

    def disconnect(self):
        if self.Connected:
            self.connection.exit()
            self.Connected = False

            return True
        else:
            return False

    def refresh(self):
        for x in self.relays:
            x.refresh()
            time.sleep(0.05)

Klakum = KlakumC()


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