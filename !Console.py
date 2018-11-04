import os
import json

if __name__ == "__main__":
    cdir = os.getcwd()
    os.chdir("..")
    os.chdir("..")


startmain = False
exitnow = 0
pausetime = 180
thisIP = None
MusicDir = None

from EveconLib import *

ttime.start()

title("Load first Programs")

class ToolsC:
    def __init__(self):
        self.EnergyPlan = self.EnergyPlanC()
        self.Run = True
    class EnergyPlanC:
        def __init__(self):
            self.cEP = None
            self.cEP_code = None
            self.cEP_id = None
            self.getEP()
            self.Plans = ["381b4222-f694-41f0-9685-ff5bb260df2e", "a1841308-3541-4fab-bc81-f71556f20b4a", "472405ce-5d19-4c83-94d7-a473c87dedad"]
            self.Plans_Dic = {"Ausbalanciert" : "381b4222-f694-41f0-9685-ff5bb260df2e", "Energiesparmodus" : "a1841308-3541-4fab-bc81-f71556f20b4a",
                              "0Sys" : "472405ce-5d19-4c83-94d7-a473c87dedad"}

        def getEP(self, printit=False):
            p = subprocess.Popen(["powercfg", "/GETACTIVESCHEME"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            output, err = p.communicate(b"input data that is passed to subprocess' stdin")
            try:
                eplan_tmp = output.decode("utf-8")
            except UnicodeDecodeError:
                eplan_tmp = 'GUID des Energieschemas: a1841308-3541-4fab-bc81-f71556f20b4a  (Energiesparmodus)'

            eplan_tmp2 = eplan_tmp.lstrip("GUID des Energieschemas").lstrip(": ")
            eplan_code = ""
            for x in range(36):
                eplan_code += eplan_tmp2[x]

            self.cEP_code = eplan_code

            if eplan_code == '381b4222-f694-41f0-9685-ff5bb260df2e':
                self.cEP = "Ausbalanciert"
                self.cEP_id = 0
            elif eplan_code == 'a1841308-3541-4fab-bc81-f71556f20b4a':
                self.cEP = "Energiesparmodus"
                self.cEP_id = 1
            elif eplan_code == '472405ce-5d19-4c83-94d7-a473c87dedad':
                self.cEP = "0Sys"
                self.cEP_id = 2
            else:
                raise EveconExceptions.EnergyPlanNotFound

            if printit:
                print("Current Plan:")
                print(self.cEP)
                print("Code: " + self.cEP_code)

            return self.cEP_id

        def Change(self, ID):
            subprocess.call(["powercfg", "/s", str(self.Plans[ID])])
        def Switch(self):
            self.getEP()
            if self.cEP_id == 0:
                self.Change(1)
            elif self.cEP_id == 1:
                self.Change(0)
            elif self.cEP_id == 2:
                self.Change(1)

    def Shutdown(self, wait=0):
        self.Run = False
        subprocess.call(["shutdown", "/s", "/f", "/t", str(wait)])
    def Sleep(self, wait=0):
        self.Run = False
        subprocess.call(["shutdown", "/h", "/t", str(wait)])
    def Reboot(self, wait=0):
        self.Run = False
        subprocess.call(["shutdown", "/r", "/t", str(wait)])

Tools = ToolsC()


def InteractiveClient(host, port):
    def x(data):
        print("[Server] " + data)

    cl = Client(ip=host, port=port, react=x)
    cl.start()

    time.sleep(1)
    x = input()

    while x != "q" and not cl.Status == "Ended":
        cl.send(x)
        #sys.stdout.write("-> ")
        time.sleep(0.2)
        if not cl.Status == "Ended":
            x = input()

    cl.exit()





def StartupServerTasks(data):
    global SST_mp, SST_mp_Ac

    if data == "shutdown":
        print("Evecon Server", "Shutdown")
        balloon_tip("Evecon Server", "Shutdown")
        Tools.Shutdown()
    elif data == "sleep":
        print("Evecon Server", "sleep")
        balloon_tip("Evecon Server", "sleep")
        Tools.Sleep()
    elif data == "ep_energysave":
        print("Evecon Server", "ep_energysave")
        balloon_tip("Evecon Server", "ep_energysave")
        StartupServer.send("Changed Energyplan to Energysaveplan")
        Tools.EnergyPlan.Change(1)
    elif data == "reboot":
        print("Evecon Server", "reboot")
        balloon_tip("Evecon Server", "reboot")
        Tools.Reboot()
    elif data == "mp_setup":
        print("Evecon Server", "mp_setup")
        balloon_tip("Evecon Server", "mp_setup")
        StartupServer.send("MusicPlayer is ready")
        SST_mp = MusicPlayerC()
        SST_mp_Ac = True
    elif data[0] == "m" and data[1] == "p" and data[2] == "_" and data[3] == "a" and data[4] == "d" and data[5] == "d" and SST_mp_Ac:
        print("Evecon Server", "mp_add " + data.lstrip("mp_").lstrip("add").lstrip("_"))
        balloon_tip("Evecon Server", "mp_add " + data.lstrip("mp_").lstrip("add").lstrip("_"))
        x = SST_mp.addMusic(data.lstrip("mp_").lstrip("add").lstrip("_"))
        if x:
            StartupServer.send("Done Loading")
        else:
            StartupServer.send("Error")
    elif data == "mp_start" and SST_mp_Ac:
        print("Evecon Server", "mp_start")
        balloon_tip("Evecon Server", "mp_start")
        StartupServer.send("Started Musicplayer")
        SST_mp.start()
    elif data == "mp_pause" and SST_mp_Ac:
        print("Evecon Server", "mp_pause")
        balloon_tip("Evecon Server", "mp_start")
        StartupServer.send("Paused/Unpaused Musicplayer")
        SST_mp.switch()
    elif data == "mp_stop" and SST_mp_Ac:
        print("Evecon Server", "mp_stop")
        balloon_tip("Evecon Server", "mp_stop")
        StartupServer.send("Stoped Musicplayer")
        SST_mp.stop()
    elif data == "mp_getsong" and SST_mp_Ac:
        StartupServer.send(SST_mp.getCur()["name"])
    elif data == "mp_status" and SST_mp_Ac:
        StartupServer.send("Status Musicplayer:")
        time.sleep(0.3)
        StartupServer.send("Playing: " + str(SST_mp.playing))
        time.sleep(0.3)
        if SST_mp.playing:
            StartupServer.send("Track: " + str(SST_mp.getCur()["name"]))
        time.sleep(0.3)
        if SST_mp.musicrun:
            StartupServer.send("End: False")
        else:
            StartupServer.send("End: True")
    elif data == "help":
        StartupServer.send("shutdown, sleep, ep_energysave, reboot, mp_setup, mp_add_*, mp_start, mp_pause, mp_stop, mp_getsong, mp_status")

class FoxiC:
    def __init__(self, browser_type=browser):
        if browser_type == "firefox":
            self.browser = Firefox()
        elif browser_type == "vivaldi":
            self.browser = Vivaldi()
        else:
            self.browser = Firefox()

        with open("data\\Foxi\\data.json") as jsonfile:
            self.data = json.load(jsonfile)


    def readJson(self):
        with open("data\\Foxi\\data.json") as jsonfile:
            self.data = json.load(jsonfile)

    def writeJson(self):
        with open("data\\Foxi\\data.json", "w") as jsonfile:
            json.dump(self.data, jsonfile, indent=4, sort_keys=True)



    def open_fox(self):
        self.browser.refresh()
        self.browser.open_win(self.data["Last"]["last_name_url"])
        if self.browser.running:
            time.sleep(1)
        else:
            time.sleep(5)
        self.browser.open_tab(self.data["Last"]["last_page_url"])

    def open_foxname(self):
        self.browser.open_win(self.data["Last"]["last_name_url"])

    def open_foxpage(self):
        self.browser.open_win(self.data["Last"]["last_page_url"])

    def fap(self, opentype="fox"):
        cls()
        print("Loading ...")
        self.readJson()
        if opentype == "fox":
            self.open_fox()
        elif opentype == "foxname":
            self.open_foxname()
        elif opentype == "foxpage":
            self.open_foxpage()
        else:
            return False

        thistime_read = 0
        thistime_time = datetime.datetime.now().strftime("%H:%S:%M")
        thistime_date = datetime.datetime.now().strftime("%d.%m.%Y")

        idstart = int(self.data["Last"]["last_name_url"].split("/")[-2])

        cls()
        print("Which is your startpage? (Begin: %s, Search for: %s)" % (self.data["Last"]["last_page"], idstart))
        pagestart = int(input())

        thistime_timeC = TimerC()
        thistime_timeC.start()

        fapping = True
        while fapping:
            cls()
            print("Foxi:\n")
            print("You read: %s" % thistime_read)
            print("You are fapping: %s\n" % thistime_timeC.getTimeFor())

            print("Everything for next HManga, Finish (FIN)")

            user_input = input()

            thistime_read += 1

            if user_input.lower() == "fin":
                break

        thistime_timeC.stop()

        cls()
        print("End HManga: (Name)")
        hmangaend_name = input()

        print("End HManga: (URL)")
        hmangaend_url = input()

        print("End Page: ")
        pageend = int(input())

        pageend_url = "https://hentaifox.com/pag/%s/" % pageend
        pageprogress = pagestart - pageend


        idend = int(hmangaend_url.split("/")[-2])
        idprogress = idend - idstart
        skipped = idprogress - thistime_read
        startname = self.data["Last"]["last_name"]
        starturl = self.data["Last"]["last_name_url"]

        self.data["Stats"] = {"fapped": self.data["Stats"]["fapped"] + 1,
                              "all_pages": self.data["Stats"]["all_pages"] + pageprogress,
                              "all_hmangas": self.data["Stats"]["all_hmangas"] + thistime_read}

        self.data["Last"] = {"last_page": pageend, "last_page_url": pageend_url,
                             "last_name": hmangaend_name, "last_name_url": hmangaend_url}

        self.data[str(self.data["Stats"]["fapped"])] = {"number": self.data["Stats"]["fapped"],
                                                   "date": thistime_date,
                                                   "starttime": thistime_time,
                                                   "time": thistime_timeC.getTimeFor(),
                                                   "foxi": {"read": thistime_read,
                                                            "skipped": skipped,
                                                            "pagestart": pagestart,
                                                            "pageend": pageend,
                                                            "pageprogress": pageprogress,
                                                            "idstart": idstart,
                                                            "idend": idend,
                                                            "idprogress": idprogress,
                                                            "start_HManga": {
                                                                "page": pagestart,
                                                                "name": startname,
                                                                "id": idstart,
                                                                "url": starturl
                                                            },
                                                            "end_HManga": {
                                                                "page": pageend,
                                                                "name": hmangaend_name,
                                                                "id": idend,
                                                                "url": hmangaend_url
                                                            }
                                                            }}

        self.writeJson()
        print("Finished")
        time.sleep(0.85)

Foxi = FoxiC()



title("Loading Arguments")

def upgrade():
    title("Updating this Program", "")
    #dir_tmp = os.getcwd()
    os.chdir("Programs\\Evecon\\Updater")
    subprocess.call(["updater.exe", "-upgrade"])

    exit_now()



def debug():
    cls()
    while True:
        exec(input())



def Music(systrayon=True):

    def Play():
        class Printerr(threading.Thread):
            def run(self):
                while not muPlayer.allowPrint:
                    time.sleep(0.5)
                while muPlayer.musicrun and muPlayer.allowPrint:
                    time.sleep(1)
                    muPlayer.printit()
                    while muPlayer.paused:
                        time.sleep(1)

        Printer = Printerr()
        Printer.start()

        #while True:
        #    print(muPlayer.allowPrint, muPlayer.musicrun, muPlayer.paused)
        #    time.sleep(0.5)

        #while muPlayer.musicrun:
        #    user_input = input()
        #    muPlayer.input(user_input)


    muPlayer = MusicPlayerC(systrayon)

    music_playlists_print = ""
    for x, y in zip(muPlayer.playlists, muPlayer.playlists_key):
        music_playlists_print += x + " (" + y.upper() + "), "
    music_playlists_print = music_playlists_print.rstrip(", ")

    cls()
    print("Playlists:")
    print("\nFix Playlists:")
    print(music_playlists_print)
    print("\nCustom:")
    print("User's Playlist (US), User defined (UD), Mix (MIX), Multiple PL (MPL), All (ALL)\n")
    music_user_input = input()

    if music_user_input.lower() == "mix":
        muPlayer.addMusic("an")
        muPlayer.addMusic("phu")
        muPlayer.addMusic("cp")
        muPlayer.addMusic("es")
        muPlayer.addMusic("jpop")
    elif music_user_input.lower() == "j":
        muPlayer.addMusic("an")
        muPlayer.addMusic("jpop")
    elif music_user_input.lower() == "all":
        for x in muPlayer.playlists_key:
            muPlayer.addMusic(x)

    elif music_user_input.lower() == "mpl":
        musicman_search = True

        muPlayer.playlists.append("User's List")

        musicman_list = []
        music_playlists_used = {}

        for x in muPlayer.playlists_key:
            music_playlists_used[x] = " "

        while musicman_search:
            music_playlists_used_List = []
            for x in muPlayer.playlists_key:
                music_playlists_used_List.append(music_playlists_used[x])
            cls()
            print("Playlists:\n")
            #print(music_playlists_print)
            #print("User's list (US), User defined (UD)")
            #print("\nLoaded:")
            for xl, x2, x3 in zip(music_playlists_used_List, muPlayer.playlists, muPlayer.playlists_key):
                print(" " + xl + " " + x2 + " (" + x3.upper() + ")")
            for x in musicman_list:
                print(" X " + x)
            print("\nFinish (FIN)\n")

            musicman_user_input = input()


            if musicman_user_input.lower() == "fin":
                musicman_search = False

            else:
                x = muPlayer.addMusic(musicman_user_input.lower())

                if x:
                    music_playlists_used[musicman_user_input.lower()] = "X"
                elif x == "ul":
                    musicman_list.append("unkown list")

    #elif music_user_input.lower() == "search":
    #    for x in muPlayer.playlists_key:
    #        muPlayer.addMusic(x, False)

    #    cls()
    #    print("What do you want to hear?")

    #    user_input_search = input()

    #    searchdir = Search(user_input_search, muPlayer.musiclistdirname)
    #    searchtrack = Search(user_input_search, muPlayer.musiclistname)

    #    musiclistpathold = muPlayer.musiclistpath
    #    muPlayer.musiclistpath = []
    #    musiclistnameold = muPlayer.musiclistname
    #    muPlayer.musiclistname = []

    #    for x in searchdir:
    #        muPlayer.searchMusic(muPlayer.musiclistdirnamefull[x])

    #    for x in searchtrack:
    #        muPlayer.musiclist.append(pyglet.media.load(musiclistpathold[x]))
    #        muPlayer.musiclistpath.append(musiclistpathold[x])
    #        muPlayer.musiclistname.append(musiclistnameold[x])

    else:
        muPlayer.addMusic(music_user_input.lower())

    if muPlayer.music["active"]:
        muPlayer.start()
        Play()
    else:
        print("No track found")

    normaltitle()


class RadioC:
    def __init__(self, systray=True):
        super().__init__()

        self.streampause = False
        self.streamrun = True
        self.streamvolume = Volume.getVolume()

        self.streamplayer = MPlayerC("Programs\\MPlayer")

        self.streamPrintOth = False
        self.streamPrintCh = False
        self.streamPrintVol = False

        self.systrayon = systray
        self.systray = None

        self.stream_playlists = ["EgoFM", "HR1", "HR3", "Bayern3", "ByteFM"]
        self.stream_playlists_key = ["egofm", "hr1", "hr3", "br3", "bytefm"]
        self.stream_playlists_name = {"egofm" : "EgoFM",
                                      "hr1" : "HR1",
                                      "hr3" : "HR3",
                                      "br3" : "BR3",
                                      "bytefm" : "ByteFM"}
        self.stream_playlists_link = {"egofm" : "https://egofm-live.cast.addradio.de/egofm/live/mp3/high/stream.mp3",
                                      "hr1" : "http://hr-hr1-live.cast.addradio.de/hr/hr1/live/mp3/128/stream.mp3",
                                      "hr3" : "http://hr-hr3-live.cast.addradio.de/hr/hr3/live/mp3/128/stream.mp3",
                                      "br3" : "https://br-br3-live.sslcast.addradio.de/br/br3/live/mp3/128/stream.mp3",
                                      "bytefm" : "https://dg-ice-eco-https-fra-eco-cdn.cast.addradio.de/bytefm/main/mid/stream.mp3"}

        self.streamplaying = self.stream_playlists_key[random.randint(0, len(self.stream_playlists_key) - 1)]

    def Unpause(self):
        self.streamplayer.unpause()
        self.streampause = False
        title("Radio", self.stream_playlists_name[self.streamplaying], "Now Playing")
    def Pause(self):
        self.streamplayer.pause()
        self.streampause = True
        title("Radio", self.stream_playlists_name[self.streamplaying], "Paused")
    def Switch(self):
        if not self.streampause:
            self.Pause()
        else:
            self.Unpause()
        #self.streamplayer.switch()
        #self.streampause = self.streamplayer.Paused
    def Change(self, key):
        self.streamplayer.stop()
        self.streamplaying = key
        self.streamplayer.start(self.stream_playlists_link[key])
        title("Radio", self.stream_playlists_name[self.streamplaying], "Now Playing")
    def vol(self, vol):
        self.streamvolume = vol
        Volume.change(vol)
        #nircmd("volume", self.streamvolume)
    def Stop(self):
        self.streamplaying = None
        self.streampause = False
        self.streamrun = False
        self.streamplayer.stop()
        if self.systrayon:
            time.sleep(1)
            killme()
    def input(self, inpt):
        inpt = inpt.lower()
        if inpt == "play" or inpt == "pau" or inpt == "pause" or inpt == "p":
            self.Switch()
            self.printit()
        elif inpt == "change" or inpt == "ch" or inpt == "c":
            self.streamPrintOth = True
            self.streamPrintCh = True
            self.printit()
            self.Change(input("Change to:"))
            self.streamPrintOth = False
            self.streamPrintCh = False
            self.printit()
        elif inpt == "stop" or inpt == "exit":
            self.Stop()
            self.printit()
        elif inpt == "vol":
            self.streamPrintOth = True
            self.streamPrintVol = True
            self.printit()
            self.vol(float(input("Volume (Now: %s)\n" % Volume.getVolume())))
            self.streamPrintOth = False
            self.streamPrintVol = False
            self.printit()

    # noinspection PyStatementEffect
    def start(self):

        title("Radio", self.stream_playlists_name[self.streamplaying], "Now Playing")
        self.streamplayer.start(self.stream_playlists_link[self.streamplaying])
        # pause/unpause , submenu mit allen sendern

        def unp_p(x):
            self.Switch()


        if self.systrayon:


            def x0(x):
                self.Change(self.stream_playlists_key[0])
            def x1(x):
                self.Change(self.stream_playlists_key[1])
            def x2(x):
                self.Change(self.stream_playlists_key[2])
            def x3(x):
                self.Change(self.stream_playlists_key[3])
            def x4(x):
                self.Change(self.stream_playlists_key[4])
            def x5(x):
                self.Change(self.stream_playlists_key[5])
            def x6(x):
                self.Change(self.stream_playlists_key[6])
            def x7(x):
                self.Change(self.stream_playlists_key[7])
            def x8(x):
                self.Change(self.stream_playlists_key[8])
            def x9(x):
                self.Change(self.stream_playlists_key[9])
            def x10(x):
                self.Change(self.stream_playlists_key[10])
            def x11(x):
                self.Change(self.stream_playlists_key[11])
            def x12(x):
                self.Change(self.stream_playlists_key[12])
            def x13(x):
                self.Change(self.stream_playlists_key[13])
            def x14(x):
                self.Change(self.stream_playlists_key[14])
            def x15(x):
                self.Change(self.stream_playlists_key[15])

            if len(self.stream_playlists) == 1:
                sub_menu1 = {self.stream_playlists[0]: x0}
            elif len(self.stream_playlists) == 2:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1}
            elif len(self.stream_playlists) == 3:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2}
            elif len(self.stream_playlists) == 4:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3}
            elif len(self.stream_playlists) == 5:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4}
            elif len(self.stream_playlists) == 6:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5}
            elif len(self.stream_playlists) == 7:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6}
            elif len(self.stream_playlists) == 8:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7}
            elif len(self.stream_playlists) == 9:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8}
            elif len(self.stream_playlists) == 10:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                            self.stream_playlists[9]: x9}
            elif len(self.stream_playlists) == 11:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                            self.stream_playlists[9]: x9, self.stream_playlists[10]: x10}
            elif len(self.stream_playlists) == 12:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                            self.stream_playlists[9]: x9, self.stream_playlists[10]: x10,
                            self.stream_playlists[11]: x11}
            elif len(self.stream_playlists) == 13:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                            self.stream_playlists[9]: x9, self.stream_playlists[10]: x10,
                            self.stream_playlists[11]: x11,
                            self.stream_playlists[12]: x12}
            elif len(self.stream_playlists) == 14:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                            self.stream_playlists[9]: x9, self.stream_playlists[10]: x10,
                            self.stream_playlists[11]: x11,
                            self.stream_playlists[12]: x12, self.stream_playlists[13]: x13}
            elif len(self.stream_playlists) == 15:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                            self.stream_playlists[9]: x9, self.stream_playlists[10]: x10,
                            self.stream_playlists[11]: x11,
                            self.stream_playlists[12]: x12, self.stream_playlists[13]: x13,
                            self.stream_playlists[14]: x14}
            elif len(self.stream_playlists) == 16:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                            self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                            self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                            self.stream_playlists[9]: x9, self.stream_playlists[10]: x10,
                            self.stream_playlists[11]: x11,
                            self.stream_playlists[12]: x12, self.stream_playlists[13]: x13,
                            self.stream_playlists[14]: x14,
                            self.stream_playlists[15]: x15}
            else:
                def nothing(x):
                    print("nothing")

                sub_menu1 = {"Nothing": nothing}

            def quitFunc(x):
                self.Stop()

            self.systray = SysTray("data\\Ico\\Radio.ico", "Evecon: Radio", {"Pause/Unpause": unp_p},
                                   sub_menu1=sub_menu1, sub_menu_name1="Change Radio", quitFunc=quitFunc)
            self.systray.start()
            self.printit()

    def printit(self):
        cls()
        if not self.streampause:
            print("Radio:\n\nPlaying:")
        else:
            print("Radio:\n\nPaused:")

        print(self.streamplaying)
        print("\n")
        if not self.streamPrintOth:
            if not self.streampause:
                print("Pause (PAU), Stop (STOP), Change (CH), Volume (VOL)")
            else:
                print("Unpause (PAU), Stop (STOP), Change (CH), Volume (VOL)")
        elif self.streamPrintVol:
            print("Volume (Now: %s)\n" % Volume.getVolume())

        elif self.streamPrintCh:

            for xl, x2 in zip(self.stream_playlists, self.stream_playlists_key):
                print(x2 + " (" + x2.upper() + ")")

            print("Change to:\n")


