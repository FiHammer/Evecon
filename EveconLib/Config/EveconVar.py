
title_time = None  # title time init later
title_refresh_time = 2.5

myType = ""

# servers init later

globalMPports = None
globalMPportsJava = None

logServer = None
logServerPort = 4222

ddbugger = None

# filePaths

import sys
if sys.platform == "win32":
    path_seg = "\\"
else:
    path_seg = "/"

environmentPath = ""  # standard path

infoPath = "data" + path_seg + "Info"
versionFile = infoPath + path_seg + "version"
changelogFile = infoPath + path_seg + "Changelog.txt"

notiePath = "data" + path_seg + "Noties"
outputPath = "data" + path_seg + "Output"


tmpPath = "data" + path_seg + "tmp"

usedPortsFile = tmpPath + path_seg + "usedPorts.txt"


dataPath = "data" + path_seg + "Data"

nheeDir = dataPath + path_seg + "nhee" + path_seg
foxiDir = dataPath + path_seg + "foxi" + path_seg


configPath = "data" + path_seg + "config"

splWeapFile = configPath + path_seg + "splWeap.json"
MusicFile = configPath + path_seg + "Music.json"
deacSSFile = configPath + path_seg + "deacSS"


logFile = "data" + path_seg + "log.txt"


backupPath = "data" + path_seg + "Backup"

backupMusicFile = backupPath + path_seg + "Music.json"

icoPath = "data" + path_seg + "Ico"
radioIcoFile = icoPath + path_seg + "Radio.ico"
