import os

if __name__ == "__main__":
    cdir = os.getcwd()
    os.chdir("..")
    os.chdir("..")

startmain = False
exitnow = 0
pausetime = 180
thisIP = None
StartupServerJava = None

from EveconLib import *


ttime.start()

title("Load first Programs")
def exit_now(killmex = False):
    ttime.deac()
    # noinspection PyGlobalUndefined
    global exitnow, startmain
    exitnow = 1
    startmain = False
    #if version_PC != 1:
    #    exit()

    if killmex:
        time.sleep(0.5)
        killme()

    sys.exit()


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

def StartupServerTasksJava(dataraw):
    global StartupServerJava
    data = dataraw.split("_")

    if data[0] == "get":
        if data[1] == "mpPort":
            globalMPportsJava.readFile()
            if globalMPportsJava.ports[0]:
                StartupServerJava.send(globalMPportsJava.ports[0])

class FoxiC:
    def __init__(self, browser_type=browser):
        if browser_type == "firefox":
            self.browser = Firefox()
        elif browser_type == "vivaldi":
            self.browser = Vivaldi()
        else:
            self.browser = Firefox()

        self.pageurl = ""
        self.working_dir = "data"+path_seg+"Data"+path_seg+"Foxi"+path_seg

        if enable_FoxNhe:
            with open(self.working_dir+"website.txt") as file:
                self.pageurl = file.readline().rstrip()

            with open(self.working_dir+"data.json") as jsonfile:
                self.data = json.load(jsonfile)

    def readJson(self):
        with open(self.working_dir+"website.txt") as file:
            self.pageurl = file.readline().rstrip()
        with open(self.working_dir+"data.json") as jsonfile:
            self.data = json.load(jsonfile)

    def writeJson(self):
        with open(self.working_dir+"data.json", "w") as jsonfile:
            json.dump(self.data, jsonfile, indent=4, sort_keys=True)

    def open_fox(self):
        if not enable_FoxNhe:
            self.readJson()
        self.browser.refresh()
        self.browser.open_win(self.data["Last"]["last_name_url"])
        if self.browser.running:
            time.sleep(4)
        else:
            time.sleep(8)
        self.browser.open_tab(self.data["Last"]["last_page_url"])

    def open_foxname(self):
        if not enable_FoxNhe:
            self.readJson()
        self.browser.open_win(self.data["Last"]["last_name_url"])

    def open_foxpage(self):
        if not enable_FoxNhe:
            self.readJson()
        self.browser.open_win(self.data["Last"]["last_page_url"])

    def fap(self, opentype="fox"):
        if not enable_FoxNhe:
            self.readJson()
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
        print("Do not forget to add 'www.googletagmanager.com' in Pi-Hole or disable it!")
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

            print("Everything for Next, Finish (FIN)")

            user_input = input()

            thistime_read += 1

            if user_input.lower() == "fin":
                break

        thistime_timeC.stop()

        cls()
        print("End Hanga: (Name)")
        hangaend_name = input()

        print("End Hanga: (URL)")
        hangaend_url = input()

        print("End Page: ")
        pageend = int(input())

        pageend_url = self.pageurl + str(pageend)+ "/"
        pageprogress = pagestart - pageend


        idend = int(hangaend_url.split("/")[-2])
        idprogress = idend - idstart
        skipped = idprogress - thistime_read
        startname = self.data["Last"]["last_name"]
        starturl = self.data["Last"]["last_name_url"]

        self.data["Stats"] = {"fapped": self.data["Stats"]["fapped"] + 1,
                              "all_pages": self.data["Stats"]["all_pages"] + pageprogress,
                              "all_hangas": self.data["Stats"]["all_hangas"] + thistime_read}

        self.data["Last"] = {"last_page": pageend, "last_page_url": pageend_url,
                             "last_name": hangaend_name, "last_name_url": hangaend_url}

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
                                                            "start_Hanga": {
                                                                "page": pagestart,
                                                                "name": startname,
                                                                "id": idstart,
                                                                "url": starturl
                                                            },
                                                            "end_Hanga": {
                                                                "page": pageend,
                                                                "name": hangaend_name,
                                                                "id": idend,
                                                                "url": hangaend_url
                                                            }
                                                            }}

        self.writeJson()
        print("Finished")
        time.sleep(0.85)


Foxi = FoxiC()



