import os
import threading
import pyglet
import sys
import random
import time

import EveconLib.Networking
import EveconLib.Config
import EveconLib.Tools

import EveconLib.Programs.Scanner
import EveconLib.Programs.SplWeapRand
import EveconLib.Programs.Player.MusicFileEditor

from queue import Queue as queue_Queue

# noinspection PyTypeChecker
class MusicPlayer(threading.Thread):
    def __init__(self, systray=True, random=True, expandRange=2, stop_del=False, scanner_active=True, balloonTip=True,
                 killMeAfterEnd=True, remote=True, remotePort=4554, selfprint=False, specialFilePath=None, neverPrint=False):
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
        # noinspection PyGlobalUndefined
        global musicrun
        musicrun = True

        self.starttime = 0
        self.hardworktime = 0
        self.musicrun = True
        self.playlist = []
        self.last_playlist = []
        self.startlist = []  # all files which are loaded are in here!
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

        self.arrowSetting = [(3, 10, 3), (11, -1, 6)]  # (minPress, maxPress (-1 = infinite), Plus)

        self.notifications = []

        self.last_backspace = False

        self.tmp_pl_input_1 = []
        self.tmp_pl_input_2 = []
        self.tmp_pl_output_1 = []
        self.tmp_pl_output_2 = []

        self.musicKeysLeft = []

        self.lastPresses = [0, time.time(), "None"]

        self.musiclist = {"names": []}
        self.multiplaylists = {}
        self.genre = []
        self.musicDir = ""

        self.musicFileEditor = EveconLib.Programs.Player.MusicFileEditor(specialFilePath)


    def findMusic(self, path, reset=True, key="cus"):
        if reset:
            self.find_music_out = {"all_files": 0, "all_dirs": 0}
        content = []

        for file in os.listdir(path):
            fullname = path + EveconLib.Config.path_seg + file
            if os.path.isdir(path + EveconLib.Config.path_seg + file):
                self.music["all_dirs"] += 1
                self.music["dir" + str(self.music["all_dirs"])] = {"file": file, "path": path, "fullname": fullname, "key": key}

                thisDirID = self.music["all_dirs"]

                self.find_music_out["all_dirs"] += 1
                self.find_music_out["dir" + str(self.music["all_dirs"])] = {"file": file, "path": path,
                                                                            "fullname": fullname, "key": key}
                dir_content = self.findMusic(fullname, False, key=key)

                self.music["dir" + str(thisDirID)]["content"] = dir_content
                self.find_music_out["dir" + str(thisDirID)]["content"] = dir_content

                content.append("dir" + str(thisDirID))  # ID of DIR

            elif os.path.isfile(fullname) and EveconLib.Tools.MusicType(file):
                name = file.rstrip(EveconLib.Tools.MusicType(file, True)).rstrip(".")

                self.music["all_files"] += 1
                self.find_music_out["all_files"] += 1

                me = EveconLib.Tools.MusicEncode(file)
                if me["valid"] and not me["noBrack"]:
                    antype = True
                    andata = me
                else:
                    antype = False
                    andata = me # oops

                self.music["file" + str(self.music["all_files"])] = {"name": name, "file": file, "path": path,
                                                                     "fullname": fullname,
                                                                     "antype": antype, "andata": andata, "key": key}

                self.find_music_out["file" + str(self.music["all_files"])] = {"name": name, "file": file, "path": path,
                                                                              "fullname": fullname,
                                                                              "antype": antype, "andata": andata, "key": key}

                content.append("file" + str(self.music["all_files"]))  # ID of FILE

        return content

    def addMusic(self, key, cusPath=False, genre=False, noList=False, printStaMSG=True, printEndMSG=True,
                 makeNoti=False):  # key (AN, LIS)

        """
        :param key: the key of the id (normal id, mpl id)
        :param cusPath: defines the path for a custom path (ignores the key)
        :param genre: forces a genre input (?)
        :param noList: only allows key to be a normal id
        :param printStaMSG: clears the screen and prints the start msg
        :param printEndMSG: prints the finished msg
        :param makeNoti: make a notification after finishing
        :return: success
        """
        self.read_musiclist()
        if noList and type(key) == str:
            if EveconLib.Tools.Search(key, self.musiclist["keys"], exact=True):
                return False
        if printStaMSG and not self.neverPrint:
            EveconLib.Tools.cls()
            if EveconLib.Config.computer == "MiniPC":
                print("Loading... (On Mini-PC)")
            elif EveconLib.Config.computer == "BigPC":
                print("Loading... (On Big-PC)")
            else:
                print("Loading...")

        old_Num = self.music["all_files"]
        if type(key) == str:
            key = key.lower()

        if EveconLib.Tools.Search(key, self.music["active"]):
            return False

        if cusPath:
            key = "cus"
        elif genre:
            if EveconLib.Tools.Search(key, self.genre, exact=True):
                if isinstance(key, str):
                    for aDir in self.musiclist["keys"]:
                        if EveconLib.Tools.Search(key, self.musiclist[aDir]["genre"], exact=True):
                            self.addMusic(aDir, printStaMSG=False, printEndMSG=printEndMSG, makeNoti=makeNoti)
                elif isinstance(key, list):
                    for aGenre in key:
                        for aDir in self.musiclist["keys"]:
                            if EveconLib.Tools.Search(aGenre, self.musiclist[aDir]["genre"], exact=True):
                                self.addMusic(aDir, printStaMSG=False, printEndMSG=printEndMSG, makeNoti=makeNoti)
                return True
            else:
                return False

        done = False
        if type(key) == str:
            for x in self.musiclist["keys"]:
                if x == key:
                    self.findMusic(self.musicDir + EveconLib.Config.path_seg + self.musiclist[key]["path"], key=key)
                    done = True
                    break
        elif type(key) == list:
            for x in self.musiclist["keys"]:
                for y in key:
                    if x == y:
                        self.addMusic(x, printStaMSG=False, printEndMSG=printEndMSG, makeNoti=makeNoti)
                        break
            return True

        if done:
            pass
        elif key == "us":
            self.findMusic("Music" + EveconLib.Config.path_seg + "User", key=key)
        elif key == "cus" and cusPath:  # cusPath
            self.findMusic(cusPath, key=key)
        elif key == "all":
            for x in self.musiclist["keys"]:
                self.addMusic(x, printStaMSG=False, printEndMSG=printEndMSG, makeNoti=makeNoti)
            return True
        elif EveconLib.Tools.Search(key, list(self.multiplaylists["keys"]), exact=True):
            self.addMusic(self.multiplaylists[key]["content"]["all_ids"], printStaMSG=False, printEndMSG=printEndMSG,
                          makeNoti=makeNoti)
        elif EveconLib.Tools.Search(key, self.genre, exact=True):
            if isinstance(key, str):
                for aDir in self.musiclist["keys"]:
                    if EveconLib.Tools.Search(key, self.musiclist[aDir]["genre"], exact=True):
                        self.addMusic(aDir, printStaMSG=False, printEndMSG=printEndMSG, makeNoti=makeNoti)
            elif isinstance(key, list):
                for aGenre in key:
                    for aDir in self.musiclist["keys"]:
                        if EveconLib.Tools.Search(aGenre, self.musiclist[aDir]["genre"], exact=True):
                            self.addMusic(aDir, printStaMSG=False, printEndMSG=printEndMSG, makeNoti=makeNoti)
            else:
                pass
            return True

        else:
            return False

        q = queue_Queue()
        num_workers = EveconLib.Config.cores * 2

        def do_work(data):
            # cls()
            # print("Loading (%s/%s)" % (data[0], self.find_music_out["all_files"]))
            self.music["file" + str(data[1] + data[0])]["loaded"] = pyglet.media.load(
                self.music["file" + str(data[1] + data[0])]["fullname"])

        def worker():
            while True:
                data = q.get()
                if data is None:
                    break
                do_work(data)
                q.task_done()

        threads_used = []

        for i in range(num_workers):
            t = threading.Thread(target=worker)
            t.start()
            threads_used.append(t)

        for numfile in range(1, self.find_music_out["all_files"] + 1):
            q.put((numfile, old_Num))

        for i in range(num_workers):
            q.put(None)

        for i in threads_used:
            i.join()

        # for numfile in range(1, self.find_music_out["all_files"] + 1):
        #    cls()
        #    print("Loading (%s/%s)" % (numfile, self.find_music_out["all_files"]))
        #    self.music["file" + str(old_Num + numfile)]["loaded"] = pyglet.media.load(self.music["file" + str(old_Num + numfile)]["fullname"])

        # self.music_playlists_active.append(key)
        self.music["active"].append(key)
        if printEndMSG and not self.neverPrint:
            print("Finished: " + key)
        if makeNoti:
            self.notificate(key.title(), title="Finished loading", screentime=2.5)
        return True

    def read_musiclist(self):
        """
        def unvalid(error, key=False, remove=False):
            nonlocal data
            if not key:
                print("Musicfile is not valid:\n" + error)
            else:
                print("Musicfile is not valid:\nKey not found! (" + error + ")")

            if remove:
                with open(EveconLib.Config.backupMusicFile) as jsonfile:
                    data = json.load(jsonfile)

            return False

        def parse(unvaild):
            version = "1.1"

            if data.get("pc") != EveconLib.Config.computer:
                if data.get("pc") != "global":
                    unvaild("Wrong PC!", remove=True)
                    return parse(unvalid)
            if data.get("version"):
                if not data["version"] == version:
                    unvaild("Wrong Version! (" + version + " required)")
                    return parse(unvalid)
            else:
                unvaild("version", True, remove=True)
                return parse(unvalid)

            if data.get("musicDir"):
                if os.path.exists(data["musicDir"]):
                    musicDir = data["musicDir"] + "\\"
                else:
                    unvaild("Wrong musicDir path", remove=True)
                    return parse(unvalid)
            else:
                unvaild("musicDir", True, remove=True)
                return parse(unvalid)

            if not data.get("directories"):
                unvaild("directories", True, remove=True)
                return parse(unvalid)
            if not data.get("multiplaylists"):
                multiPls_deac = True
                # unvaild("multiplaylists", True, remove=True)
                # return parse(unvalid)
            else:
                multiPls_deac = False

            musicDirs = {"names": []}
            musicDirs_direct = data["directories"].copy()
            multiPls = {"names": [], "keys": []}
            multiPls_direct = data["multiplaylists"].copy()

            dirIDs = []
            dirIDs_direct = list(musicDirs_direct.keys())
            mplIDs = []
            mplIDs_direct = list(multiPls_direct.keys())
            genre = []

            # generate the music directories and genre!

            for aDir in dirIDs_direct:
                if aDir == musicDirs_direct[aDir].get("id"):
                    if aDir.islower() and musicDirs_direct[aDir]["id"].islower():
                        if EveconLib.Tools.Search(aDir, dirIDs, exact=True):
                            unvalid("A Dir-ID was double (" + aDir + ")")
                            continue
                        if not os.path.exists(musicDir + musicDirs_direct[aDir].get("path")):
                            unvalid("A Dir-Path does not exist (" + musicDirs_direct[aDir].get("path") + ")")
                            continue
                        dirIDs.append(aDir)

                        musicDirs[aDir] = musicDirs_direct[aDir].copy()
                        if musicDirs_direct[aDir].get("genre"):
                            for aGenre in musicDirs_direct[aDir]["genre"]:
                                if aGenre.islower():
                                    if not EveconLib.Tools.Search(aGenre, genre, exact=True):
                                        genre.append(aGenre)
                                else:
                                    unvalid("Genre is not low (" + aGenre + ")")
                        else:
                            musicDirs[aDir]["genre"] = []
                        if not musicDirs_direct[aDir].get("name"):
                            musicDirs[aDir]["name"] = musicDirs[aDir]["path"].split("\\")[-1].title()
                        musicDirs["names"].append(musicDirs[aDir]["name"])
                    else:
                        unvalid("Dir-ID is not low (" + aDir + "/" + musicDirs_direct[aDir]["id"] + ")")
                else:
                    unvalid("Diffrent Dir-IDs (" + aDir + ")")

            musicDirs["keys"] = dirIDs

            # deleting genre
            delGenre = []
            for aGenre_ID in range(len(genre)):
                for aID in dirIDs + mplIDs_direct:  # PROBLEM THE mpl ID arent valid => maybe a genre is deleted
                    if aID == genre[aGenre_ID]:
                        delGenre.append(aGenre_ID)

            for x in delGenre:
                del genre[x]


            if not multiPls_deac:
                for aMPl in mplIDs_direct:  # get a multiplaylist ID
                    if aMPl == multiPls_direct[aMPl].get("id"):
                        if aMPl.islower():
                            if not EveconLib.Tools.Search(aMPl, dirIDs, exact=True):
                                if EveconLib.Tools.Search(aMPl, mplIDs, exact=True):
                                    unvalid("A MPl-ID was double (" + aMPl + ")")
                                    continue
                                mplIDs.append(aMPl)

                                multiPls[aMPl] = multiPls_direct[aMPl].copy()

                                if not multiPls[aMPl].get("name"):
                                    multiPls[aMPl]["name"] = multiPls[aMPl]["id"]
                                if not multiPls[aMPl]["content"].get("ids"):
                                    multiPls[aMPl]["content"]["ids"] = []
                                if not multiPls[aMPl]["content"].get("genre"):
                                    multiPls[aMPl]["content"]["genre"] = []

                                if multiPls[aMPl]["content"]["ids"]:
                                    newIDlist = []
                                    for aID in multiPls[aMPl]["content"]["ids"]:
                                        if EveconLib.Tools.Search(aID, musicDirs["keys"], exact=True):
                                            newIDlist.append(aID)
                                    multiPls[aMPl]["content"]["ids"] = newIDlist
                                multiPls[aMPl]["content"]["all_ids"] = multiPls[aMPl]["content"]["ids"].copy()

                                if multiPls[aMPl]["content"]["genre"]:
                                    newGenrelist = []
                                    for aGenre in multiPls[aMPl]["content"]["ids"]:
                                        if EveconLib.Tools.Search(aGenre, genre, exact=True):
                                            newGenrelist.append(aGenre)
                                    multiPls[aMPl]["content"]["genre"] = newGenrelist

                                    for aGenre in multiPls_direct[aMPl]["content"]["genre"]:
                                        for aDir in dirIDs:
                                            if EveconLib.Tools.Search(aGenre, musicDirs[aDir]["genre"], exact=True) and not EveconLib.Tools.Search(aDir,
                                                                                                                   multiPls[
                                                                                                                       aMPl][
                                                                                                                       "content"][
                                                                                                                       "all_ids"],
                                                                                                                   exact=True):
                                                multiPls[aMPl]["content"]["all_ids"].append(aDir)

                                if not multiPls[aMPl]["content"]["ids"] and not multiPls[aMPl]["content"]["genre"]:
                                    del multiPls[aMPl]
                                    unvalid("No Content in a MPl (" + aMPl + ")")
                                    continue

                                multiPls["names"].append(multiPls[aMPl]["name"])
                                multiPls["keys"].append(multiPls[aMPl]["id"])

                            else:
                                unvalid("MPl-ID is used in the musicDirs (" + aMPl + ")")
                        else:
                            unvalid("MPl-ID is not low (" + aMPl + ")")
                    else:
                        unvalid("Diffrent MPl-IDs (" + aMPl + ")")

            return musicDirs, multiPls, genre, musicDir

        with open("data" + EveconLib.Config.path_seg + "Config" + EveconLib.Config.path_seg + "Music.json") as jsonfile:
            data = json.load(jsonfile)

        self.musiclist, self.multiplaylists, self.genre, self.musicDir = parse(unvalid)
        """

        self.musiclist, self.multiplaylists, self.genre, self.musicDir = self.musicFileEditor.formatForMP()



    def resetInterface(self):
        self.con_main = "pl"
        self.cur_Input = ""
        self.cur_Pos = 0
        self.change = ""
        self.notifications = [] # realy?

    def reloadMusic(self, tracknum):
        if type(tracknum) == int:
            self.music["file" + str(tracknum)]["loaded"] = pyglet.media.load(
                self.music["file" + str(tracknum)]["fullname"])
        elif type(tracknum) == str:
            self.music[tracknum]["loaded"] = pyglet.media.load(self.music[tracknum]["fullname"])

    def make_playlist(self):
        # self.last_playlist = self.playlist.copy()
        if self.playing:
            newPlaylist = []
            for x in range(1, self.music["all_files"] + 1):
                newPlaylist.append("file" + str(x))

            ourID = EveconLib.Tools.Search(self.playlist[0], newPlaylist, exact=True, lower=False)
            del newPlaylist[ourID[0]]
            newPlaylist = [self.playlist[0]] + newPlaylist

            self.playlist = newPlaylist.copy()
        else:
            self.playlist = []
            for x in range(1, self.music["all_files"] + 1):
                self.playlist.append("file" + str(x))

        self.searchlist = self.playlist.copy()
        self.startlist = self.playlist.copy()
        if self.randomizer:
            self.shufflePL()
        self.last_playlist = self.playlist.copy()
        self.resetInterface()

    def shufflePL(self, first=False):
        self.last_playlist = self.playlist.copy()
        if first:
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
            return False
        else:
            lpl = self.playlist.copy()
            self.playlist = self.last_playlist.copy()
            self.last_playlist = lpl.copy()

    def refreshTitle(self):
        if self.getCur()["antype"]:
            EveconLib.Tools.title("OLD", self.getCur()["andata"]["title"], "Now Playing")
        else:
            EveconLib.Tools.title("OLD", self.getCur()["name"], "Now Playing")

    def refresh(self, title=False, printme=True):
        if title:
            self.refreshTitle()
        elif printme:
            self.printit()

    def showBalloonTip(self):
        if self.getCur()["antype"]:
            name = self.getCur()["andata"]["title"]
        else:
            name = self.getCur()["name"]
        if sys.platform == "win32":
            EveconLib.Tools.Windows.BalloonTip("Evecon: MusicPlayer", "Now playing: " + name)

    def getCur(self):
        # if len(self.playlist) == 0 and self.music["all_files"] > 0:
        #    self.make_playlist()
        # elif len(self.playlist) == 0 and self.music["all_files"] == 0:
        #    self.stop()
        if len(self.playlist) == 0:
            self.stop()
        return self.music[self.playlist[0]]

    def rerollThis(self):
        oldPL = self.playlist.copy()
        del oldPL[self.cur_Pos]
        self.playlist = oldPL + [self.playlist[self.cur_Pos]]
        if self.cur_Pos == 0:
            self.next(True)

    def sortPL(self):
        self.playlist.sort()
        self.hardworktime = time.time() + 0.2

    def sortPL_name(self):
        pl_names = []
        for fileX in self.playlist:
            pl_names.append(self.music[fileX]["name"])
        pl_names.sort()

        new_playlist = []
        for name in pl_names:
            for num_file in range(1, self.music["all_files"] + 1):
                if name == self.music["file" + str(num_file)]["name"]:
                    ok = True
                    for x in new_playlist:
                        if x == "file" + str(num_file):
                            ok = False
                    if ok:
                        new_playlist.append("file" + str(num_file))

        self.playlist = new_playlist.copy()
        self.hardworktime = time.time()

    def sortPL_an(self):
        pl_an_file = []
        pl_nonan_file = []

        for fileX in self.playlist:
            if self.music[fileX]["antype"]:
                pl_an_file.append(fileX)
            else:
                pl_nonan_file.append(fileX)

        pl_an_file.sort()
        pl_nonan_file.sort()

        new_playlist = []
        pl_an_name = []

        for an_file in pl_an_file:
            ok = True
            for x in pl_an_name:
                if x == self.music[an_file]["andata"]["animeName"]:
                    ok = False
            if ok:
                pl_an_name.append(self.music[an_file]["andata"]["animeName"])
        pl_an_name.sort()

        for an_name in pl_an_name:
            this_an = []  # files unsortiert
            this_an_name = []  # name unsortiert & sortiert
            new_pl = []  # files sortiert

            for num_file in range(1, self.music["all_files"] + 1):
                if self.music["file" + str(num_file)]["antype"] and an_name == \
                        self.music["file" + str(num_file)]["andata"]["animeName"]:
                    this_an.append("file" + str(num_file))
                    this_an_name.append(self.music["file" + str(num_file)]["name"])

            this_an_name.sort()
            for this_an_name2 in this_an_name:
                for file in this_an:
                    if this_an_name2 == self.music[file]["name"]:
                        new_pl.append(file)
                        break

            new_playlist += new_pl

        pl_nonan_name = []
        for fileX in pl_nonan_file:
            pl_nonan_name.append(self.music[fileX]["name"])
        pl_nonan_name.sort()

        for name in pl_nonan_name:
            for num_file in range(1, self.music["all_files"] + 1):
                if name == self.music["file" + str(num_file)]["name"]:
                    new_playlist.append("file" + str(num_file))

        self.playlist = new_playlist.copy()
        self.hardworktime = time.time()

    # Options

    def play(self):
        self.paused = False
        self.player.play()
        self.hardworktime = time.time() + 0.2

    def pause(self):
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

    def mute(self):
        self.muted = True
        self.mute_vol = self.volumep
        self.volp(0)

    def unmute(self):
        self.muted = False
        self.volp(self.mute_vol)

    def stop(self):
        # noinspection PyGlobalUndefined
        global musicrun
        musicrun = True

        self.musicrun = False
        self.playing = False
        self.paused = False
        self.running = False
        self.scanner.running = False

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
        try:
            #EveconLib.Config.globalMPports.remPort(self.server.port)  # autodelete
            EveconLib.Config.globalMPportsJava.remPort(self.server_java.port)
        except AttributeError:
            pass

    def next(self, skipthis=False):
        if skipthis:
            self.skip_del = True
        self.playing = False
        if self.paused:
            self.paused = False
            self.player.play()
        self.hardworktime = time.time() + 0.2

    def DelById(self, num):
        # num = Search(plfile, self.playlist)[0]
        if num == 0 and self.stop_del:
            self.stop()
        if num > len(self.playlist) - 1:
            return False

        if self.cur_Pos >= len(self.playlist) - 1:
            self.cur_Pos -= 1

        del self.playlist[num]

        if num == 0:
            self.next(True)

    def DelByFile(self, plfile):
        numList = EveconLib.Tools.Search(plfile, self.playlist)
        if len(numList) == 0:
            return False  # already deleted

        num = numList[0]
        if num == 0 and self.stop_del:
            self.stop()
        if num > len(self.playlist) - 1:
            return False

        file = self.playlist[0]
        file_del = self.playlist[num]

        if self.cur_Pos >= len(self.playlist) - 1:
            self.cur_Pos -= 1

        del self.playlist[num]

        if file == file_del:
            self.next(True)

    def DelByKey(self, key):
        """
        this will delete musicfiles from the playlist

        :param key: the key from the musicFileEditor
        :return:
        """

        if not key in self.music["active"]:
            return False  # key not loaded

        if self.multiplaylists.get(key):  # key is a multiPL and not a normal
            for singleKey in self.multiplaylists[key]["content"]["all_ids"]:
                self.DelByKey(singleKey)
            return True

        nextFile = False
        corrector = 0
        for plIndex in range(len(self.playlist)):
            if self.music[self.playlist[plIndex + corrector]]["key"] == key:
                if plIndex == 0 + corrector:
                    nextFile = True
                del self.playlist[plIndex + corrector]
                corrector -= 1

        if nextFile:
            self.next(True)


    def vol(self, vol):
        self.volume = vol
        if sys.platform == "win32":
            EveconLib.Tools.Windows.Volume.change(vol)

    def volp(self, vol):
        self.volumep = vol
        self.player.volume = self.volumep

    def queueById(self, pos):
        # ID OF THE self.playlist!
        oldPL = self.playlist.copy()
        del oldPL[pos]
        del oldPL[0]
        self.playlist = [self.playlist[0]] + [self.playlist[pos]] + oldPL
        self.hardworktime = time.time()

    def queueByFile(self, plfile):
        res = EveconLib.Tools.Search(plfile, self.playlist)
        if not res:
            oldPL = self.playlist.copy()
            del oldPL[0]
            self.playlist = [self.playlist[0], plfile] + oldPL
            self.hardworktime = time.time()
        else:
            oldPL = self.playlist.copy()
            del oldPL[res[0]]
            del oldPL[0]
            self.playlist = [self.playlist[0], plfile] + oldPL
            self.hardworktime = time.time()

    def refreshSearch(self):
        self.cur_Pos = 0

        if self.cur_Search != "":
            namelist = []

            # for x in self.startlist:
            if self.last_backspace:
                for x in self.startlist:
                    namelist.append(self.music[x]["name"])
            else:
                for x in self.searchlist:
                    namelist.append(self.music[x]["name"])

            found = EveconLib.Tools.Search(self.cur_Search, namelist)

            searchlist_name = []
            for x in found:
                searchlist_name.append(namelist[x])
            searchlist_name.sort()

            # music_dir = self.music.copy()

        else:
            searchlist_name = []
            for fileX in self.startlist:
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

        np = EveconLib.Tools.DelDouble(new_playlist)

        self.searchlist = np.copy()

    def run(self):
        if not self.music:
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
        while self.musicrun:

            if self.music[self.playlist[0]]["loaded"].is_queued:
                self.reloadMusic(self.playlist[0])

            if self.balloonTip:
                self.showBalloonTip()

            self.player.queue(self.music[self.playlist[0]]["loaded"])
            self.player.play()

            self.timer.start()

            self.player.volume = self.volumep

            self.running = True
            self.playing = True

            self.allowPrint = True
            self.refreshTitle()

            self.printit()
            self.last_print_auto = time.time()
            while self.playing:

                time.sleep(0.15)
                for x in range(5):
                    if self.player.time == 0:
                        self.playing = False
                    elif round(self.getCur()["loaded"].duration) <= round(self.timer.getTime()):
                        self.playing = False
                    time.sleep(0.1)

                    self.refresh(title=False, printme=self.selfprint)

                while self.paused:
                    self.timer.pause()
                    # Vll. hier spl pause command einfügen
                    # self.splmp.
                    while self.paused:
                        time.sleep(0.25)

                    self.timer.unpause()
                    self.refresh(title=True, printme=self.selfprint)

                    # if self.spl:
                    #    self.splmp.PlaytimeStart += time.time() - music_time_wait
                    #    self.splmp.TimeLeftStart += time.time() - music_time_wait

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
                        "screentime": screentime + 100,
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

        if self.getCur()["antype"]:
            outputList.append(
                "Playing: \n%s \nFrom %s" % (self.getCur()["andata"]["title"], self.getCur()["andata"]["animeName"]))
        else:
            outputList.append("Playing: \n%s" % self.getCur()["name"])

        outputList.append("Time: %s\\%s" % (self.timer.getTimeFor(), EveconLib.Tools.TimeFor(self.getCur()["loaded"].duration)))
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
                                        if len(self.music[self.playlist[word_num]]["name"]) > 108:
                                            outputList.append(" " + word_num_str + " * " + EveconLib.Tools.getPartStr(
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
                                            outputList.append(" " + word_num_str + "   " + EveconLib.Tools.getPartStr(
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
                                                outputList.append(" " + word_num_str + " * " + EveconLib.Tools.getPartStr(
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
                                                outputList.append(" " + word_num_str + "   " + EveconLib.Tools.getPartStr(
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
                                            outputList.append(" " + word_num_str + " * " + EveconLib.Tools.getPartStr(
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
                                            outputList.append(" " + word_num_str + "   " + EveconLib.Tools.getPartStr(
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
                                        outputList.append(" " + word_num_str + " * " + EveconLib.Tools.getPartStr(
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
                                        outputList.append(" " + word_num_str + "   " + EveconLib.Tools.getPartStr(
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
                                    " " + word_num_str + " * " + EveconLib.Tools.getPartStr(self.music[self.playlist[word_num]]["name"],
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
                                    " " + word_num_str + "   " + EveconLib.Tools.getPartStr(self.music[self.playlist[word_num]]["name"],
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
            outputList.append("Duration: " + str(EveconLib.Tools.TimeFor(self.music["file1"]["loaded"].duration)))

            if self.music[self.playlist[self.cur_Pos]]["antype"]:
                outputList.append("Title: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["title"]))
                outputList.append(
                    "Interpreter: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["interpreter"]))
                outputList.append("Musictype: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["musictype"]))
                outputList.append("Animename: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["animeName"]))
                if self.music[self.playlist[self.cur_Pos]]["andata"].get("animeSeason"):
                    outputList.append("Season: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["animeSeason"]))
                if self.music[self.playlist[self.cur_Pos]]["andata"].get("animeType"):
                    outputList.append("Type: " + str(self.music[self.playlist[self.cur_Pos]]["andata"]["animeType"]) +
                                      str(self.music[self.playlist[self.cur_Pos]]["andata"]["animeTypeNum"]))

            outputList.append("Filename: " + self.music[self.playlist[self.cur_Pos]]["name"])
            outputList.append("Parantkey: " + self.music[self.playlist[self.cur_Pos]]["key"])
            outputList.append("Filepath: " + self.music[self.playlist[self.cur_Pos]]["fullname"])
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
                                        if len(self.music[self.searchlist[word_num]]["name"]) > 108:
                                            outputList.append(" " + word_num_str + " * " + EveconLib.Tools.getPartStr(
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
                                            outputList.append(" " + word_num_str + "   " + EveconLib.Tools.getPartStr(
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
                                                outputList.append(" " + word_num_str + " * " + EveconLib.Tools.getPartStr(
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
                                                outputList.append(" " + word_num_str + "   " + EveconLib.Tools.getPartStr(
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
                                            outputList.append(" " + word_num_str + " * " + EveconLib.Tools.getPartStr(
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
                                            outputList.append(" " + word_num_str + "   " + EveconLib.Tools.getPartStr(
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
                                        outputList.append(" " + word_num_str + " * " + EveconLib.Tools.getPartStr(
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
                                        outputList.append(" " + word_num_str + "   " + EveconLib.Tools.getPartStr(
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
                                    " " + word_num_str + " * " + EveconLib.Tools.getPartStr(
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
                                    " " + word_num_str + "   " + EveconLib.Tools.getPartStr(
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
            for mus in self.music["active"]:
                cur += mus + ", "
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
            for mus in self.music["active"]:
                cur += mus + ", "
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

    def react(self, inp):
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
                    del oldPL[EveconLib.Tools.Search(self.searchlist[self.cur_Pos], self.searchlist)[0]]
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
            del oldPL[EveconLib.Tools.Search(self.searchlist[self.cur_Pos], self.searchlist)[0]]
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
                self.volp(float(self.cur_Input))
                self.cur_Input = ""
                self.change = ""
                self.con_cont = "set"

        elif self.change == "volw":
            if inp == "return":
                if len(self.cur_Input) > 4:
                    self.cur_Input = EveconLib.Tools.getPartStr(self.cur_Input, begin=0, end=4)
                self.vol(float(self.cur_Input))
                self.cur_Input = ""
                self.change = ""
                self.con_cont = "set"

        elif self.change == "spe":
            if inp == "return":
                self.spl.ChEffect(int(self.cur_Input))
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
            self.musicKeysLeft = self.musiclist["keys"].copy()
            for needToDel in self.music["active"]:
                del self.musicKeysLeft[EveconLib.Tools.Search(needToDel, self.musicKeysLeft, exact=True, lower=False)[0]]

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
            self.queueById(self.cur_Pos)
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

