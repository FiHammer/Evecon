import os
import sys
# set dir
orgDir = os.getcwd()

if sys.platform == "win32":
    path_seg = "\\"
    # adding here (for pyglet) the ffmpeg libs
    os.environ["PATH"] += r";C:\Dev\ffmpeg\bin"
else:
    path_seg = "/"


if os.getcwd() == "C:\\Users\\Mini-Pc Nutzer.000\\Desktop\\Evecon\\!Evecon\\dev":
    os.chdir("..")
    os.chdir("..")
elif os.getcwd().split(path_seg)[-1] == "!Evecon":
    os.chdir("..")
elif len(os.getcwd().split(path_seg)) <= 1:
    pass
elif os.getcwd().split(path_seg)[-2] == "!Evecon":
    if os.getcwd().split(path_seg)[-1] == "dev" or os.getcwd().split(path_seg)[-1] == "!Console" or os.getcwd().split(path_seg)[-1] == "Exe":
        os.chdir("..")
        os.chdir("..")
del path_seg

import EveconLib.Tools
import EveconLib.Programs
import EveconLib.Config
import EveconLib.Games
import EveconLib.Networking

import EveconLib.EveconExceptions


# starting startup functions

EveconLib.Programs.Startup.Startup.startup()