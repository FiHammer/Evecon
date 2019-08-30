import threading
import pyglet
import sys
import random
import time
import subprocess
import socket

import EveconLib

# noinspection PyTypeChecker
class MusicPlayer(threading.Thread):
    def __init__(self, systray=True, random=True, expandRange=2, stop_del=False, scanner_active=True, balloonTip=True,
                 killMeAfterEnd=True, remote=True, remotePort=4554, selfprint=False, specialFilePath=None, neverPrint=False,
                 autoPlayVideo=True):
        super().__init__()

        self.debug = False

        self.find_music_out = {}

        self.systray = None
        self.systrayon = systray
        self.balloonTip = balloonTip
        self.killMeAfterEnd = killMeAfterEnd
        self.remote = True
        self.remotePort = remotePort
        self.selfprint = selfprint
        self.neverPrint = neverPrint

        self.remoteAddress = ""
        self.remoteAction = ""
        if self.remote:
            self.server = EveconLib.Networking.Server(port=self.remotePort, ip=EveconLib.Config.thisIP, stdReact=self.react_remote, printLog=False)
            self.server_java = EveconLib.Networking.ServerJava(port=self.remotePort + 1, ip=EveconLib.Config.thisIP, react=self.react_remote)
        else:
            self.server = None
            self.server_java = None

        self.volume = EveconLib.Tools.Windows.Volume.getVolume()
        self.volumep = 0.5

        # stop the musicplayer while hovering over file 1 and pressing 'del'-button
        self.stop_del = stop_del
        self.randomizer = random
        self.scanner_active = scanner_active
        EveconLib.Config.musicrun = True

        self.starttime = 0
        self.hardworktime = 0
        self.musicrun = True
        self.playlist = []
        self.last_playlist = []
        self.pershuffel = False

        self.running = False
        self.playing = False
        self.exitn = False
        self.allowPrint = False
        self.autorefresh = True

        self.player = pyglet.media.Player()
        self.timer = EveconLib.Tools.Timer()
        self.scanner = EveconLib.Programs.Scanner(self.react)
        self.spl = EveconLib.Programs.SplWeapRand()
        self.rhy = EveconLib.Games.Rhythm.Game()

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

        self.arrowSetting = [(3, 15, 3), (16, -1, 6)]  # (minPress, maxPress (-1 = infinite), Plus)

        self.notifications = []

        self.last_backspace = False

        self.tmp_pl_input_1 = []
        self.tmp_pl_input_2 = []
        self.tmp_pl_output_1 = []
        self.tmp_pl_output_2 = []

        self.musicKeysLeft = []

        self.lastPresses = [0, time.time(), "None"]

        self.mfl = EveconLib.Programs.Player.MusicFileLoader(self.notificate, self.neverPrint, musicPlayer=self)

        self.videoPlayerClient = None  # client for videoPlayer
        self.autoPlayVideo = autoPlayVideo
        self.videoPlayerIsPlaying = False
        self.videoPlayerProcess = None
        self.waitForVPstart = False


    def addMusic(self, key, cusPath=False, genre=False, noList=False, printStaMSG=True, printEndMSG=True,
                 makeNoti=False, loadForPyglet=True):  # key (AN, LIS)
        """
        :param key: the key of the id (normal id, mpl id)
        :param cusPath: defines the path for a custom path (ignores the key)
        :param genre: forces a genre input (?)
        :param noList: only allows key to be a normal id
        :param printStaMSG: clears the screen and prints the start msg
        :param printEndMSG: prints the finished msg
        :param makeNoti: make a notification after finishing
        :param loadForPyglet: load for pyglet
        :return: success
        """
        return self.mfl.addMusic(key=key, cusPath=cusPath, printStaMSG=printStaMSG,
                                 printEndMSG=printEndMSG, makeNoti=makeNoti,
                                 loadForPyglet=loadForPyglet)

    def read_musiclist(self):
        self.mfl.refreshMusicList()


    def resetInterface(self):
        self.con_main = "pl"
        self.cur_Input = ""
        self.cur_Pos = 0
        self.change = ""
        self.notifications = [] # really?

    def reloadMusic(self, tracknum: int):
        self.mfl.reloadFile(tracknum)

    def make_playlist(self):
        # self.last_playlist = self.playlist.copy()
        if self.playing:
            newPlaylist = self.mfl.files_allFiles.copy()
            del newPlaylist[newPlaylist.index(self.playlist[0])]
            self.playlist = [self.playlist[0]] + newPlaylist
        else:
            self.playlist = self.mfl.files_allFiles.copy()

        self.mfl.activateAll(True, suppressActiveList=True)
        self.searchlist = self.playlist.copy()
        if self.randomizer:
            self.shufflePL()
        self.last_playlist = self.playlist.copy()
        self.resetInterface()

    def shufflePL(self, shuffleFirst=False):
        self.last_playlist = self.playlist.copy()
        if shuffleFirst:
            random.shuffle(self.playlist)
        else:
            oldPL = self.playlist.copy()
            del oldPL[0]
            random.shuffle(oldPL)
            self.playlist = [self.playlist[0]] + oldPL

        self.hardworktime = time.time() + 0.1

    def restoreLPL(self):
        """
        restores the last (pl saved in self.last_playlist) playlist
        :return: success
        """

        if self.last_playlist == self.playlist:
            return
        else:
            lpl = self.playlist.copy()
            self.playlist = self.last_playlist.copy()
            self.last_playlist = lpl.copy()

    def refreshTitle(self):
        if self.getCur().anData["valid"]:
            EveconLib.Tools.title("OLD", self.getCur().anData["title"], "Now Playing")
        else:
            EveconLib.Tools.title("OLD", self.getCur().name, "Now Playing")

    def refresh(self, title=False, printme=True):
        if title:
            self.refreshTitle()
        if printme:
            self.printit()

    def showBalloonTip(self):
        if self.getCur().anData["valid"]:
            name = self.getCur().anData["title"]
        else:
            name = self.getCur().name
        EveconLib.Tools.Windows.BalloonTip("Evecon: MusicPlayer", "Now playing: " + name)

    def getCur(self):
        if len(self.playlist) == 0:
            self.stop()
        return self.playlist[0]

    def rerollThis(self):
        self.rerollPos(self.cur_Pos)
    def rerollPos(self, filePos):
        oldPL = self.playlist.copy()
        del oldPL[filePos]
        self.playlist = oldPL + [self.playlist[filePos]]
        if filePos == 0:
            self.next(True)

    def rerollId(self, fileId):
        oldPL = self.playlist.copy()
        index = self.playlist.index(fileId)
        del oldPL[index]
        self.playlist = oldPL + [self.playlist[index]]
        if index == 0:
            self.next(True)


    def sortPL(self):
        # returns in normal sort order
        self.playlist = self.mfl.files_active_allFiles.copy()
        self.hardworktime = time.time() + 0.2

    def sortPL_name(self):
        self.playlist.sort()
        self.hardworktime = time.time() + 0.2

    def sortPL_an(self):
        pl_nonan_file = []
        pl_an_names = []

        for file in self.playlist:
            if file.anData["valid"]:
                spd = EveconLib.Tools.StrPlusData(file.anData["animeName"])
                spd.additionalData = file
                pl_an_names.append(spd)
            else:
                pl_nonan_file.append(file)

        pl_an_names.sort()
        pl_nonan_file.sort()

        new_playlist = []

        for namePart in pl_an_names:
            new_playlist.append(namePart.additionalData)
        for noNamePart in pl_nonan_file:
            new_playlist.append(pl_nonan_file)

        self.playlist = new_playlist.copy()
        self.hardworktime = time.time() + 0.5

    # Options

    def play(self, fromServer=False):
        if self.videoPlayerIsPlaying and not fromServer: # server react
            self.videoPlayerClient.send("play")

        self.paused = False
        self.player.play()
        self.hardworktime = time.time() + 0.2

    def pause(self, fromServer=False):
        if self.videoPlayerIsPlaying and not fromServer: # server react
            self.videoPlayerClient.send("pause")

        self.paused = True
        self.player.pause()
        self.hardworktime = time.time() + 0.2

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

    def mute(self, fromServer=False):
        if self.videoPlayerIsPlaying and not fromServer: # server react
            self.videoPlayerClient.send("mute")
        self.muted = True
        self.mute_vol = self.volumep
        self.volp(0)

    def unmute(self, fromServer=False):
        if self.videoPlayerIsPlaying and not fromServer: # server react
            self.videoPlayerClient.send("unmute")
        self.muted = False
        self.volp(self.mute_vol)

    def stop(self):
        # noinspection PyGlobalUndefined
        EveconLib.Config.musicrun = False

        if self.videoPlayerIsPlaying:
            self.stopVideoPlayer()

        self.musicrun = False
        self.playing = False
        self.paused = False
        self.running = False
        self.scanner.running = False
        self.player.delete()

        if self.remote:
            self.server.exit()
            #self.server.close_connection()
            self.server_java.stop()
            try:
                #EveconLib.Config.globalMPports.remPort(self.server.port)
                EveconLib.Config.globalMPportsJava.remPort(self.server_java.port)
            except AttributeError:
                pass
        if self.systrayon and self.killMeAfterEnd:
            time.sleep(1)
            EveconLib.Tools.killme()

    def __del__(self):
        print("NOOO")

        if self.videoPlayerIsPlaying:
            print("Ok then it is Ok")
            self.videoPlayerProcess.kill()

        try:
            #EveconLib.Config.globalMPports.remPort(self.server.port)  # autodelete
            EveconLib.Config.globalMPportsJava.remPort(self.server_java.port)
        except AttributeError:
            pass

    def next(self, skipthis=False, fromServer=False):
        if self.waitForVPstart:
            return
        if self.videoPlayerIsPlaying: # server react
            self.stopVideoPlayer(fromServer)

        if skipthis:
            self.skip_del = True
        self.playing = False
        if self.paused:
            self.paused = False
            # self.player.play()  # TODO HERE COULD BE A MISSTAKE (COMMENTED TO TRY IF THIS CAUSES ERRORS)
        self.hardworktime = time.time() + 0.2

    def DelById(self, num):
        # num = Search(plfile, self.playlist)[0]
        if num == 0 and self.stop_del:
            self.stop()
        if num > len(self.playlist) - 1:
            return False

        if self.cur_Pos >= len(self.playlist) - 1:
            self.cur_Pos -= 1
        self.playlist[num].active = False

        if num == 0:
            self.next(True)
        return True

    def DelByFile(self, plfile):
        num = self.playlist.index(plfile)
        if num == 0 and self.stop_del:
            self.stop()

        if self.cur_Pos >= len(self.playlist) - 1:
            self.cur_Pos -= 1

        plfile.active = False

        if num == 0:
            self.next(True)
        return True

    def DelByKey(self, key):
        """
        this will delete musicfiles from the playlist

        :param key: the key from the musicFileEditor
        :return:
        """

        keyObj = self.mfl.getK(key)
        if not keyObj:
            return  # not found

        if not keyObj.active:
            return  # already deleted
        nextFile = False
        if self.getCur() in keyObj.getExtChildrenFiles():
            nextFile = True

        keyObj.active = False

        if nextFile:
            self.next(True)


    def vol(self, vol):
        self.volume = vol
        EveconLib.Tools.Windows.Volume.change(vol)

    def volp(self, vol, fromServer=False):
        if self.videoPlayerIsPlaying and not fromServer: # server react
            self.videoPlayerClient.send("vol_"+str(vol))

        self.volumep = vol
        self.player.volume = self.volumep

    def queueByPos(self, pos):
        # ID OF THE self.playlist!
        oldPL = self.playlist.copy()
        del oldPL[pos]
        del oldPL[0]
        self.playlist = [self.playlist[0]] + [self.playlist[pos]] + oldPL
        self.hardworktime = time.time()

    def queueByFile(self, plfile):
        if not plfile in self.playlist:
            oldPL = self.playlist.copy()
            del oldPL[0]
            self.playlist = [self.playlist[0], plfile] + oldPL
        else:
            oldPL = self.playlist.copy()
            del oldPL[oldPL.index(plfile)]
            del oldPL[0]
            self.playlist = [self.playlist[0], plfile] + oldPL
        self.hardworktime = time.time()

    def refreshSearch(self):
        self.cur_Pos = 0

        if self.cur_Search != "":
            namelist = []

            # for x in self.startlist:
            if self.last_backspace:  # global search
                for plFiles in self.mfl.files_allFiles:
                    name = EveconLib.Tools.StrPlusData(plFiles.name)
                    name.additionalData = plFiles
                    namelist.append(name)
            else:  # search in searchlist
                for plFiles in self.searchlist:
                    name = EveconLib.Tools.StrPlusData(plFiles.name)
                    name.additionalData = plFiles
                    namelist.append(name)

            found = EveconLib.Tools.Search(self.cur_Search, namelist)

            searchlist_name = []
            for plFiles in found:
                searchlist_name.append(namelist[plFiles])
            searchlist_name.sort()


        else:
            searchlist_name = []
            for fileX in self.mfl.files_allFiles:
                name = EveconLib.Tools.StrPlusData(fileX.name)
                name.additionalData = fileX

                searchlist_name.append(name)
            searchlist_name.sort()

        # searchlist_name is the sorted list including name + file

        new_playlist = []
        for name in searchlist_name:
            new_playlist.append(name.additionalData)

        self.searchlist = new_playlist.copy()

    def run(self):
        if not self.mfl.files_allFiles:
            return # empty playlist => first add something
        if self.systrayon and sys.platform == "win32":
            def quitFunc(x):
                self.stop()

            def unp_p(x):
                self.switch()

            def nextm(x):
                self.next()

            def delm(x):
                self.DelById(0)
                self.playing = False
                if self.paused:
                    self.play()

            def reroll(x):
                self.shufflePL()

            def vol01(x):
                self.volp(0.1)

            def vol025(x):
                self.volp(0.25)

            def vol05(x):
                self.volp(0.5)

            def vol1(x):
                self.volp(1)

            sub_menu1 = {"0.1": vol01, "0.25": vol025, "0.5": vol05, "1": vol1}

            self.systray = EveconLib.Tools.Windows.SysTray(EveconLib.Config.radioIcoFile, "Evecon: MusicPlayer",
                                   {"Pause/Unpause": unp_p, "Next": nextm,
                                    "Del": delm, "Reroll": reroll},
                                   sub_menu1=sub_menu1, sub_menu_name1="Volume", quitFunc=quitFunc)
            self.systray.start()

        if not self.playlist:
            self.make_playlist()
        self.searchlist = self.playlist.copy()

        if self.randomizer:
            self.shufflePL(True)

        if self.remote:
            try:
                EveconLib.Config.globalMPports.addPort(self.server.port)
                EveconLib.Config.globalMPportsJava.addPort(self.server_java.port)
            except AttributeError:
                pass
            self.server.start()
            self.server_java.start()

        self.starttime = time.time()
        self.hardworktime = time.time()
        if self.scanner_active:
            self.scanner.start()

        self.player.volume = self.volumep

        while self.musicrun:
            if not self.getCur().pygletData:
                self.getCur().loadForPyglet(threadLoad=False)
            if self.getCur().pygletData._is_queued:
                self.reloadMusic(self.playlist[0].id)

            if self.balloonTip:
                self.showBalloonTip()

            # VIDEO PLAYER TEST
            if self.playlist[0].type == "video" and self.autoPlayVideo:
                self.callVideoPlayer()  # ATTENTION: THE VIDEO IS NOW PLAYING SO NORMAL PLAYER IS PAUSED

                while self.waitForVPstart:
                    time.sleep(0.5)

            else:
                self.player.queue(self.getCur().pygletData)


                if not self.paused:
                    self.player.play()

            self.timer.start()  # music timer

            self.running = True
            self.playing = True

            self.allowPrint = True
            self.refreshTitle()

            self.printit()
            self.last_print_auto = time.time()
            while self.playing:

                time.sleep(0.15)
                for x in range(5):
                    if self.videoPlayerIsPlaying:
                        if round(self.getCur().pygletData.duration) <= round(self.timer.getTime()) - 3: # three seconds wait time for async
                            self.playing = False
                        time.sleep(0.1)  # easy continue

                    elif self.player.time == 0:
                        self.playing = False
                    elif round(self.getCur().pygletData.duration) <= round(self.timer.getTime()):
                        self.playing = False
                    time.sleep(0.2)

                    self.refresh(title=False, printme=self.selfprint)

                while self.paused:
                    self.timer.pause()

                    while self.paused:
                        time.sleep(0.25)

                    self.timer.unpause()
                    self.refresh(title=True, printme=self.selfprint)

            if self.videoPlayerIsPlaying:
                self.stopVideoPlayer()

            self.timer.reset()
            self.player.next_source()

            if self.skip_del:
                self.skip_del = False
            else:
                self.playlist += [self.playlist[0]]
                del self.playlist[0]

            if self.pershuffel:
                self.shufflePL()

            self.running = False

            if self.exitn:
                self.stop()

    def notificate(self, msg, title=None, screentime=5.0, maxTime=None):
        found = False
        if title:
            for noti in self.notifications:
                if noti["title"] == title:
                    found = True
                    noti["msgs"].append({
                        "msg": msg,
                        "screentime": screentime,
                        "starttime": time.time()
                    })
                    break
        if not found:
            self.notifications.append({
                "msgs": [{
                    "msg": msg,
                    "screentime": screentime,
                    "starttime": time.time()
                }],
                "maxTime": maxTime,
                "maxTimestart": time.time(),
                "title": title
            })
        if self.autorefresh and self.running:
            self.printit()

    def return_head_info(self):
        # Info-Container

        outputList = []

        if not self.remoteAddress:
            outputList.append("Musicplayer: \n")
        else:
            if self.remoteAddress == "192.168.2.103":
                con = "FP2"
            else:
                con = self.remoteAddress
            outputList.append("Musicplayer: (%s connected)\n" % con)

        if self.getCur().anData["valid"]:
            outputList.append(
                "Playing: \n%s \nFrom %s" % (self.getCur().anData["title"], self.getCur().anData["animeName"]))
        else:
            outputList.append("Playing: \n%s" % self.getCur().name)

        outputList.append("Time: %s\\%s" % (self.timer.getTimeFor(), EveconLib.Tools.TimeFor(self.getCur().pygletData.duration)))
        if self.muted:
            # output.append(int((console_data["pixx"]/2)-3)*"|"+"Muted"+int((console_data["pixx"]/2)-2)*"|")
            l1 = ""
            l2 = ""
            pre = ""
            outputList.append(
                pre + int((EveconLib.Config.console_data["pixx"] / 2) - 3) * l1 + "Muted" + int((EveconLib.Config.console_data["pixx"] / 2) - 2) * l2)

        return outputList

    def return_head_noti(self):
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

    def print_head_info(self, forcePrint=False):
        if self.neverPrint and not forcePrint:
            return False
        for line in self.return_head_info():
            print(line)

    def print_head_noti(self, forcePrint=False):
        if self.neverPrint and not forcePrint:
            return False
        for line in self.return_head_noti():
            print(line)

    def print_head(self, forcePrint=False):
        # Info-Container

        self.print_head_info(forcePrint)

        if self.return_head_noti() and not self.neverPrint:
            print("\n" + EveconLib.Config.console_data["pixx"] * "-" + "\n")
            self.print_head_noti(forcePrint)

        # sys.stdout.write(console_data[0]*"-")

    def return_body(self):

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
                                        if len(self.playlist[word_num].name) > 108:
                                            outputList.append(" " + word_num_str + " * " + EveconLib.Tools.getPartStr(
                                                self.playlist[word_num].name, 0, 108) + "...")
                                        else:
                                            outputList.append(
                                                " " + word_num_str + " * " + self.playlist[word_num].name)
                                    else:
                                        outputList.append(
                                            " " + word_num_str + " * " + self.playlist[word_num].name + "0" +
                                            self.playlist[word_num])
                                else:
                                    if not self.debug:
                                        if len(self.playlist[word_num].name) > 108:
                                            outputList.append(" " + word_num_str + "   " + EveconLib.Tools.getPartStr(
                                                self.playlist[word_num].name, 0, 108) + "...")
                                        else:
                                            outputList.append(
                                                " " + word_num_str + "   " + self.playlist[word_num].name)
                                    else:
                                        outputList.append(
                                            " " + word_num_str + "   " + self.playlist[word_num].name + "1" +
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
                                            if len(self.playlist[word_num].name) > 108:
                                                outputList.append(" " + word_num_str + " * " + EveconLib.Tools.getPartStr(
                                                    self.playlist[word_num].name, 0, 108) + "...")
                                            else:
                                                outputList.append(
                                                    " " + word_num_str + " * " + self.playlist[word_num].name)
                                        else:
                                            outputList.append(
                                                " " + word_num_str + " * " + self.playlist[word_num].name
                                                + "2" + self.playlist[word_num])
                                    except IndexError:
                                        pass
                                else:
                                    try:
                                        if not self.debug:
                                            if len(self.playlist[word_num].name) > 108:
                                                outputList.append(" " + word_num_str + "   " + EveconLib.Tools.getPartStr(
                                                    self.playlist[word_num].name, 0, 108) + "...")
                                            else:
                                                outputList.append(
                                                    " " + word_num_str + "   " + self.playlist[word_num].name)
                                        else:
                                            outputList.append(
                                                " " + word_num_str + "   " + self.playlist[word_num].name + "3" + self.playlist[word_num])
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
                                        if len(self.playlist[word_num].name) > 108:
                                            outputList.append(" " + word_num_str + " * " + EveconLib.Tools.getPartStr(
                                                self.playlist[word_num].name, 0, 108) + "...")
                                        else:
                                            outputList.append(
                                                " " + word_num_str + " * " + self.playlist[word_num].name)
                                    else:
                                        outputList.append(
                                            " " + word_num_str + " * " + self.playlist[word_num].name + "4" +
                                            self.playlist[word_num])
                                else:
                                    if not self.debug:
                                        if len(self.playlist[word_num].name) > 108:
                                            outputList.append(" " + word_num_str + "   " + EveconLib.Tools.getPartStr(
                                                self.playlist[word_num].name, 0, 108) + "...")
                                        else:
                                            outputList.append(
                                                " " + word_num_str + "   " + self.playlist[word_num].name)
                                    else:
                                        outputList.append(
                                            " " + word_num_str + "   " + self.playlist[word_num].name + "5" +
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
                                    if len(self.playlist[word_num].name) > 108:
                                        outputList.append(" " + word_num_str + " * " + EveconLib.Tools.getPartStr(
                                            self.playlist[word_num].name, 0, 108) + "...")
                                    else:
                                        outputList.append(
                                            " " + word_num_str + " * " + self.playlist[word_num].name)
                                else:
                                    outputList.append(
                                        " " + word_num_str + " * " + self.playlist[word_num].name + "6" +
                                        self.playlist[word_num])
                            else:
                                if not self.debug:
                                    if len(self.playlist[word_num].name) > 108:
                                        outputList.append(" " + word_num_str + "   " + EveconLib.Tools.getPartStr(
                                            self.playlist[word_num].name, 0, 108) + "...")
                                    else:
                                        outputList.append(
                                            " " + word_num_str + "   " + self.playlist[word_num].name)
                                else:
                                    outputList.append(
                                        " " + word_num_str + "   " + self.playlist[word_num].name + "7" +
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
                            if len(self.playlist[word_num].name) > 108:
                                outputList.append(
                                    " " + word_num_str + " * " + EveconLib.Tools.getPartStr(self.playlist[word_num].name,
                                                                            0,
                                                                            108) + "...")
                            else:
                                outputList.append(
                                    " " + word_num_str + " * " + self.playlist[word_num].name)
                        else:
                            outputList.append(
                                " " + word_num_str + " * " + self.playlist[word_num].name + "10" +
                                self.playlist[word_num])
                    else:
                        if not self.debug:
                            if len(self.playlist[word_num].name) > 108:
                                outputList.append(
                                    " " + word_num_str + "   " + EveconLib.Tools.getPartStr(self.playlist[word_num].name,
                                                                            0,
                                                                            108) + "...")
                            else:
                                outputList.append(
                                    " " + word_num_str + "   " + self.playlist[word_num].name)
                        else:
                            outputList.append(
                                " " + word_num_str + "   " + self.playlist[word_num].name + "11" +
                                self.playlist[word_num])

        elif self.con_main == "details":
            outputList.append("Details:\n")
            outputList.append("Duration: " + str(EveconLib.Tools.TimeFor(self.playlist[self.cur_Pos].pygletData.duration)))

            if self.playlist[self.cur_Pos].anData["valid"]:
                outputList.append("Title: " + str(self.playlist[self.cur_Pos].anData["title"]))
                outputList.append(
                    "Interpreter: " + str(self.playlist[self.cur_Pos].anData["interpreter"]))
                outputList.append("Musictype: " + str(self.playlist[self.cur_Pos].anData["musictype"]))
                outputList.append("Animename: " + str(self.playlist[self.cur_Pos].anData["animeName"]))
                if self.playlist[self.cur_Pos].anData.get("animeSeason"):
                    outputList.append("Season: " + str(self.playlist[self.cur_Pos].anData["animeSeason"]))
                if self.playlist[self.cur_Pos].anData.get("animeType"):
                    outputList.append("Type: " + str(self.playlist[self.cur_Pos].anData["animeType"]) +
                                      str(self.playlist[self.cur_Pos].anData["animeTypeNum"]))

            outputList.append("Filename: " + self.playlist[self.cur_Pos].file)
            outputList.append("Musictype: " + self.playlist[self.cur_Pos].type)
            outputList.append("Parantkey: " + str(self.playlist[self.cur_Pos].parentKey))
            outputList.append("Filepath: " + self.playlist[self.cur_Pos].path)
            outputList.append("Album: " + self.playlist[self.cur_Pos].pygletData.info.album.decode())
            outputList.append("Author: " + self.playlist[self.cur_Pos].pygletData.info.author.decode())
            outputList.append("Comment: " + self.playlist[self.cur_Pos].pygletData.info.comment.decode())
            outputList.append("Copyright: " + self.playlist[self.cur_Pos].pygletData.info.copyright.decode())
            outputList.append("Genre: " + self.playlist[self.cur_Pos].pygletData.info.genre.decode())
            outputList.append("Title: " + self.playlist[self.cur_Pos].pygletData.info.title.decode())
            outputList.append("Track: " + str(self.playlist[self.cur_Pos].pygletData.info.track))
            outputList.append("Year: " + str(self.playlist[self.cur_Pos].pygletData.info.year))

        elif self.con_main == "info":
            outputList.append("Infos:\n")

            if self.server:
                outputList.append("Server: Alive %s, Port %s" % (str(self.server.is_alive()), str(self.server.port)))
            else:
                outputList.append("Server: Alive False, Port None")
            if self.server_java:
                outputList.append(
                    "Server-Java: Alive %s, Port %s" % (str(self.server_java.is_alive()), str(self.server_java.port)))
            else:
                outputList.append("Server-Java: Alive False, Port None")

            if self.remoteAddress:
                outputList.append("Remote address: " + self.remoteAddress)
                outputList.append("Remote action: " + self.remoteAction)

            outputList.append("\nPlayer:\n")

            outputList.append("Vol: " + str(EveconLib.Tools.Windows.Volume.getVolume()))
            outputList.append("Volplayer: " + str(self.volumep))
            outputList.append("Muted: " + str(self.muted))
            outputList.append("Playing: " + str(self.playing))
            outputList.append("Paused: " + str(self.paused))

            files_loadedKeys = ""
            for k in self.mfl.files_loadedKeys:
                files_loadedKeys += str(k) + ", "
            files_loadedKeys.rstrip(", ")
            outputList.append("Loaded-Key: " + files_loadedKeys)

            if self.debug:
                outputList.append("\nDebugging Details:\n")

                outputList.append("Cur-Pos: " + str(self.cur_Pos))
                outputList.append("Autorefresh: " + str(self.autorefresh))

                outputList.append("\nOther:\n")

                outputList.append("Scanner-Status: " + str(self.scanner.is_alive()))
                outputList.append("Timer direct: " + str(self.timer.getTime())) # playing time
                outputList.append("Last print: " + str(self.last_print))
                outputList.append("Last auto print: " + str(self.last_print_auto))



        elif self.con_main == "spl":
            outputList += self.spl.returnmain()
            # self.spl.printit(False)
        elif self.con_main == "rhy":
            outputList += self.rhy.getPrint()

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
                                        if len(self.searchlist[word_num].name) > 108:
                                            outputList.append(" " + word_num_str + " * " + EveconLib.Tools.getPartStr(
                                                self.searchlist[word_num].name, 0, 108) + "...")
                                        else:
                                            outputList.append(
                                                " " + word_num_str + " * " + self.searchlist[word_num].name)
                                    else:
                                        outputList.append(
                                            " " + word_num_str + " * " + self.searchlist[word_num].name + "0" + self.searchlist[word_num])
                                else:
                                    if not self.debug:
                                        if len(self.searchlist[word_num].name) > 108:
                                            outputList.append(" " + word_num_str + "   " + EveconLib.Tools.getPartStr(
                                                self.searchlist[word_num].name, 0, 108) + "...")
                                        else:
                                            outputList.append(
                                                " " + word_num_str + "   " + self.searchlist[word_num].name)
                                    else:
                                        outputList.append(
                                            " " + word_num_str + "   " + self.searchlist[word_num].name + "1" + self.searchlist[word_num])
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
                                            if len(self.searchlist[word_num].name) > 108:
                                                outputList.append(" " + word_num_str + " * " + EveconLib.Tools.getPartStr(
                                                    self.searchlist[word_num].name, 0, 108) + "...")
                                            else:
                                                outputList.append(
                                                    " " + word_num_str + " * " + self.searchlist[word_num].name)
                                        else:
                                            outputList.append(
                                                " " + word_num_str + " * " + self.searchlist[word_num].name + "2" + self.searchlist[word_num])
                                    except IndexError:
                                        pass
                                else:
                                    try:
                                        if not self.debug:
                                            if len(self.searchlist[word_num].name) > 108:
                                                outputList.append(" " + word_num_str + "   " + EveconLib.Tools.getPartStr(
                                                    self.searchlist[word_num].name, 0, 108) + "...")
                                            else:
                                                outputList.append(
                                                    " " + word_num_str + "   " + self.searchlist[word_num].name)
                                        else:
                                            outputList.append(
                                                " " + word_num_str + "   " + self.searchlist[word_num].name + "3" + self.searchlist[word_num])
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
                                        if len(self.searchlist[word_num].name) > 108:
                                            outputList.append(" " + word_num_str + " * " + EveconLib.Tools.getPartStr(
                                                self.searchlist[word_num].name, 0, 108) + "...")
                                        else:
                                            outputList.append(
                                                " " + word_num_str + " * " + self.searchlist[word_num].name)
                                    else:
                                        outputList.append(
                                            " " + word_num_str + " * " + self.searchlist[word_num].name + "4" + self.searchlist[word_num])
                                else:
                                    if not self.debug:
                                        if len(self.searchlist[word_num].name) > 108:
                                            outputList.append(" " + word_num_str + "   " + EveconLib.Tools.getPartStr(
                                                self.searchlist[word_num].name, 0, 108) + "...")
                                        else:
                                            outputList.append(
                                                " " + word_num_str + "   " + self.searchlist[word_num].name)
                                    else:
                                        outputList.append(
                                            " " + word_num_str + "   " + self.searchlist[word_num].name + "5" + self.searchlist[word_num])
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
                                    if len(self.searchlist[word_num].name) > 108:
                                        outputList.append(" " + word_num_str + " * " + EveconLib.Tools.getPartStr(
                                            self.searchlist[word_num].name, 0, 108) + "...")
                                    else:
                                        outputList.append(
                                            " " + word_num_str + " * " + self.searchlist[word_num].name)
                                else:
                                    outputList.append(
                                        " " + word_num_str + " * " + self.searchlist[word_num].name + "6" + self.searchlist[word_num])
                            else:
                                if not self.debug:
                                    if len(self.searchlist[word_num].name) > 108:
                                        outputList.append(" " + word_num_str + "   " + EveconLib.Tools.getPartStr(
                                            self.searchlist[word_num].name, 0, 108) + "...")
                                    else:
                                        outputList.append(
                                            " " + word_num_str + "   " + self.searchlist[word_num].name)
                                else:
                                    outputList.append(
                                        " " + word_num_str + "   " + self.searchlist[word_num].name + "7" + self.searchlist[word_num])
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
                            if len(self.searchlist[word_num].name) > 108:
                                outputList.append(
                                    " " + word_num_str + " * " + EveconLib.Tools.getPartStr(
                                        self.searchlist[word_num].name,
                                        0, 108) + "...")
                            else:
                                outputList.append(
                                    " " + word_num_str + " * " + self.searchlist[word_num].name)
                        else:
                            outputList.append(
                                " " + word_num_str + " * " + self.searchlist[word_num].name + "10" +
                                self.searchlist[word_num])
                    else:
                        if not self.debug:
                            if len(self.searchlist[word_num].name) > 108:
                                outputList.append(
                                    " " + word_num_str + "   " + EveconLib.Tools.getPartStr(
                                        self.searchlist[word_num].name,
                                        0, 108) + "...")
                            else:
                                outputList.append(
                                    " " + word_num_str + "   " + self.searchlist[word_num].name)
                        else:
                            outputList.append(
                                " " + word_num_str + "   " + self.searchlist[word_num].name + "11" +
                                self.searchlist[word_num])
        return outputList

    def print_body(self, forcePrint=False):
        if self.neverPrint and not forcePrint:
            return False

        for line in self.return_body():
            print(line)

    def return_foot(self):
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
            self.volume = EveconLib.Tools.Windows.Volume.getVolume()
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
            for mus in self.mfl.files_loadedKeys:
                cur += mus.key + ", "
            cur = cur.rstrip(", ")

            outputList.append("Current: " + cur)

            misStr = ""
            for misPart in self.musicKeysLeft:
                misStr += misPart + ", "
            misStr = misStr.rstrip(", ")

            outputList.append("Left: " + misStr)

            outputList.append("\n" + self.cur_Input)

        elif self.con_cont == "dekey":
            outputList.append("Remove music through their key:\n")

            cur = ""
            for mus in self.mfl.files_loadedKeys:
                cur += mus.key + ", "
            cur = cur.rstrip(", ")

            outputList.append("Current: " + cur)

            outputList.append("\n" + self.cur_Input)

        return outputList

    def print_foot(self, forcePrint=False):
        if self.neverPrint and not forcePrint:
            return False
        for line in self.return_foot():
            print(line)

    def returnit(self):
        outputList = []

        # Head-Container (Info + Noti)
        outputList += self.return_head_info()

        if self.return_head_noti():
            outputList += ["\n" + EveconLib.Config.console_data["pixx"] * "-" + "\n"]
            outputList += self.return_head_noti()

        outputList += ["\n" + EveconLib.Config.console_data["pixx"] * "-" + "\n"]

        # Main-Container
        outputList += self.return_body()

        outputList += ["\n" + EveconLib.Config.console_data["pixx"] * "-" + "\n"]
        # Control-Container
        outputList += self.return_foot()

        return outputList

    def printit(self, forcePrint=False):
        if self.neverPrint and not forcePrint:
            return False

        EveconLib.Tools.cls()
        for line in self.returnit():
            print(line)
        self.last_print = time.time()

    def react(self, inp, debug_directMulti=False):
        if debug_directMulti:
            self.cur_Input += inp
            x = self.input(self.cur_Input)
            self.printit()
            return x

        if self.lastPresses[1] + 0.2 >= time.time() and self.lastPresses[2] == inp:  # DOUBLE PRESS
            mulPress = self.lastPresses[0] + 1
            self.lastPresses = [mulPress, time.time(), inp]
        else:
            mulPress = 1
            self.lastPresses = [mulPress, time.time(), inp]
        while self.starttime + 1.5 >= time.time() and self.hardworktime + 0.65 >= time.time():
            time.sleep(0.25)

        if self.con_main == "details" or self.con_main == "info" or self.con_cont == "cont":
            self.con_main = self.con_main_last
            self.con_cont = "set"

        # Search BLOCK

        elif inp == "escape" and self.searching:
            self.con_main = "pl"
            self.con_cont = "set"
            self.searching = False
            self.cur_Search = ""
            self.cur_Input = ""
            self.cur_Pos = 0

        elif inp == " " and self.searching:
            self.cur_Search += " "
            self.refreshSearch()

        elif len(inp) == 1 and self.searching:
            if inp == inp.lower():  # SEARCH
                self.cur_Search += inp
                self.last_backspace = False
                self.refreshSearch()

            else:  # COMMANDS
                self.cur_Input += inp

                i = self.cur_Input.lower()

                # Search commands
                if i == "p":
                    oldPL = self.playlist.copy()
                    del oldPL[oldPL.index(self.searchlist[self.cur_Pos])]
                    self.playlist = [self.searchlist[self.cur_Pos]] + oldPL
                    self.next(True)

                    self.con_main = "pl"
                    self.con_cont = "set"
                    self.searching = False
                    self.cur_Search = ""
                    self.cur_Pos = 0

                    self.cur_Input = ""

                elif i == "del":
                    self.DelByFile(self.searchlist[self.cur_Pos])
                    self.refreshSearch()
                    self.cur_Input = ""

                elif i == "qu":
                    self.queueByFile(self.searchlist[self.cur_Pos])
                    self.cur_Input = ""

                # Musicplayer commands
                elif i == "pla" or i == "pau":
                    self.switch()
                    self.cur_Input = ""
                elif i == "next" or i == "n":
                    self.next()
                    self.cur_Input = ""
                elif i == "m":
                    self.switchmute()
                    self.cur_Input = ""
                elif i == "stop" or i == "exit":
                    self.stop()
                    self.cur_Input = ""



        elif inp == "del" and self.searching:
            self.DelByFile(self.searchlist[self.cur_Pos])
            self.refreshSearch()
            self.cur_Input = ""

        elif inp == "return" and self.searching:
            oldPL = self.playlist.copy()
            del oldPL[oldPL.index(self.searchlist[self.cur_Pos])]
            self.playlist = [self.searchlist[self.cur_Pos]] + oldPL
            self.next(True)

            self.con_main = "pl"
            self.con_cont = "set"
            self.searching = False
            self.cur_Search = ""
            self.cur_Pos = 0

            self.cur_Input = ""


        elif inp == "backspace" and self.searching:  # SEARCH
            if len(self.cur_Search) > 0:
                new_Search = ""
                for x in range(len(self.cur_Search) - 1):
                    new_Search += self.cur_Search[x]
                self.cur_Search = new_Search
                self.last_backspace = True
                self.refreshSearch()

        elif inp == "strg_backspace" and self.searching:  # COMMANDS
            if len(self.cur_Input) > 0:
                new_Input = ""
                for x in range(len(self.cur_Input) - 1):
                    new_Input += self.cur_Input[x]
                self.cur_Input = new_Input

        elif inp == "arrowup" and self.cur_Pos > 0 and self.searching:
            done = False
            for aS in self.arrowSetting:
                if aS[0] < mulPress < aS[1] != -1 and not done or aS[0] < mulPress and aS[1] == -1 and not done:
                    done = True
                    if self.cur_Pos - aS[2] >= 0:
                        self.cur_Pos -= aS[2]
                    else:
                        self.cur_Pos = 0
                    break

            if not done:
                self.cur_Pos -= 1

        elif inp == "arrowdown" and self.cur_Pos < len(self.searchlist) - 1 and self.searching:
            done = False
            for aS in self.arrowSetting:
                if aS[0] < mulPress < aS[1] != -1 and not done or aS[0] < mulPress and aS[1] == -1 and not done:
                    done = True
                    if self.cur_Pos + aS[2] <= len(self.searchlist) - 1:
                        self.cur_Pos += aS[2]
                    else:
                        self.cur_Pos = len(self.searchlist) - 1
                    break
            if not done:
                self.cur_Pos += 1

        elif inp == " ":
            self.switch()


        elif len(inp) == 1 and not self.searching:  # MAIN give to next method
            self.cur_Input += inp
            self.last_backspace = False
            if not self.change:
                if self.input(self.cur_Input):
                    self.cur_Input = ""

        elif inp == "backspace" and not self.searching:
            if len(self.cur_Input) > 0:
                new_Input = ""
                for x in range(len(self.cur_Input) - 1):
                    new_Input += self.cur_Input[x]
                self.last_backspace = True
                self.cur_Input = new_Input

        elif inp == "strg_backspace" and not self.searching:
            self.cur_Input = ""


        elif self.con_main != "pl" and inp == "escape":  # !! EXIT IN EVERYTHING WITH ESC
            self.resetInterface()

        elif self.change and inp == "escape":
            self.cur_Input = ""
            self.change = ""
            self.con_cont = "set"

        elif self.change == "volp":
            if inp == "return":
                try:
                    self.volp(float(self.cur_Input))
                except ValueError:
                    pass

                self.cur_Input = ""
                self.change = ""
                self.con_cont = "set"

        elif self.change == "volw":
            if inp == "return":
                try:
                    self.vol(float(self.cur_Input))
                except ValueError:
                    pass

                self.cur_Input = ""
                self.change = ""
                self.con_cont = "set"

        elif self.change == "spe":
            if inp == "return":
                try:
                    self.spl.ChEffect(int(self.cur_Input))
                except ValueError:
                    pass

                self.cur_Input = ""
                self.change = ""
                self.con_cont = "set"

        elif self.change == "add":
            if inp == "return":
                theKEY = self.cur_Input

                def addMe():
                    self.addMusic(theKEY, printStaMSG=False, printEndMSG=False, makeNoti=True)
                    self.make_playlist()

                t = threading.Thread(target=addMe)
                t.start()
                self.cur_Input = ""
                self.change = ""
                self.con_cont = "set"

        elif self.change == "dekey":
            if inp == "return":
                self.DelByKey(self.cur_Input)

                self.cur_Input = ""
                self.change = ""
                self.con_cont = "set"


        elif inp == "arrowup" and self.cur_Pos > 0 and self.con_main == "pl":
            done = False
            for aS in self.arrowSetting:
                if aS[0] < mulPress < aS[1] != -1 and not done or aS[0] < mulPress and aS[1] == -1 and not done:
                    done = True
                    if self.cur_Pos - aS[2] >= 0:
                        self.cur_Pos -= aS[2]
                    else:
                        self.cur_Pos = 0
                    break

            if not done:
                self.cur_Pos -= 1

        elif inp == "arrowdown" and self.cur_Pos < len(self.playlist) - 1 and self.con_main == "pl":
            done = False
            for aS in self.arrowSetting:
                if aS[0] < mulPress < aS[1] != -1 and not done or aS[0] < mulPress and aS[1] == -1 and not done:
                    done = True
                    if self.cur_Pos + aS[2] <= len(self.playlist) - 1:
                        self.cur_Pos += aS[2]
                    else:
                        self.cur_Pos = len(self.playlist) - 1
                    break
            if not done:
                self.cur_Pos += 1


        elif inp == "strg_arrowup" and self.cur_Pos > 0 and self.con_main == "pl" or \
                inp == "num8" and self.cur_Pos > 0 and self.con_main == "pl":
            newPL = []
            skipnext = False
            for x in range(len(self.playlist)):
                if x == self.cur_Pos - 1:
                    newPL.append(self.playlist[x + 1])
                    newPL.append(self.playlist[x])
                    skipnext = True
                elif skipnext:
                    skipnext = False
                else:
                    newPL.append(self.playlist[x])

            self.playlist = newPL.copy()

            if self.cur_Pos == 1:
                self.next(True)

            self.cur_Pos -= 1

        elif inp == "strg_arrowdown" and self.cur_Pos < len(self.playlist) - 1 and self.con_main == "pl" or \
                inp == "num2" and self.cur_Pos < len(self.playlist) - 1 and self.con_main == "pl":
            newPL = []
            skipnext = False
            for x in range(len(self.playlist)):
                if x == self.cur_Pos:
                    newPL.append(self.playlist[x + 1])
                    newPL.append(self.playlist[x])
                    skipnext = True
                elif skipnext:
                    skipnext = False
                else:
                    newPL.append(self.playlist[x])

            self.playlist = newPL.copy()

            if self.cur_Pos == 0:
                self.next(True)

            self.cur_Pos += 1

        elif inp == "del" and self.con_main == "pl":
            self.DelById(self.cur_Pos)

        elif inp == "return" and self.con_main == "pl":
            oldPL = self.playlist.copy()
            del oldPL[self.cur_Pos]
            self.playlist = [self.playlist[self.cur_Pos]] + oldPL
            self.next(True)
        else:
            return False

        self.printit()

    def input(self, i):
        if i == i.upper():
            upper = True
        else:
            upper = False

        if self.waitForVPstart:
            self.notificate("WAIT FOR VIDEO START", "Error")

        while self.waitForVPstart:  # wait loop
            time.sleep(0.4)


        i = i.lower()
        if i == "play" or i == "pau" or i == "pause" or i == "p":
            self.switch()
        elif i == "next" or i == "n":
            self.next()
        elif i == "m":
            self.switchmute()
        elif i == "stop" or i == "exit":
            self.stop()
        # elif i == "del":
        #    self.playing = False
        #    if self.paused:
        #        self.play()
        #    time.sleep(0.5)
        #    self.Del(self.playlist[-1])
        elif i == "del":
            self.DelById(self.cur_Pos)

        elif i == "add":
            self.cur_Input = ""
            self.change = "add"
            self.con_cont = "add"

            # generating the missing MusicKeysList
            self.musicKeysLeft = self.mfl.musicFileEditor.musicDirs["keys"].copy()
            for needToDel in self.mfl.files_loadedKeys:
                sol = EveconLib.Tools.Search(needToDel.key, self.musicKeysLeft, exact=True, lower=False)
                if len(sol) == 0:
                    continue  # maybe a mpl key
                del self.musicKeysLeft[sol[0]]

        elif i == "dekey":
            self.cur_Input = ""
            self.change = "dekey"
            self.con_cont = "dekey"
        elif i == "volw":
            self.cur_Input = ""
            self.change = "volw"
            self.con_cont = "volw"
        elif i == "volp":
            self.cur_Input = ""
            self.change = "volp"
            self.con_cont = "volp"
        elif i == "re":
            if not upper:
                self.shufflePL()
            else:
                self.restoreLPL()
        elif i == "lpl":
            self.restoreLPL()
        elif i == "rt":
            self.rerollThis()
        elif i == "exin":
            self.exitn = True
        elif i == "dea" and (self.con_main == "pl" or self.con_main == "search"):
            self.con_main_last = self.con_main
            self.con_main = "details"
            self.con_cont = "cont"
        elif i == "info" and (self.con_main == "pl" or self.con_main == "search"):
            self.con_main_last = self.con_main
            self.con_main = "info"
            self.con_cont = "cont"
        elif i == "sortfile":
            self.sortPL()
            self.next(True)
        elif i == "sortname":
            self.sortPL_name()
            self.next(True)
        elif i == "sortan":
            self.sortPL_an()
            self.next(True)
        elif i == "qu":
            self.queueByPos(self.cur_Pos)
        elif i == "debug":
            if self.debug:
                self.debug = False
            else:
                self.debug = True
        elif i == "refresh":
            self.refreshTitle()
            self.printit()

        elif i == "autorefresh" and self.debug:
            if self.autorefresh:
                self.autorefresh = False
            else:
                self.autorefresh = True

        elif i == "search" and self.con_main == "pl":
            self.con_main = "search"
            self.con_cont = "search"
            self.searching = True
            self.cur_Search = ""
            self.cur_Input = ""  # need this ?
            self.refreshSearch()

        elif i == "vid":  # deac video for this session and play normal
            print("vidGlobal")
            if self.cur_Pos == 0:
                if self.getCur().type == "music":
                    return False
                print("vid")

                self.getCur().type = "music"
                self.stopVideoPlayer(debug_vPIP=True)

                time.sleep(3)
                self.player.pause()
                self.timer.reset()
                if self.getCur().pygletData._is_queued:
                    self.getCur().loadForPyglet()

                self.player.next_source()
                self.player.queue(self.getCur().pygletData)
                self.player.play()
                self.timer.start()
                time.sleep(1.5)

                self.videoPlayerIsPlaying = False
            else:
                if self.playlist[self.cur_Pos].type == "music" and self.playlist[self.cur_Pos].videoAvail:
                    self.playlist[self.cur_Pos].type = "video"
                else:
                    self.playlist[self.cur_Pos].type = "music"


        elif i == "spl":
            if self.con_main == "spl":
                self.con_main_last = self.con_main
                self.con_main = "pl"
            else:
                self.con_main_last = self.con_main
                self.con_main = "spl"

        elif EveconLib.Tools.lsame(i, "sp") and not i == "sp" and self.con_main == "spl":
            if EveconLib.Tools.lsame(i, "spe"):
                self.cur_Input = ""
                self.change = "spe"
                self.con_cont = "spe"
            elif i == "spn":
                self.spl.RoundOverF()
            elif i == "spwr":
                self.spl.WRswitch()
            elif i == "spr":
                self.spl.WRreroll()
            else:
                return False

        elif i == "rhy":
            if self.con_main == "rhy":
                self.con_main_last = self.con_main
                self.con_main = "pl"
            else:
                self.rhy.start()
                self.con_main_last = self.con_main
                self.con_main = "rhy"

        elif self.con_main == "rhy":
            self.rhy.newPress()

        else:
            return False
        return True

    def react_remote(self, i, conId=0, java=False):
        if isinstance(i, tuple):
            self.remoteAddress = i[0]
        elif i is None:
            self.remoteAddress = ""
            self.remoteAction = ""
        else:  # COMMANDS
            """
            HOW:

            type_what(_value)

            eg.: 
            set_pause_0
            get_pause
            """
            data = i.split("_")

            if data[0] == "set":
                if data[1] == "next":
                    self.next()
                    self.remoteAction = "Next"
                elif data[1] == "pause":
                    if len(data) == 3:
                        if data[2] == "0":
                            self.play()
                            self.remoteAction = "Unpause"
                        elif data[2] == "1":
                            self.pause()
                            self.remoteAction = "Pause"
                    else:
                        self.switch()
                        self.remoteAction = "Switch pause"
                elif data[1] == "mute":
                    if len(data) == 3:
                        if data[2] == "0":
                            self.unmute()
                            self.remoteAction = "Unmute"
                        elif data[2] == "1":
                            self.mute()
                            self.remoteAction = "Mute"
                    else:
                        self.switchmute()
                        self.remoteAction = "Switch mute"
                elif data[1] == "exit":
                    self.stop()
                elif data[1] == "volume" and len(data) == 3:
                    self.vol(float(data[2]))
                    self.remoteAction = "Volume to: " + str(self.volume)
                elif data[1] == "volumep" and len(data) == 3:
                    self.volp(float(data[2]))
                    self.remoteAction = "VolumeP to: " + str(self.volumep)


            elif data[0] == "get":
                data_send = ""
                if data[1] == "title":
                    data_send = self.getCur()["name"]
                elif data[1] == "time":
                    data_send = round(self.timer.getTime())
                elif data[1] == "duration":
                    data_send = round(self.getCur()["loaded"].duration)
                elif data[1] == "volume":
                    data_send = str(EveconLib.Tools.Windows.Volume.getVolume())
                # print(data_send)
                if data_send:
                    if not java:
                        self.server.send(data_send)
                    else:
                        self.server_java.send(data_send)


    def callVideoPlayer(self):
        # starts a videoPlayer
        self.stopVideoPlayer()

        self.waitForVPstart = True

        self.player.pause()
        newPort = EveconLib.Tools.UsedPorts.givePort()
        self.videoPlayerClient = EveconLib.Networking.Client(socket.gethostbyname(socket.gethostname()), newPort, react=self.reactVideoPlayer)
        sp = EveconLib.Config.startProgramm
        self.videoPlayerProcess = subprocess.Popen(["python", sp, "--vp", self.getCur().path, str(newPort)])

        #print(sp)

        time.sleep(5)
        self.videoPlayerClient.start()
        self.videoPlayerClient.send("vol_"+str(self.volumep))
        self.videoPlayerIsPlaying = True

    def stopVideoPlayer(self, fromServer=False, debug_vPIP=False):  # debug_vPIP do not chance vpip in this method
        if not self.videoPlayerIsPlaying:
            return
        if not fromServer:
            pass #self.videoPlayerClient.send("exit")  # maybe kill this programm not through exit, because this could throw a error
        self.videoPlayerClient.exit(sendM=False)
        if not debug_vPIP:
            self.videoPlayerIsPlaying = False
            self.waitForVPstart = False # maybe debug
        #self.videoPlayerProcess.terminate()  # do not need
        self.videoPlayerProcess.kill()

    def reactVideoPlayer(self, msg):
        if msg == "firstStart":
            self.waitForVPstart = False
        elif msg == "play":
            self.play(fromServer=True)
        elif msg == "pause":
            self.pause(fromServer=True)
        elif msg == "exit":
            self.next(fromServer=True)  # stop this video skip to next track
        elif EveconLib.Tools.lsame(msg, "vol_"):
            try:
                self.volp(float(msg.lstrip("vol_")), fromServer=True)
            except ValueError:
                pass
        elif msg == "mute":
            self.mute(fromServer=True)
        elif msg == "unmute":
            self.unmute(fromServer=True)
        else:
            return
        self.refresh(title=False, printme=self.selfprint)