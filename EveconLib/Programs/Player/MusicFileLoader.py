import EveconLib
import pyglet
import os
import threading


from queue import Queue as queue_Queue


PS = EveconLib.Config.path_seg  # shortcut
AFT = EveconLib.Config.MP_ALLOWEDFILETYPES  # file types to accept

class MusicKey:
    def __init__(self, key: str, mfl, mfe, parentKey=None, cusPath="", activeList=None):
        self.key = key
        self.mfl = mfl
        self.mfe = mfe  # music file editor: to check if key exist and get path ...
        self.activeList = activeList

        self.cusPath = cusPath  # used if the key is "cus"

        self.path = None  # will be set after validation/ or no path exist (e.g.: mpl)

        self.parentKey = parentKey
        self.children = []  # the music directory (only index 0) OR other musicKeys

        self.id = -1

        self.validation = -1  # -1: not done, 0: false, 1: partly (used for a mpl key), 2: true
        self.loaded =  -1  # -1: not done, 0: false, 1: partly (used for a mpl key), 2: true

        self.keyType = -1   # -1: not done, 0: error, 1: single pl, 2: multi pl, 3: all, 4: cus, 5: us
                            # is this key a single playlist or multiPL/Genre/etc...

    def __str__(self):
        return "MusicKey: " + self.key

    def getActiveStatus(self):
        """
        look for the active status

        active status:
        -1: error
        0: none         no children files are active
        1: part         some children files are active
        2: all          all children files are active

        :return: active Status of all children files
        """

        activeChilds = 0
        for children in self.children:
            if children.active:
                activeChilds += 1

        status = -1
        if activeChilds == 0:
            status = 0
        elif 0 < activeChilds < len(self.children):
            status = 1
        elif activeChilds == len(self.children):
            status = 2

        return status
    def setActiveStatus(self, activeStatus: bool, suppressActiveList=False):
        """
        de/activate all children files

        :param activeStatus: activate: True, deac: False
        """
        if activeStatus == bool(self.active):
            return

        if activeStatus:  # activate
            self.mfl.files_active_allList.append(self)
            self.mfl.files_active_allListStatic["key" + str(self.id)] = self

            del self.mfl.files_inactive_allList[self.mfl.files_inactive_allList.index(self)]
            del self.mfl.files_inactive_allListStatic["key" + str(self.id)]

            self.mfl.files_active_allKeys.append(self)
            self.mfl.files_active_allKeysStatic[self.id] = self

            del self.mfl.files_inactive_allKeys[self.mfl.files_inactive_allKeys.index(self)]
            del self.mfl.files_inactive_allKeysStatic[self.id]

        else:  # deactivate
            del self.mfl.files_active_allList[self.mfl.files_active_allList.index(self)]
            del self.mfl.files_active_allListStatic["key" + str(self.id)]

            self.mfl.files_inactive_allList.append(self)
            self.mfl.files_inactive_allListStatic["key" + str(self.id)] = self

            del self.mfl.files_active_allKeys[self.mfl.files_active_allKeys.index(self)]
            del self.mfl.files_active_allKeysStatic[self.id]

            self.mfl.files_inactive_allKeys.append(self)
            self.mfl.files_inactive_allKeysStatic[self.id] = self

        for children in self.children:
            children.setActiveStatus(activeStatus, suppressActiveList)

    active = property(getActiveStatus, setActiveStatus)  # see g/setActiveStatus doc

    def getExtChildrenFiles(self):
        # this method will generate a list with every (child) file object
        output = []
        for child in self.children:
            output += child.getExtChildrenFiles()

        return output

    def getExtChildrenFileIds(self):
        # this method will generate a list with every file id including files in childrenDirs
        allObj = self.getExtChildrenFiles()
        output = []
        for file in allObj:
            output.append(file.id)
        return output


    def validate(self):
        if self.key in self.mfe.musicDirs["keys"]:
            self.keyType = 1
        elif self.key in self.mfe.multiKeyToKeyList:
            self.keyType = 2
        elif self.key == "all":
            self.keyType = 3
        elif self.key == "cus":
            self.keyType = 4
        elif self.key == "us":
            self.keyType = 5
        else:
            self.keyType = -1
            self.validation = False
            return False  # does not exist

        if not self.children:  # creating children
            self.children = []
            if self.keyType == 1:  # normal children dir
                self.children = [MusicFileDir(self.mfe.keyToPath[self.key], mfl=self.mfl, parentKey=self, activeList=self.activeList)]
            elif self.keyType == 2:  # use multi list
                for strKey in self.mfe.multiKeyToKeyList[self.key]:
                    self.children.append(MusicKey(strKey, mfl=self.mfl, mfe=self.mfe, parentKey=self, activeList=self.activeList))
            elif self.keyType == 3:  # all
                for strKey in self.mfe.musicDirs["keys"]:
                    self.children.append(MusicKey(strKey, mfl=self.mfl, mfe=self.mfe, parentKey=self, activeList=self.activeList))
            elif self.keyType == 4:  # cus
                self.children = [MusicFileDir(self.cusPath, mfl=self.mfl, parentKey=self, activeList=self.activeList)]
            elif self.keyType == 5:  # us
                self.children = [MusicFileDir("Music" + PS + "User", mfl=self.mfl, parentKey=self, activeList=self.activeList)]

        valis = 0
        for child in self.children:
            if child.validate():
                valis += 1

        self.validation = -1
        if valis == 0:
            self.validation = 0
        elif 0 < valis < len(self.children):
            self.validation = 1
        elif valis == len(self.children):
            self.validation = 2

        return self.validation

    def index(self):
        if self.validation is None:
            self.validate()
        if not self.validation:
            return False  # not a valid dir => will not index

        self.id = self.mfl.getNewKeyId()

        indis = 0
        for child in self.children:
            if child.index():
                indis += 1

        self.loaded = -1
        if indis == 0:
            self.loaded = 0
        elif 0 < indis < len(self.children):
            self.loaded = 1
        elif indis == len(self.children):
            self.loaded = 2

        # adding to mfl lists

        self.mfl.files_allList.append(self)
        self.mfl.files_allListStatic["key" + str(self.id)] = self

        self.mfl.files_allKeys.append(self)
        self.mfl.files_allKeysStatic[self.id] = self


        self.mfl.files_inactive_allList.append(self)
        self.mfl.files_inactive_allListStatic["key" + str(self.id)] = self

        self.mfl.files_inactive_allKeys.append(self)
        self.mfl.files_inactive_allKeysStatic[self.id] = self

        return self.loaded

    def loadForPyglet(self, onlyFirstLoad=False, threadLoad=True):  # meaning: loadChildrenForPyglet
        if threadLoad:  # loads the things in multi threads
            self.mfl.reloadThingsInThreads(self.getExtChildrenFiles(), specTyp=2,
                                       onlyFirstLoad=onlyFirstLoad)
            return

        for child in self.children:
            child.loadForPyglet(onlyFirstLoad=onlyFirstLoad)


