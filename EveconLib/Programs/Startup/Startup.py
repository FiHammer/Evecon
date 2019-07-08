# startup for every EveconLib

import EveconLib.Tools.NonStaticTools

def startup():
    # setting winHWND

    EveconLib.Tools.UsedPorts.startup()

    EveconLib.Tools.NonStaticTools.ctypes_windll.kernel32.SetConsoleTitleW("EVECON: Loading HWND")
    EveconLib.Tools.NonStaticTools.loadHWND("EVECON: Loading HWND")
    EveconLib.Tools.NonStaticTools.ctypes_windll.kernel32.SetConsoleTitleW("EVECON: Loading...")

    # put
    EveconLib.Config.globalMPports = EveconLib.Tools.GlobalMPports("mpPorts.txt")
    EveconLib.Config.globalMPportsJava = EveconLib.Tools.GlobalMPports("mpPortsJava.txt")
