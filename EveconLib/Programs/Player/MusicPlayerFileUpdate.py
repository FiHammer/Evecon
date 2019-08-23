import EveconLib
import pyglet
import os
import threading


from queue import Queue as queue_Queue


PS = EveconLib.Config.path_seg  # shortcut
AFT = EveconLib.Config.MP_ALLOWEDFILETYPES  # file types to accept


class MusicFileDir:
    def __init__(self, fullPath, mfl, parentKey="None", parent=None):
        self.path = fullPath
        self.mfl = mfl  # to add this object and the children in the right (things)

        self.parent = parent
        self.parentKey = parentKey
        self.children = []
        self.childrenDirs = []
        self.childrenFiles = []

        self.dirName = fullPath.split(PS)[-1]

        self.id = 0

        self.validation = None
        self.loaded = False

    def getExtChildrenFiles(self):
        # this method will generate a list with every file object including files in childrenDirs
        output = self.childrenFiles.copy()
        for childDir in self.childrenDirs:
            output += childDir.getExtChildrenFiles()

        return output

    def getExtChildrenFileIds(self):
        # this method will generate a list with every file id including files in childrenDirs
        allObj = self.getExtChildrenFiles()
        output = []
        for file in allObj:
            output.append(file.id)
        return output


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
                mDir = MusicFileDir(self.path + PS + contPart, mfl=self.mfl, parent=self, parentKey=self.parentKey)
                if mDir.validate():
                    self.children.append(mDir)
                    self.childrenDirs.append(mDir)
                    mDir.index()

            elif os.path.isfile(self.path + PS + contPart):
                mFile = MusicFile(self.path + PS + contPart, mfl=self.mfl, parent=self, parentKey=self.parentKey)
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


        if not self.mfl.files_keySorted_allList.get(self.parentKey):
            self.mfl.files_keySorted_allList[self.parentKey] = []

        self.mfl.files_keySorted_allList[self.parentKey].append(self)

        if not self.mfl.files_keySorted_allListStatic.get(self.parentKey):
            self.mfl.files_keySorted_allListStatic[self.parentKey] = {}
        self.mfl.files_keySorted_allListStatic[self.parentKey]["dir" + str(self.id)] = self

        if not self.mfl.files_keySorted_allDirs.get(self.parentKey):
            self.mfl.files_keySorted_allDirs[self.parentKey] = []
        self.mfl.files_keySorted_allDirs[self.parentKey].append(self)

        if not self.mfl.files_keySorted_allDirsStatic.get(self.parentKey):
            self.mfl.files_keySorted_allDirsStatic[self.parentKey] = {}
        self.mfl.files_keySorted_allDirsStatic[self.parentKey][self.id] = self


        self.loaded = True

    def loadForPyglet(self, onlyFirstLoad=False):  # meaning: loadChildrenForPyglet
        for child in self.children:  # loading the children
            child.loadForPyglet(onlyFirstLoad)