class MusicFileDir:
    def __init__(self, fullPath, mfl, parentKey: MusicKey, parentDir=None, activeList=None):
        self.path = fullPath
        self.mfl = mfl  # to add this object and the children in the right (things)
        self.activeList = activeList

        self.parentDir = parentDir
        self.parentKey = parentKey
        self.children = []
        self.childrenDirs = []
        self.childrenFiles = []

        self.dirName = fullPath.split(PS)[-1]

        self.id = -1

        self.validation = None
        self.loaded = False

    def __str__(self):
        return "MusicFileDir: " + self.dirName

    def getActiveStatus(self):
        """
        look for the active status

        active status:
        -1: error
        0: none         no children files are active
        1: part         some children files are active
        2: all          all children files are active

        :return: active Status of all children files
        """

        activeChilds = 0
        for children in self.children:
            if children.active:
                activeChilds += 1

        status = -1
        if activeChilds == 0:
            status = 0
        elif 0 < activeChilds < len(self.children):
            status = 1
        elif activeChilds == len(self.children):
            status = 2

        return status
    def setActiveStatus(self, activeStatus: bool, suppressActiveList=False):
        """
        de/activate all children files

        :param activeStatus: activate: True, deac: False
        """
        for children in self.children:
            children.setActiveStatus(activeStatus, suppressActiveList)

    active = property(getActiveStatus, setActiveStatus)  # see g/setActiveStatus doc

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
                mDir = MusicFileDir(self.path + PS + contPart, mfl=self.mfl, parentDir=self, parentKey=self.parentKey, activeList=self.activeList)
                if mDir.validate():
                    self.children.append(mDir)
                    self.childrenDirs.append(mDir)
                    mDir.index()

            elif os.path.isfile(self.path + PS + contPart):
                mFile = MusicFile(self.path + PS + contPart, mfl=self.mfl, parent=self, parentKey=self.parentKey, activeList=self.activeList)
                if mFile.validate():
                    self.children.append(mFile)
                    self.childrenFiles.append(mFile)
                    mFile.loadInfo()
            else:
                pass  # what is this ?

        # adding to mfl lists

        self.mfl.files_allList.append(self)
        self.mfl.files_allListStatic["dir" + str(self.id)] = self

        self.mfl.files_allDirs.append(self)
        self.mfl.files_allDirsStatic[self.id] = self

        self.loaded = True

    def loadForPyglet(self, onlyFirstLoad=False, threadLoad=False):  # meaning: loadChildrenForPyglet
        if threadLoad:  # loads the things in multi threads
            self.mfl.reloadThingsInThreads(self.getExtChildrenFiles(), specTyp=2,
                                       onlyFirstLoad=onlyFirstLoad)
            return

        for child in self.children:  # loading the children
            child.loadForPyglet(onlyFirstLoad)


