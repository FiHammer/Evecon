import time
from cls import *
import ctypes
import os
import sys
import datetime
import socket
import subprocess
import shutil




def exit_now():
	global ttime_stop
	ttime_stop = 1
	global exitnow
	exitnow = 1
	if version_PC != 1:
		exit()

cdir = os.getcwd()
if cdir == "C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\Programs\\Evecon\\Updater":
	os.chdir("..")
	os.chdir("..")
	os.chdir("..")
else:
	os.chdir("..")

title_oldstatus = "Loading"
title_oldstart = ""
exitnow = 0
Alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z" ,]




def title(status="OLD", something="OLD"):

	global title_oldstatus, title_oldstart
	if status == "OLD":
		status = title_oldstatus
	else:
		title_oldstatus = status

	if something == "OLD":
		something = title_oldstart
	else:
		title_oldstart = something


	space_status = (60 - len(status) * 2) * " "

	ctypes.windll.kernel32.SetConsoleTitleW("EVECON Updater: %s%s%s" %
	(status, space_status, something))

title("Loading Light")

def light(preset="Man"):
	if preset == "dark":
		os.system("color 07")

	if preset == "bright":
		os.system("color F0")

	if preset == "Man":
		cls()
		print("Color change")
		print("First is background")
		print("Second is foreground")
		print("Standard: 07 (White on black)\n")
		print("    0 = Schwarz     8 = Grau")
		print("    1 = Blau        9 = Hellblau")
		print("    2 = Gruen       A = Hellgruen")
		print("    3 = Tuerkis     B = Helltuerkis")
		print("    4 = Rot         C = Hellrot")
		print("    5 = Lila        D = Helllila")
		print("    6 = Gelb        E = Hellgelb")
		print("    7 = Hellgrau    F = Weiss")

		os.system("color %s" % input("\n"))

Computername = socket.gethostname()

if Computername[0] == "P":
	if os.environ.get("USERNAME") == "NEUHOF":
		if os.getlogin() == "albingerl":
			title("OLD", "OLD", "albingerl@SchoolPC")
			Computerfind_SchoolPC_alb = 1
			Computerfind_SchoolPC = 1
			computerconfig_schoolpc()
		else:
			Computerfind_SchoolPC_alb = 0
			Computerfind_SchoolPC = 1
			computerconfig_schoolpc()
	else:
		Computerfind_SchoolPC_alb = 0
		Computerfind_SchoolPC = 0
else:
	Computerfind_SchoolPC_alb = 0
	Computerfind_SchoolPC = 0

if Computername == "Computer-Testet":
	title("OLD", "OLD")
	Computerfind_MiniPC = 1
	Computerfind_BigPC = 0
	Computerfind_PapaAldi = 0
	Computerfind_Laptop = 0

elif Computername == "XX":
	title("OLD", "OLD")
	Computerfind_MiniPC = 0
	Computerfind_BigPC = 1
	Computerfind_PapaAldi = 0
	Computerfind_Laptop = 0

elif Computername == "Test":
	title("OLD", "OLD")
	Computerfind_MiniPC = 0
	Computerfind_BigPC = 0
	Computerfind_PapaAldi = 1
	Computerfind_Laptop = 0

elif Computername == "Luis":
	title("OLD", "OLD")
	Computerfind_MiniPC = 0
	Computerfind_BigPC = 0
	Computerfind_PapaAldi = 0
	Computerfind_Laptop = 1

else:
	title("OLD", "OLD")
	Computerfind_MiniPC = 0
	Computerfind_BigPC = 0
	Computerfind_PapaAldi = 0
	Computerfind_Laptop = 0

file_proversion_raw = open("data\\Info\\ProgramVersion", "r")
ProVersion = file_proversion_raw.readline()
file_proversion_raw.close()


if ProVersion == "PC-Version":
	if Computerfind_MiniPC == 1:
		version_PC = 1
		version_MiniPC = 1
		version_BigPC = 0
		version_MainStick = 0
		version_MiniStick = 0
	if Computerfind_BigPC == 1:
		version_PC = 1
		version_MiniPC = 0
		version_BigPC = 1
		version_MainStick = 0
		version_MiniStick = 0
elif ProVersion == "MainStick-Version":
	version_PC = 0
	version_MiniPC = 0
	version_BigPC = 0
	version_MainStick = 1
	version_MiniStick = 0
elif ProVersion == "MiniStick-Version":
	version_PC = 0
	version_MiniPC = 0
	version_BigPC = 0
	version_MainStick = 0
	version_MiniStick = 1
else:
	title("Loading")
	version_PC = 0
	version_MiniPC = 0
	version_BigPC = 0
	version_MainStick = 0
	version_MiniStick = 0

title("Loading Arguments")

