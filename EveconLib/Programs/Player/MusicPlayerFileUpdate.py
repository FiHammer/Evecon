import EveconLib
import pyglet
import os

PS = EveconLib.Config.path_seg  # shortcut
AFT = EveconLib.Config.MP_ALLOWEDFILETYPES  # file types to accept


class MusicFileDir:
    def __init__(self, fullPath, mfl, parent=None):
        self.path = fullPath
        self.mfl = mfl  # to add this object and the children in the right (things)

        self.parent = parent
        self.children = []
        self.childrenDirs = []
        self.childrenFiles = []

        self.id = 0

        self.validation = None
        self.loaded = False

    def validate(self):
        if not os.path.exists(self.path):
            self.validation = False
            return False  # does not exist

        content = os.listdir(self.path)
        for contPart in content:
            if os.path.isdir(self.path + PS + contPart):
                self.validation = True
                return True  # found another dir
            elif os.path.isfile(self.path + PS + contPart):
                for fileTyp in AFT:
                    if EveconLib.Tools.rsame(contPart, fileTyp):
                        self.validation = True
                        return True  # found a valid music file
            else:
                continue # what is this ?

        self.validation = False
        return False  # found nothing valid (empty or unvalid files)

    def index(self):
        if self.validation is None:
            self.validate()
        if not self.validation:
            return False  # not a valid dir => will not index

        self.id = self.mfl.getNewDirId()

        content = os.listdir(self.path)

        for contPart in content:
            if os.path.isdir(self.path + PS + contPart):
                mDir = MusicFileDir(self.path + PS + contPart, mfl=self.mfl, parent=self)
                if mDir.validate():
                    self.children.append(mDir)
                    self.childrenDirs.append(mDir)
                    mDir.index()

            elif os.path.isfile(self.path + PS + contPart):
                mFile = MusicFile(self.path + PS + contPart, mfl=self.mfl, parent=self)
                if mFile.validate():
                    self.children.append(mFile)
                    self.childrenFiles.append(mFile)
                    mFile.loadInfo()
            else:
                pass  # what is this ?

        # adding to mfl lists

        if not self.parent:
            self.mfl.files_root.append(self)
            self.mfl.files_rootStatic[self.id] = self

        self.mfl.files_allList.append(self)
        self.mfl.files_allListStatic["dir" + str(self.id)] = self

        self.mfl.files_allDirs.append(self)
        self.mfl.files_allDirsStatic[self.id] = self


        self.loaded = True

class MusicFile:
    def __init__(self, fullPath, mfl, parent=None):
        self.path = fullPath
        self.mfl = mfl

        self.parent = parent


        self.file = fullPath.split(PS)[-1]
        self.fileExt = self.file.split(".")[-1]
        self.fileName = ""

        self.anData = None
        self.pygletData = None

        self.id = 0

        self.validation = None
        self.loaded = False

        self.loadedPygletData = False

    def validate(self):
        if not os.path.exists(self.path):
            self.validation = False
            return False  # does not exist

        if not self.fileExt in AFT and not os.path.isfile(self.path):
            self.validation = False
            return False  # not valid extension or is not a file

        self.validation = True
        return True  # ok


    def loadInfo(self):
        if self.validation is None:
            self.validate()
        if not self.validation:
            return False  # not a valid file => will not load for info

        self.id = self.mfl.getNewFileId()

        self.fileName = ""
        for splitPart in self.file.split("."):
            self.fileName += splitPart + "."
        self.fileName.rstrip(".")

        self.anData = EveconLib.Tools.MusicEncode(self.fileName)

        # adding to mfl lists

        self.mfl.files_allList.append(self)
        self.mfl.files_allListStatic["file" + str(self.id)] = self

        self.mfl.files_allFiles.append(self)
        self.mfl.files_allFilesStatic[self.id] = self

        self.loaded = True

    def loadForPyglet(self):
        if self.loaded and self.validation:
            self.pygletData = pyglet.media.load(self.path)
            self.loadedPygletData = True



class MusicFileLoader:
    def __init__(self, notificationFunc=None, neverPrint=False):
        self.musicFileEditor = EveconLib.Programs.Player.MusicFileEditor()

        self.notificationFunc = notificationFunc
        self.neverPrint = neverPrint

        self.refreshMusicList()


        # save possibilities

        self.files_root = []  # a list equal to the directory tree
        self.files_rootStatic = {}  # a static list (access with id as a int) equal to the directory tree

        self.files_allList = []  # all things unsorted in a list
        self.files_allListStatic = {}  # all things in a static list (access with file/dir + id as a str)

        self.files_allFiles = []  # all files unsorted
        self.files_allFilesStatic = {}  # same static
        self.files_allDirs = []  # all dirs unsorted
        self.files_allDirsStatic = {}  # same static

        self.files_dirQuan = 0
        self.files_fileQuan = 0


    def getNewDirId(self):
        self.files_dirQuan += 1
        return self.files_dirQuan - 1 # to start from 0

    def getNewFileId(self):
        self.files_fileQuan += 1
        return self.files_fileQuan - 1 # to start from 0


    def refreshMusicList(self):
        self.musicFileEditor.readFile()

    def addMusic(self, key, cusPath="", printStaMSG=True, printEndMSG=True, makeNoti=False):  # key (AN, LIS)
        suc = None
        if key in self.musicFileEditor.multiKeyToKeyList:
            if printStaMSG and not self.neverPrint:
                EveconLib.Tools.cls()
                print("Loading key list %s..." % key.title())

            for aKey in self.musicFileEditor.multiKeyToKeyList[key]:
                self.addMusic(aKey, printStaMSG=False, printEndMSG=printEndMSG, makeNoti=makeNoti)
        elif key in self.musicFileEditor.keyToPath:
            if printStaMSG and not self.neverPrint:
                EveconLib.Tools.cls()
                print("Loading key %s..." % key.title())

            suc = self.loadDir(self.musicFileEditor.keyToPath[key])
        elif key == "all":
            for aKey in self.musicFileEditor.keyToPath[key]:
                self.addMusic(aKey, printStaMSG=False, printEndMSG=printEndMSG, makeNoti=makeNoti)
        elif key == "cus":
            if not os.path.exists(cusPath):
                return False
            suc = self.loadDir(cusPath)
        elif key == "us":
            suc = self.loadDir("Music" + EveconLib.Config.path_seg + "User")
        else:
            return False


        if printEndMSG and not self.neverPrint:
            print("Finished: " + key + " Success: " + str(suc))

        if makeNoti and self.notificationFunc:
            self.notificationFunc(key.title(), title="Finished loading", screentime=2.5)
        return True


    def loadDir(self, dirPath):
        mDir = MusicFileDir(dirPath, mfl=self)
        if mDir.validate():
            mDir.index()
            return True

        return False
