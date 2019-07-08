
class MusicPlayerRemote:

    """
    DATEN ÜBERTRAGUNG

    import pickle
    pickle.dumps({'foo': 'bar'})
    pickle.loads()
    {'foo': 'bar'}

    """

    def __init__(self, ip="127.0.0.1", port=0, showLog=False):
        """
        :type ip: str
        :param ip: the IP of the Musicplayer

        :type port: int
        :param port: the IP of the Musicplayer

        standart: searching on the current pc
        """

        if not port:
            globalMPports.readFile()
            if globalMPports.ports:
                port = globalMPports.ports[0]

        self.cl = Client(ip=ip, port=port, react=self.react, printLog=showLog)

        self.recieved = False

        # DATA VARS NO TOUCHING

        self._title = "" # Cur title
        self._time = 0.0 # Cur time
        self._duration = 0.0 # Duration of cur title
        self._vol = 0.0 # Volume (Windows)
        self._volp = 0.0 # Volume (Player)

        # TEMPORARY
        self._file = "" # a tmp file str from the last requested id

        self._playlistLen = 0
        self._playlist = []

    # control

    def stop(self):
        """
        stops the remote control

        :rtype: bool
        :return: succsess
        """

    def start(self):
        """
        starts the connection

        :rtype: bool
        :return: succsess
        """

    def react(self, dataRaw):
        """
        reacts to the data sent from the server

        :param dataRaw: data
        :type dataRaw: str
        """

        data = dataRaw.split("_")

        if data[0] == "get":
            if data[1] == "title":
                self._title = data[2]
            elif data[1] == "time":
                self._time = data[2]
            elif data[1] == "duration":
                self._duration = data[2]
            elif data[1] == "vol":
                self._vol = data[2]
            elif data[1] == "volp":
                self._volp = data[2]
            elif data[1] == "file":
                self._file = data[2]
            elif data[1] == "playlistlen":
                self._playlistLen = data[2]
            else:
                return

            self.recieved = True

    def get(self, var, wait=True):
        """
        do the waiting and recieving the info

        :param var: the data for waiting
        :type var: str
        :param wait: wait till reci?
        :type wait: bool
        """

        self.recieved = False
        self.cl.send("get_" + var)
        while not self.recieved and wait:
            time.sleep(0.1)


    # GET

    # GET (Interface)
    def getTitle(self):
        """
        :rtype: str
        :return: returns the title
        """
        self.get("title")
        return self._title
    title = property(getTitle)

    def getTime(self):
        """
        :rtype: float
        :return: the time (current playtime) in sec
        """
        self.get("time")
        return self._time
    time = property(getTime)

    def getDuration(self):
        """
        :rtype: float
        :return: the time (current playtime) in sec
        """
        self.get("duration")
        return self._duration
    duration = property(getDuration)

    def getVol(self):
        """
        :rtype: float
        :return: the cur windows vol
        """
        self.get("vol")
        return self._vol
    vol = property(getVol)

    def getVolp(self):
        """
        :rtype: float
        :return: the cur player vol
        """
        self.get("volp")
        return self._volp
    volp = property(getVolp)

    # GET (Programming)
    def getFileById(self, num):
        """
        :param num: the id of the playlist position
        :type num: int

        :return: the fileID of the playlist postion
        :rtype: str
        """
        self.get("file")
        return self._file

    def getPlaylistLen(self):
        """
        :return: length of playlist
        :rtype: int
        """
        self.get("playlistlen")
        return self._playlistLen

    def getPlaylist(self):
        """
        :return: the playlist
        :rtype: list
        """

        plLen = self.getPlaylistLen()
        self._playlist = []
        for x in range(plLen):
            self._playlist.append(self.getFileById(x))

        return self._playlist
    playlist = property(getPlaylist)

    def getMusicNameByFile(self, file):
        pass
    def getMusicFileByFile(self, file):
        pass
    def getMusicPathByFile(self, file):
        pass
    def getMusicFullnameByFile(self, file):
        pass



    # SET

    # SET (Player)

    def setPlayingStatus(self, status=2):
        pass
    def setMuteStatus(self, status=2):
        pass


    def playNext(self):
        pass
    def delById(self, num):
        pass
    def delByFile(self, file):
        pass

    def queueById(self):
        pass
    def queueByFile(self):
        pass



    def setVol(self, vol):
        pass
    def setVolp(self, vol):
        pass


    def stopPlayer(self):
        pass

    # SET (Programming)

    def addMusic(self):
        pass
    def setPlaying(self, file):
        pass
    def makePlaylist(self):
        pass

    def printRemote(self):
        pass
    def printHeadRemote(self):
        pass
    def printBodyRemote(self):
        pass
    def printFootRemote(self):
        pass


    def directReact(self, i):
        pass
    def directInput(self, i):
        pass


