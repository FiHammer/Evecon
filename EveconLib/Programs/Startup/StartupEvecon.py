import EveconLib.Config
import EveconLib.Tools.EveconSpecific
import EveconLib.Tools.GlobalMPports
import EveconLib.Networking.Server

def startup():
    # title timer: refresh title time every 2.5 seconds
    EveconLib.Config.title_time = EveconLib.Tools.EveconSpecific.title_time(EveconLib.Config.title_refresh_time)



    # noinspection PyTypeChecker
    EveconLib.Config.logServer = EveconLib.Networking.Server(stdReact=EveconLib.Tools.doNothing, ip=EveconLib.Config.thisIP, port=EveconLib.Config.logServerPort, printLog=False)
    EveconLib.Config.logServer.start()

    EveconLib.Programs.Klakum.startup()