title("Loading Arguments")





def debug():
    cls()
    print("DEBUGGING")
    while True:
        exec(input())



def Music(load=None, systrayon=True, balloonTip=True, killMeAfterEnd=True):

    def Play():
        title("Musicplayer")
        class Printerr(threading.Thread):
            def __init__(self, refreshtime=1):
                super().__init__()
                self.started = False
                self.refreshTime = refreshtime
            def run(self):
                self.started = True
                while not muPlayer.allowPrint:
                    time.sleep(0.5)
                while muPlayer.musicrun and muPlayer.allowPrint:
                    time.sleep(self.refreshTime)
                    if muPlayer.last_print_auto + self.refreshTime > time.time():
                        continue
                    muPlayer.printit()
                    muPlayer.refreshTitle()
                    while muPlayer.paused or not muPlayer.autorefresh:
                        time.sleep(1)


        Printer = Printerr()
        Printer.start()

        muPlayer.join()

        #while True:
        #    print(muPlayer.allowPrint, muPlayer.musicrun, muPlayer.paused)
        #    time.sleep(0.5)

        #while muPlayer.musicrun:
        #    user_input = input()
        #    muPlayer.input(user_input)


    muPlayer = MusicPlayerC(systray=systrayon, balloonTip=balloonTip, random=musicrandom, killMeAfterEnd=killMeAfterEnd)
    muPlayer.read_musiclist()

    if not load:
        music_playlists_print = ""
        for x, y in zip(muPlayer.musiclist["names"], muPlayer.musiclist["keys"]):
            music_playlists_print += x.title() + " (" + y.upper() + "), "
        music_playlists_print = music_playlists_print.rstrip(", ")


        music_multiplaylists_print = ""
        for x, y in zip(muPlayer.multiplaylists["names"], muPlayer.multiplaylists["keys"]):
            music_multiplaylists_print += x.title() + " (" + y.upper() + "), "
        music_multiplaylists_print = music_multiplaylists_print.rstrip(", ")


        cls()
        print("Playlists:")
        print("\nFix Playlists:")
        print(music_playlists_print)
        print("\nCustom:")
        print("User's Playlist (US), User defined (UD), Multiple PL (MPL), All (ALL)\n")
        print("MultiPL:")
        print(music_multiplaylists_print)
        music_user_input = input("\n")
    else:
        music_user_input = ""
        muPlayer.addMusic(load)

    """
    if music_user_input.lower() == "mix":
        muPlayer.addMusic("an")
        muPlayer.addMusic("phu")
        muPlayer.addMusic("cp")
        muPlayer.addMusic("es")
        muPlayer.addMusic("jpop")
        muPlayer.addMusic("mixx")
        muPlayer.addMusic("und")
        muPlayer.addMusic("del")

    elif music_user_input.lower() == "j":
        muPlayer.addMusic("an")
        muPlayer.addMusic("jpop")
    """

    if music_user_input.lower() == "all":
        for x in muPlayer.musiclist["keys"]:
            muPlayer.addMusic(x)

    elif music_user_input.lower() == "mpl":
        musicman_search = True

        muPlayer.musiclist["names"].append("User's List")

        musicman_list = []
        music_playlists_used = {}

        for x in muPlayer.musiclist["keys"]:
            music_playlists_used[x] = " "

        while musicman_search:
            music_playlists_used_List = []
            for x in muPlayer.musiclist["keys"]:
                music_playlists_used_List.append(music_playlists_used[x])
            cls()
            print("Playlists:\n")
            #print(music_playlists_print)
            #print("User's list (US), User defined (UD)")
            #print("\nLoaded:")
            for xl, x2, x3 in zip(music_playlists_used_List, muPlayer.musiclist["names"], muPlayer.musiclist["keys"]):
                print(" " + xl + " " + x2 + " (" + x3.upper() + ")")
            for x in musicman_list:
                print(" X " + x)
            print("\nFinish (FIN)\n")

            musicman_user_input = input()

            if musicman_user_input.lower() == "fin":
                musicman_search = False
            elif not Search(musicman_user_input, muPlayer.musiclist["keys"], exact=True):
                continue

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


    elif music_user_input.lower() == "search":
        muPlayer.addMusic("all")

        cls()
        print("What do you want to hear?")

        user_input_search = input().lower()

        all_music = []
        all_dir = []

        for x in range(1, muPlayer.music["all_files"] + 1):
            all_music.append(muPlayer.music["file" + str(x)]["name"])
        for x in range(1, muPlayer.music["all_dirs"] + 1):
            all_dir.append(muPlayer.music["dir" + str(x)]["file"])

        found_music = Search(user_input_search, all_music)
        found_dir = Search(user_input_search, all_dir)

        for x in found_music:
            muPlayer.playlist.append("file" + str(x + 1))

        def funcx(dirID):
            for x in muPlayer.music["dir" + str(dirID)]["content"]:
                if lsame(x, "dir"):
                    funcx(int(x.lstrip("dir"))) # weitergabe: XX
                else:
                    doit = True
                    for file in muPlayer.playlist:
                        if file == x:
                            doit = False
                            break

                    if doit:
                        muPlayer.playlist.append(x)

        for x in found_dir:
            funcx(x + 1)  # weitergabe: int XX + 1

        # ist etwas doppeltes in der PL ?

        oldPL1 = muPlayer.playlist.copy()
        oldPL2 = muPlayer.playlist.copy()

        for x in range(len(oldPL1)):
            for y in oldPL2:
                found = 0
                if oldPL1[x] == y and found == 0:
                    found += 1
                elif oldPL1[x] == y and found > 0:
                    del oldPL2[x]

        muPlayer.playlist = oldPL2.copy()


    else:
        muPlayer.addMusic(music_user_input.lower())

    if muPlayer.music["active"]:
        muPlayer.start()
        Play()
    else:
        print("No track found")

    normaltitle()




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
                Music(systrayon=False, balloonTip=False, killMeAfterEnd=True)
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
        def __init__(self):
            super().__init__()
            self.started = False
        def run(self):
            self.started = True
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

