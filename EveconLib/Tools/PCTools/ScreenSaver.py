import os

import EveconLib.Config

status = False

def refresh():
    global status
    if os.path.exists(EveconLib.Config.deacSSFile):
        status = False
    else:
        status = True


def switchStatus():
    if status:
        disable()
    else:
        enable()

def enable():
    with open(EveconLib.Config.deacSSFile, "w") as file:
        file.write("\n")
    return True


def disable():
    return os.remove(EveconLib.Config.deacSSFile)

refresh()