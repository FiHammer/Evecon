import EveconLib.Tools
import EveconLib.Programs.Scanner
import EveconLib.Programs.Printer


class Findus:
    def __init__(self, workList: list, reactUser=None, prefix=None, suffix=None, startPos=0, expandRange=2,
                 scanner=None, autoPrint=False, afterPrint=True, autoSearch=False, onlyReturn=True, autoSort=False,
                 enableCommands=False, arrowSettings=None):
        """
        :param workList: the list with the content with witch the user can play
        :type workList: list

        :param reactUser: Findus will send the input of the user to this function if it is NOT NONE
        :type reactUser: function
        :type reactUser: NoneType

        :param prefix: will be printed(returned) before the word; str for all word; dict ('content of list': prefix in str) for singel; none for none
        :type prefix: str
        :type prefix: dict
        :type prefix: NoneType

        :param suffix: will be printed(returned) after the word; str for all word; dict ('content of list': prefix in str) for singel; none for none
        :type suffix: str
        :type suffix: dict
        :type suffix: NoneType

        :param startPos: sets the startposition of the curser
        :type startPos: int

        :param expandRange: sets the range of shown entries of the list above and under the curser
        :type expandRange: int

        :param scanner: use your own scanner
        :type scanner: Scanner

        :param autoPrint: enables the autoPrint function: will print every 1.5
        :type autoPrint: bool

        :param afterPrint: automaticly prints after every action
        :type afterPrint: bool

        :param autoSearch: the user can activate the search and can search in this
        :type autoSearch: bool

        :param onlyReturn: with this the react function will only get Returns. No more keypushes!
        :type onlyReturn: bool

        :param autoSort: enables autoSorting after 'every' (with enableInput) keypus
        :type autoSort: bool

        :param enableCommands: enables (other) commands (than search (is active with autoSearch))
        :type enableCommands: bool

        :param arrowSettings: Settings for multiple pressing of arrow up and down: [(minPress, maxPress (-1 = infinite), Plus), ...]
        :type arrowSettings: array
        """

        if arrowSettings is None:
            arrowSettings = [(3, 10, 3), (11, -1, 6)]
        if startPos >= len(workList):
            startPos = 0

        self._orgList = workList
        self.normList = workList
        self.searchList = workList
        self.workList = self._orgList.copy()

        self.curPos = startPos
        self.expandRange = expandRange
        self.enableInput = autoSearch
        self.onlyReturn = onlyReturn
        self.autoSort = autoSort
        self.afterPrint = afterPrint
        self.enableCommands = enableCommands

        self.arrowSetting = arrowSettings  # (minPress, maxPress (-1 = infinite), Plus)
        self.lastPresses = [0, time.time(), "None"]

        self.prefix = {}
        if isinstance(prefix, str):
            self.prefixEnabled = True
            for x in self.workList:
                self.prefix[x] = prefix

        elif isinstance(prefix, dict):
            self.prefixEnabled = True

            self.prefix = prefix
            alreadyLoaded = []
            for x in prefix:
                alreadyLoaded.append(x)

            for x in self.workList:
                if not EveconLib.Tools.Search(x, alreadyLoaded, exact=True, lower=False):
                    self.prefix[x] = ""

        else: # None or other
            self.prefixEnabled = False
            for x in self.workList:
                self.prefix[x] = ""

        self.suffix = {}
        if isinstance(suffix, str):
            self.suffixEnabled = True
            for x in self.workList:
                self.suffix[x] = suffix

        elif isinstance(suffix, dict):
            self.suffixEnabled = True

            self.suffix = suffix
            alreadyLoaded = []
            for x in suffix:
                alreadyLoaded.append(x)

            for x in self.workList:
                if not EveconLib.Tools.Search(x, alreadyLoaded, exact=True, lower=False):
                    self.suffix[x] = ""

        else:  # None or other
            self.suffixEnabled = False
            for x in self.workList:
                self.suffix[x] = ""

        self.debug = False
        self.started = False

        self.lastInput = ""
        self.Input = ""
        self.reactUser = reactUser

        if scanner:
            self.scanner = scanner
        else:
            self.scanner = EveconLib.Programs.Scanner(self.react)

        self.autoPrint = autoPrint
        if autoPrint:
            self.printer = EveconLib.Programs.Printer(self.printit, refreshTime=2)
        else:
            self.printer = None

        self.outputMode = "normal"
        self.searching = False
        self.searchWord = ""




    def sort(self, allLists=False):
        """
        sorts the list (workList & norm-/searchList) by the name of the content

        :param allLists: all lists will be sorted
        :type allLists: bool
        """

        self.workList.sort()

        if self.searching:
            self.searchList.sort()
            if allLists:
                self.normList.sort()
        else:
            self.normList.sort()
            if allLists:
                self.searchList.sort()

    def setCurPos(self, pos: int):
        """
        this method will set the position of the curser (and check if it is posible)

        :param pos: the new position of the curser
        :type pos: int

        :return: if new position was set
        """

        if len(self.workList) - 1 >= pos:
            self.curPos = pos
            return True
        else:
            return False

    def setNewList(self, workList: list, prefix=None, suffix=None, resetSearch=True):
        """
        deletes the old workList and overwrites it with the param

        :param resetSearch: if true it resets the searchWord
        :type resetSearch: bool

        :param workList: the new workList
        :type workList: list

        :param prefix: will be printed(returned) before the word; str for all word; dict ('content of list': prefix in str) for singel; none for none
        :type prefix: str
        :type prefix: dict
        :type prefix: NoneType

        :param suffix: will be printed(returned) after the word; str for all word; dict ('content of list': prefix in str) for singel; none for none
        :type suffix: str
        :type suffix: dict
        :type suffix: NoneType
        """

        self._orgList = workList
        self.normList = workList
        self.searchList = workList
        self.workList = workList

        self.prefix = {}
        if isinstance(prefix, str):
            self.prefixEnabled = True
            for x in self.workList:
                self.prefix[x] = prefix

        elif isinstance(prefix, dict):
            self.prefixEnabled = True

            self.prefix = prefix
            alreadyLoaded = []
            for x in prefix:
                alreadyLoaded.append(x)

            for x in self.workList:
                if not EveconLib.Tools.Search(x, alreadyLoaded, exact=True, lower=False):
                    self.prefix[x] = ""

        else:  # None or other
            self.prefixEnabled = False
            for x in self.workList:
                self.prefix[x] = ""

        self.suffix = {}
        if isinstance(suffix, str):
            self.suffixEnabled = True
            for x in self.workList:
                self.suffix[x] = suffix

        elif isinstance(suffix, dict):
            self.suffixEnabled = True

            self.suffix = suffix
            alreadyLoaded = []
            for x in suffix:
                alreadyLoaded.append(x)

            for x in self.workList:
                if not EveconLib.Tools.Search(x, alreadyLoaded, exact=True, lower=False):
                    self.suffix[x] = ""

        else:  # None or other
            self.suffixEnabled = False
            for x in self.workList:
                self.suffix[x] = ""

        if resetSearch:
            self.searchWord = ""
        else:
            self.search("", overwrite=False)

    def setPrefix(self, prefix, directName=""):
        """
        sets the prefix

        :param prefix: will be printed(returned) before the word; str for all word; dict ('content of list': prefix in str) for singel; none for none
        :type prefix: dict
        :type prefix: str
        :type prefix: NoneType

        :param directName: with this you can specify which one you want to change; var is the name/content of the workList; only works with prefix: str
        :type directName: str

        :return: success
        """

        if directName:
            if isinstance(prefix, str) and isinstance(directName, str) and directName in self.prefix:
                self.prefix[directName] = prefix
            else:
                return False
        else:
            self.prefix = {}
            if isinstance(prefix, str):
                self.prefixEnabled = True
                for x in self.workList:
                    self.prefix[x] = prefix

            elif isinstance(prefix, dict):
                self.prefixEnabled = True

                self.prefix = prefix
                alreadyLoaded = []
                for x in prefix:
                    alreadyLoaded.append(x)

                for x in self.workList:
                    if not EveconLib.Tools.Search(x, alreadyLoaded, exact=True, lower=False):
                        self.prefix[x] = ""

            else:  # None or other
                self.prefixEnabled = False
                for x in self.workList:
                    self.prefix[x] = ""

        return True

    def setSuffix(self, suffix, directName=""):
        """
        sets the suffix

        :param suffix: will be printed(returned) after the word; str for all word; dict ('content of list': prefix in str) for singel; none for none
        :type suffix: dict
        :type suffix: str
        :type suffix: NoneType

        :param directName: with this you can specify which one you want to change; var is the name/content of the workList; only works with prefix: str
        :type directName: str

        :return: success
        """
        if directName:
            if isinstance(suffix, str) and isinstance(directName, str) and directName in self.prefix:
                self.prefix[directName] = suffix
            else:
                return False
        else:
            self.suffix = {}
            if isinstance(suffix, str):
                self.suffixEnabled = True
                for x in self.workList:
                    self.suffix[x] = suffix

            elif isinstance(suffix, dict):
                self.suffixEnabled = True

                self.suffix = suffix
                alreadyLoaded = []
                for x in suffix:
                    alreadyLoaded.append(x)

                for x in self.workList:
                    if not EveconLib.Tools.Search(x, alreadyLoaded, exact=True, lower=False):
                        self.suffix[x] = ""

            else:  # None or other
                self.suffixEnabled = False
                for x in self.workList:
                    self.suffix[x] = ""

        return True

    def switchSearch(self):
        """
        switch the outputMode between search or normal
        switch the var searching
        sets the CurPos to 0
        changes the workList

        :return: returns True when switched to search, false for normal
        """
        if self.outputMode == "normal":
            self.workList = self.searchList.copy()
            self.Input = ""

            self.setCurPos(0)
            self.outputMode = "search"
            self.searching = True
            return True

        else:
            self.workList = self.normList.copy()
            self.Input = ""

            self.setCurPos(0)
            self.outputMode = "normal"
            self.searching = False
            return False


    def search(self, word: str, overwrite=True, refresh=True):
        """
        changes the searchword
        refreshs the workList (if searching or refresh)

        :param word: the new (part of the) searching word
        :type word: str

        :param overwrite: if true the old word will be overridden, else it will be append
        :type overwrite: bool

        :param refresh: if not only the searchWord will be changed, else it will be searched
        :type refresh: bool

        :return: the search word
        """

        if overwrite:
            self.searchWord = word
        else:
            self.searchWord += word

        if refresh:

            solutions = EveconLib.Tools.Search(self.searchWord, self._orgList)

            newList = []
            if solutions:
                for x in solutions:
                    newList.append(self._orgList[x])
            else:
                newList = self._orgList.copy()

            if self.curPos > len(newList) - 1:
                self.curPos = 0

            self.searchList = newList.copy()

        if self.searching:
            self.workList = self.searchList.copy()

        return self.searchWord


    def start(self):
        """
        starts the scanner

        :return: success
        """

        if not self.started and not self.scanner.is_alive():
            self.started = True
            self.scanner.start()

            if self.autoPrint:
                self.printer.start()

            return True
        else:
            return False


    def react(self, inpt: str):
        """
        :param inpt: the input that comes form the Scanner-object
        :type inpt: str

        :return: success
        """
        self.lastInput = inpt

        if self.lastPresses[1] + 0.2 >= time.time() and self.lastPresses[2] == inpt:  # DOUBLE PRESS
            mulPress = self.lastPresses[0] + 1
            self.lastPresses = [mulPress, time.time(), inpt]
        else:
            mulPress = 1
            self.lastPresses = [mulPress, time.time(), inpt]

        if inpt == "arrowup" and self.curPos > 0:  # down
            self.curPos -= 1

        elif inpt == "arrowdown" and self.curPos < len(self.workList) - 1:  # up
            self.curPos += 1

        elif inpt == "arrowup" and self.curPos > 0 and self.workList:
            done = False
            for aS in self.arrowSetting:
                if aS[0] < mulPress < aS[1] != -1 and not done or aS[0] < mulPress and aS[1] == -1 and not done:
                    done = True
                    if self.curPos - aS[2] >= 0:
                        self.curPos -= aS[2]
                    else:
                        self.curPos = 0
                    break

            if not done:
                self.curPos -= 1

        elif inpt == "arrowdown" and self.curPos < len(self.workList) - 1:
            done = False
            for aS in self.arrowSetting:
                if aS[0] < mulPress < aS[1] != -1 and not done or aS[0] < mulPress and aS[1] == -1 and not done:
                    done = True
                    if self.curPos + aS[2] <= len(self.workList) - 1:
                        self.curPos += aS[2]
                    else:
                        self.curPos = len(self.workList) - 1
                    break
            if not done:
                self.curPos += 1


        elif self.enableInput and not EveconLib.Tools.lsame(inpt, "arrow"):
            if inpt == "escape" and self.searching:
                self.switchSearch()

            elif len(inpt) == 1:
                self.Input += inpt

            elif inpt == "backspace":
                if len(self.Input) > 0:
                    new_Input = ""
                    for x in range(len(self.Input) - 1):
                        new_Input += self.Input[x]
                    self.Input = new_Input

            elif inpt == "strg_backspace":  # del
                self.Input = ""

            else:
                self.sendToUser(inpt)

            if self.searching: # if in search, search for it
                self.search(self.Input)
            else:              # if no search, command
                if self.enableCommands:
                    self.commands(self.Input)
                else:
                    self.sendToUser(inpt)

        elif self.reactUser and not EveconLib.Tools.lsame(inpt, "arrow"):
            self.sendToUser(inpt)
        else:
            return False

        if self.autoSort:
            self.sort()
        if self.afterPrint:
            self.printit()
        print(inpt)
        return True

    def sendToUser(self, inpt):
        """
        mini-method, for shrinking

        :param inpt: data
        :return:
        """
        if self.reactUser:
            if self.onlyReturn:
                if inpt == "return":
                    self.reactUser(inpt)
            else:
                self.reactUser(inpt)

    def commands(self, inpt: str, sendToReact=False):
        """
        :param inpt: the command change
        :type inpt: str

        :param sendToReact: if unsuccess, send to UserReact
        :type sendToReact: bool

        :return: success
        """

        if inpt == "search":
            return self.switchSearch()
        else:
            if sendToReact:
                if self.onlyReturn:
                    if inpt == "return":
                        self.reactUser(inpt)
                else:
                    self.reactUser(inpt)
            return False
        #return True

    def printit(self):
        """
        prints all programm output, after clearing the screen
        """
        EveconLib.Tools.cls()
        self.printbody()
        self.printfoot()

    def printbody(self):
        """
        prints the programm body output
        """
        for x in self.returnbody():
            print(x)

    def printfoot(self):
        """
        prints the programm foot output
        """
        print("")
        for x in self.returnfoot():
            print(x)

    def returnit(self):
        """
        :return: returns all programm output (list)
        """
        return self.returnbody() + self.returnfoot()

    def returnbody(self):
        """
        :return: returns the programm body output (list)
        """

        outputList = []
        search_done = False
        for now in range(self.expandRange):
            if not search_done:
                if self.curPos == now:
                    if self.expandRange >= len(self.workList) - 1:
                        for word_num in range(0, len(self.workList)):
                            if word_num + 1 < 10:
                                word_num_str = str(word_num + 1) + "  "
                            elif word_num + 1 < 100:
                                word_num_str = str(word_num + 1) + " "
                            else:
                                word_num_str = str(word_num + 1)

                            if self.prefixEnabled and self.suffixEnabled:
                                prefix = self.prefix[self.workList[word_num]] + " "
                                suffix = " " + self.suffix[self.workList[word_num]] + " "
                            elif self.prefixEnabled:
                                prefix = self.prefix[self.workList[word_num]] + " "
                                suffix = ""
                            elif self.suffixEnabled:
                                prefix = ""
                                suffix = " " + self.suffix[self.workList[word_num]] + " "
                            else:
                                prefix = ""
                                suffix = ""

                            if self.curPos == word_num:
                                if not self.debug:
                                    if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                                        outputList.append(" " + word_num_str + " * " + prefix + EveconLib.Tools.getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                                    else:
                                        outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix)
                                else:
                                    outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix + "0")
                            else:
                                if not self.debug:
                                    if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                                        outputList.append(" " + word_num_str + "   " + prefix + EveconLib.Tools.getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                                    else:
                                        outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix)
                                else:
                                    outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix + "1")

                    elif 2 * self.expandRange + 1 >= len(self.workList):
                        for word_num in range(0, 2 * self.expandRange + 1):  # + 1?
                            if word_num + 1 < 10:
                                word_num_str = str(word_num + 1) + "  "
                            elif word_num + 1 < 100:
                                word_num_str = str(word_num + 1) + " "
                            else:
                                word_num_str = str(word_num + 1)

                            if self.prefixEnabled and self.suffixEnabled:
                                prefix = self.prefix[self.workList[word_num]] + " "
                                suffix = " " + self.suffix[self.workList[word_num]] + " "
                            elif self.prefixEnabled:
                                prefix = self.prefix[self.workList[word_num]] + " "
                                suffix = ""
                            elif self.suffixEnabled:
                                prefix = ""
                                suffix = " " + self.suffix[self.workList[word_num]] + " "
                            else:
                                prefix = ""
                                suffix = ""

                            if self.curPos == word_num:
                                try:
                                    if not self.debug:
                                        if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                                            outputList.append(" " + word_num_str + " * " + prefix + EveconLib.Tools.getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                                        else:
                                            outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix)
                                    else:
                                        outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix + "2")
                                except IndexError:
                                    pass
                            else:
                                try:
                                    if not self.debug:
                                        if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                                            outputList.append(" " + word_num_str + "   " + prefix + EveconLib.Tools.getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                                        else:
                                            outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix)
                                    else:
                                        outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix + "3")
                                except IndexError:
                                    pass
                    else:
                        for word_num in range(0, 2 * self.expandRange + 1):  # + 1? # Anfang
                            if word_num + 1 < 10:
                                word_num_str = str(word_num + 1) + "  "
                            elif word_num + 1 < 100:
                                word_num_str = str(word_num + 1) + " "
                            else:
                                word_num_str = str(word_num + 1)

                            if self.prefixEnabled and self.suffixEnabled:
                                prefix = self.prefix[self.workList[word_num]] + " "
                                suffix = " " + self.suffix[self.workList[word_num]] + " "
                            elif self.prefixEnabled:
                                prefix = self.prefix[self.workList[word_num]] + " "
                                suffix = ""
                            elif self.suffixEnabled:
                                prefix = ""
                                suffix = " " + self.suffix[self.workList[word_num]] + " "
                            else:
                                prefix = ""
                                suffix = ""

                            if self.curPos == word_num:
                                if not self.debug:
                                    if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                                        outputList.append(" " + word_num_str + " * " + prefix + EveconLib.Tools.getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                                    else:
                                        outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix)
                                else:
                                    outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix + "4")
                            else:
                                if not self.debug:
                                    if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                                        outputList.append(" " + word_num_str + "   " + prefix + EveconLib.Tools.getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                                    else:
                                        outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix)
                                else:
                                    outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix + "5")
                    search_done = True
                    break

                elif self.curPos == len(self.workList) - now - 1 and self.curPos >= self.expandRange:  # Ende
                    for word_num in range(self.curPos - self.expandRange - 2 + now, self.curPos + 1 + now):
                        if word_num < 0:
                            continue
                        # print(word_num, self.curPos, now, self.expandRange)
                        if word_num + 1 < 10:
                            word_num_str = str(word_num + 1) + "  "
                        elif word_num + 1 < 100:
                            word_num_str = str(word_num + 1) + " "
                        else:
                            word_num_str = str(word_num + 1)

                        if self.prefixEnabled and self.suffixEnabled:
                            prefix = self.prefix[self.workList[word_num]] + " "
                            suffix = " " + self.suffix[self.workList[word_num]] + " "
                        elif self.prefixEnabled:
                            prefix = self.prefix[self.workList[word_num]] + " "
                            suffix = ""
                        elif self.suffixEnabled:
                            prefix = ""
                            suffix = " " + self.suffix[self.workList[word_num]] + " "
                        else:
                            prefix = ""
                            suffix = ""

                        if self.curPos == word_num:
                            if not self.debug:
                                if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                                    outputList.append(" " + word_num_str + " * " + prefix + EveconLib.Tools.getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                                else:
                                    outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix)
                            else:
                                outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix + "6")
                        else:
                            if not self.debug:
                                if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                                    outputList.append(" " + word_num_str + "   " + prefix + EveconLib.Tools.getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                                else:
                                    outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix)
                            else:
                                outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix + "7")
                    search_done = True
                    break

        if not search_done:  # Mitte
            for word_num in range(self.curPos - self.expandRange, self.curPos + self.expandRange + 1):
                if word_num + 1 < 10:
                    word_num_str = str(word_num + 1) + "  "
                elif word_num + 1 < 100:
                    word_num_str = str(word_num + 1) + " "
                else:
                    word_num_str = str(word_num + 1)

                if self.prefixEnabled and self.suffixEnabled:
                    prefix = self.prefix[self.workList[word_num]] + " "
                    suffix = " " + self.suffix[self.workList[word_num]] + " "
                elif self.prefixEnabled:
                    prefix = self.prefix[self.workList[word_num]] + " "
                    suffix = ""
                elif self.suffixEnabled:
                    prefix = ""
                    suffix = " " + self.suffix[self.workList[word_num]] + " "
                else:
                    prefix = ""
                    suffix = ""

                if self.curPos == word_num:
                    if not self.debug:
                        if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                            outputList.append(" " + word_num_str + " * " + prefix + EveconLib.Tools.getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                        else:
                            outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix)
                    else:
                        outputList.append(" " + word_num_str + " * " + prefix + self.workList[word_num] + suffix + "10")
                else:
                    if not self.debug:
                        if len(self.workList[word_num]) > 108 - len(prefix) - len(suffix):
                            outputList.append(" " + word_num_str + "   " + prefix + EveconLib.Tools.getPartStr(self.workList[word_num], 0, 108 - len(prefix) - len(suffix)) + "..." + suffix)
                        else:
                            outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix)
                    else:
                        outputList.append(" " + word_num_str + "   " + prefix + self.workList[word_num] + suffix + "11")

        return outputList

    def returnfoot(self):
        """
        :return: returns the programm foot output (list)
        """
        outputList = []
        if self.enableInput:
            outputList.append("\nInput: " + self.Input)
        return outputList
