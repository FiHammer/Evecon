import os
import EveconLib

class SubTitleParser:
    """
    parses a .vtt file to a method time => subtitle part
    """

    VALID_TYPES = ["vtt"]

    def __init__(self, filePath: str):
        self.path = filePath

        self.file = self.path.split(EveconLib.Config.path_seg)[-1]
        self.fileExt = self.file.split(".")[-1]

        self.validation = None

    def validate(self):
        if not os.path.exists(self.path):
            self.validation = False
            return False

        if not os.path.isfile(self.path):
            self.validation = False  # no file
            return False

        if not self.fileExt in self.VALID_TYPES:
            self.validation = False  # wrong type
            return False

        self.validation = True
        return True

    def readFile(self):
        pass



class SubTitleParserChanger:
    """
    changes a string on end of the subtitle part
    """
    pass