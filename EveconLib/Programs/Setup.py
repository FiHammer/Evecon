import os
import sys
import shutil
import subprocess
import json

import EveconLib.Tools.NonStaticTools
# static vars
import EveconLib.Config

#import urllib
import urllib.request

def setup(): # TODO change EveconLib to dir
    # am I .exe or .py
    print("Evecon Setup:\nInitializing")
    print("Path: " + os.getcwd())
    if not EveconLib.Config.myType: # string is empty
        print("ERROR: Evecon FILE NOT FOUND")
        print("Change the file name to !Console.exe or .py (with EveconLib & Tools & Exception & MiniDebug)")
        EveconLib.Tools.NonStaticTools.exit_now()
        return

    existFile = open("selfstart", "w")
    existFile.write("Hello File!")
    existFile.close()

    curDir = os.getcwd()
    last = curDir.split(EveconLib.Config.path_seg)[-1]
    selfBuild = os.path.exists("selfbuild")

    if len(sys.argv) > 2:
        if os.path.exists(sys.argv[2]):
            os.chdir(sys.argv[2])

    selfStart = os.path.exists("selfstart")

    os.chdir(curDir)

    print("Started as " + EveconLib.Config.myType)

    if last == "dev" and EveconLib.Config.myType == "python" and selfBuild and selfStart:
        stepOne = True
    elif last == "!Console" and EveconLib.Config.myType == "lib_exe" and selfBuild and selfStart:
        stepOne = True
    elif last == "Exe" and EveconLib.Config.myType == "standalone_exe" and selfBuild and selfStart:
        stepOne = True
    else:
        print("Start copying")
        try:
            shutil.rmtree("!Evecon")
        except FileNotFoundError:
            pass
        if EveconLib.Config.myType == "python":
            os.mkdir("!Evecon")
            dst = "!Evecon" + EveconLib.Config.path_seg + "dev"
            os.mkdir(dst)
            shutil.copy("!Console.py", dst)
            shutil.copy("EveconLib.py", dst)
            shutil.copy("EveconTools.py", dst)
            shutil.copy("EveconExceptions.py", dst)
            shutil.copy("EveconMiniDebug.py", dst)

            if os.path.exists("EveconLogListener.py"):
                shutil.copy("EveconLogListener.py", dst)
            if os.path.exists("ss_time.py"):
                shutil.copy("ss_time.py", dst)
            if os.path.exists("updater.py"):
                shutil.copy("updater.py", dst)

            existFile = open(dst + EveconLib.Config.path_seg + "selfbuild", "w")
            existFile.write("Hello File!")
            existFile.close()

            print("Start from new Location")
            # input(dst + path_seg + "!Console.py")
            # subprocess.Popen(["python.exe", dst + path_seg + "!Console.py", "--setup", curDir], creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=dst)
            subprocess.Popen(["python.exe", os.getcwd() + EveconLib.Config.path_seg + dst + EveconLib.Config.path_seg + "!Console.py", "--setup", curDir],
                             cwd=dst)

        elif EveconLib.Config.myType == "standalone_exe":
            os.mkdir("!Evecon")
            dst = "!Evecon" + EveconLib.Config.path_seg + "Exe"
            os.mkdir(dst)
            shutil.copy("!Console.exe", dst)

            existFile = open(dst + EveconLib.Config.path_seg + "selfbuild", "w")
            existFile.write("Hello File!")
            existFile.close()

            print("Start from new Location")
            subprocess.Popen([os.getcwd() + EveconLib.Config.path_seg + dst + EveconLib.Config.path_seg + "!Console.exe", "--setup", curDir],
                             creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=dst)

        elif EveconLib.Config.myType == "lib_exe":
            # os.mkdir("!Evecon" + path_seg + "!Console")
            os.chdir("..")
            os.mkdir("EveconEnv")
            os.mkdir("EveconEnv" + EveconLib.Config.path_seg + "!Evecon")
            dst = "EveconEnv" + EveconLib.Config.path_seg + "!Evecon"
            shutil.copytree(last, dst)
            os.rename(dst + EveconLib.Config.path_seg + last, dst + EveconLib.Config.path_seg + "!Console")

            existFile = open(dst + EveconLib.Config.path_seg + "!Console" + EveconLib.Config.path_seg + "selfbuild", "w")
            existFile.write("Hello File!")
            existFile.close()

            print("Start from new Location")
            subprocess.Popen(
                [os.getcwd() + EveconLib.Config.path_seg + dst + EveconLib.Config.path_seg + "!Console" + EveconLib.Config.path_seg + "!Console.exe", "--setup", curDir],
                creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=dst + EveconLib.Config.path_seg + "!Console")

        EveconLib.Tools.NonStaticTools.exit_now()
        #sys.exit()

    print("Started in the right dir!")
    print("Deleting old files (no Console-Lib)")

    os.remove("selfbuild")

    os.chdir("..")
    os.chdir("..")

    if EveconLib.Config.myType == "python":
        os.remove("!Console.py")
        os.remove("EveconLib.py")
        os.remove("EveconTools.py")
        os.remove("EveconExceptions.py")

        if os.path.exists("EveconLogListener.py"):
            os.remove("EveconLogListener.py")
        if os.path.exists("EveconMiniDebug.py"):
            os.remove("EveconMiniDebug.py")
        if os.path.exists("ss_time.py"):
            os.remove("ss_time.py")
        if os.path.exists("updater.py"):
            os.remove("updater.py")

        os.remove("selfstart")

    elif EveconLib.Config.myType == "standalone_exe":
        os.remove("!Console.exe")

        os.remove("selfstart")
    else:
        os.remove("selfstart")

    print("Finished Deleting\nGeneration !Evecon/Music/Program Dirs")

    if not os.path.exists("!Evecon" + EveconLib.Config.path_seg + "!Console"):
        os.mkdir("!Evecon" + EveconLib.Config.path_seg + "!Console")
    if not os.path.exists("!Evecon" + EveconLib.Config.path_seg + "dev"):
        os.mkdir("!Evecon" + EveconLib.Config.path_seg + "dev")
    if not os.path.exists("!Evecon" + EveconLib.Config.path_seg + "Exe"):
        os.mkdir("!Evecon" + EveconLib.Config.path_seg + "Exe")

    os.mkdir("Music")
    os.mkdir("Music" + EveconLib.Config.path_seg + "Presets")
    os.mkdir("Music" + EveconLib.Config.path_seg + "User")

    os.mkdir("Programs")

    print("Generation data!")

    os.mkdir("data")
    stdDir = os.getcwd()
    os.chdir("data")

    print("Generating Backup-Files")

    os.mkdir("Backup")
    os.chdir("Backup")
    bckDir = os.getcwd()

    file = open("backup.txt", "w")
    file.write("backup.txt")
    file.close()

    with open("Music.json", "w") as jsonfile:
        json.dump(
            {'version': '1.0', 'pc': 'global', 'musicDir': 'Music\\Presets', 'directories': {}, 'multiplaylists': {}},
            jsonfile, indent=4, sort_keys=True)

    os.mkdir("!Evecon")
    os.mkdir("!Evecon" + EveconLib.Config.path_seg + "!Console")
    os.mkdir("!Evecon" + EveconLib.Config.path_seg + "dev")
    os.chdir("!Evecon" + EveconLib.Config.path_seg + "dev")

    file = open("!Console.py", "w")
    file.write("a.py-file")
    file.close()
    file = open("EveconExceptions.py", "w")
    file.write("a.py-file")
    file.close()
    file = open("EveconLib.py", "w")
    file.write("a.py-file")
    file.close()
    file = open("EveconMiniDebug.py", "w")
    file.write("a.py-file")
    file.close()
    file = open("ss_time.py", "w")
    file.write("a.py-file")
    file.close()
    file = open("updater.py", "w")
    file.write("a.py-file")
    file.close()

    os.chdir(bckDir)

    os.mkdir("data")
    os.mkdir("data" + EveconLib.Config.path_seg + "Info")
    file = open("data" + EveconLib.Config.path_seg + "Info" + EveconLib.Config.path_seg + "version", "w")
    file.write("aVERSION")
    file.close()
    file = open("data" + EveconLib.Config.path_seg + "Info" + EveconLib.Config.path_seg + "Changelog.txt", "w")
    file.write("thingsChanged!")
    file.close()

    os.chdir("..")

    print("Generating Config-Files")

    os.mkdir("Config")
    os.chdir("Config")

    file = open("config.ini", "w")
    file.write(
        "[Notepad]\nbrowser = firefox\n[ScreenSaver]\nstarttimer = 180\n[FoxNhe]\nenable_FoxNhe = True\nfoxORnhe = nhee\n[Music]\nrandom = True\n[PC]\nthisIP = 127.0.0.1\ncores = 2")
    file.close()

    with open("Music.json", "w") as jsonfile:
        json.dump(
            {'version': '1.0', 'pc': 'global', 'musicDir': 'Music\\Presets', 'directories': {}, 'multiplaylists': {}},
            jsonfile, indent=4, sort_keys=True)
    with open("splWeap.json", "w") as jsonfile:
        json.dump({"eng": ["Hallo"], "ger": ["Hello"]}, jsonfile, indent=4, sort_keys=True)

    os.chdir("..")

    print("Generating Data-Files")

    os.mkdir("Data")
    os.chdir("Data")

    os.mkdir("nhee")
    os.chdir("nhee")

    file = open("website.txt", "w")
    file.write("https://XXXX.net/?page=")
    file.close()

    with open("data.json", "w") as jsonfile:
        json.dump({'Stats': {'fapped': 0, 'all_pages': 0, 'all_hangas': 0},
                   'Last': {'last_page': '0', 'last_page_url': 'https://XXXX.net/?page=0', 'last_name': 'None',
                            'last_name_url': 'https://XXXX.net/g/0/'}}, jsonfile, indent=4, sort_keys=True)

    os.chdir("..")
    os.mkdir("foxi")
    os.chdir("foxi")

    file = open("website.txt", "w")
    file.write("https://XXXX.com/pag/")
    file.close()

    with open("data.json", "w") as jsonfile:
        json.dump({'Stats': {'fapped': 0, 'all_pages': 0, 'all_hangas': 0},
                   'Last': {'last_page': '0', 'last_page_url': 'https://XXXX.com/pag/0/', 'last_name': 'None',
                            'last_name_url': 'https://XXXX.com/gallery/0/'}}, jsonfile, indent=4, sort_keys=True)

    os.chdir("..")
    os.chdir("..")

    print("DOWNLOADING ICONS")

    os.mkdir("Ico")
    os.chdir("Ico")

    link = "https://github.com/FiHammer/Evecon/releases/download/0.9.X/working.ico"

    urllib.request.urlretrieve(link, "working.ico")
    shutil.copy("working.ico", "PC.ico")
    shutil.copy("working.ico", "Radio.ico")
    shutil.copy("working.ico", "RadioWhite.ico")

    os.chdir("..")

    print("Generating Info-files")

    os.mkdir("Info")
    os.chdir("Info")

    file = open("Changelog.txt", "w")
    file.write("something Changed")
    file.close()
    file = open("exist", "w")
    file.write("Hi")
    file.close()
    file = open("ProgramVersion", "w")
    file.write("PC-Version")
    file.close()
    file = open("updater_megalogin", "w")
    file.write("sorry")
    file.close()
    file = open("version", "w")
    file.write("0\n0.0.0.0")
    file.close()

    os.chdir("..")

    print("Generating Log-dir")
    os.mkdir("Log")

    print("Generating Notie-dir")
    os.mkdir("Noties")

    print("Generating Output-dir")
    os.mkdir("Output")

    print("Generating tmp-dir&files")
    os.mkdir("tmp")

    print("Generating Update-dir")
    os.mkdir("Update")

    print("finishing")
    os.chdir(stdDir)

    file = open("data" + EveconLib.Config.path_seg + "Info" + EveconLib.Config.path_seg + "env", "w")
    file.write("Hi")
    file.close()

    os.remove("!Evecon" + EveconLib.Config.path_seg + "dev" + EveconLib.Config.path_seg + "selfstart")

    print("END")
