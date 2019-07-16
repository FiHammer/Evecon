import random
import time
import json

import EveconLib.Config
import EveconLib.Tools.Timer

class SplWeapRand:
    def __init__(self, roundtime = 180, weaponlang="Eng"):

        self.file = EveconLib.Config.splWeapFile
        self.weapons = {"ger":
                            ["Disperser", "Disperser Neo", "Junior-Klechser", "Junior-Klechser Plus", "Fein-Disperser",
                             "Fein-Disperser Neo", "Airbrush MG", "Airbrush RG", "Klechser", "Tentatek-Klechser",
                             "Kensa-Kleckser", "Heldenwaffe Replik (Klechser)", "Okto-Klechser Replik", ".52 Gallon",
                             ".52 Gallon Deko", "N-ZAP85", "N-ZAP89", "Profi-Klechser", "Focus-Profi-Kleckser",
                             "Kensa-Profi-Kleckser", ".96 Gallon", ".96 Gallon Deko", "Platscher", "Platscher SE",

                             "Luna-Blaster", "Luna-Blaster Neo", "Kensa-Luna-Blaster", "Blaster", "Blaster SE",
                             "Helden-Blaster Replik", "Fern-Blaster", "Fern-Blaster SE", "Kontra-Blaster",
                             "Kontra-Blaster Neo", "Turbo-Blaster", "Turbo-Blaster Deko", "Turbo-Blaster Plus",
                             "Turbo-Blaster Plus Deko",

                             "L3 Tintenwerfer", "L3 Tintenwerfer D", "S3 Tintenwerfer", "S3 Tintenwerfer D",
                             "Quetscher",
                             "Quetscher Fol",

                             "Karbonroller", "Karbonroller Deko", "Klecksroller", "Medusa-Klecksroller",
                             "Kensa-Klecksroller", "Helden-Roller Replik", "Dynaroller", "Dynaroller Tesla",
                             "Kensa-Dynaroller", "Flex-Roller", "Flex-Roller Fol",
                             "Quasto", "Quasto Fresco", "Kalligraf", "Kalligraf Fresco", "Helden-Pinsel Replik",

                             "Sepiator Alpha", "Sepiator Beta", "Klecks-Konzentrator", "Rilax-Klecks-Konzentrator",
                             "Kensa-Klecks-Konzentrator", "Helden-Konzentrator Replik", "Ziel-Konzentrator",
                             "Rilax-Ziel-Konzentrator", "Kensa-Ziel-Konzentrator", "E-liter 4K", "E-liter 4K SE",
                             "Ziel-E-liter 4K", "Ziel-E-liter 4K SE", "Klotzer 14-A", "Klotzer 14-B", "T-Tuber",
                             "T-Tuber SE",

                             "Schwapper", "Schwapper Deko", "Helden-Schwapper Replik", "3R-Schwapper",
                             "3R-Schwapper Fresco", "Knall-Schwapper", "Trommel-Schwapper", "Trommel-Schwapper Neo",
                             "Kensa-Trommel-Schapper", "Wannen-Schwapper",

                             "Klecks-Splatling", "Sagitron-Klecks-Splatling", "Splatling", "Splatling Deko",
                             "Helden-Splatling Replik", "Hydrant", "Hydrant SE", "Kuli-Splatling", "Nautilus 47",

                             "Sprenkler", "Sprenkler Fresco", "Klecks-Doppler", "Enperry-Klecks-Doppler",
                             "Kensa-Klecks-Doppler", "Helden-Doppler Replik", "Kelvin 525", "Kelvin 525 Deko",
                             "Dual-Platscher", "Dual-Platscher SE", "Quadhopper Noir", "Quadhopper Blanc",

                             "Parapulviator", "Sorella-Parapulviator", "Helden-Pulviator Replik", "Camp-Pulviator",
                             "Sorella-Camp-Pulviator", "UnderCover", "Sorella-UnderCover"],

                        "eng":
                            ["Sploosh-o-matic", "Neo Sploosh-o-matic", "Splattershot Jr.", "Custom Splattershot Jr.",
                             "Splash-o-matic", "Neo Splash-o-matic", "Aerospray MG", "Aerospray RG", "Splattershot",
                             "Tentatek Splattershot", "Kensa Splattershot", "Hero Shot Replica", "Octo Shot Replica",
                             ".52 Gal", ".52 Gal Deco", "N-ZAP '85", "N-ZAP '89", "Splattershot Pro",
                             "Forge Splattershot Pro", "Kensa Splattershot Pro", ".96 Gal", ".96 Gal Deco",
                             "Jet Squelcher", "Custom Jet Squelcher",

                             "Luna Blaster", "Luna Blaster Neo", "Kensa Luna Blaster", "Blaster", "Custom Blaster",
                             "Hero Blaster Replica", "Range Blaster", "Custom Range Blaster", "Clash Blaster",
                             "Clash Blaster Neo", "Rapid Blaster", "Rapid Blaster Deco", "Rapid Blaster Pro",
                             "Rapid Blaster Pro Deco",

                             "L-3 Nozzlenose", "L-3 Nozzlenose D", "H-3 Nozzlenose", "H-3 Nozzlenose D", "Squeezer",
                             "Foil Squeezer",

                             "Carbon Roller", "Carbon Roller Deco", "Splat Roller", "Krak-On Splat Roller",
                             "Kensa Splat Roller", "Hero Roller Replica", "Dynamo Roller", "Gold Dynamo Roller",
                             "Kensa Dynamo Roller", "Flingza Roller", "Foil Flingza Roller",
                             "Inkbrush", "Inkbrush Nouveau", "Octobrush", "Octobrush Nouveau", "Herobrush Replica",

                             "Classic Squiffer", "New Squiffer", "Splat Charger", "Firefin Splat Charger",
                             "Kensa Charger", "Hero Charger Replica", "Splatterscope", "Firefin Splatterscope",
                             "Kensa Splatterscope", "E-liter 4K", "Custom E-liter 4K", "E-liter 4K Scope",
                             "Custom E-liter 4K Scope", "Bamboozler 14 MK I", "Bamboozler 14 MK II", "Goo Tuber",
                             "Custom Goo Tuber",

                             "Slosher", "Slosher Deco", "Hero Slosher Replica", "Tri-Slosher", "Tri-Slosher Nouverau",
                             "Sloshing Machine", "Sloshing Machine Neo", "Kensa Sloshing Machine", "Bloblobber",
                             "Explosher",

                             "Mini Splatling", "Zink Mini Splatling", "Heavy Splatling", "Heavy Splatling Deco",
                             "Hero Splatling Replica", "Hydra Splatling", "Custom Hydra Splatling",
                             "Ballpoint Splatling",
                             "Nautilus 47",

                             "Bapple Dualies", "Bapple Dualies Nouveau", "Splat Dualies", "Enperry Splat Dualies",
                             "Kensa Splat Dualies", "Hero Dualie Replicas", "Glooga Dualies", "Glooga Dualies Deco",
                             "Dualie Squelchers", "Custom Dualie Squelchers", "Dark Tetra Dualies",
                             "Light Tetra Dualies",

                             "Splat Brella", "Sorella Brella", "Hero Brella Replica", "Tenta Brella",
                             "Tenta Sorella Brella", "Undercover Brella", "Undercover Sorella Brella"]
                        }

        if EveconLib.Config.validEnv:
            with open(self.file) as jsonfile:
                self.weapons = json.load(jsonfile)

        self.lang = weaponlang
        self.RUN = True
        self.Start = False
        self.TimeLeft = 0
        self.TimeLeftStart = 0
        self.TimeLeftC = EveconLib.Tools.Timer()
        self.Rounds = 0
        self.Playtime = 0
        self.PlaytimeStart = 0
        self.PlaytimeC = EveconLib.Tools.Timer()
        self.RoundOver = True
        self.Effect = None

        self.RoundTime = roundtime # Debug! std: 180

        self.WR = False
        self.WRthis = self.randomWP(lang="both")
        self.WRnext = self.randomWP(lang="both")

    def input(self, inpt):
        inpt = inpt.lower()
        if inpt == "wr":
            self.WRswitch()
            return True
        elif inpt == "exit" or inpt == "stop":
            self.stop()
            return True
        elif inpt == "reroll" or inpt == "rerol" or inpt == "rero" or inpt == "re" or inpt == "r":
            self.WRreroll()
            return True
        elif len(inpt) > 1:
            if inpt[0] == "e":
                try:
                    self.ChEffect(int(inpt.lstrip("e")))
                    return True
                except ValueError:
                    return self.RoundOverF()
            else:
                return self.RoundOverF()
        else:
            return self.RoundOverF()

    def randomWP(self, printweapon=False, lang=None):
        number = random.randint(0, len(self.weapons["eng"]) - 1)

        if not lang:
            if self.lang == "eng":
                weapon = self.weapons["eng"][number]
            else:  # German
                weapon = self.weapons["ger"][number]
        else:
            if lang == "eng":
                weapon = self.weapons["eng"][number]
            elif lang == "both":
                weapon = (self.weapons["eng"][number], self.weapons["ger"][number])
            else:  # German
                weapon = self.weapons["ger"][number]

        if printweapon:
            if lang == "both":
                print("Your Weapon:\n%s (%s)" % (weapon[0], weapon[1]))
            else:
                print("Your Weapon:\n%s" % weapon)
        return weapon

    def WRswitch(self):
        if self.WR:
            self.WR = False
        else:
            self.WR = True

    def stop(self):
        self.RUN = False

    def WRreroll(self):
        WRnextTMP = self.WRnext
        self.WRnext = self.randomWP(lang="both")

        while self.WRthis == self.WRnext or WRnextTMP == self.WRnext:
            self.WRnext = self.randomWP(lang="both")

    def ChEffect(self, eff):
        self.Effect = eff

    def RoundOverF(self):
        if self.RoundOver:
            if not self.Start:
                self.PlaytimeC.start()
                self.PlaytimeStart = time.time()
            self.TimeLeftC.start()
            self.TimeLeftStart = time.time()
            self.Rounds += 1

            if self.Effect is not None and self.Effect != 0:
                self.Effect -= 1

            if self.Start:
                WRthisTMP = self.WRthis
                self.WRthis = self.WRnext
                self.WRnext = self.randomWP(lang="both")

                while WRthisTMP == self.WRnext or self.WRthis == self.WRnext:
                    self.WRnext = self.randomWP(lang="both")

            self.RoundOver = False
            self.Start = True
            return True
        else:
            return False
    def returnmain(self):
        outputList = []
        self.TimeLeft = self.RoundTime - self.TimeLeftC.getTime()
        self.TimeLeft = self.RoundTime - round(time.time() - self.TimeLeftStart)

        if self.Start:
            self.Playtime = self.PlaytimeC.getTime()
            self.Playtime = round(time.time() - self.PlaytimeStart)
        else:
            self.Playtime = 0

        if self.RoundOver:
            TimeLeftFor = "No Round Started"
        else:
            if (self.TimeLeft % 60) < 10:
                TimeLeftFor = "%s:%s%s" % (self.TimeLeft // 60, 0, self.TimeLeft % 60)
            else:
                TimeLeftFor = "%s:%s" % (self.TimeLeft // 60, self.TimeLeft % 60)

        if (self.Playtime % 60) < 10:
            PlaytimeFor = "%s:%s%s" % (self.Playtime // 60, 0, self.Playtime % 60)
        else:
            PlaytimeFor = "%s:%s" % (self.Playtime // 60, self.Playtime % 60)

        if self.TimeLeft <= 0:
            self.RoundOver = True

        outputList.append("Splatoon 2\n")
        outputList.append("Time:\t\t %s" % TimeLeftFor)
        outputList.append("Round:\t\t %s" % self.Rounds)

        if self.Effect is not None and self.Effect != 0:
            outputList.append("Effect:\t\t %s" % self.Effect)
        elif self.Effect == 0:
            outputList.append("Effect:\t\t No Effect Active")

        outputList.append("Playtime:\t %s" % PlaytimeFor)
        if self.WR:
            outputList.append("\nWeapon Randomizer:")
            outputList.append("This Round:\t %s (%s)" % self.WRthis)
            outputList.append("Next Round:\t %s (%s)" % self.WRnext)

        if self.RoundOver:
            outputList.append("\nStart Next Round?")
        return outputList

    def printit(self, printcom=True):
        for line in self.returnmain():
            print(line)
        if printcom:
            for line in self.returncom():
                print(line)

    def returncom(self):
        outputList = []
        if self.WR:
            outputList.append("Weapon Randomizer (spWR), Effect (spE), Next Round (spN), Reroll Next Weapon (spR)")
        else:
            outputList.append("Weapon Randomizer (spWR), Effect (spE), Next Round (spN)")
        return outputList

    def printcom(self):
        for line in self.returncom():
            print(line)
