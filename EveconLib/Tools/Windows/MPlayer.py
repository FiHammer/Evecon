import subprocess
import EveconLib.Tools.Tools

class MPlayer:
    def __init__(self, path):
        self.path = path + "\\mplayer.exe"
        self.Running = False
        self.Paused = False
        self.Stopped = False
        self.Type = None
        self.mplayer = None
        self.Track = None

    def start(self, track):
        if not self.Running:
            self.Track = track
            if EveconLib.Tools.Tools.lsame(self.Track, "http"):
                self.Type = "stream"
            else:
                self.Type = EveconLib.Tools.Tools.MusicType(self.Track, True)
            self.mplayer = subprocess.Popen([self.path, self.Track], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

            self.Stopped = False
            self.Running = True
            self.Paused = False

    def stop(self):
        if self.Running:
            self.mplayer.terminate()
            self.Stopped = True
            self.Track = None
            self.Type = None
            self.Running = False
            self.mplayer = None

    def pause(self):
        if not self.Paused:
            self.mplayer.terminate()
            self.Paused = True
            self.Running = False

    def unpause(self):
        if self.Paused:
            self.mplayer = subprocess.Popen([self.path, self.Track], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            self.Running = True
            self.Paused = False

    def switch(self):
        if self.Paused:
            self.unpause()
        else:
            self.pause()