def Alarm():
    cls()
    hr = int(input("Hour:\n"))
    mi = int(input("\nMinute:\n"))
    sec = int(input("\nSecond:\n"))
    Timerprint(hr,mi,sec)
    Alarmprint(colorCh=True)






#MusicPlayerTest = MusicPlayerC()

def Splatoon():
    spl = SplatoonC()

    class Printerr(threading.Thread):
        def __init__(self):
            super().__init__()
            self.started = False
        def run(self):
            self.started = True
            while spl.RUN:
                cls()
                spl.printit()
                time.sleep(1)

    Printer = Printerr()
    Printer.start()

    while spl.RUN:
        user_input = input()
        spl.input(user_input)



def Timer():
    """
        Function Timer:
        is a user interface with use of the TimerC
    """
    class TimePrinter(threading.Thread):
        def __init__(self):
            super().__init__()
            self.Running = False
            self.t = TimerC()
        def run(self):
            self.Running = True
            self.t.start()
            while self.Running:
                time.sleep(0.8)
                os.system("cls")
                print("Running:")
                print(self.t.getTimeFor())
        def stop(self):
            self.Running = False
            self.t.stop()
            os.system("cls")
            print("Stopped:")
            print(self.t.getTimeFor())
            input()

    p = TimePrinter()

    print("Start?")
    input()
    p.start()
    input()
    p.stop()


