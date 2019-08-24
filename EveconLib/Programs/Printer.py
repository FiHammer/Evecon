import threading
import EveconLib.Tools.Tools

class Printer(threading.Thread):
    def __init__(self, printit, waitTime=1.5, refreshTime=1, waitUntil=0):
        """
        An easy printer, which will print every some secons the function(s)

        :param printit: the function(s) to print
        :type printit: list
        :type printit: function

        :param waitTime: time between every print
        :type waitTime: float
        :type printit: double

        :param refreshTime: time between pause
        :type refreshTime: int
        :type refreshTime: float
        :type refreshTime: double

        :param waitUntil: this should be a time from time.time(); the printer will wait until the time is over
        :type waitUntil: int
        :type waitUntil: float
        :type waitUntil: double

        running: started/stopped
        printing: printing loop
        waiting: waiting loop
        """
        super().__init__()

        if isinstance(printit, list):
            self.printitS = printit
        else:
            self.printitS = [printit]

        self.waitTime = waitTime
        self.refreshTime = refreshTime

        self.running = False
        self.printing = False
        self.waiting = False
        self.waitUntil = waitUntil


    def run(self):
        """
        script
        """
        self.running = True
        self.printing = True
        self.waiting = True

        while self.running:
            while self.printing and self.waitUntil < time.time():
                EveconLib.Tools.cls()
                for printFunc in self.printitS:
                    printFunc()
                time.sleep(self.waitTime)
            while self.waiting:
                time.sleep(self.refreshTime)
            time.sleep(0.1)

    def pause(self):
        """
        pause the printer

        :return: True if success
        """

        if self.printing:
            self.printing = False
            self.waiting = True

            return True
        else:
            return False

    def unpause(self):
        """
        unpause the printer

        :return: True if success
        """

        if self.waiting:
            self.printing = True
            self.waiting = False

            return True
        else:
            return False

    def switch(self):
        """
        switch between pause

        :return: if True pause, False unpause
        """

        if self.printing:
            self.pause()
            return True
        else:
            self.unpause()
            return False