def Radio(systrayon=True):
    radioPlayer = RadioC(systrayon)
    cls()

    print("Radios:\n")

    for x1, x2 in zip(radioPlayer.stream_playlists, radioPlayer.stream_playlists_key):
        print(x1 + " (" + x2.upper() + ")")

    print("\nChange to:\n")

    user_input = input().lower()
    y = False
    for x in radioPlayer.stream_playlists_key:
        if x == user_input:
            y = True
    if y:
        radioPlayer.streamplaying = user_input
        radioPlayer.start()



    while y:
        radioPlayer.input(input())



def screensaver(preset = None):
    #   thread für time zähler,
    #   dann background time printer
    #   dann zur input console (main())

    #   light funktion machen
    def deacss():
        if os.path.exists("data\\tmp\\Screensaver\\deac"):
            os.remove("data\\tmp\\Screensaver\\deac")
        else:
            file = open("data\\tmp\\Screensaver\\deac", "w")
            file.write("deactivated")
            file.close()

    def ss():
        global ss_active, killmem

        title("Screensaver", "")

        oldEP = Tools.EnergyPlan.getEP()
        Tools.EnergyPlan.Change(1)

        ttime.ss_switch()

        killmem = False
        sleeps = True
        ss_active = True
        backcolor = "dark"

        # class Timecount(threading.Thread):
        #    def run(self):
        #        global ss_pause##

        #        ss_start = time.time()
        #        while sleeps:
        #            time.sleep(0.1)

        #        ss_pause = time.time() - ss_start

        # Machen wenn pause time counter
        #backtime = Timecount()

        # ss_start = time.time()

        #dir_tmp = os.getcwd()
        #os.chdir("Programs\\Evecon\\Screensaver_time")
        #os.system("start ss_time.exe")
        #subprocess.call("ss_time.exe") # time printer
        #os.chdir(dir_tmp)
        #time.sleep(1)

        nircmd("foreground")
        nircmd("setsize")

        def screensavertime():

            dir_tmp = os.getcwd()
            os.chdir("Programs\\Evecon\\Screensaver_time")
            subprocess.call("ss_time.exe")
            os.chdir(dir_tmp)

        def lightss():
            nonlocal backcolor
            if backcolor != "dark":
                os.system("color 07")
                color_data = open("data\\tmp\\sscolor", "w")
                color_data.write("dark")
                color_data.close()
                color = "dark"
            elif backcolor != "bright":
                os.system("color F0")
                color_data = open("data\\tmp\\sscolor", "w")
                color_data.write("bright")
                color_data.close()
                color = "bright"

        def deac():
            if os.path.exists("data\\tmp\\Screensaver\\deac"):
                os.remove("data\\tmp\\Screensaver\\deac")
            else:
                file = open("data\\tmp\\Screensaver\\deac", "w")
                file.write("deactivated")
                file.close()

        while sleeps:
            cls()
            user_input = input("Screensaver\n\nWhat to do?\nLight (L), Deac (DEAC)\n\n")

            if user_input.lower() == "l":
                lightss()
            elif user_input.lower() == "deac":
                deac()
            elif user_input.lower() == "time":
                screensavertime()
            elif user_input.lower() == "debug":
                debug()
            #elif user_input.lower() == "games":
            #    games()
            #elif user_input.lower() == "snake":
            #    games("snake")
            elif user_input.lower() == "music":
                Music(False)
                killmem = True
            elif user_input.lower() == "radio":
                Radio(False)
            elif user_input.lower() == "main":
                main()
            else:
                sleeps = False


        subprocess.call(["taskkill", "/IM", "ss_time.exe"])

        # schreibe in die Datei ...
        #ss_pause = time.time() - ss_start
        Tools.EnergyPlan.Change(oldEP)
        exit_now(killmem)

    if preset is None:
        ss()
    elif preset == "deac":
        deacss()