def Evecons(findversions=0):
	global Evecons_multi, Evecons_mainstick, Evecons_mainstick_path, Evecons_mainstick_pathkey, Evecons_PC, Evecons_PC_path, Evecons_ministick, Evecons_ministick_path, Evecons_ministick_pathkey

	Eveconss = []
	Evecons_multi = 0
	Evecons_mainstick = 0
	Evecons_mainstick_path = 0
	Evecons_mainstick_pathkey = 0
	Evecons_PC = 0
	if os.path.isfile("C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\data\\Info\\exist"):
		Evecons_PC_path = "C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon"
	elif  os.path.isfile(""):   # BigPC noch einfügen
		Evecons_PC_path = ""
	Evecons_ministick = 0
	Evecons_ministick_path = 0
	Evecons_ministick_pathkey = 0

	for Alpha in Alphabet:
		if os.path.isfile("%s:\\Evecon\\data\\Info\\exist" % Alpha):
			file_proversionstick_raw = open("data\\Info\\ProgramVersion", "r")
			proversionunkownstick = file_proversionstick_raw.readline()
			file_proversionstick_raw.close()

			if proversionunkownstick == "MainStick-Version":

				Eveconss.append("MainStick")
				Evecons_mainstick = 1
				Evecons_mainstick_pathkey = Alpha
				Evecons_mainstick_path = ("%s:\\Evecon" % Alpha)

				def mainstick_version():
					file_mainstick_version_raw = open("%s:\\Evecon\\data\\Info\\version" % Evecons_mainstick_pathkey, "r")
					mainstickversion = []
					for x in file_mainstick_version_raw:
						mainstickversion.append(x.strip())
					file_mainstick_version_raw.close()

				if findversions == 1:
					mainstick_version()

			if proversionunkownstick == "MiniStick-Version":

				Eveconss.append("MiniStick")
				Evecons_ministick = 1
				Evecons_ministick_pathkey = Alpha
				Evecons_ministick_path = ("%s:\\Evecon" % Alpha)

				def ministick_version():
					file_ministick_version_raw = open("%s:\\Evecon\\data\\Info\\version" % Evecons_ministick_pathkey, "r")
					ministickversion = []
					for x in file_ministick_version_raw:
						ministickversion.append(x.strip())
					file_ministick_version_raw.close()

				if findversions == 1:
					ministick_version()

	if version_MainStick == 1:
		if os.path.isfile("C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\data\\Info\\exist"):

			Eveconss.append("PC")
			Evecons_PC = 1

			def PC_version():
				file_PC_version_raw = open("C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\data\\Info\\version", "r")
				PCversion = []
				for x in file_PC_version_raw:
					PCversion.append(x.strip())
				file_PC_version_raw.close()

			if findversions == 1:
				PC_version()

		elif os.path.isfile(""):  # BigPC einfügen

			Eveconss.append("PC")
			Evecons_PC = 1

			def PC_version():
				file_PC_version_raw = open("", "r")
				PCversion = []
				for x in file_PC_version_raw:
					PCversion.append(x.strip())
				file_PC_version_raw.close()

			if findversions == 1:
				PC_version()

	if version_MiniStick == 1:
		if os.path.isfile("C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\data\\Info\\exist"):

			Eveconss.append("PC")
			Evecons_PC = 1

			def PC_version():
				file_PC_version_raw = open("C:\\Users\\Mini-Pc Nutzer\\Desktop\\Evecon\\data\\Info\\version", "r")
				PCversion = []
				for x in file_PC_version_raw:
					PCversion.append(x.strip())
				file_PC_version_raw.close()

			if findversions == 1:
				PC_version()

		elif os.path.isfile(""): # BigPC einfügen

			Eveconss.append("PC")
			Evecons_PC = 1

			def PC_version():
				file_PC_version_raw = open("", "r")
				PCversion = []
				for x in file_PC_version_raw:
					PCversion.append(x.strip())
				file_PC_version_raw.close()

			if findversions == 1:
				PC_version()


	if len(Eveconss) >= 2:
		Evecons_multi = 1


def version():
	file_version_raw = open("data\\Info\\version", "r")
	global this_version
	this_version = []
	for xcc in file_version_raw:
		this_version.append(xcc.strip())
	file_version_raw.close()


