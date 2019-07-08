import os
# set dir
orgDir = os.getcwd()

path_seg = "\\"

if os.getcwd() == "C:\\Users\\Mini-Pc Nutzer.000\\Desktop\\Evecon\\!Evecon\\dev":
    os.chdir("..")
    os.chdir("..")

elif os.getcwd().split(path_seg)[-2] == "!Evecon":
    if os.getcwd().split(path_seg)[-1] == "dev" or os.getcwd().split(path_seg)[-1] == "!Console" or os.getcwd().split(path_seg)[-1] == "Exe":
        os.chdir("..")
        os.chdir("..")
elif os.getcwd().split(path_seg)[-1] == "!Evecon":
    os.chdir("..")
del path_seg



import EveconLib.Config
import EveconLib.Games
import EveconLib.Networking
import EveconLib.Programs
import EveconLib.Tools

import EveconLib.EveconExceptions


# starting startup functions

EveconLib.Programs.Startup.Startup.startup()