def startStartupServer(serverport: int, ballonTIP=True):
    global StartupServer
    global StartupServerJava
    StartupServer = Server(ip=thisIP, port=serverport, react=StartupServerTasks)
    StartupServerJava = ServerJava(ip=thisIP, port=serverport + 2, react=StartupServerTasksJava, allowPrint=True, sendIP=False, giveJava=False)
    print("JAVA-SERVER port: " + str(StartupServerJava.port))
    print("Server initialized!\nNow Running Systray")

    def quitFunc(x):
        StartupServer.exit()
        StartupServerJava.stop()
    def switchEP(x):
        Tools.EnergyPlan.Switch()
        msg = "Änderte EP zu: " + Tools.EnergyPlan.cEP
        print(msg)
        if ballonTIP:
            Tools.EnergyPlan.getEP(False)
            balloon_tip("Evecon: StartupServer", msg)
    def setEP_energysaver(x):
        Tools.EnergyPlan.Change(1)
        msg = "Änderte EP zu: Stromsparen"
        print(msg)
        if ballonTIP:
            Tools.EnergyPlan.getEP(False)
            balloon_tip("Evecon: StartupServer", msg)
    def setEP_fastmode(x):
        Tools.EnergyPlan.Change(0)
        msg = "Änderte EP zu: Ausbalanciert"
        print(msg)
        if ballonTIP:
            Tools.EnergyPlan.getEP(False)
            balloon_tip("Evecon: StartupServer", msg)
    def switchSS(x):
        print("HI")
        Tools.ScreenSaverSettings.switchStatus()
        if Tools.ScreenSaverSettings.status:
            msg = "Schaltete SreenSaver: AN"
        else:
            msg = "Schaltete SreenSaver: AUS"
        print(msg)
        if ballonTIP:
            Tools.EnergyPlan.getEP(False)
            balloon_tip("Evecon: StartupServer", msg)
    def switchKlakumLight(x):
        balloon_tip("OK", "HIER")
        """
        TODO: HIER WEGMACHEN WENN LAMPE AN
        Klakum.connect()
        Klakum.relays[4].switch()
        Klakum.disconnect()
        if ballonTIP:
            Tools.EnergyPlan.getEP(False)
            if Klakum.relay[4].value == 1:
                msg =  "Schaltete die Lampe: AN"
            else:
                msg = "Schaltete die Lampe: AUS"
            balloon_tip("Evecon: StartupServer", msg)
        """
    def shutdown(x):
        Tools.shutdown()
        if ballonTIP:
            Tools.EnergyPlan.getEP(False)
            balloon_tip("Evecon: StartupServer", "Fahre herrunter")

    sub_menu1 = {"Ausbalanciert": setEP_fastmode, "Energiesparen": setEP_energysaver}
    main_menu = {"SS wechseln": switchSS, "EP wechseln": switchEP, "Schreibtischlicht wechseln": switchKlakumLight, "Herrunterfahren": shutdown}
    sysTray = SysTray("data"+path_seg+"ico"+path_seg+"PC.ico", "Evecon: StartupServer",
                      main_menu, sub_menu1=sub_menu1, sub_menu_name1="EPs", quitFunc=quitFunc)

    sysTray.start()

    StartupServer.start()
    StartupServerJava.start()
    StartupServer.join()
    StartupServerJava.join()



def main():
    versionFind()

    title("Waiting for Input", something="Logport: " + str(logServer.port))

    cls()

    print("Evecon")
    print("PC: " + Computername)

    print("\nMenu:")

    print("\nFuntions:")
    print("Musicplayer (MUSIC), Radio (RADIO), Foxi (FOX)")
    print("Time (TIME), Timer (TIMER), Alarm (ALARM)")

    print("\nSettings:")
    print("Light (L)")

    print("\nDev:")
    print("Debug (DEBUG), Status (STATUS)")


    user_input = input("\n\n")

    if user_input.lower() == "fap":
        if foxORnhe == "foxi":
            Foxi.fap()
        elif foxORnhe == "nhee":
            Nhee.fap()
    elif user_input.lower() == "foxpage":
        Foxi.open_foxpage()
    elif user_input.lower() == "foxname":
        Foxi.open_foxname()
    elif user_input.lower() == "nhee" or user_input.lower() == "nhe":
        Nhee.fap()
    elif user_input.lower() == "nheepage":
        Nhee.open_foxpage()
    elif user_input.lower() == "nheename":
        Nhee.open_foxname()
    elif user_input.lower() == "l":
        color.Man()
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
    #elif user_input.lower() == "pw":
    #    passwordmanager()
    elif user_input.lower() == "radio":
        Radio()
    elif user_input.lower() == "alarm":
        Alarm()
    elif user_input.lower() == "status":
        Status()
    elif user_input.lower() == "timer":
        Timer()