def Timeprint():
    cls()

    print("Preset:\nRight (R)")
    user_input = input()

    if user_input.lower() == "r":

        nircmd("maxi")

        space = "\t" * 24

        def printerIT():
            cls()
            for x in range(len(hour1)):
                print(space + hour1[x] + empty + hour2[x])
            for x in range(len(minu1)):
                print(space + minu1[x] + empty + minu2[x])
            for x in range(len(sec1)):
                print(space + sec1[x] + empty + sec2[x])

    else:
        print("ERROR") # hier standart wenn es es gibt
        def printerIT():
            cls()
            for x in range(len(hour1)):
                print(space + hour1[x] + empty + hour2[x])
            for x in range(len(minu1)):
                print(space + minu1[x] + empty + minu2[x])
            for x in range(len(sec1)):
                print(space + sec1[x] + empty + sec2[x])



    empty = " "
    nothingit = "-"  # nothing in time
    iss = "X"  # ist was oder so


    blockempty = nothingit * 19
    blockfull = nothingit * 2 + iss * 15 + nothingit * 2
    blockside = nothingit * 2 + iss + nothingit * 13 + iss + nothingit * 2
    blockemptyfull = nothingit * 16 + iss + nothingit * 2
    blockfullempty = nothingit * 2 + iss + nothingit * 16

    global hour1, hour2, minu1, minu2, sec1, sec2

    hour1 = [blockempty, blockfull,
             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
             blockfull,
             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
             blockfull]
    hour2 = [blockempty, blockfull,
             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
             blockfull,
             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
             blockfull]
    minu1 = [blockempty, blockfull,
             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
             blockfull,
             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
             blockfull]
    minu2 = [blockempty, blockfull,
             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
             blockfull,
             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
             blockfull]
    sec1 = [blockempty, blockfull,
            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
            blockfull,
            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
            blockfull, blockempty]
    sec2 = [blockempty, blockfull,
            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
            blockfull,
            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
            blockfull, blockempty]

    def refreshtime():
        global lasthour, lastminu, lastsec, hour1, hour2, minu1, minu2, sec1, sec2
        hour = datetime.datetime.now().strftime("%H")
        minu = datetime.datetime.now().strftime("%M")
        sec = datetime.datetime.now().strftime("%S")
        if lasthour != hour:
            if lasthour[0] != hour[0]:
                if hour[0] == "0":
                    hour1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[0] == "1":
                    hour1 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[0] == "2":
                    hour1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull]
                if hour[0] == "3":
                    hour1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if hour[0] == "4":
                    hour1 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[0] == "5":
                    hour1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if hour[0] == "6":
                    hour1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[0] == "7":
                    hour1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[0] == "8":
                    hour1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[0] == "9":
                    hour1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
            if lasthour[1] != hour[1]:
                if hour[1] == "0":
                    hour2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[1] == "1":
                    hour2 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[1] == "2":
                    hour2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull]
                if hour[1] == "3":
                    hour2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if hour[1] == "4":
                    hour2 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[1] == "5":
                    hour2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if hour[1] == "6":
                    hour2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[1] == "7":
                    hour2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[1] == "8":
                    hour2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[1] == "9":
                    hour2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
            lasthour = hour
        if lastminu != minu:
            if lastminu[0] != minu[0]:
                if minu[0] == "0":
                    minu1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[0] == "1":
                    minu1 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[0] == "2":
                    minu1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull]
                if minu[0] == "3":
                    minu1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if minu[0] == "4":
                    minu1 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[0] == "5":
                    minu1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if minu[0] == "6":
                    minu1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[0] == "7":
                    minu1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[0] == "8":
                    minu1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[0] == "9":
                    minu1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
            if lastminu[1] != minu[1]:
                if minu[1] == "0":
                    minu2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[1] == "1":
                    minu2 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[1] == "2":
                    minu2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull]
                if minu[1] == "3":
                    minu2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if minu[1] == "4":
                    minu2 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[1] == "5":
                    minu2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if minu[1] == "6":
                    minu2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[1] == "7":
                    minu2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[1] == "8":
                    minu2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[1] == "9":
                    minu2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
            lastminu = minu
        if lastsec != sec:
            if lastsec[0] != sec[0]:
                if sec[0] == "0":
                    sec1 = [blockempty, blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockside,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull, blockempty]
                if sec[0] == "1":
                    sec1 = [blockempty, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockempty]
                if sec[0] == "2":
                    sec1 = [blockempty, blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull,
                            blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                            blockfullempty, blockfullempty, blockfullempty,
                            blockfull, blockempty]
                if sec[0] == "3":
                    sec1 = [blockempty, blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull, blockempty]
                if sec[0] == "4":
                    sec1 = [blockempty, blockside,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockempty]
                if sec[0] == "5":
                    sec1 = [blockempty, blockfull,
                            blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                            blockfullempty, blockfullempty, blockfullempty,
                            blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull, blockempty]
                if sec[0] == "6":
                    sec1 = [blockempty, blockfull,
                            blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                            blockfullempty, blockfullempty, blockfullempty,
                            blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull, blockempty]
                if sec[0] == "7":
                    sec1 = [blockempty, blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockempty]
                if sec[0] == "8":
                    sec1 = [blockempty, blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull, blockempty]
                if sec[0] == "9":
                    sec1 = [blockempty, blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull, blockempty]
            if lastsec[1] != sec[1]:
                if sec[1] == "0":
                    sec2 = [blockempty, blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockside,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull, blockempty]
                if sec[1] == "1":
                    sec2 = [blockempty, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockempty]
                if sec[1] == "2":
                    sec2 = [blockempty, blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull,
                            blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                            blockfullempty, blockfullempty, blockfullempty,
                            blockfull, blockempty]
                if sec[1] == "3":
                    sec2 = [blockempty, blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull, blockempty]
                if sec[1] == "4":
                    sec2 = [blockempty, blockside,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockempty]
                if sec[1] == "5":
                    sec2 = [blockempty, blockfull,
                            blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                            blockfullempty, blockfullempty, blockfullempty,
                            blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull, blockempty]
                if sec[1] == "6":
                    sec2 = [blockempty, blockfull,
                            blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                            blockfullempty, blockfullempty, blockfullempty,
                            blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull, blockempty]
                if sec[1] == "7":
                    sec2 = [blockempty, blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockempty]
                if sec[1] == "8":
                    sec2 = [blockempty, blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull, blockempty]
                if sec[1] == "9":
                    sec2 = [blockempty, blockfull,
                            blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                            blockfull,
                            blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                            blockemptyfull, blockemptyfull, blockemptyfull,
                            blockfull, blockempty]
            lastsec = sec

    global lasthour, lastminu, lastsec
    lasthour = "EE"
    lastminu = "EE"
    lastsec = "EE"


    ttime.deac()

    while True:
        refreshtime()
        printerIT()
        time.sleep(1)



