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
        pass
    def stop(self):
        pass
    def pause(self):
        pass
    def unpause(self):
        pass
    def switch(self):
        pass
