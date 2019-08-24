import os
import shutil
import subprocess
import datetime
import sys
import time

WORK = True



cdir = os.getcwd()
if cdir == "C:\\Users\\Mini-Pc Nutzer.000\\Desktop\\Evecon\\!Evecon\\dev":
    os.chdir("..")
    os.chdir("..")
else:
    os.chdir("..")
    os.chdir("..")
    os.chdir("..")

import EveconLib

Megacmd = EveconLib.Tools.Windows.MegaCMD
szip = EveconLib.Tools.Windows.SZip
title = EveconLib.Tools.title
exit_now = EveconLib.Tools.exit_now
this_version = EveconLib.Config.file_versions
cls = EveconLib.Tools.cls


ddbugger = EveconLib.Tools.ddbug()
ddbugger.start()


def update():
    this_version = EveconLib.Config.file_versions()
    #check version
    #check if newer
    #check if in cache
    #download in cache
    #install
    #delete

    newVersion = checkVersion()

    if newVersion[0] > this_version[0]: # cloud = newer
        if not os.path.exists("data\\Update\\Evecon-" + newVersion[1] + ".zip"):
            downloadUpdate(newVersion[1])

        install("data\\Update\\Evecon-" + newVersion[1] + ".zip")
        os.remove("data\\Update\\Evecon-" + newVersion[1] + ".zip")




def checkVersion():
    logindata = open("data\\Info\\updater_megalogin", "r")
    email = logindata.readline().rstrip()
    pw = logindata.readline().rstrip()
    logindata.close()

    Megacmd.login(email, pw)
    Megacmd.download("/Evecon/version", "data\\Update")
    #Megacmd.exit()

    newVersionFile = open("data\\Update\\version")
    newVersion = []
    for x in newVersionFile:
        newVersion.append(x.strip())
    newVersionFile.close()

    os.remove("data\\Update\\version")

    return newVersion

