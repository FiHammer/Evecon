import json
import datetime
import time

import EveconLib.Config
import EveconLib.Tools


def readJson():
    global pageurl, data
    with open(EveconLib.Config.nheeDir + "website.txt") as file:
        pageurl = file.readline().rstrip()
    with open(EveconLib.Config.nheeDir + "data.json") as jsonfile:
        data = json.load(jsonfile)


def writeJson():
    with open(EveconLib.Config.nheeDir + "data.json", "w") as jsonfile:
        json.dump(data, jsonfile, indent=4, sort_keys=True)


def open_nhee():
    if not EveconLib.Config.enable_FoxNhe:
        readJson()
    browser.refresh()
    browser.open_win(data["Last"]["last_name_url"])
    if browser.running:
        time.sleep(4)
    else:
        time.sleep(8)
    browser.open_tab(data["Last"]["last_page_url"])


def open_nheename():
    if not EveconLib.Config.enable_FoxNhe:
        readJson()
    browser.open_win(data["Last"]["last_name_url"])


def open_nheepage():
    if not EveconLib.Config.enable_FoxNhe:
        readJson()
    browser.open_win(data["Last"]["last_page_url"])


def fap(opentype="nhee"):
    global data
    if not EveconLib.Config.enable_FoxNhe:
        readJson()
    EveconLib.Tools.cls()
    print("Loading ...")
    readJson()
    if opentype == "nhee":
        open_nhee()
    elif opentype == "nheename":
        open_nheename()
    elif opentype == "nheepage":
        open_nheepage()
    else:
        return False

    thistime_read = 0
    thistime_time = datetime.datetime.now().strftime("%H:%S:%M")
    thistime_date = datetime.datetime.now().strftime("%d.%m.%Y")

    idstart = int(data["Last"]["last_name_url"].split("/")[-2])

    EveconLib.Tools.cls()
    firstID = int(input("First ID of page:\n"))
    print("Which is your startpage (around %s)? (Begin: %s, Search for: %s)" % (
    (round((firstID - idstart) / 25) + data["Last"]["last_page"]), data["Last"]["last_page"], idstart))
    pagestart = int(input())

    thistime_timeC = EveconLib.Tools.Timer()
    thistime_timeC.start()

    flapping = True
    while flapping:
        EveconLib.Tools.cls()
        print("foxi:\n")
        print("You read: %s" % thistime_read)
        print("You are flapping: %s\n" % thistime_timeC.getTimeFor())

        print("Everything for Next, Finish (FIN)")

        user_input = input()

        if user_input == "p":
            thistime_timeC.pause()
            input("Pause END?")
            thistime_timeC.unpause()
        else:
            thistime_read += 1

            if user_input.lower() == "fin":
                break

    thistime_timeC.stop()

    EveconLib.Tools.cls()
    print("End Hanga: (Name)")
    hangaend_name = input()

    print("End Hanga: (URL)")
    hangaend_url = input()

    print("End Page: ")
    pageend = int(input())

    pageend_url = pageurl + str(pageend)
    pageprogress = pagestart - pageend

    idend = int(hangaend_url.split("/")[-2])
    idprogress = idend - idstart
    skipped = idprogress - thistime_read
    startname = data["Last"]["last_name"]
    starturl = data["Last"]["last_name_url"]

    data["Stats"] = {"fapped": data["Stats"]["fapped"] + 1,
                          "all_pages": data["Stats"]["all_pages"] + pageprogress,
                          "all_hangas": data["Stats"]["all_hangas"] + thistime_read}

    data["Last"] = {"last_page": pageend, "last_page_url": pageend_url,
                         "last_name": hangaend_name, "last_name_url": hangaend_url}

    data[str(data["Stats"]["fapped"])] = {"number": data["Stats"]["fapped"],
                                                    "date": thistime_date,
                                                    "starttime": thistime_time,
                                                    "time": thistime_timeC.getTimeFor(),
                                                    "foxi": {"read": thistime_read,
                                                             "skipped": skipped,
                                                             "pagestart": pagestart,
                                                             "pageend": pageend,
                                                             "pageprogress": pageprogress,
                                                             "idstart": idstart,
                                                             "idend": idend,
                                                             "idprogress": idprogress,
                                                             "start_Hanga": {
                                                                 "page": pagestart,
                                                                 "name": startname,
                                                                 "id": idstart,
                                                                 "url": starturl
                                                             },
                                                             "end_Hanga": {
                                                                 "page": pageend,
                                                                 "name": hangaend_name,
                                                                 "id": idend,
                                                                 "url": hangaend_url
                                                             }
                                                             }}

    writeJson()
    print("Finished")
    time.sleep(0.85)



if EveconLib.Config.browser == "firefox":
    browser = EveconLib.Tools.Browser.Firefox()
elif EveconLib.Config.browser == "vivaldi":
    browser = EveconLib.Tools.Browser.Vivaldi()
else:
    browser = EveconLib.Tools.Browser.Firefox()

pageurl = ""
import os
print(os.getcwd())
if EveconLib.Config.enable_FoxNhe and EveconLib.Config.validEnv:
    with open(EveconLib.Config.nheeDir + "website.txt") as file:
        pageurl = file.readline().rstrip()

    with open(EveconLib.Config.nheeDir + "data.json") as jsonfile:
        data = json.load(jsonfile)