def Timerprint(hourT, minuT, secT):

    # insgesamter Block: 135x60
    empty = " "
    nothingit = "-" # nothing in time
    iss = "X" # ist was oder so

    space = "\t" * 24
    blockempty = nothingit * 19
    blockfull = nothingit * 2 + iss * 15 + nothingit * 2
    blockside = nothingit * 2 + iss + nothingit * 13 + iss + nothingit * 2
    blockemptyfull = nothingit * 16 + iss + nothingit * 2
    blockfullempty = nothingit * 2 + iss + nothingit * 16

    global hour1, hour2, minu1, minu2, sec1, sec2

    hour1 = [blockempty, blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull]
    hour2 = [blockempty, blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull]
    minu1 = [blockempty, blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull]
    minu2 = [blockempty, blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull]
    sec1 = [blockempty, blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull, blockempty]
    sec2 = [blockempty, blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull,
                blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                blockfull, blockempty]

    waittime = hourT * 3600 +  minuT * 60 + secT

    def printtime():
        cls()
        for x in range(len(hour1)):
            print(space + hour1[x] + empty + hour2[x])
        for x in range(len(minu1)):
            print(space + minu1[x] + empty + minu2[x])
        for x in range(len(sec1)):
            print(space + sec1[x] + empty + sec2[x])


    def refreshtime():
        global lasthour, lastminu, lastsec, hour1, hour2, minu1, minu2, sec1, sec2
        nonlocal waittime


        hour = str(waittime // 3600)
        if len(hour) == 1:
            hour = "0" + hour

        minu = str((waittime % 3600) // 60)
        if len(minu) == 1:
            minu = "0" + minu

        sec = str((waittime % 3600) % 60)
        if len(sec) == 1:
            sec = "0" + sec

        if lasthour != hour:
            if lasthour[0] != hour[0]:
                if hour[0] == "0":
                    hour1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[0] == "1":
                    hour1 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[0] == "2":
                    hour1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfull]
                if hour[0] == "3":
                    hour1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if hour[0] == "4":
                    hour1 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[0] == "5":
                    hour1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if hour[0] == "6":
                    hour1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[0] == "7":
                    hour1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[0] == "8":
                    hour1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[0] == "9":
                    hour1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
            if lasthour[1] != hour[1]:
                if hour[1] == "0":
                    hour2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[1] == "1":
                    hour2 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[1] == "2":
                    hour2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfull]
                if hour[1] == "3":
                    hour2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if hour[1] == "4":
                    hour2 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[1] == "5":
                    hour2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if hour[1] == "6":
                    hour2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[1] == "7":
                    hour2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if hour[1] == "8":
                    hour2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if hour[1] == "9":
                    hour2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
            lasthour = hour
        if lastminu != minu:
            if lastminu[0] != minu[0]:
                if minu[0] == "0":
                    minu1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[0] == "1":
                    minu1 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[0] == "2":
                    minu1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull]
                if minu[0] == "3":
                    minu1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if minu[0] == "4":
                    minu1 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[0] == "5":
                    minu1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if minu[0] == "6":
                    minu1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[0] == "7":
                    minu1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[0] == "8":
                    minu1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[0] == "9":
                    minu1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
            if lastminu[1] != minu[1]:
                if minu[1] == "0":
                    minu2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[1] == "1":
                    minu2 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[1] == "2":
                    minu2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull]
                if minu[1] == "3":
                    minu2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if minu[1] == "4":
                    minu2 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[1] == "5":
                    minu2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
                if minu[1] == "6":
                    minu2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[1] == "7":
                    minu2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull]
                if minu[1] == "8":
                    minu2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull]
                if minu[1] == "9":
                    minu2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull]
            lastminu = minu
        if lastsec != sec:
            if lastsec[0] != sec[0]:
                if sec[0] == "0":
                    sec1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull, blockempty]
                if sec[0] == "1":
                    sec1 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockempty]
                if sec[0] == "2":
                    sec1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull, blockempty]
                if sec[0] == "3":
                    sec1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull, blockempty]
                if sec[0] == "4":
                    sec1 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockempty]
                if sec[0] == "5":
                    sec1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull, blockempty]
                if sec[0] == "6":
                    sec1 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull, blockempty]
                if sec[0] == "7":
                    sec1 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockempty]
                if sec[0] == "8":
                    sec1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull, blockempty]
                if sec[0] == "9":
                    sec1 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull, blockempty]
            if lastsec[1] != sec[1]:
                if sec[1] == "0":
                    sec2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull, blockempty]
                if sec[1] == "1":
                    sec2 = [blockempty, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockempty]
                if sec[1] == "2":
                    sec2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull, blockempty]
                if sec[1] == "3":
                    sec2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull, blockempty]
                if sec[1] == "4":
                    sec2 = [blockempty, blockside,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockempty]
                if sec[1] == "5":
                    sec2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull, blockempty]
                if sec[1] == "6":
                    sec2 = [blockempty, blockfull,
                             blockfullempty, blockfullempty, blockfullempty, blockfullempty, blockfullempty,
                             blockfullempty, blockfullempty, blockfullempty,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull, blockempty]
                if sec[1] == "7":
                    sec2 = [blockempty, blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockempty]
                if sec[1] == "8":
                    sec2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull, blockempty]
                if sec[1] == "9":
                    sec2 = [blockempty, blockfull,
                             blockside, blockside, blockside, blockside, blockside, blockside, blockside, blockside,
                             blockfull,
                             blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull, blockemptyfull,
                             blockemptyfull, blockemptyfull, blockemptyfull,
                             blockfull, blockempty]
            lastsec = sec



    global lasthour, lastminu, lastsec, RUN
    lasthour = "EE"
    lastminu = "EE"
    lastsec = "EE"
    RUN = True

    class runner(threading.Thread):
        def run(self):
            global RUN
            nonlocal waittime
            while RUN:
                waittime -= 1
                time.sleep(1)
                if waittime == 0:
                    RUN = False

    runer = runner()
    runer.start()

    while RUN:
        refreshtime()
        printtime()
        time.sleep(1)


def Alarmprint(x=230, y=65, colorCh=False):
    # insgesamter Block: 135x60

    def randi(x):
        randlist = ["1", "2", " "]
        #randlist = ["/", "\\", "_"]
        key = random.randint(0, 100)
        if key == 0:
            randlist.append("X")
        elif key == 1:
            randlist = ["/", "\\", "_"]
        elif key == 2:
            listx = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                     "U",
                     "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
                     "p",
                     "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                     "!",
                     "§", "$", "%", "&", "/", "(", ")", "=", "?", "ß", "#", "'", "+", "*", "~", "ü", "ö", "ä", "-", "_",
                     ".",
                     ":", ",", ";", "{", "[", "]", "}", ">", "<", "|"]
            randlist = [listx[random.randint(0, len(listx) - 1)], listx[random.randint(0, len(listx) - 1)], listx[random.randint(0, len(listx) - 1)]]
        for z in range(random.randint(1, 5)):
            randlist.append(randlist[random.randint(0, len(randlist) - 1)])

        block = ""
        for z in range(x):
            block += str(randlist[random.randint(0, len(randlist) - 1)])
        return block


    afk = True

    oldColor = color.CurColor

    class printre(threading.Thread):
        def __init__(self, x, y, colorCh):
            super().__init__()

            self.x = x
            self.y = y
            self.colorCh = colorCh

        def run(self):
            nonlocal afk
            while afk:

                if self.colorCh:
                    randcolor = ""
                    randcolor += color.colorKeys[random.randint(0, len(color.colorKeys) - 1)]
                    randcolor += "0"
                    color.change(randcolor)
                cls()
                for x in range(self.y):
                    print(randi(self.x))
                time.sleep(0.75)

    printri = printre(x, y, colorCh)
    printri.start()

    input()
    afk = False
    color.change(oldColor)

def Timer():
    cls()
    hr = int(input("Hour:\n"))
    mi = int(input("\nMinute:\n"))
    sec = int(input("\nSecond:\n"))
    Timerprint(hr,mi,sec)
    Alarmprint(colorCh=True)