class MusicFile:
    def __init__(self, fullPath, mfl, parent=None, parentKey="None"):
        self.path = fullPath
        self.mfl = mfl

        self.parent = parent
        self.parentKey = parentKey


        self.file = fullPath.split(PS)[-1]
        self.fileExt = self.file.split(".")[-1]
        self.fileName = ""

        self.anData = None
        self.pygletData = None

        self.id = 0

        self.validation = None
        self.loaded = False
        self.active = False

        self.loadedPygletData = False


    def validate(self):
        if not os.path.exists(self.path):
            self.validation = False
            return False  # does not exist

        if not self.fileExt in AFT or not os.path.isfile(self.path):
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


        if not self.mfl.files_keySorted_allList.get(self.parentKey):
            self.mfl.files_keySorted_allList[self.parentKey] = []
        self.mfl.files_keySorted_allList[self.parentKey].append(self)

        if not self.mfl.files_keySorted_allListStatic.get(self.parentKey):
            self.mfl.files_keySorted_allListStatic[self.parentKey] = {}
        self.mfl.files_keySorted_allListStatic[self.parentKey]["file" + str(self.id)] = self

        if not self.mfl.files_keySorted_allFiles.get(self.parentKey):
            self.mfl.files_keySorted_allFiles[self.parentKey] = []
        self.mfl.files_keySorted_allFiles[self.parentKey].append(self)

        if not self.mfl.files_keySorted_allFilesStatic.get(self.parentKey):
            self.mfl.files_keySorted_allFilesStatic[self.parentKey] = {}
        self.mfl.files_keySorted_allFilesStatic[self.parentKey][self.id] = self

        self.loaded = True

    def loadForPyglet(self, onlyFirstLoad=False):
        if self.loadedPygletData and onlyFirstLoad:
            return   # the data is already loaded and parm true => will not load again
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


        self.files_keySorted_allList = {}  # all things unsorted in a list, but sorted in the dict with key:list
        self.files_keySorted_allListStatic = {}  # all things in a static list (access (first with playlistKey) with file/dir + id as a str), but sorted in the dict with key:list

        self.files_keySorted_allFiles = {}  # all files unsorted, but sorted in the dict with key:list
        self.files_keySorted_allFilesStatic = {}  # same static
        self.files_keySorted_allDirs = {}  # all dirs unsorted, but sorted in the dict with key:list
        self.files_keySorted_allDirsStatic = {}  # same static


        #self.files_active_allList = {}  # all things unsorted in a list, but sorted in the dict with key:list
        #self.files_active_allListStatic = {}  # all things in a static list (access (first with playlistKey) with file/dir + id as a str), but sorted in the dict with key:list

        #self.files_active_allFiles = {}  # all files unsorted, but sorted in the dict with key:list
        #self.files_active_allFilesStatic = {}  # same static


        self.loadedKeys = []  # pygletLoaded
        self.indexedKeys = []  # indexed

    def getNewDirId(self):
        self.files_dirQuan += 1
        return self.files_dirQuan - 1 # to start from 0

    def getNewFileId(self):
        self.files_fileQuan += 1
        return self.files_fileQuan - 1 # to start from 0


    def refreshMusicList(self):
        self.musicFileEditor.readFile()

    def addMusic(self, key, cusPath="", printStaMSG=True, printEndMSG=True, makeNoti=False, loadForPyglet=True):  # key (AN, LIS)
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

            suc = self.loadDir(self.musicFileEditor.keyToPath[key], key)
        elif key == "all":
            for aKey in self.musicFileEditor.keyToPath[key]:
                self.addMusic(aKey, printStaMSG=False, printEndMSG=printEndMSG, makeNoti=makeNoti)
        elif key == "cus":
            if not os.path.exists(cusPath):
                return False
            suc = self.loadDir(cusPath, key)
        elif key == "us":
            suc = self.loadDir("Music" + EveconLib.Config.path_seg + "User", key)
        else:
            return False

        self.indexedKeys.append(key)
        EveconLib.Tools.Log("MusicFileLoader (addMusic)", "Begin to load files for pyglet from the key %s" % key)

        self.reloadKey(key, onlyFirstLoad=True, threadLoad=True)

        self.loadedKeys.append(key)
        if printEndMSG and not self.neverPrint:
            print("Finished: " + key + " Success: " + str(suc))

        if makeNoti and self.notificationFunc:
            self.notificationFunc(key.title(), title="Finished loading", screentime=2.5)
        return True


    def loadDir(self, dirPath, parentKey="None"):
        mDir = MusicFileDir(dirPath, mfl=self, parentKey=parentKey)
        if mDir.validate():
            mDir.index()
            return True

        return False

    def reloadFile(self, file, onlyFirstLoad=False, threadLoad=False):
        if type(file) != str:  # if int is given parse to str
            file = str(file)
        if not EveconLib.Tools.lsame(file, "file"):  # try to catch part if only file id is given
            file = "file" + file

        if threadLoad:
            pass  # disabled for single files

        self.files_allFilesStatic[file].loadForPyglet(onlyFirstLoad)

    def reloadDir(self, dirId, onlyFirstLoad=True, threadLoad=False):
        if type(dirId) != str:  # if int is given parse to str
            dirId = str(dirId)
        if not EveconLib.Tools.lsame(dirId, "dir"):  # try to catch part if only dir id is given
            dirId = "dir" + dirId

        if threadLoad:
            self.reloadThingsInThreads(self.files_allDirsStatic[dirId].getExtChildrenFiles(), specTyp=2, onlyFirstLoad=onlyFirstLoad)
            return

        self.files_allDirsStatic[dirId].loadForPyglet(onlyFirstLoad)


    def reloadThing(self, thingId: str, onlyFirstLoad=False, threadLoad=False):
        if threadLoad:
            pass  # disabled for single things
            #self.reloadThingsInThreads([self.files_allListStatic[thingId]], specTyp=2,
            #                           onlyFirstLoad=onlyFirstLoad)
            #return


        self.files_allListStatic[thingId].loadForPyglet(onlyFirstLoad)

    def reloadKey(self, key: str, onlyFirstLoad=True, threadLoad=True):
        # important onlyFirstLoad AND threadLoad is set to TRUE
        if not key in self.indexedKeys:
            raise EveconLib.EveconExceptions.KeyNotIndexedError(key)

        self.reloadThingsInThreads(self.files_keySorted_allFiles[key], specTyp=2, onlyFirstLoad=onlyFirstLoad)


    def reloadThingsInThreads(self, things: list, specTyp=-1, onlyFirstLoad=True):
        """

        :param things: list including ids
        :param specTyp: -1 no type => things must be strs and begin with file/dir
                        0  file    => things can be strs (file+x) or int (only x)
                        1  dir     => things can be strs (dir+x) or in (only x)
                        2  object  => things must be MusicFile
        :param onlyFirstLoad: load files only one time
        """
        q = queue_Queue()
        num_workers = EveconLib.Config.cores * 2

        def do_work(data):
            if data[2] == -1:  # specTyp
                self.reloadThing(data[0], data[1], False)  # 0: file id; 1: load a second time; 2: no thread load
            elif data[2] == 0:
                self.reloadFile(data[0], data[1], False)  # 0: file id; 1: load a second time; 2: no thread load
            elif data[2] == 1:
                self.reloadDir(data[0], data[1], False)  # 0: file id; 1: load a second time; 2: no thread load
            elif data[2] == 2:
                data[0].loadForPyglet(data[1])

        def worker():
            while True:
                data = q.get()
                if data is None:
                    break
                do_work(data)
                q.task_done()

        threads_used = []

        for numfile in things:
            q.put((numfile, onlyFirstLoad, specTyp))

        for i in range(num_workers):
            q.put(None)

        for i in range(num_workers):
            t = threading.Thread(target=worker)
            t.start()
            threads_used.append(t)

        for i in threads_used:
            i.join()
