from EveconLib.Config.StaticVar import *
from EveconLib.Config.EveconVar import *


loadFull = False

# startup
import configparser
import os

file_versions = []
file_version = code_version
def refreshVersion():
    global file_versions
    with open("data" + path_seg + "Info" + path_seg + "version", "r") as file_version_raw:
        file_versions = file_version_raw.readlines()
    del file_version_raw
    file_versions.append(code_version)

    file_version = file_versions[1]


def readConfig():
    global browser, musicrandom, enable_FoxNhe, thisIP, cores, foxORnhe, firefox_path, vivaldi_path
    config = configparser.ConfigParser()
    config.read("data" + path_seg + "Config" + path_seg + "config.ini")
    try:
        enable_FoxNhe_tmp = config["FoxNhe"]["enable_FoxNhe"]
        if enable_FoxNhe_tmp == "True":
            enable_FoxNhe = True
        elif enable_FoxNhe_tmp == "False":
            enable_FoxNhe = False
        foxORnhe = config["FoxNhe"]["foxORnhe"]

        musicrandom_tmp = config["Music"]["random"]
        if musicrandom_tmp == "True":
            musicrandom = True
        elif musicrandom_tmp == "False":
            musicrandom = False

        browser = config["Notepad"]["browser"]
        firefox_path = config["Browser"]["firefox_path"]
        vivaldi_path = config["Browser"]["vivaldi_path"]

        thisIP = config["PC"]["thisIP"]

        cores = int(config["PC"]["cores"])
    except KeyError:
        pass

if os.path.exists("!Console.py") and os.path.exists("EveconLib"):
    myType = "python_file"
elif os.path.exists("!Console.exe") and not os.path.exists("!Console.exe.manifest"):
    myType = "standalone_exe"
elif os.path.exists("!Console.exe") and os.path.exists("!Console.exe.manifest"):
    myType = "lib_exe"

import socket

Computername = socket.gethostname()

if Computername == "Computer-Testet":
    computer = "MiniPC"
    HomePC = True

elif Computername == "Bigger-PC":
    computer = "BigPC"
    HomePC = True

elif Computername == "Test":
    computer = "AldiPC"

elif Computername == "Luis":
    computer = "Laptop"

else:
    computer = None


refreshVersion()

# read config

readConfig()