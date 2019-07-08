import EveconLib.Tools.PCTools.EnergyPlan
import EveconLib.Tools.PCTools.ScreenSaver

# global functions
import subprocess

def Shutdown(wait=0):
    subprocess.call(["shutdown", "/s", "/f", "/t", str(wait)])

def Sleep(wait=0):
    subprocess.call(["shutdown", "/h", "/t", str(wait)])

def Reboot(wait=0):
    subprocess.call(["shutdown", "/r", "/t", str(wait)])