def update():
	cls()
	version()
	global this_version

	Evecons(1)

	global Evecons_multi, Evecons_mainstick, Evecons_mainstick_path, Evecons_PC, Evecons_PC_path, Evecons_ministick, Evecons_ministick_path, restart


	def this_to_PC():
		backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_PC_path, "w")  # von diesem auf PC
		backuptime.write("Backup:\nFrom: %s\nTo: Mini-PC\nDate: %s\nTime: %s\nVersion: %s" % (
		ProVersion.rstrip("-Version"), datetime.datetime.now().strftime("%d.%m.%Y"),
		datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
		backuptime.close()
		shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_PC_path)
		shutil.copytree("%s\\!Evecon" % Evecons_PC_path, "%s\\data\\Backup\\!Evecon" % Evecons_PC_path)
		shutil.rmtree("%s\\!Evecon" % Evecons_PC_path)
		shutil.copytree("!Evecon", "%s" % Evecons_PC_path)
		shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_PC_path)
		shutil.copytree("%s\\data\\Notepad" % Evecons_PC_path, "%s\\data\\Backup\\data\\Notepad" % Evecons_PC_path)
		shutil.rmtree("%s\\data\\Notepad" % Evecons_PC_path)
		shutil.copytree("data\\Notepad", "%s\\data\\Notepad" % Evecons_PC_path)

		os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_PC_path)
		shutil.copy("%s\\data\\Info\\version" % Evecons_PC_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_PC_path)
		os.remove("%s\\data\\Info\\version" % Evecons_PC_path)
		shutil.copy("data\\Info\\version", "%s\\data\\Info" % Evecons_PC_path)
		os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_PC_path)
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_PC_path)
		os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path)
		shutil.copy("data\\Info\\Changelog.txt", "%s\\data\\Info" % Evecons_PC_path)

	def PC_to_this():
		backuptime = open("data\\Backup\\backup.txt", "w")  # von PC auf diesen
		backuptime.write("Backup:\nFrom: Mini-PC\nTo: %s\nDate: %s\nTime: %s\nVersion: %s" % (
			ProVersion.rstrip("-Version"), datetime.datetime.now().strftime("%d.%m.%Y"),
			datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
		backuptime.close()
		shutil.rmtree("data\\Backup\\!Evecon")
		shutil.copytree("!Evecon", "data\\Backup\\!Evecon")
		shutil.rmtree("!Evecon")
		shutil.copytree("%s\\!Evecon" % Evecons_PC_path, "!Evecon")
		shutil.rmtree("data\\Backup\\data\\Notepad")
		shutil.copytree("data\\Notepad", "data\\Backup\\data\\Notepad")
		shutil.rmtree("data\\Notepad")
		shutil.copytree("%s\\data\\Notepad" % Evecons_PC_path, "data\\Notepad")

		os.remove("data\\Backup\\data\\Info\\version")
		shutil.copy("data\\Info\\version", "data\\Backup\\data\\Info")
		os.remove("data\\Info\\version")
		shutil.copy("%s\\data\\Info\\version" % Evecons_PC_path, "data\\Info")
		os.remove("data\\Backup\\data\\Info\\Changelog.txt")
		shutil.copy("data\\Info\\Changelog.txt", "data\\Backup\\data\\Info")
		os.remove("data\\Info\\Changelog.txt")
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path, "data\\Info")

	def this_to_Mainstick():
		backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_mainstick_path, "w")  # von diesem auf Mainstick
		backuptime.write("Backup:\nFrom: %s\nTo: Mainstick\nDate: %s\nTime: %s\nVersion: %s" % (
			ProVersion.rstrip("-Version"), datetime.datetime.now().strftime("%d.%m.%Y"),
			datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
		backuptime.close()
		shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_mainstick_path)
		shutil.copytree("%s\\!Evecon" % Evecons_mainstick_path,
						"%s\\data\\Backup\\!Evecon" % Evecons_mainstick_path)
		shutil.rmtree("%s\\!Evecon" % Evecons_mainstick_path)
		shutil.copytree("!Evecon", "%s\\!Evecon" % Evecons_mainstick_path)
		shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_mainstick_path)
		shutil.copytree("%s\\data\\Notepad" % Evecons_mainstick_path,
						"%s\\data\\Backup\\data\\Notepad" % Evecons_mainstick_path)
		shutil.rmtree("%s\\data\\Notepad" % Evecons_mainstick_path)
		shutil.copytree("data\\Notepad", "%s\\data\\Notepad" % Evecons_mainstick_path)

		os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_mainstick_path)
		shutil.copy("%s\\data\\Info\\version" % Evecons_mainstick_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_mainstick_path)
		os.remove("%s\\data\\Info\\version" % Evecons_mainstick_path)
		shutil.copy("data\\Info\\version", "%s\\data\\Info" % Evecons_mainstick_path)
		os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_mainstick_path)
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_mainstick_path)
		os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path)
		shutil.copy("data\\Info\\Changelog.txt", "%s\\data\\Info" % Evecons_mainstick_path)

	def Mainstick_to_this():
		backuptime = open("data\\Backup\\backup.txt", "w")  # von Mainstick auf diesen
		backuptime.write("Backup:\nFrom: Mainstick\nTo: %s\nDate: %s\nTime: %s\nVersion: %s" % (
			ProVersion.rstrip("-Version"), datetime.datetime.now().strftime("%d.%m.%Y"),
			datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
		backuptime.close()
		shutil.rmtree("data\\Backup\\!Evecon")
		shutil.copytree("!Evecon", "data\\Backup\\!Evecon")
		shutil.rmtree("!Evecon")
		shutil.copytree("%s\\!Evecon" % Evecons_mainstick_path, "!Evecon")
		shutil.rmtree("data\\Backup\\data\\Notepad")
		shutil.copytree("data\\Notepad", "data\\Backup\\data\\Notepad")
		shutil.rmtree("data\\Notepad")
		shutil.copytree("%s\\data\\Notepad" % Evecons_mainstick_path, "data\\Notepad")

		os.remove("data\\Backup\\data\\Info\\version")
		shutil.copy("data\\Info\\version", "data\\Backup\\data\\Info")
		os.remove("data\\Info\\version")
		shutil.copy("%s\\data\\Info\\version" % Evecons_mainstick_path, "data\\Info")
		os.remove("data\\Backup\\data\\Info\\Changelog.txt")
		shutil.copy("data\\Info\\Changelog.txt", "data\\Backup\\data\\Info")
		os.remove("data\\Info\\Changelog.txt")
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path, "data\\Info")

	def this_to_Ministick():
		backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_ministick_path, "w")  # von diesem auf Ministick
		backuptime.write("Backup:\nFrom: %s\nTo: Ministick-PC\nDate: %s\nTime: %s\nVersion: %s" % (
			ProVersion.rstrip("-Version"), datetime.datetime.now().strftime("%d.%m.%Y"),
			datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
		backuptime.close()
		shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_ministick_path)
		shutil.copytree("%s\\!Evecon" % Evecons_ministick_path,
						"%s\\data\\Backup\\!Evecon" % Evecons_ministick_path)
		shutil.rmtree("%s\\!Evecon" % Evecons_ministick_path)
		shutil.copytree("!Evecon", "%s\\!Evecon" % Evecons_ministick_path)
		shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_ministick_path)
		shutil.copytree("%s\\data\\Notepad" % Evecons_ministick_path,
						"%s\\data\\Backup\\data\\Notepad" % Evecons_ministick_path)
		shutil.rmtree("%s\\data\\Notepad" % Evecons_ministick_path)
		shutil.copytree("data\\Notepad", "%s\\data\\Notepad" % Evecons_ministick_path)

		os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_ministick_path)
		shutil.copy("%s\\data\\Info\\version" % Evecons_ministick_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_ministick_path)
		os.remove("%s\\data\\Info\\version" % Evecons_ministick_path)
		shutil.copy("data\\Info\\version", "%s\\data\\Info" % Evecons_ministick_path)
		os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_ministick_path)
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_ministick_path)
		os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path)
		shutil.copy("data\\Info\\Changelog.txt", "%s\\data\\Info" % Evecons_ministick_path)

	def Ministick_to_this():
		backuptime = open("data\\Backup\\backup.txt", "w")  # von Ministick auf diesen
		backuptime.write("Backup:\nFrom: Ministick\nTo: %s\nDate: %s\nTime: %s\nVersion: %s" % (
			ProVersion.rstrip("-Version"), datetime.datetime.now().strftime("%d.%m.%Y"),
			datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
		backuptime.close()
		shutil.rmtree("data\\Backup\\!Evecon")
		shutil.copytree("!Evecon", "data\\Backup\\!Evecon")
		shutil.rmtree("!Evecon")
		shutil.copytree("%s\\!Evecon" % Evecons_ministick_path, "!Evecon")
		shutil.rmtree("data\\Backup\\data\\Notepad")
		shutil.copytree("data\\Notepad", "data\\Backup\\data\\Notepad")
		shutil.rmtree("data\\Notepad")
		shutil.copytree("%s\\data\\Notepad" % Evecons_ministick_path, "data\\Notepad")

		os.remove("data\\Backup\\data\\Info\\version")
		shutil.copy("data\\Info\\version", "data\\Backup\\data\\Info")
		os.remove("data\\Info\\version")
		shutil.copy("%s\\data\\Info\\version" % Evecons_ministick_path, "data\\Info")
		os.remove("data\\Backup\\data\\Info\\Changelog.txt")
		shutil.copy("data\\Info\\Changelog.txt", "data\\Backup\\data\\Info")
		os.remove("data\\Info\\Changelog.txt")
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path, "data\\Info")

	def PC_to_Mainstick():
		backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_mainstick_path, "w")  # von PC auf Mainstick
		backuptime.write("Backup:\nFrom: PC\nTo: Mainstick\nDate: %s\nTime: %s\nVersion: %s" % (
			datetime.datetime.now().strftime("%d.%m.%Y"),
			datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
		backuptime.close()
		shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_mainstick_path)
		shutil.copytree("%s\\!Evecon" % Evecons_mainstick_path,
						"%s\\data\\Backup\\!Evecon" % Evecons_mainstick_path)
		shutil.rmtree("%s\\!Evecon" % Evecons_mainstick_path)
		shutil.copytree("%s\\!Evecon" % Evecons_PC_path, "%s\\!Evecon" % Evecons_mainstick_path)
		shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_mainstick_path)
		shutil.copytree("%s\\data\\Notepad" % Evecons_mainstick_path,
						"%s\\data\\Backup\\data\\Notepad" % Evecons_mainstick_path)
		shutil.rmtree("%s\\data\\Notepad" % Evecons_mainstick_path)
		shutil.copytree("%s\\data\\Notepad" % Evecons_PC_path, "%s\\data\\Notepad" % Evecons_mainstick_path)

		os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_mainstick_path)
		shutil.copy("%s\\data\\Info\\version" % Evecons_mainstick_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_mainstick_path)
		os.remove("%s\\data\\Info\\version" % Evecons_mainstick_path)
		shutil.copy("%s\\data\\Info\\version" % Evecons_PC_path, "%s\\data\\Info" % Evecons_mainstick_path)
		os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_mainstick_path)
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_mainstick_path)
		os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path)
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path, "%s\\data\\Info" % Evecons_mainstick_path)

	def PC_to_Ministick():
		backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_ministick_path, "w")  # von PC auf Ministick
		backuptime.write("Backup:\nFrom: PC\nTo: Ministick\nDate: %s\nTime: %s\nVersion: %s" % (
			datetime.datetime.now().strftime("%d.%m.%Y"),
			datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
		backuptime.close()
		shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_ministick_path)
		shutil.copytree("%s\\!Evecon" % Evecons_ministick_path,
						"%s\\data\\Backup\\!Evecon" % Evecons_ministick_path)
		shutil.rmtree("%s\\!Evecon" % Evecons_ministick_path)
		shutil.copytree("%s\\!Evecon" % Evecons_PC_path, "%s\\!Evecon" % Evecons_ministick_path)
		shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_ministick_path)
		shutil.copytree("%s\\data\\Notepad" % Evecons_ministick_path,
						"%s\\data\\Backup\\data\\Notepad" % Evecons_ministick_path)
		shutil.rmtree("%s\\data\\Notepad" % Evecons_ministick_path)
		shutil.copytree("%s\\data\\Notepad" % Evecons_PC_path, "%s\\data\\Notepad" % Evecons_ministick_path)

		os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_ministick_path)
		shutil.copy("%s\\data\\Info\\version" % Evecons_ministick_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_ministick_path)
		os.remove("%s\\data\\Info\\version" % Evecons_ministick_path)
		shutil.copy("%s\\data\\Info\\version" % Evecons_PC_path, "%s\\data\\Info" % Evecons_ministick_path)
		os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_ministick_path)
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_ministick_path)
		os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path)
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path, "%s\\data\\Info" % Evecons_ministick_path)

	def Mainstick_to_Ministick():
		backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_ministick_path, "w")  # von Mainstick auf Ministick
		backuptime.write("Backup:\nFrom: Mainstick\nTo: Ministick\nDate: %s\nTime: %s\nVersion: %s" % (
			datetime.datetime.now().strftime("%d.%m.%Y"),
			datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
		backuptime.close()
		shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_ministick_path)
		shutil.copytree("%s\\!Evecon" % Evecons_ministick_path, "%s\\data\\Backup\\!Evecon" % Evecons_ministick_path)
		shutil.rmtree("%s\\!Evecon" % Evecons_ministick_path)
		shutil.copytree("%s\\!Evecon" % Evecons_mainstick_path, "%s\\!Evecon" % Evecons_ministick_path)
		shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_ministick_path)
		shutil.copytree("%s\\data\\Notepad" % Evecons_ministick_path,
						"%s\\data\\Backup\\data\\Notepad" % Evecons_ministick_path)
		shutil.rmtree("%s\\data\\Notepad" % Evecons_ministick_path)
		shutil.copytree("%s\\data\\Notepad" % Evecons_mainstick_path, "%s\\data\\Notepad" % Evecons_ministick_path)

		os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_ministick_path)
		shutil.copy("%s\\data\\Info\\version" % Evecons_ministick_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_ministick_path)
		os.remove("%s\\data\\Info\\version" % Evecons_ministick_path)
		shutil.copy("%s\\data\\Info\\version" % Evecons_mainstick_path, "%s\\data\\Info" % Evecons_ministick_path)
		os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_ministick_path)
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_ministick_path)
		os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path)
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path, "%s\\data\\Info" % Evecons_ministick_path)

	def Ministick_to_Mainstick():
		backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_mainstick_path, "w")  # von Ministick auf Mainstick
		backuptime.write("Backup:\nFrom: Mainstick\nTo: Ministick\nDate: %s\nTime: %s\nVersion: %s" % (
			datetime.datetime.now().strftime("%d.%m.%Y"),
			datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
		backuptime.close()
		shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_mainstick_path)
		shutil.copytree("%s\\!Evecon" % Evecons_mainstick_path, "%s\\data\\Backup\\!Evecon" % Evecons_mainstick_path)
		shutil.rmtree("%s\\!Evecon" % Evecons_mainstick_path)
		shutil.copytree("%s\\!Evecon" % Evecons_ministick_path, "%s\\!Evecon" % Evecons_mainstick_path)
		shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_mainstick_path)
		shutil.copytree("%s\\data\\Notepad" % Evecons_mainstick_path,
						"%s\\data\\Backup\\data\\Notepad" % Evecons_mainstick_path)
		shutil.rmtree("%s\\data\\Notepad" % Evecons_mainstick_path)
		shutil.copytree("%s\\data\\Notepad" % Evecons_ministick_path, "%s\\data\\Notepad" % Evecons_mainstick_path)

		os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_mainstick_path)
		shutil.copy("%s\\data\\Info\\version" % Evecons_mainstick_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_mainstick_path)
		os.remove("%s\\data\\Info\\version" % Evecons_mainstick_path)
		shutil.copy("%s\\data\\Info\\version" % Evecons_ministick_path, "%s\\data\\Info" % Evecons_mainstick_path)
		os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_mainstick_path)
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_mainstick_path)
		os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path)
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path, "%s\\data\\Info" % Evecons_mainstick_path)

	def Ministick_to_PC():
		backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_PC_path,
						  "w")
		backuptime.write("Backup:\nFrom: Mainstick\nTo: Ministick\nDate: %s\nTime: %s\nVersion: %s" % (
			datetime.datetime.now().strftime("%d.%m.%Y"),
			datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
		backuptime.close()
		shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_PC_path)
		shutil.copytree("%s\\!Evecon" % Evecons_PC_path,
						"%s\\data\\Backup\\!Evecon" % Evecons_PC_path)
		shutil.rmtree("%s\\!Evecon" % Evecons_PC_path)
		shutil.copytree("%s\\!Evecon" % Evecons_ministick_path,
						"%s\\!Evecon" % Evecons_PC_path)
		shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_PC_path)
		shutil.copytree("%s\\data\\Notepad" % Evecons_PC_path,
						"%s\\data\\Backup\\data\\Notepad" % Evecons_PC_path)
		shutil.rmtree("%s\\data\\Notepad" % Evecons_PC_path)
		shutil.copytree("%s\\data\\Notepad" % Evecons_ministick_path,
						"%s\\data\\Notepad" % Evecons_PC_path)

		os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_PC_path)
		shutil.copy("%s\\data\\Info\\version" % Evecons_PC_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_PC_path)
		os.remove("%s\\data\\Info\\version" % Evecons_PC_path)
		shutil.copy("%s\\data\\Info\\version" % Evecons_ministick_path,
					"%s\\data\\Info" % Evecons_PC_path)
		os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_PC_path)
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_PC_path)
		os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path)
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_ministick_path,
					"%s\\data\\Info" % Evecons_PC_path)

	def Mainstick_to_PC():
		backuptime = open("%s\\data\\Backup\\backup.txt" % Evecons_PC_path, "w")  # von Mainstick auf Ministick
		backuptime.write("Backup:\nFrom: Mainstick\nTo: Ministick\nDate: %s\nTime: %s\nVersion: %s" % (
			datetime.datetime.now().strftime("%d.%m.%Y"),
			datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
		backuptime.close()
		shutil.rmtree("%s\\data\\Backup\\!Evecon" % Evecons_PC_path)
		shutil.copytree("%s\\!Evecon" % Evecons_PC_path, "%s\\data\\Backup\\!Evecon" % Evecons_PC_path)
		shutil.rmtree("%s\\!Evecon" % Evecons_PC_path)
		shutil.copytree("%s\\!Evecon" % Evecons_mainstick_path, "%s\\!Evecon" % Evecons_PC_path)
		shutil.rmtree("%s\\data\\Backup\\data\\Notepad" % Evecons_PC_path)
		shutil.copytree("%s\\data\\Notepad" % Evecons_PC_path,
						"%s\\data\\Backup\\data\\Notepad" % Evecons_PC_path)
		shutil.rmtree("%s\\data\\Notepad" % Evecons_PC_path)
		shutil.copytree("%s\\data\\Notepad" % Evecons_mainstick_path, "%s\\data\\Notepad" % Evecons_PC_path)

		os.remove("%s\\data\\Backup\\data\\Info\\version" % Evecons_PC_path)
		shutil.copy("%s\\data\\Info\\version" % Evecons_PC_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_PC_path)
		os.remove("%s\\data\\Info\\version" % Evecons_PC_path)
		shutil.copy("%s\\data\\Info\\version" % Evecons_mainstick_path, "%s\\data\\Info" % Evecons_PC_path)
		os.remove("%s\\data\\Backup\\data\\Info\\Changelog.txt" % Evecons_PC_path)
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path,
					"%s\\data\\Backup\\data\\Info" % Evecons_PC_path)
		os.remove("%s\\data\\Info\\Changelog.txt" % Evecons_PC_path)
		shutil.copy("%s\\data\\Info\\Changelog.txt" % Evecons_mainstick_path, "%s\\data\\Info" % Evecons_PC_path)

	if Evecons_multi == 0:
		if Evecons_PC == 1:
			if this_version[0] > PCversion[0]:
				this_to_PC()

			elif this_version[0] < PCversion[0]:
				PC_to_this()
				restart = True

		elif Evecons_mainstick == 1:
			if this_version[0] > mainstickversion[0]:
				this_to_Mainstick()

			elif this_version[0] < mainstickversion[0]:
				Mainstick_to_this()
				restart = True

		elif Evecons_ministick == 1:
			if this_version[0] > ministickversion[0]:
				this_to_Ministick()

			elif this_version[0] < ministickversion[0]:
				Ministick_to_this()
				restart = True

	else:                                   # Wenn mehr als drei Programme gleichzeitig dies umprogrammieren!
		if version_PC == 1:
			if mainstickversion[0] > ministickversion[0]:
				highestversion = mainstickversion[0]
				highestversionname = "Mainstick"
				mustupdateanother = 1
			elif mainstickversion[0] < ministickversion[0]:
				highestversion = ministickversion[0]
				highestversionname = "Ministick"
				mustupdateanother = 1
			else:
				highestversion = mainstickversion[0]
				highestversionname = "Mainstick"
				mustupdateanother = 0

			if this_version[0] > highestversion:

				this_to_Mainstick()
				this_to_Ministick()


			elif this_version[0] < highestversion:
				if mustupdateanother == 1: # beide update
					if highestversionname == "Mainstick":

						Mainstick_to_this()
						Mainstick_to_Ministick()
						restart = True


					elif highestversionname == "Ministick":

						Ministick_to_this()
						Ministick_to_Mainstick()
						restart = True

				else:

					Mainstick_to_this()
					restart = True

			elif this_version[0] == highestversion:
				if mustupdateanother == 1:
					if highestversionname == "Mainstick":
						# von diesem (PC) auf Ministick
						this_to_Ministick()

					elif highestversionname == "Ministick":
						# von diesem (PC) auf Mainstick
						this_to_Mainstick()

		elif version_MainStick == 1:
			if PCversion[0] > ministickversion[0]:
				highestversion = PCversion[0]
				highestversionname = "PC"
				mustupdateanother = 1
			elif PCversion[0] < ministickversion[0]:
				highestversion = ministickversion[0]
				highestversionname = "Ministick"
				mustupdateanother = 1
			else:
				highestversion = PCversion[0]
				highestversionname = "Mainstick"
				mustupdateanother = 0

			if this_version[0] > highestversion:

				this_to_PC()
				this_to_Ministick()

			elif this_version[0] < highestversion:
				if mustupdateanother == 1:  # beide update
					if highestversionname == "PC":

						# von PC auf diesen (Mainstick)
						PC_to_this()

						# von PC auf Ministick
						PC_to_Ministick()
						restart = True

					elif highestversionname == "Ministick":

						# von Ministick auf diesen (Mainstick)
						Ministick_to_this()

						# von Ministick auf PC
						Ministick_to_PC()
						restart = True

				else:
					# PC auf diesen (Mainstick)
					PC_to_Mainstick()


			elif this_version[0] == highestversion:
				if mustupdateanother == 1:
					if highestversionname == "PC":

						# von PC auf Ministick
						PC_to_Ministick()

					elif highestversionname == "Ministick":

						# von diesem (Mainstick) auf PC
						this_to_PC()

		elif version_MiniStick == 1:
			if PCversion[0] > mainstickversion[0]:
				highestversion = PCversion[0]
				highestversionname = "PC"
				mustupdateanother = 1
			elif PCversion[0] < mainstickversion[0]:
				highestversion = mainstickversion[0]
				highestversionname = "Mainstick"
				mustupdateanother = 1
			else:
				highestversion = PCversion[0]
				highestversionname = "Mainstick"
				mustupdateanother = 0

			if this_version[0] > highestversion:

				# von diesem (MiniStick) auf PC
				this_to_PC()

				# von diesem (MiniStick) auf Mainstick
				this_to_Mainstick()

			elif this_version[0] < highestversion:
				if mustupdateanother == 1:  # beide update
					if highestversionname == "PC":

						# von PC auf diesen (MiniStick)
						PC_to_this()

						# von PC auf Mainstick
						PC_to_Mainstick()
						restart = True

					elif highestversionname == "Mainstick":

						# von Mainstick auf diesen (MiniStick)
						Mainstick_to_this()
						# von Mainstick auf PC
						Mainstick_to_PC()
						restart = True

				else:

					# von PC auf diesen (MiniStick)
					PC_to_this()
					restart = True

			elif this_version[0] == highestversion:

				if mustupdateanother == 1:

					if highestversionname == "PC":

						# von PC auf Mainstick
						PC_to_Mainstick()

					elif highestversionname == "Mainstick":

						# von Mainstick auf PC
						Mainstick_to_PC()


def upgrade():
	cls()
	if version_PC == 1:
		title("Upgrade", "Changelog")
		version()
		global this_version
		print("Changelog\n\nOld Version: %s" % this_version[1])
		newversion = input("\nNew Version: ")
		newupdate = []
		newupdate_firstinput = False
		while True:
			cls()
			print("Updates:\n")
			if newupdate_firstinput:
				print("In this Update:")
				for x in range(len(newupdate)):
					print(newupdate[x])
			newupdate_input = input("Type 'END' to exit\n\n")
			if newupdate_input.lower() == "end":
				break
			newupdate.append(newupdate_input)
			newupdate_firstinput = True
		cls()
		title("Upgrade", "Backup")

		backuptime = open("data\\Backup\\backup.txt", "w")
		backuptime.write("Backup while Upgrading:\nDate: %s\nTime: %s\nVersion: %s" % (
			datetime.datetime.now().strftime("%d.%m.%Y"),
			datetime.datetime.now().strftime("%H:%M:%S"), this_version[1]))
		backuptime.close()
		shutil.rmtree("data\\Backup\\!Evecon")
		shutil.copytree("!Evecon", "data\\Backup\\!Evecon")

		os.remove("data\\Backup\\data\\Info\\version")
		shutil.copy("data\\Info\\version", "data\\Backup\\data\\Info")
		os.remove("data\\Backup\\data\\Info\\Changelog.txt")
		shutil.copy("data\\Info\\Changelog.txt", "data\\Backup\\data\\Info")

		title("Upgrade", "Change Version")

		this_version_1 = int(this_version[0]) + 1
		file_change_version_raw = open("data\\Info\\version", "w")
		file_change_version_raw.write("%s\n%s" % (str(this_version_1), newversion))
		file_change_version_raw.close()

		title("Upgrade", "Change Changelog")

		file_changelog_raw = open("data\\Info\\Changelog.txt", "a+")
		file_changelog_raw.write("Version: %s\nNumber: %s\nDate: %s\nTime: %s\nChanges:\n" % (newversion, str(this_version_1),
			datetime.datetime.now().strftime("%d.%m.%Y"), datetime.datetime.now().strftime("%H:%M:%S")))
		for x in range(len(newupdate)):
			file_changelog_raw.write(newupdate[x])
			file_changelog_raw.write("\n")
		file_changelog_raw.write("\n\n")
		file_changelog_raw.close()


		version()

		title("Upgrade", "Deleting")

		dir_tmp = os.getcwd()
		os.chdir("!Evecon\\dev")
		shutil.rmtree("build\\!Console")
		shutil.rmtree("dist\\!Console")

		title("Upgrade", "Installing")

		os.system("pyinstaller !Console.py")
		time.sleep(1)
		os.chdir(dir_tmp)
		shutil.rmtree("!Evecon\\!Console")
		shutil.copytree("!Evecon\\dev\\dist\\!Console", "!Evecon\\!Console")
		shutil.copy("!Evecon\\dev\\dll\\avbin64.dll", "!Evecon\\!Console")

		# 2. Changelog und neue version abfragen mit alte zeigen (version) 3. backup 4. os.system("pyinstaller x") 5. kopieren 6. neustart wenn mit arg -re mit !Evecon.bat
	else:
		print("Only at a PC with PyInstaller!")
		time.sleep(3)

skiparg = []

for x in range(3):
	try:
		sys.argv[x]
	except IndexError:
		sys.argv.append(None)
		skiparg.append(x)
test = []
if not skiparg:
	skiparg.append(2)

for x in range(1, 2):
	if x >= skiparg[0]:
		break
	if sys.argv[x] == "-update":
		title("Updating", "Self-start")
		update()
		if restart:
			subprocess.call(["!Evecon.bat"])
		exit_now()
	if sys.argv[x] == "-upgrade":
		title("Upgrading", "Self-start")
		upgrade()
		subprocess.call(["!Evecon.bat"])
		exit_now()


def main():
	title("Waiting for Input")

	cls()
	user_input = input("What to do?\nUpdate (UD), Upgrade (UG)\n\n")

	if user_input.lower() == "ud":
		update()
	if user_input.lower() == "ug":
		upgrade()



if exitnow == 0:
	if __name__ == "__main__":
		main()
		time.sleep(0)

		exit_now()


