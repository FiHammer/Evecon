from EveconLib.Config.StaticVar import *
from EveconLib.Config.EveconVar import *


loadFull = False
suppressErros = False

# startup
import configparser
import os

file_versions = []
file_version = code_version
def refreshVersion():
    global file_versions
    if not os.path.exists(versionFile):
        file_versions = [0, "0.0.0.0", "0.0.0.0"]
        file_version = "0.0.0.0"
        return
    with open(versionFile, "r") as file_version_raw:
        file_versions = file_version_raw.readlines()
    del file_version_raw
    file_versions.append(code_version)

    file_version = file_versions[1]

validEnv = False
def testEnv():
    #print(os.path.exists(usedPortsFile), os.path.exists(backupMusicFile))
    if os.path.exists(usedPortsFile) and os.path.exists(backupMusicFile):
        validEnv = True
        return True
    else:
        validEnv = False

        if suppressErros:
            print("Invalid Enviroment!")
        else:
            input("Invalid Enviroment!\nYou can go on (Enter), but something could happen")
        return False


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


        thisIP = config["PC"]["thisIP"]

        cores = int(config["PC"]["cores"])

        browser = config["Notepad"]["browser"]
        firefox_path = config["Browser"]["firefox_path"]
        vivaldi_path = config["Browser"]["vivaldi_path"]
    except KeyError:
        if suppressErros:
            print("Config Error something crashed!")
        else:
            input("Config Error something crashed!\nYou can go on (Enter), but something could happen")


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
testEnv()
# read config

readConfig()