def Arg():

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
        if sys.argv[x] == "--l_dark":
            title("Load Argument", "Argument: Dark")
            color.change("07")
        if sys.argv[x] == "--l_bright":
            title("Load Argument", "Argument: Bright")
            color.change("F0")

        if sys.argv[x] == "-fap":
            title("Load Argument", "Foxi")
            ttime.deac()
            if foxORnhe == "foxi":
                Foxi.fap()
            elif foxORnhe == "nhee":
                Nhee.fap()
            exit_now()

        if sys.argv[x] == "--foxi" or sys.argv[x] == "-fap":
            title("Load Argument", "Foxi")
            ttime.deac()
            Foxi.fap()
            exit_now()
        if sys.argv[x] == "--foxi_page":
            title("Load Argument", "Notie: FOXPAGE")
            ttime.deac()
            Foxi.open_foxpage()
            exit_now()
        if sys.argv[x] == "--foxi_name":
            title("Load Argument", "Notie: FOXNAME")
            ttime.deac()
            Foxi.open_foxname()
            exit_now()
        if sys.argv[x] == "--nhee":
            title("Load Argument", "Nhee")
            ttime.deac()
            Nhee.fap()
            exit_now()
        if sys.argv[x] == "--nhee_page":
            title("Load Argument", "Nhee: NHEEPAGE")
            ttime.deac()
            Nhee.open_nheepage()
            exit_now()
        if sys.argv[x] == "--nhee_name":
            title("Load Argument", "Nhee: NHEENAME")
            ttime.deac()
            Nhee.open_nheename()
            exit_now()

        if sys.argv[x] == "--nc_stdsize":
            title("Load Argument", "Nircmd: Standard size")
            nircmd("setsize", 1000, 520)
        if sys.argv[x] == "--tt_freq":
            title("Load Argument", "TTime: Change Freq")
            title_time.freq = float(sys.argv[x + 1])
        if sys.argv[x] == "--tt_deac":
            title("Load Argument", "TTime: Deactivate")
            ttime.deac()
            # if sys.argv[x] == "-update":
            #    title("Load Argument", "Updater: Updating")
            #    update()
        #if sys.argv[x] == "--upgrade":
        #    title("Load Argument", "Updater: Upgrading")
        #    upgrade()
        if sys.argv[x] == "--screensaver":
            title("Load Argument", "Screensaver")
            screensaver()
            exit_now()
        if sys.argv[x] == "--ep_switch":
            title("Load Argument", "Switch Energy Plan")
            ttime.deac()
            Tools.EnergyPlan.Switch()
            Tools.EnergyPlan.getEP(True)
            time.sleep(2)
            exit_now()
        if sys.argv[x] == "--shutdown":
            title("Load Argument", "Shutdown")
            ttime.deac()
            Tools.Shutdown()
            exit_now()
        if sys.argv[x] == "--reboot":
            title("Load Argument", "Reboot")
            ttime.deac()
            Tools.Reboot()
            exit_now()
        if sys.argv[x] == "--start_server":
            title("Server", " ", " ")
            ttime.deac()
            serverport = int(sys.argv[x + 1])
            if not sys.argv[x + 2] == "app":
                killConsoleWin()
            startStartupServer(serverport)
            exit_now()
        if sys.argv[x] == "--inter_client":
            title("Interactive Client", " ", " ")
            ttime.deac()
            host = sys.argv[x + 1]
            port = int(sys.argv[x + 2])
            InteractiveClient(host, port)
            exit_now()
        if sys.argv[x] == "--music":
            title("Load Argument", "Musicplayer")
            if len(sys.argv) > x + 1:
                Music(sys.argv[x + 1])
            else:
                Music()
            exit_now()
        if sys.argv[x] == "--radio":
            title("Load Argument", "Radio")
            Radio()
            exit_now()
        if sys.argv[x] == "--Klakum_switch_light":
            title("Load Argument", "Switch Light", "Klakum")
            Klakum.connect()
            Klakum.relays[4].switch()
            Klakum.disconnect()
            exit_now()


def debug_startup():
    """
    def x(x):
        print(x.encode())

    s = Scanner(x, True)
    s.start()
    s.join()
    """

    """
    myList = []

    for x in range(15):
        myList.append(randompw(True, printpw=False))

    done = True

    def hi(i):
        nonlocal done
        print(i)
        if i == "return":
            done = False

    f = Findus(workList=myList, reactUser=hi, onlyReturn=True, autoPrint=False, autoSearch=True, autoSort=True, afterPrint=True, suffix="LOL", prefix="HI")
    f.setPrefix("NICE", f.workList[0])
    f.start()

    while done:
        time.sleep(0.6)

    cls()
    print("You chose: " + f.workList[f.curPos])

    input()
    """

if exitnow == 0:
    if __name__ == "__main__":
        if sys.argv:
            Arg()
        title("Search for Updates")
        #update()
        title("Start Enviroment")
        debug_startup()
        main()
        time.sleep(0)

        exit_now()
