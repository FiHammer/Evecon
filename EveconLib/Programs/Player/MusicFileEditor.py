import json
import os

import EveconLib.Config
import EveconLib.Tools

class MusicFileEditor:
    def __init__(self, specialFilePath=None):
        self.minVersion = "1.1"
        self.latestVersion = "1.1"
        self.forbiddenIDs = ["names", "ids"]

        self.nFilePath = EveconLib.Config.MusicFile  # normal file path
        self.bFilePath = EveconLib.Config.backupMusicFile  # backup file path

        self.filePath = None
        self.specialPath = specialFilePath

        self.data = None
        self.setFilePath = False
        # data vars from file

        self.version = None
        self.pc = None
        self.musicDir = None

        self.musicDirs = None
        self.multiPls = None
        self.genre = None

        # easily parsed lists (dirs)

        self.keyToPath = {}  # all normal keys
        self.multiKeyToKeyList = {}  # all multi keys (mpl, genre)

    def formatEasy(self):
        self.multiKeyToKeyList.clear()
        self.keyToPath.clear()
        for key in self.multiPls["keys"]:
            self.multiKeyToKeyList[key] = self.multiPls[key]["content"]["all_ids"]
        for genreKey in self.genre:
            self.multiKeyToKeyList[genreKey] = []

        for key in self.musicDirs["keys"]:
            for genre in self.musicDirs[key]["genre"]:  # appending for genre search
                self.multiKeyToKeyList[genre].append(key)
            self.keyToPath[key] = self.musicDir + self.musicDirs[key]["path"]

    def readFile(self):
        if not self.setFilePath:
            self.chooseFilePath()
        with open(self.filePath) as jsonfile:
            data = json.load(jsonfile)

        result = self.decodeJson(data)
        if result:
            self.data = data
            self.musicDirs, self.multiPls, self.genre, self.musicDir, self.version, self.pc = result
            self.formatEasy()

    def vertifyFile(self, filePath):
        """
        vertifies the filepath
        :param filePath: filepath
        :return: vertification
        """
        if os.path.exists(filePath):
            with open(filePath) as jsonfile:
                data = json.load(jsonfile)
            if self.decodeJson(data):
                return True
            else:
                return False
        return False

    def chooseFilePath(self):
        """
        :return: if the specialPath got used: 2, 1 = normal, 0=backup
        """
        if self.specialPath:
            if self.vertifyFile(self.specialPath):
                self.filePath = self.specialPath
                self.setFilePath = True
                return 2
        else:
            if self.vertifyFile(self.nFilePath):
                self.filePath = self.nFilePath
                self.setFilePath = True
                return 1
            else:
                self.filePath = self.bFilePath
                self.setFilePath = True
                return 0

    def setSpecialFilePath(self, spFilePath):
        """
        resets the spcial file path
        :param spFilePath: filepath
        :return: special filepath was set correctly and is valid
        """
        self.setFilePath = False
        self.specialPath = spFilePath
        if self.chooseFilePath() == 2:
            return True
        else:
            return False

    def writeFile(self, specialFilePath=None):
        data = self.encodeData(self.musicDirs.copy(), self.multiPls.copy(), self.genre.copy(), self.musicDir,
                               self.version, self.pc)
        if data:
            if specialFilePath:
                filePath = specialFilePath
            else:
                filePath = self.filePath
            self.data = data
            with open(filePath, "w") as jsonfile:
                json.dump(data, jsonfile, indent=4, sort_keys=True)

            if specialFilePath:
                self.setSpecialFilePath(specialFilePath)

    def formatForMP(self):
        """
        formats the file compatible with the musicplayer
        :return: the dir for the mp
        """
        if not self.data:
            self.readFile()
        return self.musicDirs, self.multiPls, self.genre, self.musicDir

    # noinspection PyTypeChecker
    def decodeJson(self, data):
        """
        vertifies the data

        :param data: needs to be the formatted json
        :return: musicDirs, multiPls, genre, musicDir, version, pc
        """

        def errorPrinter(error, key=False):
            if not key:
                print("Musicfile is not valid:\n" + error)
            else:
                print("Musicfile is not valid:\nKey not found! (" + error + ")")

            return False

        if data.get("pc") != EveconLib.Config.computer:
            if data.get("pc") != "global":
                return errorPrinter("Wrong PC!")
        if data.get("version"):
            if not data["version"] >= self.minVersion:
                return errorPrinter("Wrong Version! (" + self.minVersion + " required)")
        else:
            return errorPrinter("version", True)

        if data.get("musicDir"):
            if os.path.exists(data["musicDir"]):
                musicDir = data["musicDir"] + "\\"
            else:
                return errorPrinter("Wrong musicDir path")
        else:
            return errorPrinter("musicDir", True)

        if not data.get("directories"):
            return errorPrinter("directories", True)
        if not data.get("multiplaylists"):
            multiPls_deac = True
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
                        errorPrinter("A Dir-ID was double (" + aDir + ")")
                        continue
                    if not os.path.exists(musicDir + musicDirs_direct[aDir].get("path")):
                        errorPrinter("A Dir-Path does not exist (" + musicDirs_direct[aDir].get("path") + ")")
                        continue
                    dirIDs.append(aDir)

                    musicDirs[aDir] = musicDirs_direct[aDir].copy()
                    if musicDirs_direct[aDir].get("genre"):
                        for aGenre in musicDirs_direct[aDir]["genre"]:
                            if aGenre.islower():
                                if not EveconLib.Tools.Search(aGenre, genre, exact=True):
                                    genre.append(aGenre)
                            else:
                                errorPrinter("Genre is not low (" + aGenre + ")")
                    else:
                        musicDirs[aDir]["genre"] = []
                    if not musicDirs_direct[aDir].get("name"):
                        musicDirs[aDir]["name"] = musicDirs[aDir]["path"].split("\\")[-1].title()
                    musicDirs["names"].append(musicDirs[aDir]["name"])
                else:
                    errorPrinter("Dir-ID is not low (" + aDir + "/" + musicDirs_direct[aDir]["id"] + ")")
            else:
                errorPrinter("Diffrent Dir-IDs (" + aDir + ")")

        musicDirs["keys"] = dirIDs

        # deleting genre
        delGenre = []
        for aGenre_ID in range(len(genre)):
            for aID in dirIDs + mplIDs_direct:  # PROBLEM THE mpl ID arent valid => maybe a genre is deleted
                if aID == genre[aGenre_ID]:
                    delGenre.append(aGenre_ID)

        for x in delGenre:
            del genre[x]

        # generate mpl

        if not multiPls_deac:
            for aMPl in mplIDs_direct:  # get a multiplaylist ID
                if aMPl == multiPls_direct[aMPl].get("id"):
                    if aMPl.islower():
                        if not EveconLib.Tools.Search(aMPl, dirIDs, exact=True):
                            if EveconLib.Tools.Search(aMPl, mplIDs, exact=True):
                                errorPrinter("A MPl-ID was double (" + aMPl + ")")
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
                                errorPrinter("No Content in a MPl (" + aMPl + ")")
                                continue

                            multiPls["names"].append(multiPls[aMPl]["name"])
                            multiPls["keys"].append(multiPls[aMPl]["id"])

                        else:
                            errorPrinter("MPl-ID is used in the musicDirs (" + aMPl + ")")
                    else:
                        errorPrinter("MPl-ID is not low (" + aMPl + ")")
                else:
                    errorPrinter("Diffrent MPl-IDs (" + aMPl + ")")

        return musicDirs, multiPls, genre, musicDir, data["version"], data["pc"]

    # noinspection PyTypeChecker
    def encodeData(self, musicDirs, multiPls, genre, musicDir, versionX, pcX):
        """
        encodes the data to a json (dir)

        :return: directory
        """

        def errorPrinter(error):
            print("Musicdata is not valid:\n" + error)

            return False

        data = {"version": versionX, "pc": pcX, "musicDir": musicDir, "directories": {}, "multiplaylists": {}}

        if not self.minVersion <= versionX <= self.latestVersion:
            return errorPrinter(
                "Version out of range (Min: %s, Max: %s, Data's: %s" % (self.minVersion, self.latestVersion, versionX))

        if not os.path.exists(musicDir):
            return errorPrinter("musicDir does not exist")

        if not musicDirs:
            return errorPrinter("musicDirs empty")

        for directory in musicDirs["keys"]:
            data["directories"][directory] = {"id": directory, "path": musicDirs[directory]["path"],
                                              "genre": musicDirs[directory]["genre"],
                                              "name": musicDirs[directory]["name"]}

        if multiPls:

            for directory in multiPls["keys"]:
                data["multiplaylists"][directory] = {"id": directory, "name": multiPls[directory]["name"],
                                                     "content": {
                                                         "ids": multiPls[directory]["content"]["ids"],
                                                         "genre": multiPls[directory]["content"]["genre"]
                                                     }}

        return data

    def addMusicDir(self, idX, path, name=None, genre=None):
        """
        adds a new music dir
        :param idX: the id does not exist already
        :param path: the path of the dir
        :param name: a name
        :param genre: a genre in array form
        :return: success
        """
        if os.path.exists(path) and not id in self.forbiddenIDs and not id in self.musicDirs["keys"]:
            if not name:
                name = idX
            idX = idX.lower()
            if genre:
                for aGenID in range(len(genre)):
                    genre[aGenID] = genre[aGenID].lower()
                    if not genre[aGenID] in self.genre:
                        self.genre.append(genre[aGenID])
            else:
                genre = []

            self.musicDirs["names"].append(name)
            self.musicDirs["keys"].append(idX)
            self.musicDirs[idX] = {"id": idX, "name": name, "path": path, "genre": genre}

            return True
        else:
            return False