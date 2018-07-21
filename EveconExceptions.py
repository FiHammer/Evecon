
# !Console







# Updater


class MegaIsRunning(Exception):
    def __init__(self, background):
        if background:
            print("The MEGAcmdServer is running in background!")
        else:
            print("The MEGAcmdServer is already running in Evecon!")

class MegaNotRunning(Exception):
    def __init__(self):
        print("The MEGAcmdServer is not running!")