class MusicFile:
    def __init__(self, fullPath, mfl, parent=None, parentKey=None, activeList=None):
        self.path = fullPath
        self.mfl = mfl
        self.activeList = activeList

        self.parent = parent
        self.parentKey = parentKey


        self.file = fullPath.split(PS)[-1]
        self.fileExt = self.file.split(".")[-1]
        self.fileName = ""
        self.name = ""

        self.anData = None
        self.pygletData = None

        self.id = -1

        self.validation = None
        self.loaded = False
        self._active = False

        self.loadedPygletData = False

    def __str__(self):
        return "MusicFile: " + self.name

    def __lt__(self, other):
        return self.name.capitalize() < other.name.capitalize()
    def __le__(self, other):
        return self.name.capitalize() <= other.name.capitalize()
    def __eq__(self, other):
        if type(other) == MusicFile:
            return self.name.capitalize() == other.name.capitalize()
        else:
            return super().__eq__(other)
    def __ne__(self, other):
        return self.name.capitalize() != other.name.capitalize()
    def __gt__(self, other):
        return self.name.capitalize() > other.name.capitalize()
    def __ge__(self, other):
        return self.name.capitalize() >= other.name.capitalize()

    def getActiveStatus(self):
        return self._active

    def setActiveStatus(self, activeStatus: bool, suppressActiveList=False):
        """
        de/activate files => 1. set this status
                             2. add/remove this file from active/inactive list in mfl

        :param activeStatus: acitvate: True, deac: False
        """
        if activeStatus == self._active or not self.validation:
            return

        if activeStatus:  # activate
            self.mfl.files_active_allList.append(self)
            self.mfl.files_active_allListStatic["file" + str(self.id)] = self

            del self.mfl.files_inactive_allList[self.mfl.files_inactive_allList.index(self)]
            del self.mfl.files_inactive_allListStatic["file" + str(self.id)]


            self.mfl.files_active_allFiles.append(self)
            self.mfl.files_active_allFilesStatic["file" + str(self.id)] = self

            del self.mfl.files_inactive_allFiles[self.mfl.files_inactive_allFiles.index(self)]
            del self.mfl.files_inactive_allFilesStatic["file" + str(self.id)]

            if self.activeList is not None and not suppressActiveList:
                self.activeList.append(self)

        else:  # deactivate
            del self.mfl.files_active_allList[self.mfl.files_active_allList.index(self)]
            del self.mfl.files_active_allListStatic["file" + str(self.id)]

            self.mfl.files_inactive_allList.append(self)
            self.mfl.files_inactive_allListStatic["file" + str(self.id)] = self


            del self.mfl.files_active_allFiles[self.mfl.files_active_allFiles.index(self)]
            del self.mfl.files_active_allFilesStatic["file" + str(self.id)]

            self.mfl.files_inactive_allFiles.append(self)
            self.mfl.files_inactive_allFilesStatic["file" + str(self.id)] = self

            if self.activeList is not None and not suppressActiveList:
                del self.activeList[self.activeList.index(self)]

        self._active = activeStatus

    active = property(getActiveStatus, setActiveStatus)  # see g/setActiveStatus doc


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
        splits = self.file.split(".")
        for splitPartIndex in range(len(splits) - 1):
            self.fileName += splits[splitPartIndex] + "."
        self.fileName = self.fileName.rstrip(".")
        self.name = self.fileName

        self.anData = EveconLib.Tools.MusicEncode(self.fileName)

        # adding to mfl lists

        self.mfl.files_allList.append(self)
        self.mfl.files_allListStatic["file" + str(self.id)] = self

        self.mfl.files_allFiles.append(self)
        self.mfl.files_allFilesStatic[self.id] = self


        self.mfl.files_inactive_allList.append(self)
        self.mfl.files_inactive_allListStatic["file" + str(self.id)] = self

        self.mfl.files_inactive_allFiles.append(self)
        self.mfl.files_inactive_allFilesStatic["file" + str(self.id)] = self


        self.loaded = True

    def loadForPyglet(self, onlyFirstLoad=False, threadLoad=False):
        if self.loadedPygletData and onlyFirstLoad:
            return   # the data is already loaded and parm true => will not load again
        if threadLoad:
            pass  # activated for single files

        if self.loaded and self.validation:
            self.pygletData = pyglet.media.load(self.path)
            self.loadedPygletData = True



