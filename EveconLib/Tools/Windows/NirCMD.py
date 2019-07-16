import os
import subprocess
import time

def setsize(length=995, width=521, x=100, y=100):
    dir_tmp = os.getcwd()
    os.chdir("Programs\\nircmd")
    # subprocess.call(["nircmd", "win", "setsize", "process", "py.exe", x, y, length, width])
    # subprocess.call(["nircmd", "win", "setsize", "process", "/%s" % os.getpid(), x, y, length, width])
    os.system("nircmdc win setsize process py.exe %s %s %s %s" % (x, y, length, width))
    # os.system("nircmdc win setsize process /%s %s %s %s %s" % (os.getpid(), x, y, length, width))
    time.sleep(0.25)
    os.chdir(dir_tmp)


def volume(volume_i):  # 0.45

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
    # global ttime_pause
    # ttime_pause = False
    # ctypes.windll.kernel32.SetConsoleTitleW("Evecon: Loading")
    subprocess.call(["nircmdc", "win", "activate", "process", "py.exe"])
    subprocess.call(["nircmdc", "win", "activate", "process", "/%s" % os.getpid()])
    # subprocess.call(["nircmdc", "win", "activate", "title", "Evecon: Loading"])
    # os.system('nircmd win activate title "Evecon: Loading"')
    # ttime_pause = True
    os.chdir(dir_tmp)
