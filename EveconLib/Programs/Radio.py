import random
import sys

import EveconLib.Tools


class Radio:
    def __init__(self, systray=True):
        self.streampause = False
        self.streamrun = True
        self.streamvolume = EveconLib.Tools.Windows.Volume.getVolume()

        self.streamplayer = EveconLib.Tools.MPlayer("Programs\\MPlayer")

        self.streamPrintOth = False
        self.streamPrintCh = False
        self.streamPrintVol = False

        self.systrayon = systray and sys.platform == "win32"
        self.systray = None

        self.stream_playlists = ["EgoFM", "HR1", "HR3", "Bayern3", "ByteFM"]
        self.stream_playlists_key = ["egofm", "hr1", "hr3", "br3", "bytefm"]
        self.stream_playlists_name = {"egofm" : "EgoFM",
                                      "hr1" : "HR1",
                                      "hr3" : "HR3",
                                      "br3" : "BR3",
                                      "bytefm" : "ByteFM"}
        self.stream_playlists_link = {"egofm" : "https://egofm-live.cast.addradio.de/egofm/live/mp3/high/stream.mp3",
                                      "hr1" : "http://hr-hr1-live.cast.addradio.de/hr/hr1/live/mp3/128/stream.mp3",
                                      "hr3" : "http://hr-hr3-live.cast.addradio.de/hr/hr3/live/mp3/128/stream.mp3",
                                      "br3" : "https://br-br3-live.sslcast.addradio.de/br/br3/live/mp3/128/stream.mp3",
                                      "bytefm" : "https://dg-ice-eco-https-fra-eco-cdn.cast.addradio.de/bytefm/main/mid/stream.mp3"}

        self.streamplaying = self.stream_playlists_key[random.randint(0, len(self.stream_playlists_key) - 1)]

    def Unpause(self):
        self.streamplayer.unpause()
        self.streampause = False
        EveconLib.Tools.title("Radio", self.stream_playlists_name[self.streamplaying], "Now Playing")
    def Pause(self):
        self.streamplayer.pause()
        self.streampause = True
        EveconLib.Tools.title("Radio", self.stream_playlists_name[self.streamplaying], "Paused")
    def Switch(self):
        if not self.streampause:
            self.Pause()
        else:
            self.Unpause()
        #self.streamplayer.switch()
        #self.streampause = self.streamplayer.Paused
    def Change(self, key):
        self.streamplayer.stop()
        self.streamplaying = key
        self.streamplayer.start(self.stream_playlists_link[key])
        EveconLib.Tools.title("Radio", self.stream_playlists_name[self.streamplaying], "Now Playing")
    def vol(self, vol):
        self.streamvolume = vol
        EveconLib.Tools.Windows.Volume.change(vol)
        #nircmd("volume", self.streamvolume)
    def Stop(self):
        self.streamplaying = None
        self.streampause = False
        self.streamrun = False
        self.streamplayer.stop()
        if self.systrayon:
            time.sleep(1)
            EveconLib.Tools.killme()
    def input(self, inpt):
        inpt = inpt.lower()
        if inpt == "play" or inpt == "pau" or inpt == "pause" or inpt == "p":
            self.Switch()
            self.printit()
        elif inpt == "change" or inpt == "ch" or inpt == "c":
            self.streamPrintOth = True
            self.streamPrintCh = True
            self.printit()
            self.Change(input("Change to:"))
            self.streamPrintOth = False
            self.streamPrintCh = False
            self.printit()
        elif inpt == "stop" or inpt == "exit":
            self.Stop()
            self.printit()
        elif inpt == "vol":
            self.streamPrintOth = True
            self.streamPrintVol = True
            self.printit()
            self.vol(float(input("Volume (Now: %s)\n" % EveconLib.Tools.Windows.Volume.getVolume())))
            self.streamPrintOth = False
            self.streamPrintVol = False
            self.printit()

    # noinspection PyStatementEffect
    def start(self):

        EveconLib.Tools.title("Radio", self.stream_playlists_name[self.streamplaying], "Now Playing")
        self.streamplayer.start(self.stream_playlists_link[self.streamplaying])
        # pause/unpause , submenu mit allen sendern

        def unp_p(x):
            self.Switch()


        if self.systrayon and sys.platform == "win32":


            def x0(x):
                self.Change(self.stream_playlists_key[0])
            def x1(x):
                self.Change(self.stream_playlists_key[1])
            def x2(x):
                self.Change(self.stream_playlists_key[2])
            def x3(x):
                self.Change(self.stream_playlists_key[3])
            def x4(x):
                self.Change(self.stream_playlists_key[4])
            def x5(x):
                self.Change(self.stream_playlists_key[5])
            def x6(x):
                self.Change(self.stream_playlists_key[6])
            def x7(x):
                self.Change(self.stream_playlists_key[7])
            def x8(x):
                self.Change(self.stream_playlists_key[8])
            def x9(x):
                self.Change(self.stream_playlists_key[9])
            def x10(x):
                self.Change(self.stream_playlists_key[10])
            def x11(x):
                self.Change(self.stream_playlists_key[11])
            def x12(x):
                self.Change(self.stream_playlists_key[12])
            def x13(x):
                self.Change(self.stream_playlists_key[13])
            def x14(x):
                self.Change(self.stream_playlists_key[14])
            def x15(x):
                self.Change(self.stream_playlists_key[15])

            if len(self.stream_playlists) == 1:
                sub_menu1 = {self.stream_playlists[0]: x0}
            elif len(self.stream_playlists) == 2:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1}
            elif len(self.stream_playlists) == 3:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2}
            elif len(self.stream_playlists) == 4:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                             self.stream_playlists[3]: x3}
            elif len(self.stream_playlists) == 5:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                             self.stream_playlists[3]: x3, self.stream_playlists[4]: x4}
            elif len(self.stream_playlists) == 6:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                             self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5}
            elif len(self.stream_playlists) == 7:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                             self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                             self.stream_playlists[6]: x6}
            elif len(self.stream_playlists) == 8:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                             self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                             self.stream_playlists[6]: x6, self.stream_playlists[7]: x7}
            elif len(self.stream_playlists) == 9:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                             self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                             self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8}
            elif len(self.stream_playlists) == 10:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                             self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                             self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                             self.stream_playlists[9]: x9}
            elif len(self.stream_playlists) == 11:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                             self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                             self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                             self.stream_playlists[9]: x9, self.stream_playlists[10]: x10}
            elif len(self.stream_playlists) == 12:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                             self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                             self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                             self.stream_playlists[9]: x9, self.stream_playlists[10]: x10,
                             self.stream_playlists[11]: x11}
            elif len(self.stream_playlists) == 13:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                             self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                             self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                             self.stream_playlists[9]: x9, self.stream_playlists[10]: x10,
                             self.stream_playlists[11]: x11,
                             self.stream_playlists[12]: x12}
            elif len(self.stream_playlists) == 14:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                             self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                             self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                             self.stream_playlists[9]: x9, self.stream_playlists[10]: x10,
                             self.stream_playlists[11]: x11,
                             self.stream_playlists[12]: x12, self.stream_playlists[13]: x13}
            elif len(self.stream_playlists) == 15:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                             self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                             self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                             self.stream_playlists[9]: x9, self.stream_playlists[10]: x10,
                             self.stream_playlists[11]: x11,
                             self.stream_playlists[12]: x12, self.stream_playlists[13]: x13,
                             self.stream_playlists[14]: x14}
            elif len(self.stream_playlists) == 16:
                sub_menu1 = {self.stream_playlists[0]: x0, self.stream_playlists[1]: x1, self.stream_playlists[2]: x2,
                             self.stream_playlists[3]: x3, self.stream_playlists[4]: x4, self.stream_playlists[5]: x5,
                             self.stream_playlists[6]: x6, self.stream_playlists[7]: x7, self.stream_playlists[8]: x8,
                             self.stream_playlists[9]: x9, self.stream_playlists[10]: x10,
                             self.stream_playlists[11]: x11,
                             self.stream_playlists[12]: x12, self.stream_playlists[13]: x13,
                             self.stream_playlists[14]: x14,
                             self.stream_playlists[15]: x15}
            else:
                def nothing(x):
                    print("nothing")

                sub_menu1 = {"Nothing": nothing}

            def quitFunc(x):
                self.Stop()

            self.systray = EveconLib.Tools.Windows.SysTray("data\\Ico\\Radio.ico", "Evecon: Radio", {"Pause/Unpause": unp_p},
                                   sub_menu1=sub_menu1, sub_menu_name1="Change Radio", quitFunc=quitFunc)
            self.systray.start()
            self.printit()

    def printit(self):
        EveconLib.Tools.cls()
        if not self.streampause:
            print("Radio:\n\nPlaying:")
        else:
            print("Radio:\n\nPaused:")

        print(self.streamplaying)
        print("\n")
        if not self.streamPrintOth:
            if not self.streampause:
                print("Pause (PAU), Stop (STOP), Change (CH), Volume (VOL)")
            else:
                print("Unpause (PAU), Stop (STOP), Change (CH), Volume (VOL)")
        elif self.streamPrintVol:
            print("Volume (Now: %s)\n" % EveconLib.Tools.Windows.Volume.getVolume())

        elif self.streamPrintCh:

            for xl, x2 in zip(self.stream_playlists, self.stream_playlists_key):
                print(x2 + " (" + x2.upper() + ")")

            print("Change to:\n")