class MusicFileLoader:
    def __init__(self, notificationFunc=None, neverPrint=False, activeList=None):
        self.musicFileEditor = EveconLib.Programs.Player.MusicFileEditor()

        self.notificationFunc = notificationFunc
        self.neverPrint = neverPrint
        self.activeList = activeList

        self.refreshMusicList()


        # save possibilities

        self.files_allList = []  # all things unsorted in a list
        self.files_allListStatic = {}  # all things in a static list (access with file/dir + id as a str)

        self.files_allFiles = []  # all files unsorted
        self.files_allFilesStatic = {}  # same static
        self.files_allDirs = []  # all dirs unsorted
        self.files_allDirsStatic = {}  # same static
        self.files_allKeys = []  # all keys unsorted
        self.files_allKeysStatic = {}  # same static


        self.files_dirQuan = 0
        self.files_fileQuan = 0
        self.files_keyQuan = 0


        self.files_active_allList = []  # all things unsorted in a list, but sorted in the dict with key:list
        self.files_active_allListStatic = {}  # all things in a static list (access (first with playlistKey) with file/dir + id as a str), but sorted in the dict with key:list

        self.files_active_allFiles = []  # all files unsorted, but sorted in the dict with key:list
        self.files_active_allFilesStatic = {}  # same static
        self.files_active_allKeys = []  # all keys unsorted, but sorted in the dict with key:list
        self.files_active_allKeysStatic = {}  # same static

        self.files_inactive_allList = []  # all things unsorted in a list, but sorted in the dict with key:list
        self.files_inactive_allListStatic = {}  # all things in a static list (access (first with playlistKey) with file/dir + id as a str), but sorted in the dict with key:list

        self.files_inactive_allFiles = []  # all files unsorted, but sorted in the dict with key:list
        self.files_inactive_allFilesStatic = {}  # same static
        self.files_inactive_allKeys = []  # all keys unsorted, but sorted in the dict with key:list
        self.files_inactive_allKeysStatic = {}  # same static


        self.loadedKeys = []  # pygletLoaded
        self.indexedKeys = []  # indexed

    def getNewDirId(self):
        self.files_dirQuan += 1
        return self.files_dirQuan - 1 # to start from 0

    def getNewFileId(self):
        self.files_fileQuan += 1
        return self.files_fileQuan - 1 # to start from 0

    def getNewKeyId(self):
        self.files_keyQuan+= 1
        return self.files_keyQuan - 1 # to start from 0


    def refreshMusicList(self):
        self.musicFileEditor.readFile()

    def addMusic(self, key, cusPath="", printStaMSG=True, printEndMSG=True, makeNoti=False, loadForPyglet=True):  # key (AN, LIS)
        suc = None

        if printStaMSG and not self.neverPrint:
            EveconLib.Tools.cls()
            print("Loading key %s" % key.title())

        keyOj = MusicKey(key, mfl=self, mfe=self.musicFileEditor, cusPath=cusPath, activeList=self.activeList)
        val = keyOj.validate()
        keyOj.index()

        if not val:
            return False

        if printEndMSG and not self.neverPrint:
            print("Key %s indexed successful" % key.title())

        self.indexedKeys.append(keyOj)
        if loadForPyglet:
            EveconLib.Tools.Log("MusicFileLoader (addMusic)", "Begin to load files for pyglet from the key %s" % key)

            keyOj.loadForPyglet(onlyFirstLoad=True, threadLoad=True)

            self.loadedKeys.append(keyOj)

        if printEndMSG and not self.neverPrint:
            print("Finished: " + key)

        if makeNoti and self.notificationFunc:
            self.notificationFunc(key.title(), title="Finished loading", screentime=2.5)
        return True


    def loadDir(self, dirPath, parentKey):
        mDir = MusicFileDir(dirPath, mfl=self, parentKey=parentKey)
        if mDir.validate():
            mDir.index()
            return True

        return False

    def reloadFile(self, fileId, onlyFirstLoad=False, threadLoad=False):
        if type(fileId) != int:
            dirId = int(fileId.lstrip("file"))

        self.files_allFilesStatic[fileId].loadForPyglet(onlyFirstLoad, threadLoad)

    def reloadDir(self, dirId, onlyFirstLoad=True, threadLoad=False):
        if type(dirId) != int:
            dirId = int(dirId.lstrip("dir"))

        self.files_allDirsStatic[dirId].loadForPyglet(onlyFirstLoad, threadLoad)

    def reloadThing(self, thingId: str, onlyFirstLoad=False, threadLoad=False):
        self.files_allListStatic[thingId].loadForPyglet(onlyFirstLoad, threadLoad)

    def reloadKey(self, keyId, onlyFirstLoad=True, threadLoad=True):
        # important onlyFirstLoad AND threadLoad is set to TRUE
        if type(keyId) != int:
            dirId = int(keyId.lstrip("key"))

        self.files_allKeysStatic[keyId].loadForPyglet(onlyFirstLoad, threadLoad)


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


    def activateFile(self, fileId, status: bool, suppressActiveList=False):
        if type(fileId) != int:
            dirId = int(fileId.lstrip("file"))

        self.files_allFilesStatic[fileId].setActiveStatus(status, suppressActiveList)

    def activateDir(self, dirId, status: bool, suppressActiveList=False):
        if type(dirId) != int:
            dirId = int(dirId.lstrip("dir"))

        self.files_allDirsStatic[dirId].setActiveStatus(status, suppressActiveList)

    def activateThing(self, thingId: str, status: bool, suppressActiveList=False):
        self.files_allListStatic[thingId].active = status

    def activateKey(self, keyId: str, status: bool, suppressActiveList=False):
        if type(keyId) != int:
            dirId = int(keyId.lstrip("key"))

        self.files_allKeysStatic[keyId].setActiveStatus(status, suppressActiveList)

    def activateAll(self, status: bool, suppressActiveList=False):
        if status:
            for file in self.files_inactive_allFiles:
                file.setActiveStatus(status, suppressActiveList)
        else:
            for file in self.files_active_allFiles:
                file.setActiveStatus(status, suppressActiveList)

    def getF(self, file):
        """
        returns the file object
        :param file: file id
        :return: file
        """
        if type(file) != str:  # if int is given parse to str
            file = str(file)
        if not EveconLib.Tools.lsame(file, "file"):  # try to catch part if only file id is given
            file = "file" + file
        return self.files_allFilesStatic[file]

    def getK(self, key):
        for keyObj in self.files_allKeys:
            if keyObj.key == key:
                return keyObj