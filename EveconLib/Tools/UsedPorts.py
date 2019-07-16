import os
import psutil
import EveconLib.Tools.Tools
import EveconLib.Config



ports = []
programs = 0

usePorts = []

python = 0
evecon = 0


def readFile():
    global ports, programs, python, evecon
    ports = []
    programs = 0
    python = 0
    evecon = 0

    for x in psutil.process_iter():
        if x.name() == "!Console.exe":
            evecon += 1
        elif x.name() == "python.exe":
            python += 1
    """
    if python + evecon == 1 or self.programs > python + evecon:
        self.resetFile()

    else:
    """
    if EveconLib.Config.validEnv:
        with open(EveconLib.Config.usedPortsFile) as file:
            lines = file.readlines()
            for x in range(len(lines)):
                if x == 0:  # first Line
                    programs = int(lines[x].rstrip())
                else:
                    try:
                        int(x)
                        ports.append(lines[x].rstrip())
                    except ValueError:
                        resetFile()
                        break
        if len(ports) < programs:
            resetFile()


def writeFile():
    global ports, programs
    if EveconLib.Config.validEnv:
        with open(EveconLib.Config.usedPortsFile, "w") as file:
            for x in range(len(ports) + 1):
                if x == 0:
                    file.write(str(programs) + "\n")
                elif x == len(ports):
                    file.write(ports[x - 1])
                else:
                    file.write(ports[x - 1] + "\n")


def resetFile():
    global ports, programs, python, evecon, usePorts
    programs = 0
    python = 0
    evecon = 0
    usePorts = []
    ports = []
    with open(EveconLib.Config.usedPortsFile, "w") as file:
        file.write(str(programs))


def addPort(port):
    global ports, programs
    if EveconLib.Tools.Tools.Search(str(port), ports):
        return False
    ports.append(str(port))
    if not usePorts:
        programs += 1
    usePorts.append(str(port))
    writeFile()


def remPort(port):
    global ports, programs
    found = EveconLib.Tools.Tools.Search(str(port), ports)
    if not found:
        return
    del ports[found[0]]

    found = EveconLib.Tools.Tools.Search(str(port), usePorts)
    del usePorts[found[0]]
    if not usePorts:
        programs -= 1
    writeFile()


def isAvalible(port):
    readFile()
    if EveconLib.Tools.Tools.Search(str(port), ports):
        return False
    else:
        return True


def getNextPort(port):
    readFile()
    while True:
        port += 1
        if not EveconLib.Tools.Tools.Search(str(port), ports):
            return port


def givePort(port=4000):
    if not isAvalible(port):
        port = getNextPort(port)
    addPort(port)
    return port

def startup():
    global evecon, python, programs

    if not os.path.exists(EveconLib.Config.usedPortsFile):
        return

    for x in psutil.process_iter():
        if x.name() == "!Console.exe":
            evecon += 1
        elif x.name() == "python.exe":
            python += 1

    if python + evecon == 1 or programs > python + evecon - 1:
        resetFile()
    else:
        if os.path.exists(EveconLib.Config.usedPortsFile):
            with open(EveconLib.Config.usedPortsFile) as file:
                lines = file.readlines()
                for x in range(len(lines)):
                    if x == 0:  # first Line
                        programs = int(lines[x].rstrip())
                    else:
                        try:
                            int(x)
                            ports.append(lines[x].rstrip())
                        except ValueError:
                            resetFile()
                            break
        else:
            resetFile()


#startup() #now in global startup file