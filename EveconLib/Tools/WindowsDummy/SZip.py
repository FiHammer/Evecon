class szipC:
    def __init__(self, path):
        self.path = path + "\\7za.exe"
    def create_archive(self, archive, filenames, switches=None, workpath=None, archive_type="zip"):
        pass
    def extract_archive(self, archive, output=None, switches=None, EveconPath=True):
        pass
SZip = szipC("Programs\\7z")