def passwordmanager():
    import simplecrypt
    title("Passwordmanager")

    def start():

        global pw0, pw1, pw2, pw3
        pw0 = None
        pw1 = None
        pw2 = None
        pw3 = None

        def unlock(lvl=None):


            def lvl0():
                global pw0

                cls()
                print("Loading...")

                mpw0 = "$sQHB<~aws7!w3,§4t)1köBc_,dtid>ümMU?m>tlG>GD+l%/KjKIb0U%gK§j<bU]R?W§;z|r9s|bE>.t,?MjC+u1t)DV_!E(IqW?vpy8Vd&kw§ißäYTc%g}U3xKM_}ZxI}Zr)agk_|-nJeü*.):(~7"

                pw0_raw = open("data\\Password\\MPwds\\pw0", "rb")
                pw0_lock = pw0_raw.read()

                pw0 = simplecrypt.decrypt(mpw0, pw0_lock).decode("utf-8")
                pw0_raw.close()

            def lvl1():
                global pw1

                cls()
                mpw1 = input("Master Password No.1:\n")
                cls()
                print("Loading...")

                pw1_raw = open("data\\Password\\MPwds\\pw1", "rb")
                pw1_lock = pw1_raw.read()
                try:
                    pw1 = simplecrypt.decrypt(mpw1, pw1_lock).decode("utf-8")
                except simplecrypt.DecryptionException:
                    print("Wrong Masterpassword")
                    time.sleep(1.5)
                pw1_raw.close()

            def lvl2():
                global pw2
                cls()
                mpw2 = input("Master Password No.2:\n")
                cls()
                print("Loading...")

                pw2_raw = open("data\\Password\\MPwds\\pw2", "rb")
                pw2_lock = pw2_raw.read()

                try:
                    pw2 = simplecrypt.decrypt(mpw2, pw2_lock).decode("utf-8")
                except simplecrypt.DecryptionException:
                    print("Wrong Masterpassword")
                    time.sleep(1.5)
                pw2_raw.close()

            def lvl3():
                global pw3
                cls()
                mpw3 = input("Master Password No.3:\n")
                cls()
                print("Loading...")

                pw3_raw = open("data\\Password\\MPwds\\pw3", "rb")
                pw3_lock = pw3_raw.read()

                try:
                    pw3 = simplecrypt.decrypt(mpw3, pw3_lock).decode("utf-8")
                except simplecrypt.DecryptionException:
                    print("Wrong Masterpassword")
                    time.sleep(1.5)
                pw3_raw.close()

            if lvl == 0:
                lvl0()
            elif lvl == 1:
                lvl1()
            elif lvl == 2:
                lvl2()
            elif lvl == 3:
                lvl3()
            elif lvl is None:
                cls()
                print("Unlock lvl 1/2/3")
                lvlu = input()
                if lvlu == 1:
                    lvl1()
                elif lvlu == 2:
                    lvl2()
                elif lvlu == 3:
                    lvl3()

        def creapw(): # vergess nicht hier kein crea, del, mpw liste erstellen lassen!
            title("Create a PW")
            cls()

            def start_input():

                #pwlvl = None
                #pwfullname = None
                #pwemail = None
                #pwnumber = None
                #pwbdate = None
                #pwgender = None
                #pwresidence = None
                #pwpassword = None
                #pwsq1 = None
                pwsq1a = None
                pwsq2 = None
                pwsq2a = None
                pwsq3 = None
                pwsq3a = None

                cls()
                print("%s:\n\nPassword (RAN):" % pwname)
                pwpassword = input().rstrip("\n")
                if pwpassword.lower() == "ran":
                    pwpassword = randompw(True)
                    cls()
                    print("Your random Password:\n\n%s" % pwpassword)
                    input()
                cls()
                print("%s:\n\nPassword Level (1/2/3):" % pwname)
                pwlvl = input().rstrip("\n")

                if int(pwlvl) == 1:
                    unlock(1)
                elif int(pwlvl) == 2:
                    unlock(2)
                elif int(pwlvl) == 3:
                    unlock(3)

                cls()
                print("%s:\n\nWebsite:" % pwname)
                pwwebsite = input().rstrip("\n")
                cls()
                print("%s:\n\nType:" % pwname)
                pwtype = input().rstrip("\n")
                cls()
                print("%s:\n'None' for nothing, today (NOW)\n\nDate:" % pwname)
                pwdate = input().rstrip("\n")
                if pwdate.lower() == "none" or pwdate.lower() == "":
                    pwdate = None
                elif pwdate.lower() == "now":
                    pwdate = datetime.datetime.now().strftime("%d.%m.%Y")
                cls()
                print("%s:\n'None' for nothing\n\nNickname:" % pwname)
                pwnick = input().rstrip("\n")
                if pwnick.lower() == "none" or pwnick.lower() == "":
                    pwnick = None
                cls()
                print("%s:\n'None' for nothing\n\nFull name:" % pwname)
                pwfullname = input().rstrip("\n")
                if pwfullname.lower() == "none" or pwfullname.lower() == "":
                    pwfullname = None
                cls()
                print("%s:\n'None' for nothing, lualbi11@aol.de (REAL)\n\nE-Mail:" % pwname)
                pwemail = input().rstrip("\n")
                if pwemail.lower() == "none" or pwemail.lower() == "":
                    pwemail = None
                elif pwemail.lower() == "real":
                    pwemail = "lualbi11@aol.de"
                cls()
                print("%s:\n'None' for nothing\n\nPhonenumber:" % pwname)
                pwnumber = input().rstrip("\n")
                if pwnumber.lower() == "none" or pwnumber.lower() == "":
                    pwnumber = None
                cls()
                print("%s:\n'None' for nothing\n\nBirthdate:" % pwname)
                pwbdate = input().rstrip("\n")
                if pwbdate.lower() == "none" or pwbdate.lower() == "":
                    pwbdate = None
                cls()
                print("%s:\n'None' for nothing\n\nGender:" % pwname)
                pwgender = input().rstrip("\n")
                if pwgender.lower() == "none" or pwgender.lower() == "":
                    pwgender = None
                cls()
                print("%s:\n'None' for nothing\n\nResidence:" % pwname)
                pwresidence = input().rstrip("\n")
                if pwresidence.lower() == "none" or pwresidence.lower() == "":
                    pwresidence = None
                cls()
                print("%s:\n'None' for nothing\n\nSecurity Question:" % pwname)
                pwsq1 = input().rstrip("\n")
                if pwsq1.lower() == "none" or pwsq1.lower() == "":
                    pwsq1 = None
                cls()
                if pwsq1 is not None:
                    print("%s:\n\nSecurity Question answer:" % pwname)
                    pwsq1a = input().rstrip("\n")
                    cls()
                    print("%s:\n'None' for nothing\n\nSecurity Question 2:" % pwname)
                    pwsq2 = input().rstrip("\n")
                    if pwsq2.lower() == "none" or pwsq2.lower() == "":
                        pwsq2 = None
                    cls()
                    if pwsq2 is not None:
                        print("%s:\n\nSecurity Question 2 answer:" % pwname)
                        pwsq2a = input().rstrip("\n")
                        cls()
                        print("%s:\n'None' for nothing\n\nSecurity Question 3:" % pwname)
                        pwsq3 = input().rstrip("\n")
                        if pwsq3.lower() == "none" or pwsq3.lower() == "":
                            pwsq3 = None
                        cls()
                        if pwsq3 is not None:
                            print("%s:\n\nSecurity Question 3 answer:" % pwname)
                            pwsq3a = input().rstrip("\n")
                            cls()

                print("%s:\n'None' for nothing\n\nComment:" % pwname)
                pwcomment = input().rstrip("\n")
                if pwcomment.lower() == "none" or pwcomment.lower() == "":
                    pwcomment = None
                cls()


                title("Encrypting")

                os.mkdir("data\\Password\\Pwds\\%s" % pwname)
                os.mkdir("data\\Password\\Pwds\\%s\\pwd" % pwname)
                os.mkdir("data\\Password\\Pwds\\%s\\personaldata" % pwname)


                pwlist.append(pwname + "\n")
                pwlist.sort()

                chpwlist_raw = open("data\\Password\\list.txt", "w")
                for xcl in pwlist:
                    chpwlist_raw.write(xcl)
                chpwlist_raw.close()


                pwinfo = [pwname + "\n", pwwebsite + "\n", pwtype + "\n"]

                if pwdate is not None:
                    pwinfo.append(pwdate)

                pwinfo_raw = open("data\\Password\\Pwds\\%s\\info.txt" % pwname, "w")

                for xcl in pwinfo:
                    pwinfo_raw.write(xcl)
                pwinfo_raw.close()

                if pwnick is not None:
                    pwnick_raw = open("data\\Password\\Pwds\\%s\\personaldata\\nickname.txt" % pwname, "w")
                    pwnick_raw.write(pwnick)
                    pwinfo_raw.close()

                if pwfullname is not None:
                    pwfullname_raw = open("data\\Password\\Pwds\\%s\\personaldata\\name" % pwname, "wb")
                    if int(pwlvl) == 0:
                        pwfullname_raw.write(simplecrypt.encrypt(pw0, pwfullname))
                    elif int(pwlvl) == 1:
                        pwfullname_raw.write(simplecrypt.encrypt(pw1, pwfullname))
                    elif int(pwlvl) == 2:
                        pwfullname_raw.write(simplecrypt.encrypt(pw2, pwfullname))
                    elif int(pwlvl) == 3:
                        pwfullname_raw.write(simplecrypt.encrypt(pw3, pwfullname))

                    pwfullname_raw.close()

                if pwemail is not None:
                    pwemail_raw = open("data\\Password\\Pwds\\%s\\personaldata\\email" % pwname, "wb")
                    if int(pwlvl) == 0:
                        pwemail_raw.write(simplecrypt.encrypt(pw0, pwemail))
                    elif int(pwlvl) == 1:
                        pwemail_raw.write(simplecrypt.encrypt(pw1, pwemail))
                    elif int(pwlvl) == 2:
                        pwemail_raw.write(simplecrypt.encrypt(pw2, pwemail))
                    elif int(pwlvl) == 3:
                        pwemail_raw.write(simplecrypt.encrypt(pw3, pwemail))

                    pwemail_raw.close()


                if pwnumber is not None:
                    pwnumber_raw = open("data\\Password\\Pwds\\%s\\personaldata\\pnumber" % pwname, "wb")
                    if int(pwlvl) == 0:
                        pwnumber_raw.write(simplecrypt.encrypt(pw0, pwnumber))
                    elif int(pwlvl) == 1:
                        pwnumber_raw.write(simplecrypt.encrypt(pw1, pwnumber))
                    elif int(pwlvl) == 2:
                        pwnumber_raw.write(simplecrypt.encrypt(pw2, pwnumber))
                    elif int(pwlvl) == 3:
                        pwnumber_raw.write(simplecrypt.encrypt(pw3, pwnumber))

                    pwnumber_raw.close()


                if pwbdate is not None:
                    pwbdate_raw = open("data\\Password\\Pwds\\%s\\personaldata\\bdate" % pwname, "wb")
                    if int(pwlvl) == 0:
                        pwbdate_raw.write(simplecrypt.encrypt(pw0, pwbdate))
                    elif int(pwlvl) == 1:
                        pwbdate_raw.write(simplecrypt.encrypt(pw1, pwbdate))
                    elif int(pwlvl) == 2:
                        pwbdate_raw.write(simplecrypt.encrypt(pw2, pwbdate))
                    elif int(pwlvl) == 3:
                        pwbdate_raw.write(simplecrypt.encrypt(pw3, pwbdate))

                    pwbdate_raw.close()

                if pwgender is not None:
                    pwgender_raw = open("data\\Password\\Pwds\\%s\\personaldata\\gender" % pwname, "wb")
                    if int(pwlvl) == 0:
                        pwgender_raw.write(simplecrypt.encrypt(pw0, pwgender))
                    elif int(pwlvl) == 1:
                        pwgender_raw.write(simplecrypt.encrypt(pw1, pwgender))
                    elif int(pwlvl) == 2:
                        pwgender_raw.write(simplecrypt.encrypt(pw2, pwgender))
                    elif int(pwlvl) == 3:
                        pwgender_raw.write(simplecrypt.encrypt(pw3, pwgender))

                    pwgender_raw.close()

                if pwresidence is not None:
                    pwresidence_raw = open("data\\Password\\Pwds\\%s\\personaldata\\residence" % pwname, "wb")
                    if int(pwlvl) == 0:
                        pwresidence_raw.write(simplecrypt.encrypt(pw0, pwresidence))
                    elif int(pwlvl) == 1:
                        pwresidence_raw.write(simplecrypt.encrypt(pw1, pwresidence))
                    elif int(pwlvl) == 2:
                        pwresidence_raw.write(simplecrypt.encrypt(pw2, pwresidence))
                    elif int(pwlvl) == 3:
                        pwresidence_raw.write(simplecrypt.encrypt(pw3, pwresidence))

                    pwresidence_raw.close()

                pwlvl_raw = open("data\\Password\\Pwds\\%s\\pwd\\pwdlvl" % pwname, "wb")
                pwlvl_raw.write(simplecrypt.encrypt(pw0, pwlvl))
                pwlvl_raw.close()

                pwpassword_raw = open("data\\Password\\Pwds\\%s\\pwd\\pwd" % pwname, "wb")
                if int(pwlvl) == 0:
                    pwpassword_raw.write(simplecrypt.encrypt(pw0, pwpassword))
                elif int(pwlvl) == 1:
                    pwpassword_raw.write(simplecrypt.encrypt(pw1, pwpassword))
                elif int(pwlvl) == 2:
                    pwpassword_raw.write(simplecrypt.encrypt(pw2, pwpassword))
                elif int(pwlvl) == 3:
                    pwpassword_raw.write(simplecrypt.encrypt(pw3, pwpassword))

                pwpassword_raw.close()


                if pwsq1 is not None:
                    pwsq1_raw = open("data\\Password\\Pwds\\%s\\pwd\\sq1" % pwname, "w")
                    pwsq1_raw.write(pwsq1)
                    pwsq1_raw.close()

                    pwsq1a_raw = open("data\\Password\\Pwds\\%s\\pwd\\sq1a" % pwname, "wb")
                    if int(pwlvl) == 0:
                        pwsq1a_raw.write(simplecrypt.encrypt(pw0, pwsq1a))
                    elif int(pwlvl) == 1:
                        pwsq1a_raw.write(simplecrypt.encrypt(pw1, pwsq1a))
                    elif int(pwlvl) == 2:
                        pwsq1a_raw.write(simplecrypt.encrypt(pw2, pwsq1a))
                    elif int(pwlvl) == 3:
                        pwsq1a_raw.write(simplecrypt.encrypt(pw3, pwsq1a))

                        pwsq1a_raw.close()

                    if pwsq2 is not None:
                        pwsq2_raw = open("data\\Password\\Pwds\\%s\\pwd\\sq2" % pwname, "w")
                        pwsq2_raw.write(pwsq2)
                        pwsq2_raw.close()

                        pwsq2a_raw = open("data\\Password\\Pwds\\%s\\pwd\\sq2a" % pwname, "wb")
                        if int(pwlvl) == 0:
                            pwsq2a_raw.write(simplecrypt.encrypt(pw0, pwsq2a))
                        elif int(pwlvl) == 1:
                            pwsq2a_raw.write(simplecrypt.encrypt(pw1, pwsq2a))
                        elif int(pwlvl) == 2:
                            pwsq2a_raw.write(simplecrypt.encrypt(pw2, pwsq2a))
                        elif int(pwlvl) == 3:
                            pwsq2a_raw.write(simplecrypt.encrypt(pw3, pwsq2a))

                            pwsq2a_raw.close()

                        if pwsq3 is not None:
                            pwsq3_raw = open("data\\Password\\Pwds\\%s\\pwd\\sq3" % pwname, "w")
                            pwsq3_raw.write(pwsq2)
                            pwsq3_raw.close()

                            pwsq3a_raw = open("data\\Password\\Pwds\\%s\\pwd\\sq3a" % pwname, "wb")
                            if int(pwlvl) == 0:
                                pwsq3a_raw.write(simplecrypt.encrypt(pw0, pwsq3a))
                            elif int(pwlvl) == 1:
                                pwsq3a_raw.write(simplecrypt.encrypt(pw1, pwsq3a))
                            elif int(pwlvl) == 2:
                                pwsq3a_raw.write(simplecrypt.encrypt(pw2, pwsq3a))
                            elif int(pwlvl) == 3:
                                pwsq3a_raw.write(simplecrypt.encrypt(pw3, pwsq3a))

                            pwsq3a_raw.close()

                if pwcomment is not None:
                    pwcomment_raw = open("data\\Password\\Pwds\\%s\\comment.txt" % pwname, "w")
                    pwcomment_raw.write(pwcomment)
                    pwcomment_raw.close()


                cls()
                title("Created PW")
                time.sleep(1)
                print("Success")




            startin = True

            print("Name:")
            pwname = input().rstrip("\n")

            for xn in pwlist:
                if pwname == xn:
                    startin = False


            if pwname.lower() == "del":
                startin = False
            elif pwname.lower() == "mpw":
                startin = False
            elif pwname.lower() == "crea":
                startin = False

            if startin:
                start_input()



        def delpw():
            pass
        def chmpw():
            cls()
            print("Change lvl 1/2/3")
            changelvl = int(input())
            if changelvl == 1:
                cls()
                oldmpw = input("Old Masterpw:\n")
                cls()
                newmpw = input("New Masterpw:\n")

                if newmpw == input("Reapeat new Masterpw:\n"):
                    cls()
                    print("Loading...")
                    oldpw_raw = open("data\\Password\\MPwds\\pw1", "rb")
                    oldpw_lock = oldpw_raw.read()
                    oldpw = simplecrypt.decrypt(oldmpw, oldpw_lock).decode("utf-8")
                    oldpw_raw.close()

                    pw_raw = open("data\\Password\\MPwds\\pw1", "wb")
                    pw_raw.write(simplecrypt.encrypt(newmpw, oldpw))
                    pw_raw.close()

                else:
                    cls()
                    print("Error")


            elif changelvl == 2:
                cls()
                oldmpw = input("Old Masterpw:\n")
                cls()
                newmpw = input("New Masterpw:\n")

                if newmpw == input("Reapeat new Masterpw:\n"):
                    cls()
                    print("Loading...")
                    oldpw_raw = open("data\\Password\\MPwds\\pw2", "rb")
                    oldpw_lock = oldpw_raw.read()
                    oldpw = simplecrypt.decrypt(oldmpw, oldpw_lock).decode("utf-8")
                    oldpw_raw.close()

                    pw_raw = open("data\\Password\\MPwds\\pw2", "wb")
                    pw_raw.write(simplecrypt.encrypt(newmpw, oldpw))
                    pw_raw.close()

                else:
                    cls()
                    print("Error")

            elif changelvl == 3:
                cls()
                oldmpw = input("Old Masterpw:\n")
                cls()
                newmpw = input("New Masterpw:\n")

                if newmpw == input("Reapeat new Masterpw:\n"):
                    cls()
                    print("Loading...")
                    oldpw_raw = open("data\\Password\\MPwds\\pw3", "rb")
                    oldpw_lock = oldpw_raw.read()
                    oldpw = simplecrypt.decrypt(oldmpw, oldpw_lock).decode("utf-8")
                    oldpw_raw.close()

                    pw_raw = open("data\\Password\\MPwds\\pw3", "wb")
                    pw_raw.write(simplecrypt.encrypt(newmpw, oldpw))
                    pw_raw.close()

                else:
                    cls()
                    print("Error")

        def pw(listname):
            global pw0, pw1, pw2, pw3, userdata, securityquestion

            title("PW: decoding %s" % listname)
            cls()
            print("Loading...")

            userdata = False
            securityquestion = False

            userdataskip = False
            passwordskip = False
            securityquestionskip = False

            pwlvl = None
            pwfullname = None
            pwemail = None
            pwnumber = None
            pwbdate = None
            pwgender = None
            pwresidence = None
            pwpassword = None
            pwsq1 = None
            pwsq1a = None
            pwsq2 = None
            pwsq2a = None
            pwsq3 = None
            pwsq3a = None

            def userdataac():
                global userdata
                userdata = True

            def securityquestionac():
                global securityquestion
                securityquestion = True

            while True:



                pw_info_raw = open("data\\Password\\Pwds\\%s\\info.txt" % listname, "r")
                pw_info = []
                for pwi in  pw_info_raw:
                    pw_info.append(pwi)
                pw_info_raw.close()
                pwname = pw_info[0]
                pwwebsite = pw_info[1]
                pwtype = pw_info[2]
                try:
                    pwdate = pw_info[3]
                except IndexError:
                    pwdate = None

                if os.path.exists("data\\Password\\Pwds\\%s\\personaldata\\nickname.txt" % listname):
                    pwnick_raw = open("data\\Password\\Pwds\\%s\\personaldata\\nickname.txt" % listname, "r")
                    pwnick = pwnick_raw.read()
                    pwnick_raw.close()
                else:
                    pwnick = None

                if not passwordskip:

                    pwlvl_raw = open("data\\Password\\Pwds\\%s\\pwd\\pwdlvl" % listname, "rb")
                    pwlvl_lock = pwlvl_raw.read()
                    pwlvl_raw.close()

                    pwlvl = int(simplecrypt.decrypt(pw0, pwlvl_lock).decode("utf-8"))

                    if pwlvl == 0:
                        pwpassword_raw = open("data\\Password\\Pwds\\%s\\pwd\\pwd" % listname, "rb")
                        pwpassword_lock = pwpassword_raw.read()
                        pwpassword_raw.close()

                        pwpassword = simplecrypt.decrypt(pw0, pwpassword_lock).decode("utf-8")

                    elif pwlvl == 1:
                        if pw1 is not None:
                            pwpassword_raw = open("data\\Password\\Pwds\\%s\\pwd\\pwd" % listname, "rb")
                            pwpassword_lock = pwpassword_raw.read()
                            pwpassword_raw.close()

                            pwpassword = simplecrypt.decrypt(pw1, pwpassword_lock).decode("utf-8")
                        else:
                            pwpassword = "*locked, please unlock lvl 1*"

                    elif pwlvl == 2:
                        if pw2 is not None:
                            pwpassword_raw = open("data\\Password\\Pwds\\%s\\pwd\\pwd" % listname, "rb")
                            pwpassword_lock = pwpassword_raw.read()
                            pwpassword_raw.close()

                            pwpassword = simplecrypt.decrypt(pw2, pwpassword_lock).decode("utf-8")
                        else:
                            pwpassword = "*locked, please unlock lvl 2*"

                    elif pwlvl == 3:
                        if pw3 is not None:
                            pwpassword_raw = open("data\\Password\\Pwds\\%s\\pwd\\pwd" % listname, "rb")
                            pwpassword_lock = pwpassword_raw.read()
                            pwpassword_raw.close()

                            pwpassword = simplecrypt.decrypt(pw3, pwpassword_lock).decode("utf-8")
                        else:
                            pwpassword = "*locked, please unlock lvl 3*"

                    else:
                        pwpassword = "*Error: lvl not found*"

                    passwordskip = True

                #if pwlvl == 1:
                #    if pw1 is not None:
                #        pwlvlunlock = True
                #        a1 = True
                #    else:
                #        pwlvlunlock = False
                #elif pwlvl == 2:
                #    if pw2 is not None:
                #        pwlvlunlock = True
                #    else:
                #        pwlvlunlock = False
                #elif pwlvl == 3:
                #    if pw3 is not None:
                #        pwlvlunlock = True
                #    else:
                #        pwlvlunlock = False

                if not userdataskip:
                    if userdata:
                        if os.path.exists("data\\Password\\Pwds\\%s\\personaldata\\name" % listname):
                            pwfullname_raw = open("data\\Password\\Pwds\\%s\\personaldata\\name" % listname, "rb")
                            pwfullname_lock = pwfullname_raw.read()
                            pwfullname_raw.close()
                            if pwlvl == 0:
                                pwfullname = simplecrypt.decrypt(pw0, pwfullname_lock).decode("utf-8")
                            elif pwlvl == 1:
                                if pw1 is not None:
                                    pwfullname = simplecrypt.decrypt(pw1, pwfullname_lock).decode("utf-8")
                                else:
                                    pwfullname = "*locked, please unlock lvl 1*"
                            elif pwlvl == 2:
                                if pw2 is not None:
                                    pwfullname = simplecrypt.decrypt(pw2, pwfullname_lock).decode("utf-8")
                                else:
                                    pwfullname = "*locked, please unlock lvl 2*"
                            elif pwlvl == 3:
                                if pw3 is not None:
                                    pwfullname = simplecrypt.decrypt(pw3, pwfullname_lock).decode("utf-8")
                                else:
                                    pwfullname = "*locked, please unlock lvl 3*"
                        else:
                            pwfullname = None

                        if os.path.exists("data\\Password\\Pwds\\%s\\personaldata\\email" % listname):
                            pwemail_raw = open("data\\Password\\Pwds\\%s\\personaldata\\email" % listname, "rb")
                            pwemail_lock = pwemail_raw.read()
                            pwemail_raw.close()
                            if pwlvl == 0:
                                pwemail = simplecrypt.decrypt(pw0, pwemail_lock).decode("utf-8")
                            elif pwlvl == 1:
                                if pw1 is not None:
                                    pwemail = simplecrypt.decrypt(pw1, pwemail_lock).decode("utf-8")
                                else:
                                    pwemail = "*locked, please unlock lvl 1*"
                            elif pwlvl == 2:
                                if pw2 is not None:
                                    pwemail = simplecrypt.decrypt(pw2, pwemail_lock).decode("utf-8")
                                else:
                                    pwemail = "*locked, please unlock lvl 2*"
                            elif pwlvl == 3:
                                if pw3 is not None:
                                    pwemail = simplecrypt.decrypt(pw3, pwemail_lock).decode("utf-8")
                                else:
                                    pwemail = "*locked, please unlock lvl 3*"
                        else:
                            pwemail = None

                        if os.path.exists("data\\Password\\Pwds\\%s\\personaldata\\pnumber" % listname):
                            pwnumber_raw = open("data\\Password\\Pwds\\%s\\personaldata\\pnumber" % listname, "rb")
                            pwnumber_lock = pwnumber_raw.read()
                            pwnumber_raw.close()

                            if pwlvl == 0:
                                pwnumber = simplecrypt.decrypt(pw0, pwnumber_lock).decode("utf-8")
                            elif pwlvl == 1:
                                if pw1 is not None:
                                    pwnumber = simplecrypt.decrypt(pw1, pwnumber_lock).decode("utf-8")
                                else:
                                    pwnumber = "*locked, please unlock lvl 1*"
                            elif pwlvl == 2:
                                if pw2 is not None:
                                    pwnumber = simplecrypt.decrypt(pw2, pwnumber_lock).decode("utf-8")
                                else:
                                    pwnumber = "*locked, please unlock lvl 3*"
                            elif pwlvl == 3:
                                if pw3 is not None:
                                    pwnumber = simplecrypt.decrypt(pw3, pwnumber_lock).decode("utf-8")
                                else:
                                    pwnumber = "*locked, please unlock lvl 3*"
                        else:
                            pwnumber = None

                        if os.path.exists("data\\Password\\Pwds\\%s\\personaldata\\bdate" % listname):
                            pwbdate_raw = open("data\\Password\\Pwds\\%s\\personaldata\\bdate" % listname, "rb")
                            pwbdate_lock = pwbdate_raw.read()
                            pwbdate_raw.close()

                            if pwlvl == 0:
                                pwbdate = simplecrypt.decrypt(pw0, pwbdate_lock).decode("utf-8")
                            elif pwlvl == 1:
                                if pw1 is not None:
                                    pwbdate = simplecrypt.decrypt(pw1, pwbdate_lock).decode("utf-8")
                                else:
                                    pwbdate = "*locked, please unlock lvl 1*"
                            elif pwlvl == 2:
                                if pw2 is not None:
                                    pwbdate = simplecrypt.decrypt(pw2, pwbdate_lock).decode("utf-8")
                                else:
                                    pwbdate = "*locked, please unlock lvl 2*"
                            elif pwlvl == 3:
                                if pw3 is not None:
                                    pwbdate = simplecrypt.decrypt(pw3, pwbdate_lock).decode("utf-8")
                                else:
                                    pwbdate = "*locked, please unlock lvl 3*"
                        else:
                            pwbdate = None

                        if os.path.exists("data\\Password\\Pwds\\%s\\personaldata\\gender" % listname):
                            pwgender_raw = open("data\\Password\\Pwds\\%s\\personaldata\\gender" % listname, "rb")
                            pwgender_lock = pwgender_raw.read()
                            pwgender_raw.close()

                            if pwlvl == 0:
                                pwgender = simplecrypt.decrypt(pw0, pwgender_lock).decode("utf-8")
                            elif pwlvl == 1:
                                if pw1 is not None:
                                    pwgender = simplecrypt.decrypt(pw1, pwgender_lock).decode("utf-8")
                                else:
                                    pwgender = "*locked, please unlock lvl 1*"
                            elif pwlvl == 2:
                                if pw2 is not None:
                                    pwgender = simplecrypt.decrypt(pw2, pwgender_lock).decode("utf-8")
                                else:
                                    pwgender = "*locked, please unlock lvl 2*"
                            elif pwlvl == 3:
                                if pw3 is not None:
                                    pwgender = simplecrypt.decrypt(pw3, pwgender_lock).decode("utf-8")
                                else:
                                    pwgender = "*locked, please unlock lvl 3*"
                        else:
                            pwgender = None

                        if os.path.exists("data\\Password\\Pwds\\%s\\personaldata\\residence" % listname):
                            pwresidence_raw = open("data\\Password\\Pwds\\%s\\personaldata\\residence" % listname, "rb")
                            pwresidence_lock = pwresidence_raw.read()
                            pwresidence_raw.close()

                            if pwlvl == 0:
                                pwresidence = simplecrypt.decrypt(pw0, pwresidence_lock).decode("utf-8")
                            elif pwlvl == 1:
                                if pw1 is not None:
                                    pwresidence = simplecrypt.decrypt(pw1, pwresidence_lock).decode("utf-8")
                                else:
                                    pwresidence = "*locked, please unlock lvl 1*"
                            elif pwlvl == 2:
                                if pw2 is not None:
                                    pwresidence = simplecrypt.decrypt(pw2, pwresidence_lock).decode("utf-8")
                                else:
                                    pwresidence = "*locked, please unlock lvl 2*"
                            elif pwlvl == 3:
                                if pw3 is not None:
                                    pwresidence = simplecrypt.decrypt(pw3, pwresidence_lock).decode("utf-8")
                                else:
                                    pwresidence = "*locked, please unlock lvl 3*"
                        else:
                            pwresidence = None

                        userdataskip = True

                    else:
                        pwfullname = None
                        pwemail = None
                        pwnumber = None
                        pwbdate = None
                        pwgender = None
                        pwresidence = None





                if not securityquestionskip:
                    if os.path.exists("data\\Password\\Pwds\\%s\\pwd\\sq1.txt" % listname):
                        pwsq1_raw = open("data\\Password\\Pwds\\%s\\personaldata\\sq1.txt" % listname, "r")
                        pwsq1 = pwsq1_raw.read()
                        pwsq1_raw.close()


                        pwsq1a_raw = open("data\\Password\\Pwds\\%s\\personaldata\\sq1a" % listname, "rb")
                        pwsq1a_lock = pwsq1a_raw.read()
                        pwsq1a_raw.close()

                        if pwlvl == 0:
                            pwsq1a = simplecrypt.decrypt(pw0, pwsq1a_lock).decode("utf-8")
                        elif pwlvl == 1:
                            pwsq1a = simplecrypt.decrypt(pw1, pwsq1a_lock).decode("utf-8")
                        elif pwlvl == 2:
                            pwsq1a = simplecrypt.decrypt(pw2, pwsq1a_lock).decode("utf-8")
                        elif pwlvl == 3:
                            pwsq1a = simplecrypt.decrypt(pw3, pwsq1a_lock).decode("utf-8")
                        else:
                            pwsq1a = "*Error: lvl not found*"


                        if os.path.exists("data\\Password\\Pwds\\%s\\pwd\\sq2.txt" % listname):
                            pwsq2_raw = open("data\\Password\\Pwds\\%s\\personaldata\\sq2.txt" % listname, "r")
                            pwsq2 = pwsq2_raw.read()
                            pwsq2_raw.close()

                            pwsq2a_raw = open("data\\Password\\Pwds\\%s\\personaldata\\sq2a" % listname, "rb")
                            pwsq2a_lock = pwsq2a_raw.read()
                            pwsq2a_raw.close()

                            if pwlvl == 0:
                                pwsq2a = simplecrypt.decrypt(pw0, pwsq2a_lock).decode("utf-8")
                            elif pwlvl == 1:
                                pwsq2a = simplecrypt.decrypt(pw1, pwsq2a_lock).decode("utf-8")
                            elif pwlvl == 2:
                                pwsq2a = simplecrypt.decrypt(pw2, pwsq2a_lock).decode("utf-8")
                            elif pwlvl == 3:
                                pwsq2a = simplecrypt.decrypt(pw3, pwsq2a_lock).decode("utf-8")
                            else:
                                pwsq2a = "*Error: lvl not found*"

                            if os.path.exists("data\\Password\\Pwds\\%s\\pwd\\sq3.txt" % listname):
                                pwsq3_raw = open("data\\Password\\Pwds\\%s\\personaldata\\sq3.txt" % listname, "r")
                                pwsq3 = pwsq3_raw.read()
                                pwsq3_raw.close()

                                pwsq3a_raw = open("data\\Password\\Pwds\\%s\\personaldata\\sq3a" % listname, "rb")
                                pwsq3a_lock = pwsq3a_raw.read()
                                pwsq3a_raw.close()

                                if pwlvl == 0:
                                    pwsq3a = simplecrypt.decrypt(pw0, pwsq3a_lock).decode("utf-8")
                                elif pwlvl == 1:
                                    pwsq3a = simplecrypt.decrypt(pw1, pwsq3a_lock).decode("utf-8")
                                elif pwlvl == 2:
                                    pwsq3a = simplecrypt.decrypt(pw2, pwsq3a_lock).decode("utf-8")
                                elif pwlvl == 3:
                                    pwsq3a = simplecrypt.decrypt(pw3, pwsq3a_lock).decode("utf-8")
                                else:
                                    pwsq3a = "*Error: lvl not found*"





                    securityquestionskip = True

                if os.path.exists("data\\Password\\Pwds\\%s\\comment.txt" % listname):
                    pwcomment_raw = open("data\\Password\\Pwds\\%s\\comment.txt" % listname, "r")
                    pwcomment = pwcomment_raw.read()
                    pwcomment_raw.close()
                else:
                    pwcomment = None


                title("PW: %s" % listname)

                cls()


                print("%s:\n" % pwname.rstrip("\n"))
                print("Website:\t  %s" % pwwebsite.rstrip("\n"))
                print("Type:\t\t  %s" % pwtype)
                if pwdate is not None:
                    print("Date of sign up:  %s\n" % pwdate)
                if pwnick is not None:
                    print("Nickname:\t  %s" % pwnick)
                if pwfullname is not None:
                    print("Fullname:\t  %s" % pwfullname)
                if pwemail is not None:
                    print("E-Mail:\t\t  %s" % pwemail)
                if pwnumber is not None:
                    print("Phonenummber:\t  %s" % pwnumber)
                if pwbdate is not None:
                    print("Birthdate:\t  %s" % pwbdate)
                if pwgender is not None:
                    print("Gender:\t\t  %s" % pwgender)
                if pwresidence is not None:
                    print("Residence:\t  %s" % pwresidence)

                print("\nPassword:\n%s\n" % pwpassword)

                if pwsq1 is not None:
                    print("Security Question 1:\n%s" % pwsq1)
                    print("Security Question 1 answer:\n%s" % pwsq1a)
                if pwsq2 is not None:
                    print("Security Question 2:\n%s" % pwsq2)
                    print("Security Question 2 answer:\n%s" % pwsq2a)
                if pwsq3 is not None:
                    print("Security Question 3:\n%s" % pwsq3)
                    print("Security Question 3 answer:\n%s" % pwsq3a)
                if pwcomment is not None:
                    print("Comment:\n%s" % pwcomment)

                user_input_pw = input("\n\n")

                if user_input_pw.lower() == "unlock":
                    unlock()
                    passwordskip = False
                    userdataskip = False
                    securityquestionskip = False
                elif user_input_pw.lower() == "unlock1":
                    unlock(1)
                    passwordskip = False
                    userdataskip = False
                    securityquestionskip = False
                elif user_input_pw.lower() == "unlock2":           
                    unlock(2)                                      
                    passwordskip = False
                    userdataskip = False
                    securityquestionskip = False
                elif user_input_pw.lower() == "unlock3":           
                    unlock(3)                                      
                    passwordskip = False
                    userdataskip = False
                    securityquestionskip = False
                elif user_input_pw.lower() == "ud":                
                    userdataac()                                   
                    cls()                                          
                    print("Loading...")
                    userdataskip = False                           
                elif user_input_pw.lower() == "sq":                
                    securityquestionac()                           
                    cls()
                    print("Loading...")
                    securityquestionskip = False
                else:
                    break


        unlock(0)

        pwlist_raw = open("data\\Password\\list.txt", "r")
        pwlist = []
        for xl in pwlist_raw:
            pwlist.append(xl)
        pwlist_raw.close()

        cls()
        print("Commands:\nCreate a new password (CREA), Delete a password (DEL), Unlock pw (UNLOCK)\n\nPasswords:\n") # geheim: change masterpw (mpw)
        for xl in pwlist:
            print(xl.rstrip("\n"))

        user_input_p = input("\n")

        if user_input_p.lower() == "crea":
            creapw()
        elif user_input_p.lower() == "del":
            delpw()
        elif user_input_p.lower() == "mpw":
            chmpw()
        elif user_input_p.lower() == "unlock":
            unlock()
        elif user_input_p.lower() == "unlock1":
            unlock(1)
        elif user_input_p.lower() == "unlock2":
            unlock(2)
        elif user_input_p.lower() == "unlock3":
            unlock(3)

        for xl in pwlist:
            if user_input_p == xl.rstrip("\n"):
                pw(user_input_p)
    cls()

    print("Password:\n")

    if input() == "Luis":
        start()





