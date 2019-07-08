class VideoPlayer:
    def __init__(self, filepath, subtitle=True):
        self.player = pyglet.media.Player()
        self.vid = pyglet.media.load(filepath)
        self.filepath = filepath
        self.player.queue(self.vid)

        # player setup finished, label setup
        subpath = ""
        fpspl = filepath.split(".")
        for a in range(len(fpspl) - 1):
            subpath += fpspl[a] + "."

        subpath += "srt"

        if subtitle:
            subtitle = os.path.exists(subpath)

        if subtitle:
            pass  # parse subtitle here

        self.win = pyglet.window.Window(resizable=True)
        self.win.set_visible(False)

        @self.win.event
        def on_draw():
            self.player.get_texture().blit(0, 0)

        @self.win.event
        def on_close():
            self.player.delete()

    def start(self):
        self.win.set_visible(True)
        self.player.play()
        pyglet.app.run()
