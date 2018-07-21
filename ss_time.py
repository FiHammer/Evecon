# nach licht dateien suchen
# time ausgabe

import subprocess
import time
import datetime
import ctypes
import os
import threading
from cls import *

cdir = os.getcwd()
os.chdir("..")
os.chdir("..")
os.chdir("..")

ctypes.windll.kernel32.SetConsoleTitleW("Time Printer")

dir_tmp = os.getcwd()
os.chdir("Programs\\nircmd")
subprocess.call(["nircmdc", "win", "max", "title", "Time Printer"])# nircmd mach mich groß # nircmdc win max title "NirCmd"
time.sleep(0.1)
os.chdir(dir_tmp)





class colorsearcher(threading.Thread):
    def run(self):
        while True:
             # file exist ? => read => lösche => color change

            if os.path.exists("data\\tmp\\sscolor"):

                color_data = open("data\\tmp\\sscolor", "r")
                color = color_data.readline()
                color_data.close()

                os.remove("data\\tmp\\sscolor")

                if color == "dark":
                    os.system("color 07")
                elif color == "bright":
                    os.system("color F0")

            time.sleep(0.15)

colorsearch = colorsearcher()
colorsearch.start()

def Timeprint():
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
            while RUN:
                refreshtime()
                printtime()
                time.sleep(1)

    runer = runner()
    runer.start()


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

def Alarmprint():
    import random
    # insgesamter Block: 135x60
    afk = True
    def randi():
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
        for x in range(random.randint(1, 5)):
            randlist.append(randlist[random.randint(0, len(randlist) - 1)])

        block = ""
        for x in range(230):
            block += str(randlist[random.randint(0, len(randlist) - 1)])
        return block
    class printre(threading.Thread):
        def run(self):
            nonlocal afk
            while afk:
                cls()
                for x in range(65):
                    print(randi())
                time.sleep(0.75)

    printri = printre()
    printri.start()

    input()
    afk = False


Timeprint()

while True:
    user_input = input()
    if user_input.lower() == "t" or user_input.lower() == "tim" or user_input.lower() == "timer":
        RUN = False
        cls()
        print("Timer\nStunden:")
        hoursx = input()
        if hoursx == "":
            hoursx = 0
        else:
            try:
                hoursx = int(hoursx)
            except ValueError:
                print("Wrong input")
                hoursx = 0

        cls()
        print("Timer\nMinuten:")
        minux = input()
        if minux == "":
            minux = 0
        else:
            try:
                minux = int(minux)
            except ValueError:
                print("Wrong input")
                minux = 0

        cls()
        print("Timer\nSekunden:")
        secx = input()
        if secx == "":
            secx = 0
        else:
            try:
                secx = int(secx)
            except ValueError:
                print("Wrong input")
                secx = 0

        Timerprint(hoursx, minux, secx)
        Alarmprint()
        Timeprint()