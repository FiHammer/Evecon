
import sys
if sys.platform == "win32":
    path_seg = "\\"
else:
    path_seg = "/"
firefox_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
vivaldi_path = "C:\\Program Files (x86)\\Vivaldi\\Application\\vivaldi.exe"

code_version = "0.9.9.1"

ss_active = False
exitnow = 0
pausetime = 180
musicrun = False
thisIP = "127.0.0.1"
StartupServer = None
browser = "firefox"
startmain = False
Alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
musicrandom = True
enable_FoxNhe = False
foxORnhe = "nhee"
cores = 2
console_data = {"lenx": 120, "leny": 30, "posx": 0, "posy": 0, "pixx": 120, "pixy": 30}
thisHWND = 0

myType = "" # type of the console: python_file, standalone_exe, lib_exe

title_oldstatus = "Loading"
title_oldstart = "Error"
title_oldversion = "Error"
title_dead = False
