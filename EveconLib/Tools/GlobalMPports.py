import psutil
import os
import EveconLib.Config
import EveconLib.Tools.Tools

class GlobalMPports:
    def __init__(self, file):
        self.file = file
        self.ports = []
        self.programs = 0

        self.usePorts = []

        python = 0
        evecon = 0

        if not os.path.exists(file):
            return

        for x in psutil.process_iter():
            if x.name() == "!Console.exe":
                evecon += 1
            elif x.name() == "python.exe":
                python += 1

        if python + evecon == 1 or self.programs > python + evecon:
            self.resetFile()

        else:
            if os.path.exists(EveconLib.Config.tmpPath + EveconLib.Config.path_seg + self.file):
                if EveconLib.Config.validEnv:
                    with open(EveconLib.Config.tmpPath + EveconLib.Config.path_seg + self.file) as file:
                        lines = file.readlines()
                        for x in range(len(lines)):
                            if x == 0: # first Line
                                self.programs = int(lines[x].rstrip())
                            else:
                                try:
                                    int(x)
                                    self.ports.append(lines[x].rstrip())
                                except ValueError:
                                    self.resetFile()
                                    break
            else:
                self.resetFile()

    def readFile(self):
        python = 0
        evecon = 0

        for x in psutil.process_iter():
            if x.name() == "!Console.exe":
                evecon += 1
            elif x.name() == "python.exe":
                python += 1

        if python + evecon == 1 or self.programs > python + evecon:
            self.resetFile()

        else:
            if EveconLib.Config.validEnv:
                with open(EveconLib.Config.tmpPath + EveconLib.Config.path_seg + self.file) as file:
                    lines = file.readlines()
                    for x in range(len(lines)):
                        if x == 0: # first Line
                            self.programs = int(lines[x].rstrip())
                        else:
                            try:
                                int(x)
                                self.ports.append(lines[x].rstrip())
                            except ValueError:
                                self.resetFile()
                                break
                if len(self.ports) < self.programs:
                    self.resetFile()

    def writeFile(self):
        if EveconLib.Config.validEnv:
            with open(EveconLib.Config.tmpPath + EveconLib.Config.path_seg + self.file, "w") as file:
                for x in range(len(self.ports) + 1):
                    if x == 0:
                        file.write(str(self.programs) + "\n")
                    elif x == len(self.ports):
                        file.write(self.ports[x - 1])
                    else:
                        file.write(self.ports[x - 1] + "\n")
    def resetFile(self):
        self.programs = 0
        if EveconLib.Config.validEnv:
            with open(EveconLib.Config.tmpPath + EveconLib.Config.path_seg + self.file, "w") as file:
                file.write(str(self.programs))

    def addPort(self, port):
        if EveconLib.Tools.Tools.Search(str(port), self.ports):
            return False
        self.ports.append(str(port))
        if not self.usePorts:
            self.programs += 1
        self.usePorts.append(str(port))
        self.writeFile()
    def remPort(self, port):
        found = EveconLib.Tools.Tools.Search(str(port), self.ports)
        del self.ports[found[0]]

        found = EveconLib.Tools.Tools.Search(str(port), self.usePorts)
        del self.usePorts[found[0]]
        if not self.usePorts:
            self.programs -= 1
        self.writeFile()

