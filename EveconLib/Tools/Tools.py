import time
import os
import sys
import threading
import random
import subprocess

def cls():
    if sys.platform == "win32":
        #pass
        os.system("cls")

class ddbug(threading.Thread):
    def __init__(self):
        super().__init__()
        self.work = True

    def run(self):
        while self.work:
            time.sleep(1)

def turnStr(word: str):
    wordfin = ""
    for x in range(len(word)):
        wordfin += word[len(word) - 1 - x]
    return wordfin


def lsame(fullword: str, partword: str, exact=True):
    matches = 0
    if not exact:
        fullword = fullword.lower()
        partword = partword.lower()
    for x, y in zip(fullword, partword):
        if x == y:
            matches += 1
    if matches == len(partword):
        return True
    else:
        return False


def rsame(fullword: str, partword: str, exact=True):
    matches = 0
    if not exact:
        fullword = fullword.lower()
        partword = partword.lower()
    fullwordX = turnStr(fullword)
    partwordX = turnStr(partword)
    for x, y in zip(fullwordX, partwordX):
        if x == y:
            matches += 1
    if matches == len(partword):
        return True
    else:
        return False



def TimeFor(Time):
    if (round(Time) % 60) == 0:
        TimeFor = "%s:%s%s" % (round(Time) // 60, 0, 0)
    elif (round(Time) % 60) < 10:
        TimeFor = "%s:%s%s" % (round(Time) // 60, 0, round(Time) % 60)
    else:
        TimeFor = "%s:%s" % (round(Time) // 60, round(Time) % 60)
    return TimeFor

def timeFormat_minsec(milsec, enMilsec=True, enSec=True, enMin=True, enHr=False, enDay=False, auto=True, units=True):
    """
    formats the time, given in milliseconds, parsed in str
    the parameters beginning with 'en' enables the output
    seconds, minutes, hours, days
    :param auto: this will automaticly decide, which ouput types will be activated

    :type milsec: int
    :type enMilsec: bool
    :type enSec: bool
    :type enMin: bool
    :type enHr: bool
    :type enDay: bool
    :type auto: bool
    :type units: bool

    :rtype: str
    :return: formatted time day:hr:min:sec:milsec
    """

    _milsec = milsec
    _sec = _milsec // 1000
    _mi = _sec // 60
    _hr = _mi // 60
    _day = _hr // 60

    milsec = _milsec % 1000
    sec = _sec % 60
    mi = _mi % 60
    hr = _hr % 24
    day = _day

    parse = ""

    if auto:
        if day:
            if units:
                parse += str(int(day)) + "d:"
            else:
                parse += str(int(day)) + ":"
        else:
            hr += day * 60
        if hr:
            if units:
                parse += str(int(hr)) + "h:"
            else:
                parse += str(int(hr)) + ":"
        else:
            mi += hr * 60
        if mi:
            if units:
                parse += str(int(mi)) + "m:"
            else:
                parse += str(int(mi)) + ":"
        else:
            sec += mi * 60
        if sec:
            if units:
                parse += str(sec) + "s:"
            else:
                parse += str(sec) + ":"
        else:
            milsec += sec * 60
        if milsec:
            if units:
                parse += str(int(milsec)) + "ms"
            else:
                parse += str(int(milsec))
    else:
        if enDay:
            if units:
                parse += str(int(day)) + "d:"
            else:
                parse += str(int(day)) + ":"
        else:
            hr += day * 60
        if enHr:
            if units:
                parse += str(int(hr)) + "h:"
            else:
                parse += str(int(hr)) + ":"
        else:
            mi += hr * 60
        if enMin:
            if units:
                parse += str(int(mi)) + "m:"
            else:
                parse += str(int(mi)) + ":"
        else:
            sec += mi * 60
        if enSec:
            if units:
                parse += str(int(sec)) + "s:"
            else:
                parse += str(int(sec)) + ":"
        else:
            milsec += sec * 60
        if enMilsec:
            if units:
                parse += str(int(milsec)) + "ms"
            else:
                parse += str(int(milsec))

    return parse


def timeFormat_sec(sec, enMilsec=True, enSec=True, enMin=True, enHr=False, enDay=False, auto=True, units=True):
    """
    formats the time, given in milliseconds, parsed in str
    the parameters beginning with 'en' enables the output
    seconds, minutes, hours, days
    :param auto: this will automaticly decide, which ouput types will be activated

    :type sec: float
    :type enMilsec: bool
    :type enSec: bool
    :type enMin: bool
    :type enHr: bool
    :type enDay: bool
    :type auto: bool
    :type units: bool

    :rtype: str
    :return: formatted time
    """

    _milsec = sec * 1000
    _sec = _milsec // 1000
    _mi = _sec // 60
    _hr = _mi // 60
    _day = _hr // 60

    milsec = _milsec % 1000
    sec = _sec % 60
    mi = _mi % 60
    hr = _hr % 24
    day = _day

    parse = ""

    if auto:
        if day:
            if units:
                parse += str(int(day)) + "d:"
            else:
                parse += str(int(day)) + ":"
        else:
            hr += day * 60
        if hr:
            if units:
                parse += str(int(hr)) + "h:"
            else:
                parse += str(int(hr)) + ":"
        else:
            mi += hr * 60
        if mi:
            if units:
                parse += str(int(mi)) + "m:"
            else:
                parse += str(int(mi)) + ":"
        else:
            sec += mi * 60
        if sec:
            if units:
                parse += str(int(sec)) + "s:"
            else:
                parse += str(int(sec)) + ":"
        else:
            milsec += sec * 60
        if milsec:
            if units:
                parse += str(int(milsec)) + "ms"
            else:
                parse += str(int(milsec))
    else:
        if enDay:
            if units:
                parse += str(int(day)) + "d:"
            else:
                parse += str(int(day)) + ":"
        else:
            hr += day * 60
        if enHr:
            if units:
                parse += str(int(hr)) + "h:"
            else:
                parse += str(int(hr)) + ":"
        else:
            mi += hr * 60
        if enMin:
            if units:
                parse += str(int(mi)) + "m:"
            else:
                parse += str(int(mi)) + ":"
        else:
            sec += mi * 60
        if enSec:
            if units:
                parse += str(int(sec)) + "s:"
            else:
                parse += str(int(sec)) + ":"
        else:
            milsec += sec * 60
        if enMilsec:
            if units:
                parse += str(int(milsec)) + "ms"
            else:
                parse += str(int(milsec))

    return parse


def timeFormat_min(mi, enMilsec=True, enSec=True, enMin=True, enHr=False, enDay=False, auto=True, units=True):
    """
    formats the time, given in milliseconds, parsed in str
    the parameters beginning with 'en' enables the output
    seconds, minutes, hours, days
    :param auto: this will automaticly decide, which ouput types will be activated

    :type mi: float
    :type enMilsec: bool
    :type enSec: bool
    :type enMin: bool
    :type enHr: bool
    :type enDay: bool
    :type auto: bool
    :type units: bool

    :rtype: str
    :return: formatted time
    """

    _milsec = mi * 60 * 1000
    _sec = _milsec // 1000
    _mi = _sec // 60
    _hr = _mi // 60
    _day = _hr // 60

    milsec = _milsec % 1000
    sec = _sec % 60
    mi = _mi % 60
    hr = _hr % 24
    day = _day

    parse = ""

    if auto:
        if day:
            if units:
                parse += str(int(day)) + "d:"
            else:
                parse += str(int(day)) + ":"
        else:
            hr += day * 60
        if hr:
            if units:
                parse += str(int(hr)) + "h:"
            else:
                parse += str(int(hr)) + ":"
        else:
            mi += hr * 60
        if mi:
            if units:
                parse += str(int(mi)) + "m:"
            else:
                parse += str(int(mi)) + ":"
        else:
            sec += mi * 60
        if sec:
            if units:
                parse += str(sec) + "s:"
            else:
                parse += str(sec) + ":"
        else:
            milsec += sec * 60
        if milsec:
            if units:
                parse += str(int(milsec)) + "ms"
            else:
                parse += str(int(milsec))
    else:
        if enDay:
            if units:
                parse += str(int(day)) + "d:"
            else:
                parse += str(int(day)) + ":"
        else:
            hr += day * 60
        if enHr:
            if units:
                parse += str(int(hr)) + "h:"
            else:
                parse += str(int(hr)) + ":"
        else:
            mi += hr * 60
        if enMin:
            if units:
                parse += str(int(mi)) + "m:"
            else:
                parse += str(int(mi)) + ":"
        else:
            sec += mi * 60
        if enSec:
            if units:
                parse += str(int(sec)) + "s:"
            else:
                parse += str(int(sec)) + ":"
        else:
            milsec += sec * 60
        if enMilsec:
            if units:
                parse += str(int(milsec)) + "ms"
            else:
                parse += str(int(milsec))

    return parse


def timeFormat_hr(hr, enMilsec=True, enSec=True, enMin=True, enHr=False, enDay=False, auto=True, units=True):
    """
    formats the time, given in milliseconds, parsed in str
    the parameters beginning with 'en' enables the output
    seconds, minutes, hours, days
    :param auto: this will automaticly decide, which ouput types will be activated

    :type hr: float
    :type enMilsec: bool
    :type enSec: bool
    :type enMin: bool
    :type enHr: bool
    :type enDay: bool
    :type auto: bool
    :type units: bool

    :rtype: str
    :return: formatted time
    """

    _milsec = hr * 60 * 60 * 1000
    _sec = _milsec // 1000
    _mi = _sec // 60
    _hr = _mi // 60
    _day = _hr // 60

    milsec = _milsec % 1000
    sec = _sec % 60
    mi = _mi % 60
    hr = _hr % 24
    day = _day

    parse = ""

    if auto:
        if day:
            if units:
                parse += str(int(day)) + "d:"
            else:
                parse += str(int(day)) + ":"
        else:
            hr += day * 60
        if hr:
            if units:
                parse += str(int(hr)) + "h:"
            else:
                parse += str(int(hr)) + ":"
        else:
            mi += hr * 60
        if mi:
            if units:
                parse += str(int(mi)) + "m:"
            else:
                parse += str(int(mi)) + ":"
        else:
            sec += mi * 60
        if sec:
            if units:
                parse += str(int(sec)) + "s:"
            else:
                parse += str(int(sec)) + ":"
        else:
            milsec += sec * 60
        if milsec:
            if units:
                parse += str(int(milsec)) + "ms"
            else:
                parse += str(int(milsec))
    else:
        if enDay:
            if units:
                parse += str(int(day)) + "d:"
            else:
                parse += str(int(day)) + ":"
        else:
            hr += day * 60
        if enHr:
            if units:
                parse += str(int(hr)) + "h:"
            else:
                parse += str(int(hr)) + ":"
        else:
            mi += hr * 60
        if enMin:
            if units:
                parse += str(int(mi)) + "m:"
            else:
                parse += str(int(mi)) + ":"
        else:
            sec += mi * 60
        if enSec:
            if units:
                parse += str(int(sec)) + "s:"
            else:
                parse += str(int(sec)) + ":"
        else:
            milsec += sec * 60
        if enMilsec:
            if units:
                parse += str(int(milsec)) + "ms"
            else:
                parse += str(int(milsec))

    return parse


def timeFormat_day(day, enMilsec=True, enSec=True, enMin=True, enHr=False, enDay=False, auto=True, units=True):
    """
    formats the time, given in milliseconds, parsed in str
    the parameters beginning with 'en' enables the output
    seconds, minutes, hours, days
    :param auto: this will automaticly decide, which ouput types will be activated

    :type day: float
    :type enMilsec: bool
    :type enSec: bool
    :type enMin: bool
    :type enHr: bool
    :type enDay: bool
    :type auto: bool
    :type units: bool

    :rtype: str
    :return: formatted time
    """

    _milsec = day * 24 * 60 * 60 * 1000
    _sec = _milsec // 1000
    _mi = _sec // 60
    _hr = _mi // 60
    _day = _hr // 60

    milsec = _milsec % 1000
    sec = _sec % 60
    mi = _mi % 60
    hr = _hr % 24
    day = _day

    parse = ""

    if auto:
        if day:
            if units:
                parse += str(int(day)) + "d:"
            else:
                parse += str(int(day)) + ":"
        else:
            hr += day * 60
        if hr:
            if units:
                parse += str(int(hr)) + "h:"
            else:
                parse += str(int(hr)) + ":"
        else:
            mi += hr * 60
        if mi:
            if units:
                parse += str(int(mi)) + "m:"
            else:
                parse += str(int(mi)) + ":"
        else:
            sec += mi * 60
        if sec:
            if units:
                parse += str(int(sec)) + "s:"
            else:
                parse += str(int(sec)) + ":"
        else:
            milsec += sec * 60
        if milsec:
            if units:
                parse += str(int(milsec)) + "ms"
            else:
                parse += str(int(milsec))
    else:
        if enDay:
            if units:
                parse += str(int(day)) + "d:"
            else:
                parse += str(int(day)) + ":"
        else:
            hr += day * 60
        if enHr:
            if units:
                parse += str(int(hr)) + "h:"
            else:
                parse += str(int(hr)) + ":"
        else:
            mi += hr * 60
        if enMin:
            if units:
                parse += str(int(mi)) + "m:"
            else:
                parse += str(int(mi)) + ":"
        else:
            sec += mi * 60
        if enSec:
            if units:
                parse += str(int(sec)) + "s:"
            else:
                parse += str(int(sec)) + ":"
        else:
            milsec += sec * 60
        if enMilsec:
            if units:
                parse += str(int(milsec)) + "ms"
            else:
                parse += str(int(milsec))

    return parse


def MusicType(mType, exact=False):
    if rsame(mType, "mp3"):
        if exact:
            return "mp3"
        else:
            return True
    elif rsame(mType, "mp4"):
        if exact:
            return "mp4"
        else:
            return True
    else:
        return False


def Search(searchkeyU, searchlistU, exact=False, lower=True, onlyOnce=True):

    if len(searchkeyU) == 0 or type(searchkeyU) != str:
        return []

    if lower:
        searchkey = searchkeyU.lower()
        searchlist = []
        for x in searchlistU:
            searchlist.append(x.lower())
    else:
        searchkey = searchkeyU
        searchlist = []
        for x in searchlistU:
            searchlist.append(x)

    OutputNum = []

    for sListNum in range(len(searchlist)): # wort aus der liste
        if exact:
            if searchlist[sListNum] == searchkey:
                OutputNum.append(sListNum)
            else:
                continue
        if len(searchkey) > len(searchlist[sListNum]):
            continue  # suchwort größer als anderes wort (jetzt in der Liste)

        for letterNum in range(len(searchlist[sListNum])): # buchstabe aus wort aus der gesamt liste
            if searchlist[sListNum][letterNum] == searchkey[0]: # ist ein Buchstabe (aus der for-Schleife) auch in dem Suchwort[0] vorhanden?
                test = True

                for keyNum in range(len(searchkey)):
                    if test:
                        test = False
                        if keyNum == len(searchkey) - 1: # Fall: Wenn das Suchwort nur ein Buchstabe groß ist!
                            OutputNum.append(sListNum)
                            break
                        continue

                    # was macht das ?: wenn es der letzte buchstabe vom String ist ende
                    if len(searchlist[sListNum]) - 1 < keyNum + letterNum:
                        break
                    #if len(searchlist[sListNum]) - 1 < keyNum + letterNum:
                    #    print(OutputNum, sListNum, searchlist[sListNum], letterNum, searchlist[sListNum][letterNum], keyNum)

                    if searchlist[sListNum][keyNum + letterNum] == searchkey[keyNum]:
                        if keyNum == len(searchkey) - 1:

                            # if the keyword is two times in the fullword: this is a protect of duplication
                            doit = True
                            for NumOldList in OutputNum:
                                if NumOldList == sListNum:
                                    doit = False
                                    break

                            if doit:
                                OutputNum.append(sListNum)
                            break
                    else:
                        break

    if onlyOnce:
        OutputNum = DelDouble(OutputNum)


    return OutputNum


def DelDouble(workList: list):
    """
    deletes everything in the list which is multiple in the list

    :param workList: the list
    :return: new list
    """

    newList = []

    for x in workList:
        found=False
        for y in newList:
            if x == y:
                found=True
        if not found:
            newList.append(x)


    return newList


def SearchStr(searchkeyU: str, searchStrU: str, exact=False):

    if len(searchkeyU) == 0:
        return None

    if not exact:
        searchkey = searchkeyU.lower()
        searchlist = searchStrU.lower()
    else:
        searchkey = searchkeyU
        searchlist = searchStrU

    OutputNum = []


    for letterNum in range(len(searchlist)):
        if searchlist[letterNum] == searchkey[0]:
            test = False

            for keyNum in range(len(searchkey)):
                if test:
                    test = False
                    if keyNum == len(searchkey) - 1:
                        OutputNum.append(keyNum)
                        break
                    continue
                if len(searchlist) - 1 < keyNum + letterNum:
                    break

                if searchlist[keyNum + letterNum] == searchkey[keyNum]:
                    if keyNum == len(searchkey) - 1:
                        OutputNum.append(letterNum)
                        break
                else:
                    break

    return OutputNum

def unge(zahl):
    if type(zahl) != int:
        pass
    elif zahl/2 == int(zahl/2):
        return 0
    else:
        return 1

def getPartStr(word: str, begin: int, end: int):
    part = ""
    if len(word) < end or len(word) <= begin or begin >= end:
        return False

    for x in range(end):
        if x < begin:
            continue
        part += word[x]
    return part

def getPartStrToStr(word: str, endkey: str, beginkey="", exact=False):
    if exact:
        word = word.lower()
        endkey = endkey.lower()
    part = ""
    x = 0
    end = False
    beginskip = False
    beginover = False
    while True:
        if beginkey != "" and not beginover:
            z = 0
            for y in range(len(beginkey)):
                if word[x + y] == beginkey[y]:
                    z += 1
                else:
                    beginskip = True
                if z == len(beginkey):
                    beginover = True
                    x += z
            if beginskip:
                beginskip = False
                x += 1
                continue
        z = 0
        for y in range(len(endkey)):
            if word[x + y] == endkey[y]:
                z += 1
            else:
                break
            if z == len(endkey):
                end = True
                break
        if end:
            break
        part += word[x]
        x += 1

    return part


def randompw(returnpw=False, length=150, printpw=True, exclude=None):
    """

    :param returnpw:
    :param length:
    :param printpw:
    :param exclude:
    :return:
    :rtype: str
    """
    if exclude is None:
        exclude = []
    listx = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
             "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
             "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!",
             "§", "$", "%", "&", "/", "(", ")", "=", "?", "ß", "#", "'", "+", "*", "~", "ü", "ö", "ä", "-", "_", ".",
             ":", ",", ";", "{", "[", "]", "}", ">", "<", "|"]

    for x in exclude:
        for y in range(len(listx) - 1):
            if x == listx[y]:
                del listx[y]

    pw = ""

    for rx in range(length):
        pw += listx[random.randint(0, len(listx) - 1)]

    if returnpw:
        return pw

    if printpw:
        cls()
        print("Password: (length: %s) \n\n%s" % (length, pw))

        input()


"""
def MusicEncode(musicname):
    if MusicType(musicname):
        name = musicname.rstrip("." + MusicType(musicname, True))
    else:
        name = musicname

    try:
        title = getPartStrToStr(name, " by ")
        interpreter = getPartStrToStr(name, beginkey=title + " by ", endkey=" (")
        musictype = turnStr(getPartStrToStr(turnStr(name), endkey= turnStr(") - ")))

        part = getPartStrToStr(name, beginkey=title + " by " + interpreter + " (From ", endkey=") - " + musictype)

        x = SearchStr(" S", part, exact = True)
    except IndexError:
        return False


    animeSeason = True
    if len(x) > 1:
        x = x[len(x) - 1] + 1
    elif len(x) == 0:
        animeSeason = None
    else:
        x = x[0]  + 1

    if animeSeason:
        try:
            animeSeason = int(part[x + 1] + part[x + 2])
        except ValueError:
            animeSeason = int(part[x + 1])
        except IndexError:
            animeSeason = int(part[x + 1])

    y = SearchStr(" OP", part, exact = True)
    animeTypeNum = True
    if len(y) > 1:
        y = y[len(y) - 1] + 2
        animeType = "OP"
    elif len(y) == 0:
        y = SearchStr(" EN", part, exact=True)
        if len(y) > 1:
            y = y[len(y) - 1] + 2
            animeType = "EN"
        elif len(y) == 0:
            animeType = None
            animeTypeNum = None
        else:
            y = y[0] + 2
            animeType = "EN"
    else:
        y = y[0] + 2
        animeType = "OP"

    if animeTypeNum:
        try:
            animeTypeNum = int(part[y + 1] + part[y + 2])
        except ValueError:
            animeTypeNum = int(part[y + 1])
        except IndexError:
            animeTypeNum = int(part[y + 1])

    if animeSeason is not None:
        #animeName = gerPartStrToStr(part, endkey=" " + part[x] + part[x + 1])

        animeName = getPartStr(part, 0, x - 1)
    elif animeTypeNum is not None:
        #animeName = gerPartStrToStr(part, endkey=" " + part[y] + part[y + 1])

        animeName = getPartStr(part, 0, y - 1)
    else:
        animeName = part

    output = {"title": title, "interpreter": interpreter, "musictype": musictype, "animeName": animeName,
              "animeSeason": animeSeason, "animeType": animeType, "animeTypeNum": animeTypeNum}
    return output
"""

def MusicEncode(fileName: str):
    """
    output:
    dictionary with the keyword:
        title, interpreter, musictype, animeName, animeSeason, animeType, animeTypeNum
        valid, validAnime, noBrack

    :param fileName:
    :return: dict
    """

    output = {}

    x = MusicType(fileName, exact=True)
    if x:
        fileName = fileName.rstrip(x).rstrip(".")

    # getting possible positions

    find_by = SearchStr(" by ", fileName, exact=True)
    find_From = SearchStr(" (From ", fileName, exact=True)
    find_BrackClose =SearchStr(") - ", fileName, exact=True)

    by_pos = -1
    from_pos = -1
    brackClose_pos = -1

    # finding right positions

    if len(find_by) == 0:
        by_pos = -1  # not exisisting
    elif len(find_by) == 1:
        by_pos = find_by[0]
    else:  # more uses
        if len(find_From) == 1:
            if find_From[0] <= find_by[0]:
                by_pos = -1  # can not be after From

            elif find_From[0] > find_by[-1]:
                by_pos = find_by[-1]

            else: # between the bys
                for x in range(len(find_by)):
                    if find_by[x] < find_From[0]:
                        continue
                    else:
                        by_pos = find_by[x - 1]
                        break
        else:
            by_pos = -1

    if len(find_From) == 0 or len(find_BrackClose) == 0:
        from_pos = -1
        brackClose_pos = -1
    elif len(find_From) == 1:
        from_pos = find_From[0]
        if find_BrackClose[-1] > from_pos:
            for aPos in find_BrackClose:
                if aPos > from_pos:
                    brackClose_pos = aPos
                    break
        else:
            brackClose_pos = -1

    else:
        if find_BrackClose[-1] > find_From[0]:
            for x in range(len(find_From), 0, -1):
                if find_From[x] < find_BrackClose[-1]:
                    # should validate content
                    from_pos = find_From[x]
                    brackClose_pos = find_BrackClose[-1]
                    break
        else:
            from_pos = -1
            brackClose_pos = -1

    # validating positions

    if from_pos + brackClose_pos == -2 and 0 < by_pos:
        output["noBrack"] = True
        output["valid"] = True
    else:
        output["noBrack"] = False

        if 0 < by_pos < from_pos < brackClose_pos:
            output["valid"] = True
        else:
            output["valid"] = False
            return output


    if output["noBrack"]:  # only title + interpreter
        output["title"] = getPartStr(fileName, 0, by_pos)
        output["interpreter"] = getPartStr(fileName, by_pos + 4, len(fileName))

        output["valid"] = False # only for tmp purpose!
        return output
    else:
        output["title"] = getPartStr(fileName, 0, by_pos)
        output["interpreter"] = getPartStr(fileName, by_pos + 4, from_pos)
        output["musictype"] = getPartStr(fileName, brackClose_pos + 4, len(fileName))
        # inner bracket stuff

        brackStr = getPartStr(fileName, from_pos + 7, brackClose_pos)

        spaceParts = brackStr.split(" ")

        done = {"S": False, "Type": False}
        possibleParts = len(done)
        #print(fileName, spaceParts)
        if len(spaceParts) > 1:
            for stringPart in range(1, possibleParts+1):
                if lsame(spaceParts[-stringPart], "S", exact=True) and not done["S"]:
                    try:
                        output["animeSeason"] = int(spaceParts[-stringPart].lstrip("S"))
                        done["S"] = True
                    except ValueError:
                        pass
                elif lsame(spaceParts[-stringPart], "OP", exact=True) and not done["Type"]:
                    try:
                        output["animeTypeNum"] = int(spaceParts[-stringPart].lstrip("OP"))
                        output["animeType"] = "OP"
                        done["Type"] = True
                    except ValueError:
                        pass
                elif lsame(spaceParts[-stringPart], "EN", exact=True) and not done["Type"]:
                    try:
                        output["animeTypeNum"] = int(spaceParts[-stringPart].lstrip("EN"))
                        output["animeType"] = "EN"
                        done["Type"] = True
                    except ValueError:
                        pass
                elif lsame(spaceParts[-stringPart], "OST", exact=True) and not done["Type"]:
                    try:
                        output["animeTypeNum"] = int(spaceParts[-stringPart].lstrip("OST"))
                        output["animeType"] = "OST"
                        done["Type"] = True
                    except ValueError:
                        pass
        else:
            pass

        for x in done:
            if done[x]:
                del spaceParts[-1]

        output["animeName"] = ""
        for part in spaceParts:
            output["animeName"] += part + " "
        output["animeName"].rstrip()
        return output

def killme():
    subprocess.call(["taskkill", "/F", "/PID", str(os.getpid())])
    #os.system("taskkill /PID /F %s" % str(os.getpid()))



def doNothing(a="",b="",c="",d=""):
    pass

