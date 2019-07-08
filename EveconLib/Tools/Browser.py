import psutil
import os
import subprocess
import webbrowser

import EveconLib.Config

class Browser:
    def __init__(self, path):
        self.path = path

        self.com_newWin = ""
        self.com_newTab = ""
        self.path_dir = ""
        for x in self.path.split(EveconLib.Config.path_seg):
            if x == "C:":
                self.path_dir = x
            elif x != "firefox.exe":
                self.path_dir += EveconLib.Config.path_seg + x

        self.name = self.path.split(EveconLib.Config.path_seg)[-1]
        if self.name in (p.name() for p in psutil.process_iter()):
            self.running = True
        else:
            self.running = False


    def open(self, url: list, new_type=2):
        if type(url) != list:
            url = [url]
        for x in url:
            self.open_tab(url=str(x))

    def open_win(self, url: str):
        dir_tmp = os.getcwd()
        os.chdir(self.path_dir)
        subprocess.call([self.name, self.com_newWin, url])
        time.sleep(0.15)
        os.chdir(dir_tmp)

    def open_tab(self, url: str):
        dir_tmp = os.getcwd()
        os.chdir(self.path_dir)
        subprocess.call([self.name, self.com_newTab, url])
        time.sleep(0.15)
        os.chdir(dir_tmp)

    def refresh(self):
        if self.name in (p.name() for p in psutil.process_iter()):
            self.running = True
        else:
            self.running = False

class Firefox(Browser):
    def __init__(self, path=EveconLib.Config.firefox_path):
        super().__init__(path)

        self.com_newWin = "-new-window"
        self.com_newTab = "-new-tab"

class BrowserOld:
    def __init__(self, path):
        self.path = path
        self.bro = None

        self.name = self.path.split(EveconLib.Config.path_seg)[-1]
        if self.name in (p.name() for p in psutil.process_iter()):
            self.running = True
        else:
            self.running = False

    def open(self, url: list, new_type=2):
        if type(url) != list:
            url = [url]
        for x in url:
            self.bro.open(url=x, new=new_type)

    def open_win(self, url: list):
        self.open(url=url, new_type=1)

    def open_tab(self, url: list):
        self.open(url=url, new_type=2)

    def refresh(self):
        if self.name in (p.name() for p in psutil.process_iter()):
            self.running = True
        else:
            self.running = False


class Vivaldi(BrowserOld):
    def __init__(self, path=EveconLib.Config.vivaldi_path):
        super().__init__(path)

        self.bro = webbrowser.Chrome(self.path)
