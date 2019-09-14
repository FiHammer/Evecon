# startup for every EveconLib

import EveconLib

def startup():
    # setting winHWND


    if EveconLib.Tools.sys.platform == "win32" and EveconLib.Config.enableTitleChange:
        EveconLib.Tools.NonStaticTools.ctypes_windll.kernel32.SetConsoleTitleW("EVECON: Loading HWND")
        EveconLib.Tools.NonStaticTools.loadHWND("EVECON: Loading HWND")
        EveconLib.Tools.NonStaticTools.ctypes_windll.kernel32.SetConsoleTitleW("EVECON: Loading...")

    # put
    if EveconLib.Config.validEnv:
        EveconLib.Tools.UsedPorts.startup()

        EveconLib.Config.globalMPports = EveconLib.Tools.GlobalMPports("mpPorts.txt")
        EveconLib.Config.globalMPportsJava = EveconLib.Tools.GlobalMPports("mpPortsJava.txt")


    # start the debugger, if debugging

    EveconLib.Tools.Debugging.setupDebuggingExtreme()