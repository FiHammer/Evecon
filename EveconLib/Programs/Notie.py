import os
import simplecrypt
import json
import shutil

import EveconLib.Tools
import EveconLib.Config

class Notie:
    def __init__(self, keyname: str):
        """
        starts the object, search if it exists

        :param keyname: the KEYname of the note. It is ONLY for the programme
        """

        self.keyname = keyname

        allNoties = os.listdir(EveconLib.Config.notiePath)
        self.allNoties = []
        for note in allNoties:
            if EveconLib.Tools.rsame(note, ".json"):
                self.allNoties.append(note.rstrip(".json"))
        self.existing = bool(EveconLib.Tools.Search(self.keyname, self.allNoties))

        self.file = EveconLib.Config.notiePath + EveconLib.Config.path_seg + self.keyname + ".json"
        self.dir = EveconLib.Config.notiePath + EveconLib.Config.path_seg + self.keyname + EveconLib.Config.path_seg

        self.name = ""
        self.lines = []
        self.lines_en = []
        self.encryption = False
        self.encryptionKey = ""

        self.saveEnKey = None
        self.autosave = None

        self.started = False

    def __del__(self):
        """
        if autosave the file will be saved
        """
        if self.started and self.autosave:
            self.save()

    def _len(self):
        return len(self.getLines())
    len = property(_len)

    def _read(self):
        """
        reads the file

        :return: success
        """
        with open(self.file) as jsonfile:
            data = json.load(jsonfile)

        self.name = data["name"]
        self.encryption = data["config"]["encryption"]
        self.saveEnKey = data["config"]["saveEnKey"]
        self.autosave = data["config"]["autosave"]
        lineLen = data["len"]

        if self.encryption:
            self.lines_en = []
            # noinspection PyArgumentList
            for num in range(lineLen):
                with open(self.dir+str(num)+".byte", "rb") as bytefile:
                    self.lines_en.append(bytefile.read())

        else:
            self.lines_en = data["lines"]

        if self.encryption and self.saveEnKey:
            self.encryptionKey = data["encryptionKey"]
        elif self.encryption and not self.saveEnKey:
            pass
        else:
            self.encryptionKey = ""
        self._decrypt()

        return bool(data)

    def _write(self):
        """
        reads the file

        :return: success
        """
        self._encrypt()

        if self.saveEnKey:
            enKey = self.encryptionKey
        else:
            enKey = ""

        if self.encryption:
            if not os.path.exists(self.dir.rstrip(EveconLib.Config.path_seg)):
                os.mkdir(self.dir.rstrip(EveconLib.Config.path_seg))

            for x in range(len(self.lines_en)):
                with open(self.dir+str(x)+".byte", "wb") as bytefile:
                    bytefile.write(self.lines_en[x])

            output = {
                "config": {"encryption": self.encryption, "saveEnKey": self.saveEnKey, "autosave": self.autosave},
                "lines": [],
                "encryptionKey": enKey, "len": self._len(), "name": self.name}

        else:
            output = {
                "config": {"encryption": self.encryption, "saveEnKey": self.saveEnKey, "autosave": self.autosave},
                "lines": self.lines,
                "encryptionKey": enKey, "len": self._len(), "name": self.name}



        with open(self.file, "w") as jsonfile:
            json.dump(output, jsonfile, indent=4, sort_keys=True)

        return os.path.exists(self.file)

    def _encrypt(self):
        """
        encrypt the self.lines in self.lines_en
        """
        if self.encryption:
            self.lines_en = []
            for line in self.lines:
                self.lines_en.append(simplecrypt.encrypt(self.encryptionKey, line))
        else:
            self.lines_en = self.lines.copy()
    def _decrypt(self):
        """
        decrypt the self.lines_en in self.lines
        """
        if self.encryption:
            self.lines = []
            for line in self.lines_en:
                self.lines.append(simplecrypt.decrypt(self.encryptionKey, line).decode())
        else:
            self.lines = self.lines_en.copy()

    def enableEncryption(self, encryptionKey=EveconLib.Tools.randompw(returnpw=True, printpw=False, length=10), saveEnKey=True):
        """
        enables the encryption

        :param encryptionKey: the key for the encryption
        :param saveEnKey: if True it saves the encrpytion key in the SAME file with the content
        :rtype: bool
        :return: success
        """
        if self.started and not self.encryption:
            self.encryptionKey = encryptionKey
            self.saveEnKey = saveEnKey

            return  self._write()
        else:
            return False

    def setConfig(self, config: str, value):
        """
        resets the config

        :param config: the config name
        :param value: the value
        :return: succsess
        """

        if config == "autosave":
            self.autosave = value
        elif config == "saveEnKey":
            self.saveEnKey = value
        else:
            return False

        if self.autosave:
            return self._write()
        return True

    def open(self, encryptionKey=""):
        """
        Reads the file for the first time!
        :param encryptionKey: if needed the encryptkey for the file (DO not need if: 1. no encryption 2. saveEnKey

        :rtype: bool
        :return: success
        """

        if self.existing and not self.started:
            self.started = True


            if os.path.exists(self.dir+"0.byte"):

                with open(self.file) as jsonfile:
                    data = json.load(jsonfile)

                self.saveEnKey = data["config"]["saveEnKey"]
                if self.saveEnKey:
                    encryptionKey = data["encryptionKey"]

                with open(self.dir+"0.byte", "rb") as file:
                    b = file.read()
                try:
                    simplecrypt.decrypt(encryptionKey, b)
                except simplecrypt.DecryptionException or ValueError:
                    return False

            return self._read()
        else:
            return False

    def create(self, name: str, content="", encryption=False, encryptionKey=EveconLib.Tools.randompw(returnpw=True, printpw=False, length=10), saveEnKey=True, autosave=True):
        """
        Creates a note (if it already exists or opened it will be OVERRIDDEN)

        :param name: the name of the file (title)
        :param content: the predefined first line of the file
        :param encryption: enables the encryption
        :param encryptionKey: the key for the encryption
        :param saveEnKey: if True it saves the encrpytion key in the SAME file with the content
        :param autosave: saves the file after every change (slow with encryption)
        :return: success
        """

        if self.started or self.existing:
            self.remove()

        self.started = True

        self.name = name
        self.encryption = encryption
        if self.encryption:
            self.encryptionKey = encryptionKey
        else:
            self.encryptionKey = ""

        if content:
            self.lines = [content]
        else:
            self.lines = []

        self.lines_en = []

        self.saveEnKey = saveEnKey
        self.autosave = autosave

        return self._write()


    def export(self, filename="", path=EveconLib.Config.outputPath):
        """
        :param filename: the name of the export file (without .txt)
        :param path: the specified path of the export directory

        :rtype: bool
        :return: success
        """
        if self.started:
            if filename:
                filename += ".txt"
            else:
                filename = self.name + ".txt"

            content = self.name + ":\n\n"
            for con in range(len(self.lines)):
                if con == len(self.lines) - 1: # last line
                    content += self.lines[con]
                else:
                    content += self.lines[con] + "\n"

            with open(path + filename, "w") as file:
                file.write(content)

            return os.path.exists(path+filename)
        else:
            return False
    def save(self):
        """
        saves the file

        :rtype: bool
        :return: success
        """

        return self._write()
    def clear(self):
        """
        clears the content/lines

        :rtype: bool
        :return: success
        """

        self.lines = []
        if self.autosave:
            self._write()
    def remove(self):
        """
        removes the file

        :rtype: bool
        :return: success
        """

        if self.existing:
            self.name = ""
            self.lines = []
            self.lines_en = []
            self.encryption = False
            self.encryptionKey = ""

            self.saveEnKey = None
            self.autosave = None

            self.started = False

            os.remove(self.file)
            if self.encryption:
                shutil.rmtree(self.dir.rstrip(EveconLib.Config.path_seg))

            return not os.path.exists(self.file) and not os.path.exists(self.dir)
        else:
            return False

    def add(self, text: str):
        """
        adds one line
        :param text: text
        """
        self.lines.append(text)
        if self.autosave:
            self._write()
    def set(self, lines: list):
        """
        sets all lines
        :param lines: lines in list
        :return:
        """
        self.lines = lines
        if self.autosave:
            self._write()
    def setLine(self, line: int, text: str):
        """
        sets one specific line

        :param line: the line number
        :param text: text
        """
        self.lines[line] = text
        if self.autosave:
            self._write()
    def setName(self, name: str):
        """
        sets the name new

        :param name: name
        :return:
        """
        self.name = name
        if self.autosave:
            self._write()

    def getLines(self, read=False):
        """
        gets all lines

        :param read: if true the file will be read again (slow with encryption)
        :rtype: list
        :return: all lines
        """
        if read:
            self._read()
        return self.lines

    def getLine(self, line: int, read=False):
        """
        gets one specific line

        :param line: the line
        :param read: if true the file will be read again (slow with encryption)
        :rtype: list
        :return: one line
        """
        if read:
            self._read()
        return self.lines[line]
    def getName(self, read=False):
        """
        gets the name

        :param read: if true the file will be read again (slow with encryption)
        :rtype: str
        :return: name
        """
        if read:
            self._read()
        return self.name