#MusicPlayerTest = MusicPlayerC()

def Splatoon():
    spl = SplatoonC()

    class Printerr(threading.Thread):
        def run(self):
            while spl.RUN:
                cls()
                spl.printit()
                time.sleep(1)

    Printer = Printerr()
    Printer.start()

    while spl.RUN:
        user_input = input()
        spl.input(user_input)



def main():
    versionFind()
    title("Waiting for Input")

    cls()

    print("Evecon")
    print("PC: " + Computername)

    print("\nMenu:")

    print("\nFuntions:")
    print("Musicplayer (MUSIC), Radio (RADIO), Foxi (FOX)")
    print("Time (TIME), Timer (TIMER)")

    print("\nSettings:")
    print("Light (L)")

    print("\nDev:")
    print("Upgrade (UG), Debug (DEBUG), Status (STATUS)")


    user_input = input("\n\n")

    if user_input.lower() == "fox" or user_input.lower() == "fap" or user_input.lower() == "foxi":
        Foxi.fap()
    elif user_input.lower() == "foxpage":
        Foxi.open_foxpage()
    elif user_input.lower() == "foxname":
        Foxi.open_foxname()
    elif user_input.lower() == "l":
        color.Man()
    elif user_input.lower() == "ug":
        upgrade()
    elif user_input.lower() == "debug":
        debug()
    #elif user_input.lower() == "games":
    #    games()
    #elif user_input.lower() == "snake":
    #    games("snake")
    elif user_input.lower() == "music":
        Music()
    elif user_input.lower() == "time":
        Timeprint()
    elif user_input.lower() == "randpw":
        randompw()
    elif user_input.lower() == "pw":
        passwordmanager()
    elif user_input.lower() == "radio":
        Radio()
    elif user_input.lower() == "timer":
        Timer()
    elif user_input.lower() == "status":
        Status()


