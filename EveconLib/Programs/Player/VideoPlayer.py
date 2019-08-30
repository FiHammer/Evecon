import EveconLib
from EveconLib.Programs.Player.MusicFileLoader import MusicFile
import pyglet
import time

class VideoPlayer:
    def __init__(self, musicFile: str, enableWindowControl=True, enableServer=False, port=-1, forcePort=False,
                 server_sendFirstStartAndWaitForClient=False, subs=True):
        self.musicFilePath = musicFile
        self.musicFile = MusicFile(musicFile, None)


        self.enableWindowControl = enableWindowControl

        self.window = pyglet.window.Window(visible=False, resizable=True)
        self.subtitleBox = pyglet.text.Label(y=50, font_size=32, width=50, multiline=True)

        self.player = pyglet.media.Player()

        self.musicData = None
        self.validation = None

        self.timer = EveconLib.Tools.Timer()

        self.playing = False  # playing music
        self.running = False  # started the playback

        self.prevVolume = 0.0  # prev Vol save for mute
        self.volume = 0.5  # volume
        self.muted = False  #is player muted

        self.player.volume = self.volume

        self.showSubs = subs
        self.subChanger = None
        self.musicFile.loadInfo()
        if self.musicFile.subAvail and self.showSubs:
            self.subChanger = EveconLib.Programs.Player.SubTitleParserChanger(self.setSub, self.musicFile.subFile, self.timer)

        if enableServer:
            if port == -1:
                self.port = EveconLib.Tools.UsedPorts.givePort()
            else:
                self.port = port
            self.server = EveconLib.Networking.Server(port=self.port, forcePort=forcePort, stdReact=self.serverReact, printLog=False)
        else:
            self.server = None

        self.server_sendFirstStartAndWaitForClient = server_sendFirstStartAndWaitForClient

    def serverReact(self, msg, connectionId):
        if msg == "play":
            self.play(fromServer=True)
        elif msg == "pause":
            self.pause(fromServer=True)
        elif EveconLib.Tools.lsame(msg, "vol_"):
            try:
                self.setVol(float(msg.lstrip("vol_")), fromServer=True)
            except ValueError:
                pass
        elif msg == "exit":
            self.exit(fromServer=True)
        elif msg == "mute":
            self.mute(fromServer=True)
        elif msg == "unmute":
            self.unmute(fromServer=True)
        elif msg == "msg":
            self.setSub("Hallo Ich bin toll")

    def validate(self):
        if not self.musicFile.loaded:
            self.musicFile.loadInfo()

        if self.musicFile.type != "video":
            self.validation = False
            return False

        self.validation = self.musicFile.validate()
        return self.validation


    def start(self):
        if self.validation is None:
            self.validate()
        if not self.validation:
            return   # not valid
        # generating player & window
        self.running = True
        self.musicFile.loadForPyglet(onlyFirstLoad=True)

        if self.musicFile.anData["valid"]:
            self.window.set_caption("Evecon: VideoPlayer        Now Playing      " + self.musicFile.anData["title"])
        else:
            self.window.set_caption("Evecon: VideoPlayer        Now Playing            " + self.musicFile.name)


        @self.window.event
        def on_draw():
            self.player.get_texture().blit(self.window.width/2 - self.musicFile.pygletData.video_format.width/2,
                                           self.window.height/2 - self.musicFile.pygletData.video_format.height/2)
            if self.showSubs and self.subtitleBox and self.subChanger:
                #sb = self.subBoxes.copy()
                #for box in :
                self.subtitleBox.x = self.window.width // 2 - self.subtitleBox.width // 2 - 20
                self.subtitleBox.draw()

                x = self.subChanger.canChange()
                if x:
                    self.setSub(x)
                #print(self.subtitleBox, self.window.width, self.subtitleBox.width)
                #self.subtitleBox.x = self.window.width//2 - self.subtitleBox.width//2 - 20
                #self.subtitleBox.draw()

        @self.window.event
        def on_close():
            self.exit()

        @self.window.event
        def on_key_press(symbol, modifiers):
            if not self.enableWindowControl:
                return

            if symbol == 32:  # space => pause/play
                self.switch()
            elif symbol == 65480:  # F11 => switchfullscreen
                self.fullscreenSwitch()
            elif symbol == 65364:  # arrow down => vol-
                self.setVol(self.volume - 0.1)
            elif symbol == 65362:  # arrow up => vol+
                self.setVol(self.volume + 0.1)
            elif symbol == 109:  # m => mute
                self.muteSwitch()
            elif symbol == 101:  # e => exit
                self.exit()
            #print(symbol, modifiers)

        @self.player.event
        def on_player_eos():
            print(0)
            self.exit()

        @self.player.event
        def on_eos():
            print(1)
            self.exit()

        @self.player.event
        def on_source_group_eos():
            print(2)
            self.exit()



        if self.server:
            self.server.start()

        self.player.queue(self.musicFile.pygletData)

        self.window.set_fullscreen(False)
        self.window.set_visible(True)

        if self.showSubs and self.subChanger:
            pass #self.subChanger.start()
        #self.setSub("Haklo")

        if self.server and self.server_sendFirstStartAndWaitForClient:
            while not self.server.hasActiveConnections():
                time.sleep(1)
            self.server.sendToAll("firstStart")

        self.timer.start()
        self.playing = True
        self.player.play()

        pyglet.app.run()

        self.exit(fromServer=True)

    def setSub(self, text):
        width = len(text) * 20
        y = 75
        #print(width, y, text)
        label = pyglet.text.Label(text, y=y, font_size=32, width=width)
        self.subtitleBox = label

        #self.subtitleBox.
        #self.subtitleBox.delete_text()
        #self.subtitleBox.text.insert_text(text)

    def switch(self):
        if self.playing:
            self.pause()
        else:
            self.play()

    def pause(self, fromServer=False):
        if not self.running:
            return
        self.timer.pause()
        self.playing = False
        self.player.pause()

        if self.server and not fromServer: # server react
            self.server.sendToAll("pause")

    def play(self, fromServer=False):
        if not self.running:
            return
        self.timer.start()
        self.playing = True
        self.player.play()

        if self.server and not fromServer: # server react
            self.server.sendToAll("play")

    def switchSubs(self):
        if self.showSubs:
            self.unhideSubs()
        else:
            self.hideSubs()

    def unhideSubs(self):
        self.showSubs = True

    def hideSubs(self):
        self.showSubs = False

    def windowVis(self, status):
        if not self.running:
            return
        self.window.set_visible(status)

    def fullscreenSwitch(self):
        if not self.running:
            return

        if self.window.fullscreen:
            self.window.set_fullscreen(False, screen=self.window.screen)
        else:
            self.window.set_fullscreen(True, screen=self.window.screen)

    def muteSwitch(self):
        if self.muted:
            self.unmute()
        else:
            self.mute()

    def setVol(self, vol: float, fromServer=False):
        if vol < 0.0:  # min
            vol = 0.0
        elif vol > 1.0:  # max
            vol = 1.0
        self.volume = vol
        self.player.volume = vol

        if self.server and not fromServer: # server react
            self.server.sendToAll("vol_" + str(self.volume))

    def mute(self, fromServer=False):
        if self.server and not fromServer: # server react
            self.server.sendToAll("mute")

        self.prevVolume = self.volume
        self.muted = True
        self.volume = 0.0
        self.player.volume = 0.0

    def unmute(self, fromServer=False):
        if self.server and not fromServer: # server react
            self.server.sendToAll("unmute")

        self.muted = False

        self.volume = self.prevVolume
        self.player.volume = self.prevVolume

    def exit(self, fromServer=False):
        if self.server and not fromServer: # server react
            self.server.sendToAll("exit")
            self.server.exit()

        self.playing = False  # playing music
        self.running = False  # started the playback
        self.window.close()
        self.player.delete()
        pyglet.app.exit()