# noinspection PyTypeChecker
class MusicPlayerBetterRemoteControl(threading.Thread):
    def __init__(self, systray=True, random=True, expandRange=2, stop_del=False, scanner_active=True, balloonTip=True,
                 killMeAfterEnd=True, remote=True, remotePort=4554, selfprint=False):
        super().__init__()

        self.debug = False

        self.music = {"all_files": 0, "all_dirs": 0, "active": []}
        self.find_music_out = {}

        self.systray = None
        self.systrayon = systray
        self.balloonTip = balloonTip
        self.killMeAfterEnd = killMeAfterEnd
        self.remote = True
        self.remotePort = remotePort
        self.selfprint = selfprint

        self.volume = Volume.getVolume()
        self.volumep = 0.5

        # stop the musicplayer while hovering over file 1 and pressing 'del'-button
        self.stop_del = stop_del
        self.randomizer = random
        self.scanner_active = scanner_active
        # noinspection PyGlobalUndefined
        global musicrun
        musicrun = True

        self.starttime = 0
        self.hardworktime = 0
        self.musicrun = True
        self.playlist = []
        self.pershuffel = False

        self.running = False
        self.playing = False
        self.exitn = False
        self.allowPrint = False
        self.autorefresh = True

        self.player = pyglet.media.Player()
        self.timer = TimerC()
        self.scanner = Scanner(self.react)
        self.spl = SplatoonC()

        self.skip_del = False
        self.paused = False
        self.pause_type = ""
        self.muted = False
        self.mute_vol = 1
        self.con_main = "pl"
        self.con_main_last = None
        self.con_cont = "set"
        self.change = ""

        self.last_print = 0
        self.last_print_auto = 0

        self.cur_Input = ""
        self.cur_Pos = 0
        self.expandRange = expandRange

        self.searching = False
        self.searchlist = []
        self.cur_Search = ""

        self.notifications = []

        self.tmp_pl_input_1 = []
        self.tmp_pl_input_2 = []
        self.tmp_pl_output_1 = []
        self.tmp_pl_output_2 = []

        self.musiclist = {"names": []}
        self.multiplaylists = {}
        self.genre = []
        self.musicDir = ""



    def addMusic(self, key, cusPath=False, genre=False, noList=False, printStaMSG=True, printEndMSG=True,
                 makeNoti=False):  # key (AN, LIS)

        """
        adds music

        :param key: the key of the id (normal id, mpl id)
        :param cusPath: defines the path for a custom path (ignores the key)
        :param genre: forces a genre input (?)
        :param noList: only allows key to be a normal id
        :param printStaMSG: clears the screen and prints the start msg
        :param printEndMSG: prints the finished msg
        :param makeNoti: make a notification after finishing
        :return: success
        """

    def resetInterface(self):
        """
        resets interface
        :return:
        """

    def make_playlist(self):
        """
        makes the playlist

        :return:
        """

    def shufflePL(self, first=False):
        """
        reroll everthing

        :param first: also the current playing
        :return:
        """

    def refresh(self, title=False, printme=True):
        """
        refresh the following
        :param title:
        :param printme:
        :return:
        """

    def showBalloonTip(self):
        """
        do we need it?
        :return:
        """

    def rerollThis(self):
        """
        reroll the current position (stream/control)

        :return:
        """

    def sortPL(self):
        """
        sorts the PL
        :return:
        """

    def sortPL_name(self):
        """
        sorts the pl by name
        :return:
        """
    def sortPL_an(self):
        """
        sorts the PL by an
        :return:
        """
    # Options

    def play(self):
        """
        play
        :return:
        """

    def pause(self):
        """
        pause
        :return:
        """

    def switch(self):
        if self.paused:
            self.play()
        else:
            self.pause()

    def switchmute(self):
        if self.muted:
            self.unmute()
        else:
            self.mute()

    def mute(self):
        """
        mutes the player
        :return:
        """

    def unmute(self):
        """
        unmutes the player
        :return:
        """

    def stop(self):
        """
        stops the REMOTE player
        :return:
        """

    def next(self, skipthis=False):
        """
        play the next

        :param skipthis: ?
        :return:
        """

    def DelById(self, num):
        """
        del the file by id

        :param num:
        :return:
        """

    def DelByFile(self, plfile):
        """
        del the file by file name
        :param plfile:
        :return:
        """

    def vol(self, vol):
        """
        changes the windows volume
        :param vol:
        :return:
        """

    def volp(self, vol):
        """
        changes the player volume
        :param vol:
        :return:
        """

    def queueById(self, pos):
        """
        queue the track by pos (?)
        :param pos:
        :return:
        """

    def queueByFile(self, plfile):
        """
        queue the track by file-name
        :param plfile:
        :return:
        """

    def refreshSearch(self):
        """
        refresh the search (CLIENT)
        TODO remake from org server code
        :return:
        """

        self.cur_Pos = 0

        if self.cur_Search != "":
            namelist = []

            for x in self.playlist:
                namelist.append(self.music[x]["name"])

            found = Search(self.cur_Search, namelist)

            searchlist_name = []
            for x in found:
                searchlist_name.append(namelist[x])

            searchlist_name.sort()

            music_dir = self.music.copy()

        else:
            searchlist_name = []
            for fileX in self.playlist:
                searchlist_name.append(self.music[fileX]["name"])
            searchlist_name.sort()

        self.tmp_pl_input_1 = []
        self.tmp_pl_input_2 = []
        for name in searchlist_name:
            if len(searchlist_name) / 2 > len(self.tmp_pl_input_1):
                self.tmp_pl_input_1.append(name)
            else:
                self.tmp_pl_input_2.append(name)


        def work1():
            music_dir = self.music.copy()

            new_playlist = []
            for name in self.tmp_pl_input_1:
                for num_file in range(1, music_dir["all_files"] + 1):
                    try:
                        if name == music_dir["file" + str(num_file)]["name"]:
                            new_playlist.append("file" + str(num_file))
                            del music_dir["file" + str(num_file)]
                            break
                    except KeyError:
                        pass
            self.tmp_pl_output_1 = new_playlist

        def work2():
            music_dir = self.music.copy()

            new_playlist = []
            for name in self.tmp_pl_input_2:
                for num_file in range(1, music_dir["all_files"] + 1):
                    try:
                        if name == music_dir["file" + str(num_file)]["name"]:
                            new_playlist.append("file" + str(num_file))
                            del music_dir["file" + str(num_file)]
                            break
                    except KeyError:
                        pass
            self.tmp_pl_output_2 = new_playlist

        t1 = threading.Thread(target=work1)
        t2 = threading.Thread(target=work2)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        new_playlist = self.tmp_pl_output_1 + self.tmp_pl_output_2

        self.searchlist = new_playlist.copy()

    def run(self):
        """
        starts the connection
        :return:
        """

    def notificate(self, msg, title=None, screentime=5, maxTime=None):
        """
        make a notification
        :param msg:
        :param title:
        :param screentime:
        :param maxTime:
        :return:
        """

    def return_head_info(self):
        """
        returns the head info (CLIENT)
        :return:
        """
        # Info-Container

        outputList = ["Musicplayer: \n"]

        if self.getCur()["antype"]:
            outputList.append(
                "Playing: \n%s \nFrom %s" % (self.getCur()["andata"]["title"], self.getCur()["andata"]["animeName"]))
        else:
            outputList.append("Playing: \n%s" % self.getCur()["name"])

            outputList.append("Time: %s\\%s" % (self.timer.getTimeFor(), TimeFor(self.getCur()["loaded"].duration)))
        if self.muted:
            # output.append(int((console_data["pixx"]/2)-3)*"|"+"Muted"+int((console_data["pixx"]/2)-2)*"|")
            l1 = ""
            l2 = ""
            pre = ""
            outputList.append(
                pre + int((console_data["pixx"] / 2) - 3) * l1 + "Muted" + int((console_data["pixx"] / 2) - 2) * l2)

        return outputList

    def return_head_noti(self):
        """
        returns the head noti (CLIENT)
        :return:
        """
        # notification

        outputList = []

        oldNoti = self.notifications.copy()
        delMSG = []
        delNOT = []
        titleUsed = False

        def workAmsg(msgID):
            nonlocal titleUsed
            if oldNoti[notiID]["msgs"][msgID]["starttime"] + oldNoti[notiID]["msgs"][msgID][
                "screentime"] < time.time():  # invalid msg time
                delMSG.append((notiID, msgID))
            else:
                if oldNoti[notiID]["title"] and not titleUsed:
                    titleUsed = True
                    outputList.append(oldNoti[notiID]["title"] + ":")
                outputList.append(oldNoti[notiID]["msgs"][msgID]["msg"])

        def workANote(notiID):
            nonlocal titleUsed
            if oldNoti[notiID]["maxTime"]:
                if time.time() > oldNoti[notiID]["maxTime"] + oldNoti[notiID]["maxTimestart"]:  # invalid: MAXTIME
                    delNOT.append(notiID)
            else:
                titleUsed = False
                # if len(oldNoti[notiID]["msgs"]) == 1:
                #    workAmsg(0)
                for msgID in range(0, len(oldNoti[notiID]["msgs"])):
                    workAmsg(msgID)

                if len(oldNoti[notiID]["msgs"]) == 0:
                    delNOT.append(notiID)

        # if len(oldNoti) == 0:
        #    workANote(0)
        for notiID in range(0, len(oldNoti)):
            workANote(notiID)

        for x in range(-1, -len(delMSG) - 1, -1):
            del self.notifications[delMSG[x][0]]["msgs"][delMSG[x][1]]
        for x in range(-1, -len(delNOT) - 1, -1):
            del self.notifications[delNOT[x]]

        return outputList

    def print_head_info(self):
        for line in self.return_head_info():
            print(line)

    def print_head_noti(self):
        for line in self.return_head_noti():
            print(line)

    def print_head(self):
        # Info-Container

        self.print_head_info()

        if self.return_head_noti():
            print("\n" + console_data["pixx"] * "-" + "\n")
            self.print_head_noti()

        # sys.stdout.write(console_data[0]*"-")

    def return_body(self):
        """
        returns the body (CLIENT)
        :return:
        """
        outputList = []

        # Main-Container

        if self.con_main == "pl":
            outputList.append("Playlist: (%s)\n" % str(len(self.playlist)))

            search_done = False
            for now in range(self.expandRange):
                if not search_done:
                    if self.cur_Pos == now:
                        if self.expandRange >= len(self.playlist) - 1:
                            for word_num in range(0, len(self.playlist)):
                                if word_num + 1 < 10:
                                    word_num_str = str(word_num + 1) + "  "
                                elif word_num + 1 < 100:
                                    word_num_str = str(word_num + 1) + " "
                                else:
                                    word_num_str = str(word_num + 1)

                                if self.cur_Pos == word_num:
                                    if not self.debug:
                                        if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                            outputList.append(" " + word_num_str + " * " + getPartStr(
                                                self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                                        else:
                                            outputList.append(
                                                " " + word_num_str + " * " + self.music[self.playlist[word_num]][
                                                    "name"])
                                    else:
                                        outputList.append(
                                            " " + word_num_str + " * " + self.music[self.playlist[word_num]][
                                                "name"] + "0" +
                                            self.playlist[word_num])
                                else:
                                    if not self.debug:
                                        if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                            outputList.append(" " + word_num_str + "   " + getPartStr(
                                                self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                                        else:
                                            outputList.append(
                                                " " + word_num_str + "   " + self.music[self.playlist[word_num]][
                                                    "name"])
                                    else:
                                        outputList.append(
                                            " " + word_num_str + "   " + self.music[self.playlist[word_num]][
                                                "name"] + "1" +
                                            self.playlist[word_num])
                        elif 2 * self.expandRange + 1 >= len(self.playlist):
                            for word_num in range(0, 2 * self.expandRange + 1):  # + 1?
                                if word_num + 1 < 10:
                                    word_num_str = str(word_num + 1) + "  "
                                elif word_num + 1 < 100:
                                    word_num_str = str(word_num + 1) + " "
                                else:
                                    word_num_str = str(word_num + 1)

                                if self.cur_Pos == word_num:
                                    try:
                                        if not self.debug:
                                            if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                                outputList.append(" " + word_num_str + " * " + getPartStr(
                                                    self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                                            else:
                                                outputList.append(
                                                    " " + word_num_str + " * " + self.music[self.playlist[word_num]][
                                                        "name"])
                                        else:
                                            outputList.append(
                                                " " + word_num_str + " * " + self.music[self.playlist[word_num]][
                                                    "name"] + "2" + self.playlist[word_num])
                                    except IndexError:
                                        pass
                                else:
                                    try:
                                        if not self.debug:
                                            if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                                outputList.append(" " + word_num_str + "   " + getPartStr(
                                                    self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                                            else:
                                                outputList.append(
                                                    " " + word_num_str + "   " + self.music[self.playlist[word_num]][
                                                        "name"])
                                        else:
                                            outputList.append(
                                                " " + word_num_str + "   " + self.music[self.playlist[word_num]][
                                                    "name"] + "3" + self.playlist[word_num])
                                    except IndexError:
                                        pass
                        else:
                            for word_num in range(0, 2 * self.expandRange + 1):  # + 1? # Anfang
                                if word_num + 1 < 10:
                                    word_num_str = str(word_num + 1) + "  "
                                elif word_num + 1 < 100:
                                    word_num_str = str(word_num + 1) + " "
                                else:
                                    word_num_str = str(word_num + 1)
                                if self.cur_Pos == word_num:
                                    if not self.debug:
                                        if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                            outputList.append(" " + word_num_str + " * " + getPartStr(
                                                self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                                        else:
                                            outputList.append(
                                                " " + word_num_str + " * " + self.music[self.playlist[word_num]][
                                                    "name"])
                                    else:
                                        outputList.append(
                                            " " + word_num_str + " * " + self.music[self.playlist[word_num]][
                                                "name"] + "4" +
                                            self.playlist[word_num])
                                else:
                                    if not self.debug:
                                        if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                            outputList.append(" " + word_num_str + "   " + getPartStr(
                                                self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                                        else:
                                            outputList.append(
                                                " " + word_num_str + "   " + self.music[self.playlist[word_num]][
                                                    "name"])
                                    else:
                                        outputList.append(
                                            " " + word_num_str + "   " + self.music[self.playlist[word_num]][
                                                "name"] + "5" +
                                            self.playlist[word_num])
                        search_done = True
                        break

                    elif self.cur_Pos == len(self.playlist) - now - 1 and self.cur_Pos >= self.expandRange:  # Ende
                        for word_num in range(self.cur_Pos - self.expandRange - 2 + now, self.cur_Pos + 1 + now):
                            if word_num < 0:
                                continue
                            # outputList.append(word_num, self.curPos, now, self.expandRange)
                            if word_num + 1 < 10:
                                word_num_str = str(word_num + 1) + "  "
                            elif word_num + 1 < 100:
                                word_num_str = str(word_num + 1) + " "
                            else:
                                word_num_str = str(word_num + 1)
                            if self.cur_Pos == word_num:
                                if not self.debug:
                                    if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                        outputList.append(" " + word_num_str + " * " + getPartStr(
                                            self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                                    else:
                                        outputList.append(
                                            " " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"])
                                else:
                                    outputList.append(
                                        " " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"] + "6" +
                                        self.playlist[word_num])
                            else:
                                if not self.debug:
                                    if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                        outputList.append(" " + word_num_str + "   " + getPartStr(
                                            self.music[self.playlist[word_num]]["name"], 0, 108) + "...")
                                    else:
                                        outputList.append(
                                            " " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"])
                                else:
                                    outputList.append(
                                        " " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"] + "7" +
                                        self.playlist[word_num])
                        search_done = True
                        break

            if not search_done:  # Mitte
                for word_num in range(self.cur_Pos - self.expandRange, self.cur_Pos + self.expandRange + 1):
                    if word_num + 1 < 10:
                        word_num_str = str(word_num + 1) + "  "
                    elif word_num + 1 < 100:
                        word_num_str = str(word_num + 1) + " "
                    else:
                        word_num_str = str(word_num + 1)
                    if self.cur_Pos == word_num:
                        if not self.debug:
                            if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                outputList.append(
                                    " " + word_num_str + " * " + getPartStr(self.music[self.playlist[word_num]]["name"],
                                                                            0,
                                                                            108) + "...")
                            else:
                                outputList.append(
                                    " " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"])
                        else:
                            outputList.append(
                                " " + word_num_str + " * " + self.music[self.playlist[word_num]]["name"] + "10" +
                                self.playlist[word_num])
                    else:
                        if not self.debug:
                            if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                outputList.append(
                                    " " + word_num_str + "   " + getPartStr(self.music[self.playlist[word_num]]["name"],
                                                                            0,
                                                                            108) + "...")
                            else:
                                outputList.append(
                                    " " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"])
                        else:
                            outputList.append(
                                " " + word_num_str + "   " + self.music[self.playlist[word_num]]["name"] + "11" +
                                self.playlist[word_num])

        elif self.con_main == "details":
            outputList.append("Details:\n")
            outputList.append("Duration: " + str(TimeFor(self.music["file1"]["loaded"].duration)))

            if self.music[self.playlist[self.cur_Pos]]["antype"]:
                outputList.append("Title: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["title"]))
                outputList.append(
                    "Interpreter: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["interpreter"]))
                outputList.append("Musictype: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["musictype"]))
                outputList.append("Animename: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["animeName"]))
                outputList.append("Season: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["animeSeason"]))
                outputList.append("Type: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["animeType"]) +
                                  str(self.music[self.playlist[self.cur_Pos]]["andata"]["animeTypeNum"]))

            outputList.append("Filename: " + self.music[self.playlist[self.cur_Pos]]["name"])
            outputList.append("Album: " + self.music[self.playlist[self.cur_Pos]]["loaded"].info.album.decode())
            outputList.append("Author: " + self.music[self.playlist[self.cur_Pos]]["loaded"].info.author.decode())
            outputList.append("Comment: " + self.music[self.playlist[self.cur_Pos]]["loaded"].info.comment.decode())
            outputList.append("Copyright: " + self.music[self.playlist[self.cur_Pos]]["loaded"].info.copyright.decode())
            outputList.append("Genre: " + self.music[self.playlist[self.cur_Pos]]["loaded"].info.genre.decode())
            outputList.append("Title: " + self.music[self.playlist[self.cur_Pos]]["loaded"].info.title.decode())
            outputList.append("Track: " + str(self.music[self.playlist[self.cur_Pos]]["loaded"].info.track))
            outputList.append("Year: " + str(self.music[self.playlist[self.cur_Pos]]["loaded"].info.year))



        elif self.con_main == "info":
            outputList.append("Infos:\n")

            outputList.append("\nPlayer:\n")

            outputList.append("Vol: " + str(Volume.getVolume()))
            outputList.append("Volplayer: " + str(self.volumep))
            outputList.append("Muted: " + str(self.muted))
            outputList.append("Playing: " + str(self.playing))
            outputList.append("Paused: " + str(self.paused))
            outputList.append("Loaded-Key: " + str(self.music["active"]))

            if self.debug:
                outputList.append("\nDebugging Details:\n")

                outputList.append("Cur-Pos: " + str(self.cur_Pos))
                outputList.append("Autorefresh: " + str(self.autorefresh))

                outputList.append("File:\n")
                outputList.append("Filename: " + self.music[self.playlist[self.cur_Pos]]["file"])
                outputList.append("Path: " + self.music[self.playlist[self.cur_Pos]]["path"])

                outputList.append("\nOther:\n")

                outputList.append("Scanner-Status: " + str(self.scanner.is_alive()))
                outputList.append("Timer direct: " + str(self.timer.getTime()))
                outputList.append("Last print: " + str(self.last_print))



        elif self.con_main == "spl":
            outputList += self.spl.returnmain()
            # self.spl.printit(False)


        elif self.con_main == "search":
            # outputList.append(self.searchlist)
            outputList.append("Search: (%s)\n" % str(len(self.searchlist)))

            search_done = False
            for now in range(self.expandRange):
                if not search_done:
                    if self.cur_Pos == now:
                        if self.expandRange >= len(self.searchlist) - 1:
                            for word_num in range(0, len(self.searchlist)):
                                if word_num + 1 < 10:
                                    word_num_str = str(word_num + 1) + "  "
                                elif word_num + 1 < 100:
                                    word_num_str = str(word_num + 1) + " "
                                else:
                                    word_num_str = str(word_num + 1)

                                if self.cur_Pos == word_num:
                                    if not self.debug:
                                        if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                            outputList.append(" " + word_num_str + " * " + getPartStr(
                                                self.music[self.searchlist[word_num]]["name"], 0, 108) + "...")
                                        else:
                                            outputList.append(
                                                " " + word_num_str + " * " + self.music[self.searchlist[word_num]][
                                                    "name"])
                                    else:
                                        outputList.append(
                                            " " + word_num_str + " * " + self.music[self.searchlist[word_num]][
                                                "name"] + "0" + self.searchlist[word_num])
                                else:
                                    if not self.debug:
                                        if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                            outputList.append(" " + word_num_str + "   " + getPartStr(
                                                self.music[self.searchlist[word_num]]["name"], 0, 108) + "...")
                                        else:
                                            outputList.append(
                                                " " + word_num_str + "   " + self.music[self.searchlist[word_num]][
                                                    "name"])
                                    else:
                                        outputList.append(
                                            " " + word_num_str + "   " + self.music[self.searchlist[word_num]][
                                                "name"] + "1" + self.searchlist[word_num])
                        elif 2 * self.expandRange + 1 >= len(self.searchlist):
                            for word_num in range(0, 2 * self.expandRange + 1):  # + 1?
                                if word_num + 1 < 10:
                                    word_num_str = str(word_num + 1) + "  "
                                elif word_num + 1 < 100:
                                    word_num_str = str(word_num + 1) + " "
                                else:
                                    word_num_str = str(word_num + 1)

                                if self.cur_Pos == word_num:
                                    try:
                                        if not self.debug:
                                            if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                                outputList.append(" " + word_num_str + " * " + getPartStr(
                                                    self.music[self.searchlist[word_num]]["name"], 0, 108) + "...")
                                            else:
                                                outputList.append(
                                                    " " + word_num_str + " * " + self.music[self.searchlist[word_num]][
                                                        "name"])
                                        else:
                                            outputList.append(
                                                " " + word_num_str + " * " + self.music[self.searchlist[word_num]][
                                                    "name"] + "2" + self.searchlist[word_num])
                                    except IndexError:
                                        pass
                                else:
                                    try:
                                        if not self.debug:
                                            if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                                outputList.append(" " + word_num_str + "   " + getPartStr(
                                                    self.music[self.searchlist[word_num]]["name"], 0, 108) + "...")
                                            else:
                                                outputList.append(
                                                    " " + word_num_str + "   " + self.music[self.searchlist[word_num]][
                                                        "name"])
                                        else:
                                            outputList.append(
                                                " " + word_num_str + "   " + self.music[self.searchlist[word_num]][
                                                    "name"] + "3" + self.searchlist[word_num])
                                    except IndexError:
                                        pass
                        else:
                            for word_num in range(0, 2 * self.expandRange + 1):  # + 1? # Anfang
                                if word_num + 1 < 10:
                                    word_num_str = str(word_num + 1) + "  "
                                elif word_num + 1 < 100:
                                    word_num_str = str(word_num + 1) + " "
                                else:
                                    word_num_str = str(word_num + 1)
                                if self.cur_Pos == word_num:
                                    if not self.debug:
                                        if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                            outputList.append(" " + word_num_str + " * " + getPartStr(
                                                self.music[self.searchlist[word_num]]["name"], 0, 108) + "...")
                                        else:
                                            outputList.append(
                                                " " + word_num_str + " * " + self.music[self.searchlist[word_num]][
                                                    "name"])
                                    else:
                                        outputList.append(
                                            " " + word_num_str + " * " + self.music[self.searchlist[word_num]][
                                                "name"] + "4" + self.searchlist[word_num])
                                else:
                                    if not self.debug:
                                        if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                            outputList.append(" " + word_num_str + "   " + getPartStr(
                                                self.music[self.searchlist[word_num]]["name"], 0, 108) + "...")
                                        else:
                                            outputList.append(
                                                " " + word_num_str + "   " + self.music[self.searchlist[word_num]][
                                                    "name"])
                                    else:
                                        outputList.append(
                                            " " + word_num_str + "   " + self.music[self.searchlist[word_num]][
                                                "name"] + "5" + self.searchlist[word_num])
                        search_done = True
                        break

                    elif self.cur_Pos == len(self.searchlist) - now - 1 and self.cur_Pos >= self.expandRange:  # Ende
                        for word_num in range(self.cur_Pos - self.expandRange - 2 + now, self.cur_Pos + 1 + now):
                            if word_num < 0:
                                continue
                            # outputList.append(word_num, self.curPos, now, self.expandRange)
                            if word_num + 1 < 10:
                                word_num_str = str(word_num + 1) + "  "
                            elif word_num + 1 < 100:
                                word_num_str = str(word_num + 1) + " "
                            else:
                                word_num_str = str(word_num + 1)
                            if self.cur_Pos == word_num:
                                if not self.debug:
                                    if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                        outputList.append(" " + word_num_str + " * " + getPartStr(
                                            self.music[self.searchlist[word_num]]["name"], 0, 108) + "...")
                                    else:
                                        outputList.append(
                                            " " + word_num_str + " * " + self.music[self.searchlist[word_num]]["name"])
                                else:
                                    outputList.append(
                                        " " + word_num_str + " * " + self.music[self.searchlist[word_num]][
                                            "name"] + "6" + self.searchlist[word_num])
                            else:
                                if not self.debug:
                                    if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                        outputList.append(" " + word_num_str + "   " + getPartStr(
                                            self.music[self.searchlist[word_num]]["name"], 0, 108) + "...")
                                    else:
                                        outputList.append(
                                            " " + word_num_str + "   " + self.music[self.searchlist[word_num]]["name"])
                                else:
                                    outputList.append(
                                        " " + word_num_str + "   " + self.music[self.searchlist[word_num]][
                                            "name"] + "7" + self.searchlist[word_num])
                        search_done = True
                        break

            if not search_done:  # Mitte
                for word_num in range(self.cur_Pos - self.expandRange, self.cur_Pos + self.expandRange + 1):
                    if word_num + 1 < 10:
                        word_num_str = str(word_num + 1) + "  "
                    elif word_num + 1 < 100:
                        word_num_str = str(word_num + 1) + " "
                    else:
                        word_num_str = str(word_num + 1)
                    if self.cur_Pos == word_num:
                        if not self.debug:
                            if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                outputList.append(
                                    " " + word_num_str + " * " + getPartStr(
                                        self.music[self.searchlist[word_num]]["name"],
                                        0, 108) + "...")
                            else:
                                outputList.append(
                                    " " + word_num_str + " * " + self.music[self.searchlist[word_num]]["name"])
                        else:
                            outputList.append(
                                " " + word_num_str + " * " + self.music[self.searchlist[word_num]]["name"] + "10" +
                                self.searchlist[word_num])
                    else:
                        if not self.debug:
                            if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                outputList.append(
                                    " " + word_num_str + "   " + getPartStr(
                                        self.music[self.searchlist[word_num]]["name"],
                                        0, 108) + "...")
                            else:
                                outputList.append(
                                    " " + word_num_str + "   " + self.music[self.searchlist[word_num]]["name"])
                        else:
                            outputList.append(
                                " " + word_num_str + "   " + self.music[self.searchlist[word_num]]["name"] + "11" +
                                self.searchlist[word_num])
        return outputList

    def print_body(self):
        for line in self.return_body():
            print(line)

    def return_foot(self):
        """
        returns the foot (CLIENT)
        :return:
        """

        outputList = []

        if self.con_cont == "set":
            outputList.append("Commands:\n")

            if not self.paused:
                outputList.append(
                    "Pause (P), Delthis (DEL), Next (N), Reroll all (RE), Reroll this (RT), Queue this (QU), Details (DEA)")
            elif self.paused:
                outputList.append(
                    "Play (P), Delthis (DEL), Next (N), Reroll all (RE), Reroll this (RT), Queue this (QU), Details (DEA)")

            if self.con_main == "spl":
                outputList += self.spl.returncom()
                # self.spl.printcom()

            outputList.append("\nInput:\n%s" % self.cur_Input)

        elif self.con_cont == "search":
            outputList.append("Commands: (with UPPER LETTERs)\n")

            outputList.append("Play this (P), Delthis (DEL), Queue this (QU)")

            outputList.append("\nInput: %s" % self.cur_Input.upper())

            outputList.append("\nSearch: (with lower letters)\n")
            outputList.append("Input: %s" % self.cur_Search)

        elif self.con_cont == "conf":
            outputList.append("Confirm\n")
            outputList.append("Y/N")

        elif self.con_cont == "cont":
            outputList.append("Continue?\n")
            outputList.append("Press something")

        elif self.con_cont == "volp":
            outputList.append("Change Volume (Player):\n")
            outputList.append("Current: " + str(self.volumep))

            outputList.append("\n" + self.cur_Input)

        elif self.con_cont == "volw":
            self.volume = Volume.getVolume()
            outputList.append("Change Volume (Windows):\n")
            outputList.append("Current: " + str(self.volume))

            outputList.append("\n" + self.cur_Input)

        elif self.con_cont == "spe":
            outputList.append("Change Effectduration (Spl):\n")
            outputList.append("Current: " + str(self.spl.Effect))

            outputList.append("\n" + self.cur_Input)

        elif self.con_cont == "add":
            outputList.append("Add new Music:\n")

            cur = ""
            for mus in self.music["active"]:
                cur += mus + ", "
            cur = cur.rstrip(", ")

            outputList.append("Current: " + cur)

            outputList.append("\n" + self.cur_Input)

        return outputList

    def print_foot(self):
        for line in self.return_foot():
            print(line)

    def returnit(self):
        outputList = []


        # Head-Container (Info + Noti)
        outputList += self.return_head_info()

        if self.return_head_noti():
            outputList += ["\n" + console_data["pixx"]*"-" + "\n"]
            outputList += self.return_head_noti()

        outputList += ["\n" + console_data["pixx"]*"-" + "\n"]

        # Main-Container
        outputList += self.return_body()

        outputList += ["\n" + console_data["pixx"]*"-" + "\n"]
        # Control-Container
        outputList += self.return_foot()

        return outputList

    def printit(self):
        """
        prints the output (CLIENT)
        :return:
        """
        cls()
        for line in self.returnit():
            print(line)

    def react(self, inp):
        """
        direct input from scanner

        :param inp: input from scanner
        :return:
        """

    def input(self, i):
        """
        the tasks

        :param i: input
        :return:
        """

    def getCur(self):
        """
        returns the cur track
        :return:
        """