def install(zipFile, installDir="", installPY=True, unzipDir="data\\Update\\unzipTMP"):

    # unzip
    # copy
    # remove unzip

    if installDir != "":
        installDir = installDir.rstrip("\\") + "\\"

    unzipDir = "data\\Update\\unzipTMP"

    if os.path.exists(unzipDir):
        shutil.rmtree("data\\Update\\unzipTMP")
    #else:
        #unzipDir = "unzipTMP"
        #if os.path.exists(unzipDir):
        #    shutil.rmtree(unzipDir)


    os.mkdir(unzipDir)
    szip.extract_archive(zipFile, unzipDir)

    backuptime = open(installDir + "data\\Backup\\backup.txt", "w")
    backuptime.write("Backup:\nFrom: Zip\nTo: Me\nDate: %s\n_time: %s\nVersion: %s" % (
        datetime.datetime.now().strftime("%d.%m.%Y"),
        datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
    backuptime.close()

    shutil.rmtree(installDir + "data\\Backup\\!Evecon\\!Console")
    shutil.copytree(installDir + "!Evecon\\!Console", installDir + "data\\Backup\\!Evecon\\!Console")
    shutil.rmtree(installDir + "!Evecon\\!Console")
    while not os.path.exists("data\\Update\\unzipTMP\\!Console"):
        print("Wait for file!")
        time.sleep(0.5)
    shutil.copytree("data\\Update\\unzipTMP\\!Console", installDir + "!Evecon\\!Console")

    os.remove(installDir + "data\\Backup\\data\\Info\\version")
    shutil.copy(installDir + "data\\Info\\version", installDir + "data\\Backup\\data\\Info")
    os.remove(installDir + "data\\Info\\version")
    while not os.path.exists("data\\Update\\unzipTMP\\version"):
        print("Wait for file!")
        time.sleep(0.5)
    shutil.copy("data\\Update\\unzipTMP\\version", installDir + "data\\Info")


    os.remove(installDir + "data\\Backup\\data\\Info\\Changelog.txt")
    shutil.copy(installDir + "data\\Info\\Changelog.txt", installDir + "data\\Backup\\data\\Info")
    os.remove(installDir + "data\\Info\\Changelog.txt")
    while not os.path.exists("data\\Update\\unzipTMP\\Changelog.txt"):
        print("Wait for file!")
        time.sleep(0.5)
    shutil.copy("data\\Update\\unzipTMP\\Changelog.txt", installDir + "data\\Info")


    os.remove(installDir + "data\\Backup\\!Evecon\\dev\\!Console.py")
    shutil.copy(installDir + "!Evecon\\dev\\!Console.py", installDir + "data\\Backup\\!Evecon\\dev\\!Console.py")
    os.remove(installDir + "!Evecon\\dev\\!Console.py")
    while not os.path.exists("data\\Update\\unzipTMP\\!Console.py"):
        print("Wait for file!")
        time.sleep(0.5)
    shutil.copy("data\\Update\\unzipTMP\\!Console.py", installDir + "!Evecon\\dev")

    shutil.rmtree(installDir + "data\\Backup\\!Evecon\\dev\\EveconLib")
    shutil.copytree(installDir + "!Evecon\\dev\\EveconLib", installDir + "data\\Backup\\!Evecon\\dev\\EveconLib")
    shutil.rmtree(installDir + "!Evecon\\dev\\EveconLib")
    while not os.path.exists("data\\Update\\unzipTMP\\EveconLib"):
        print("Wait for file!")
        time.sleep(0.5)
    shutil.copytree("data\\Update\\unzipTMP\\EveconLib", installDir + "!Evecon\\dev\\EveconLib")


    os.remove(installDir + "data\\Backup\\!Evecon\\dev\\ss_time.py")
    shutil.copy(installDir + "!Evecon\\dev\\ss_time.py", installDir + "data\\Backup\\!Evecon\\dev\\ss_time.py")
    os.remove(installDir + "!Evecon\\dev\\ss_time.py")
    while not os.path.exists("data\\Update\\unzipTMP\\ss_time.py"):
        print("Wait for file!")
        time.sleep(0.5)
    shutil.copy("data\\Update\\unzipTMP\\ss_time.py", installDir + "!Evecon\\dev")

    os.remove(installDir + "data\\Backup\\!Evecon\\dev\\updater.py")
    shutil.copy(installDir + "!Evecon\\dev\\updater.py", installDir + "data\\Backup\\!Evecon\\dev\\updater.py")
    os.remove(installDir + "!Evecon\\dev\\updater.py")
    while not os.path.exists("data\\Update\\unzipTMP\\updater.py"):
        print("Wait for file!")
        time.sleep(0.5)
    shutil.copy("data\\Update\\unzipTMP\\updater.py", installDir + "!Evecon\\dev")


    shutil.rmtree("data\\Update\\unzipTMP")

def downloadUpdate(downlVersion="newest", downlDir="data\\Update", EveconPath=True):

    if downlVersion == "newest":
        downlVersion = checkVersion()[1]

    logindata = open("data\\Info\\updater_megalogin", "r")
    email = logindata.readline().rstrip()
    pw = logindata.readline().rstrip()
    logindata.close()

    if EveconPath:
        downlDir = os.getcwd() + "\\" + downlDir

    Megacmd.login(email, pw)
    Megacmd.download("/Evecon/Versions/%s/Evecon-%s.zip" % (downlVersion, downlVersion), downlDir, Eveconpath=False)
    Megacmd.exit()


def zipme():
    title("Upgrade", "Zipping")
    newarchive = "data\\Update\\Evecon-" + this_version[1] + ".zip"
    allfiles = ["!Evecon\\dev\\!Console.py", "!Evecon\\dev\\updater.py", "!Evecon\\dev\\ss_time.py",
    #            "!Evecon\\dev\\EveconExceptions.py", "!Evecon\\dev\\EveconMiniDebug.py", "!Evecon\\dev\\EveconLib.py",
                "data\\Info\\Changelog.txt", "data\\Info\\version"]
    alldic = ["!Evecon\\!Console", "!Evecon\\dev\\EveconLib"]

    szip.create_archive(newarchive, allfiles + alldic)

    if os.path.isfile(newarchive):
        print("Success")
    else:
        print("ERROR")
        raise EveconLib.EveconExceptions.UpdateZip


def upload():
    #
    # aktuelles Evecon in eine Zipfile komprimieren! (7-Zip) (FIN)
    # dazu gehört: '!Console', 'dev' bzw darin NUR *.py und 'dll', 'data\Info\Changelog.txt + version' (FIN)
    # diese zip-File dann auf Mega.nz mit dem Konto -------@*.com und PW -------- hochladen.
    # bzw. auf Mega einige Ordner erstellen UND die aktuelle Versions-Datei ersetzen! (die normale 'version')
    EveconLib.Config.refreshVersion()
    zipme()
    title("Upgrade", "Uploading")


    logindata = open("data\\Info\\updater_megalogin", "r")
    email = logindata.readline().rstrip()
    pw = logindata.readline().rstrip()
    logindata.close()

    Megacmd.login(email, pw)
    Megacmd.rm("/Evecon/version")
    Megacmd.upload("data\\Info\\version", "/Evecon")
    Megacmd.mkdir("/Evecon/Versions/%s" % this_version[1])
    Megacmd.upload("data\\Update\\Evecon-" + this_version[1] + ".zip", "/Evecon/Versions/%s" % this_version[1])
    Megacmd.exit()
    time.sleep(0.5)
    cls()
    os.remove("data\\Update\\Evecon-" + this_version[1] + ".zip")

def backup():
    title("Upgrade", "Backup")

    backuptime = open("data\\Backup\\backup.txt", "w")
    backuptime.write("Backup while Upgrading:\nDate: %s\n_time: %s\nVersion: %s" % (
        datetime.datetime.now().strftime("%d.%m.%Y"),
        datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
    backuptime.close()


    shutil.rmtree("data\\Backup\\!Evecon")
    shutil.copytree("!Evecon\\!Console", "data\\Backup\\!Evecon\\!Console")
    os.mkdir("data\\Backup\\!Evecon\\dev")

    shutil.copy("!Evecon\\dev\\!Console.py", "data\\Backup\\!Evecon\\dev")
    shutil.copytree("!Evecon\\dev\\EveconLib", "data\\Backup\\!Evecon\\dev\\EveconLib")
    #shutil.copy("!Evecon\\dev\\EveconLib.py", "data\\Backup\\!Evecon\\dev")
    #shutil.copy("!Evecon\\dev\\EveconExceptions.py", "data\\Backup\\!Evecon\\dev")
    #shutil.copy("!Evecon\\dev\\EveconMiniDebug.py", "data\\Backup\\!Evecon\\dev")
    shutil.copy("!Evecon\\dev\\ss_time.py", "data\\Backup\\!Evecon\\dev")
    shutil.copy("!Evecon\\dev\\updater.py", "data\\Backup\\!Evecon\\dev")

    os.remove("data\\Backup\\data\\Info\\version")
    shutil.copy("data\\Info\\version", "data\\Backup\\data\\Info")
    os.remove("data\\Backup\\data\\Info\\Changelog.txt")
    shutil.copy("data\\Info\\Changelog.txt", "data\\Backup\\data\\Info")

def upgrade():
    subprocess.call(["taskkill", "/IM", "!Console.exe", "/f"])
    cls()
    if EveconLib.Config.computer == "MiniPC":
        title("Upgrade", "Changelog")
        print("Changelog\n\nOld Version: %s" % this_version[1])
        newversion = input("\nNew Version: ")
        newupdate = []
        newupdate_firstinput = False
        while True:
            cls()
            print("Updates:\n")
            if newupdate_firstinput:
                print("In this Update:")
                for x in range(len(newupdate)):
                    print(newupdate[x])
            newupdate_input = input("\nType 'END' to exit\n\n")
            if newupdate_input.lower() == "end":
                break
            newupdate.append(newupdate_input)
            newupdate_firstinput = True
        cls()
        backup()

        title("Upgrade", "Change Version")

        this_version_1 = int(this_version[0]) + 1
        file_change_version_raw = open("data\\Info\\version", "w")
        file_change_version_raw.write("%s\n%s" % (str(this_version_1), newversion))
        file_change_version_raw.close()

        title("Upgrade", "Change Changelog")

        file_changelog_raw = open("data\\Info\\Changelog.txt", "a+")
        file_changelog_raw.write(
            "Version: %s\nNumber: %s\nDate: %s\n_time: %s\nChanges:\n" % (newversion, str(this_version_1),
                                                                         datetime.datetime.now().strftime("%d.%m.%Y"),
                                                                         datetime.datetime.now().strftime("%H:%M:%S")))
        for x in range(len(newupdate)):
            file_changelog_raw.write(newupdate[x])
            file_changelog_raw.write("\n")
        file_changelog_raw.write("\n\n")
        file_changelog_raw.close()

        print(EveconLib.Config.file_versions)
        EveconLib.Config.refreshVersion()
        print(EveconLib.Config.file_versions)
        input()
        title("Upgrade", "Deleting")

        dir_tmp = os.getcwd()
        os.chdir("!Evecon\\dev")
        #shutil.rmtree("build\\!Console")
        shutil.rmtree("dist\\!Console")

        title("Upgrade", "Installing")

        subprocess.call(["pyinstaller.exe", "!Console.py"])
        #os.system("pyinstaller !Console.py")
        time.sleep(1)
        os.chdir(dir_tmp)
        shutil.rmtree("!Evecon\\!Console")
        shutil.copytree("!Evecon\\dev\\dist\\!Console", "!Evecon\\!Console")
        shutil.copy("!Evecon\\dev\\dll\\avbin64.dll", "!Evecon\\!Console")


        upload()
        makeSingleFile()


    # 2. Changelog und neue version abfragen mit alte zeigen (version) 3. backup 4. os.system("pyinstaller x") 5. kopieren 6. neustart wenn mit arg -re mit !Evecon.bat
    else:
        print("Only at a PC with PyInstaller!")
        time.sleep(3)

def makeSingleFile():
    title("Upgrade", "Singelfile")
    if os.path.exists("!Evecon\\dev\\dist\\!Console.exe"):
        os.remove("!Evecon\\dev\\dist\\!Console.exe")
    d = os.getcwd()
    os.chdir("!Evecon\\dev")
    subprocess.call(["pyinstaller.exe", "!Console.py", "--onefile"])
    time.sleep(1)
    os.chdir(d)
    EveconLib.Config.refreshVersion()

    shutil.move("!Evecon\\dev\\dist\\!Console.exe", "!Evecon\\Exe\\!Console-%s.exe" % EveconLib.Config.file_versions[1])

skiparg = []

for x in range(3):
    try:
        sys.argv[x]
    except IndexError:
        sys.argv.append(None)
        skiparg.append(x)
test = []
if not skiparg:
    skiparg.append(2)

for x in range(1, 2):
    if x >= skiparg[0]:
        break
    if sys.argv[x] == "-update":
        title("Updating", "Self-start")
        update()
        #if restart:
        #    subprocess.call(["!Evecon.bat"])
        exit_now()
    if sys.argv[x] == "-upgrade":
        title("Upgrading", "Self-start")
        upgrade()
        subprocess.call(["!Evecon.bat"])
        exit_now()
    elif sys.argv[x] == "-download":
        title("Installing new Version", "")
        downloadUpdate()
        exit_now()



def main():
    title("Waiting for Input")

    cls()
    user_input = input("What to do?\nUpdate (UD), Upgrade (UG)\n\n")

    if user_input.lower() == "ud":
        update()
    if user_input.lower() == "ug":
        upgrade()
    elif user_input.lower() == "in":
        install(input("ZipFile:\n"))
    elif user_input.lower() == "zip" or user_input.lower() == "zipme":
        zipme()
    elif user_input.lower() == "down":
        downloadUpdate() # latest
    elif user_input.lower() == "onefile":
        makeSingleFile()


if EveconLib.Config.exitnow == 0:
    if __name__ == "__main__":
        main()
        time.sleep(0.2)

        exit_now()
        ddbugger.work = False