def Arg():
    global StartupServer

    skiparg = []

    for x in range(5):
        try:
            sys.argv[x]
        except IndexError:
            sys.argv.append(None)
            skiparg.append(x)
    if not skiparg:
        skiparg.append(4)

    for x in range(1, 4):
        if x >= skiparg[0]:
            break
        if sys.argv[x] == "-l_dark":
            title("Load Argument", "Argument: Dark")
            color.change("07")
        if sys.argv[x] == "-l_bright":
            title("Load Argument", "Argument: Bright")
            color.change("F0")
        if sys.argv[x] == "-foxi" or sys.argv[x] == "-fap":
            title("Load Argument", "Foxi")
            ttime.deac()
            Foxi.fap()
            exit_now()
        if sys.argv[x] == "-foxi_page":
            title("Load Argument", "Notie: FOXPAGE")
            ttime.deac()
            Foxi.open_foxpage()
            exit_now()
        if sys.argv[x] == "-foxi_name":
            title("Load Argument", "Notie: FOXNAME")
            ttime.deac()
            Foxi.open_foxname()
            exit_now()
        if sys.argv[x] == "-nc_stdsize":
            title("Load Argument", "Nircmd: Standard size")
            nircmd("setsize", 1000, 520)
        if sys.argv[x] == "-tt_freq":
            title("Load Argument", "TTime: Change Freq")
            title_time.freq = float(sys.argv[x + 1])
        if sys.argv[x] == "-tt_deac":
            title("Load Argument", "TTime: Deactivate")
            ttime.deac()
            # if sys.argv[x] == "-update":
            #    title("Load Argument", "Updater: Updating")
            #    update()
        if sys.argv[x] == "-upgrade":
            title("Load Argument", "Updater: Upgrading")
            upgrade()
        if sys.argv[x] == "-screensaver":
            title("Load Argument", "Screensaver")
            screensaver()
        if sys.argv[x] == "-ep_switch":
            title("Load Argument", "Switch Energy Plan")
            ttime.deac()
            Tools.EnergyPlan.Switch()
            Tools.EnergyPlan.getEP(True)
            time.sleep(2)
            exit_now()
        if sys.argv[x] == "-shutdown":
            title("Load Argument", "Shutdown")
            ttime.deac()
            Tools.Shutdown()
            exit_now()
        if sys.argv[x] == "-reboot":
            title("Load Argument", "Reboot")
            ttime.deac()
            Tools.Reboot()
            exit_now()
        if sys.argv[x] == "-start_server":
            title("Server", " ", " ")
            ttime.deac()
            serverport = int(sys.argv[x + 1])
            if not sys.argv[x + 2] == "app":
                killConsoleWin()
            StartupServer = Server(ip=thisIP, port=serverport, react=StartupServerTasks)
            StartupServer.start()
            StartupServer.join()
            exit_now()
        if sys.argv[x] == "-inter_client":
            title("Interactive Client", " ", " ")
            ttime.deac()
            host = sys.argv[x + 1]
            port = int(sys.argv[x + 2])
            InteractiveClient(host, port)
            exit_now()
        if sys.argv[x] == "-music":
            title("Load Argument", "Musicplayer")
            Music()
            exit_now()
        if sys.argv[x] == "-radio":
            title("Load Argument", "Radio")
            Radio()
            exit_now()

if sys.argv:
    Arg()

if exitnow == 0:
    if __name__ == "__main__":
        title("Search for Updates")
        #update()
        title("Start Enviroment")
        main()
        time.sleep(0)

        exit_now()


# Ideas:
# Status, settings ?
