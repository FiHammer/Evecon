# All



class MegaIsRunning(Exception):
    def __init__(self, background):
        if background:
            print("The MEGAcmdServer is running in background!")
        else:
            print("The MEGAcmdServer is already running in Evecon!")

class MegaNotRunning(Exception):
    def __init__(self):
        print("The MEGAcmdServer is not running!")

class MegaLoggedIn(Exception):
    def __init__(self):
        print("You are already logged in!")

class MegaNotLoggedIn(Exception):
    def __init__(self, details):
        if details == "upload":
            print("You are NOT logged in, so you can not upload files!")
        elif details == "logout":
            print("You are already logged out!")


# !Console

class EnergyPlanNotFound(Exception):
    def __init__(self):
        print("This Energy Plan is unkown")

#class EnergyUnicodeError(Exception):




# Updater



class UpdateZip(Exception):
    def __init__(self):
        print("zipping was not succsessful")