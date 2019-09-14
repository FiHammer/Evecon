import EveconLib.Config
import EveconLib.Tools.EveconSpecific
import EveconLib.Tools.GlobalMPports
import EveconLib.Networking.Server

def startup(titleTime=True, logServer=True, klakumStartup=True):
    if titleTime:
        # title timer: refresh title time every 2.5 seconds
        EveconLib.Config.title_time = EveconLib.Tools.EveconSpecific.title_time(EveconLib.Config.title_refresh_time)
    if logServer:
        # noinspection PyTypeChecker
        EveconLib.Config.logServer = EveconLib.Networking.Server(stdReact=EveconLib.Tools.doNothing, ip=EveconLib.Config.thisIP, port=EveconLib.Config.logServerPort, printLog=False)
        EveconLib.Config.logServer.start()
    if klakumStartup:
        EveconLib.Programs.Klakum.startup()