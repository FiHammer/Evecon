import simplecrypt
import socket
import datetime
import time
import random
import threading
import EveconLib.EveconExceptions as EveconExceptions

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
class Timer:
    def __init__(self):
        self.starttime = 0
        self.stoptime = 0
        self.startpausetime = 0
        self.stoppausetime = 0
        self._time = 0
        self.Pause = 0
        self.curPause = 0
        self.startcurPause = 0
        self.startpausetimetmp = 0

        self.Running = False
        self.Paused = False
        self.End = False

    def start(self):
        self.reset()
        self.Running = True
        self.starttime = time.time()

    def stop(self):
        if self.Running:
            if self.Paused:
                self.unpause()
            self.stoptime = time.time()
            self.reload()
            self.End = True

    def pause(self):
        if not self.End:
            if not self.Paused:
                self.Paused = True
                self.startcurPause = time.time()
                self.startpausetimetmp = time.time()

    def unpause(self):
        if not self.End:
            if self.Paused:
                self.Paused = False
                self.startpausetime += self.startpausetimetmp
                self.stoppausetime += time.time()
                self.reload()
                self.curPause = 0
                self.startcurPause = 0

    def reset(self):
        self.starttime = 0
        self.stoptime = 0
        self.startpausetime = 0
        self.stoppausetime = 0
        self._time = 0
        self.Pause = 0
        self.curPause = 0
        self.startcurPause = 0
        self.startpausetimetmp = 0

        self.Running = False
        self.Paused = False
        self.End = False

    def switch(self):
        if not self.Paused:
            self.pause()
        else:
            self.unpause()

    def reload(self):
        if self.Running:
            if self.Paused:
                self.curPause = time.time() - self.startcurPause
            else:
                self.curPause = 0
                self.startcurPause = 0

            self.Pause = self.stoppausetime - self.startpausetime

            if self.End:
                self._time = self.stoptime - self.starttime - self.Pause
            else:
                self._time = time.time() - self.starttime - self.Pause - self.curPause
        else:
            self._time = 0

    def getTime(self):
        self.reload()

        return self._time

    time = property(getTime)

    def getTimeFor(self):
        return TimeFor(self.time)

def LogServerless(functioni, info, typei = "Normal", printIt=False):
    part_time = "[" + datetime.datetime.now().strftime("%H:%M:%S:%f") + "]"
    if typei == "Debug" or typei == -1:
        part_type = "[Debug]"
    elif typei == "Normal" or typei == 0:
        part_type = "[Info]"
    elif typei == "Warning" or typei == 1:
        part_type = "[Warning]"
    elif typei == "Error" or typei == 2:
        part_type = "[Error]"
    else:
        part_type = ""
    part_func = "[" + functioni + "]"

    log_write = part_time + " " + part_type + " " + part_func + ": " + str(info) + "\n"

    if printIt:
        print(log_write.rstrip())


    return log_write
def TimeFor(Time):
    if (round(Time) % 60) == 0:
        TimeFor = "%s:%s%s" % (round(Time) // 60, 0, 0)
    elif (round(Time) % 60) < 10:
        TimeFor = "%s:%s%s" % (round(Time) // 60, 0, round(Time) % 60)
    else:
        TimeFor = "%s:%s" % (round(Time) // 60, round(Time) % 60)
    return TimeFor

class Client(threading.Thread):
    def __init__(self, ip: str, port: int, react, buffersize=1024, accountName="", accountPW="", accountKey="",
                 secuLevel=0, printLog=False, java=False, forcePort=False):
        """
        a fantastic client

        :param ip: ip of the server
        :param port: port of the server
        :param react: function with the recieved data
        :param buffersize: buffersize of the connection
        :param accountName: login name
        :param accountPW: login pw
        :param accountKey: login encryption key
        :param secuLevel: seculevel
        :param printLog: prints the log in the console
        :param forcePort: forces the use of the port (no usedPorts)
        """
        super().__init__()

        self.port = port
        self.react = react
        self.ip = ip
        self.buffersize = buffersize
        self.printLog = printLog

        self.java = java

        self.accountName = accountName
        self.accountPW = accountPW
        self.accountKey = accountKey

        if accountName or accountPW or accountKey:
            self.useAccount = True
        else:
            self.useAccount = False

        self.secu = {"status": 0, "level": secuLevel, "key": ""}

        self.dataRec = []
        self.dataSend = []

        self.timer = Timer()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.running = False
        self.status = 0

        self.tmp_longMsg_rec = []
        """
        status
        0:  not running
        1:  setup
        2:  recieving
        3:  sending
        4:  end

        """

        self.conAddress = None

    def run(self):
        self.status = 1

        try:
            self.socket.connect((self.ip, self.port))

        except TimeoutError:
            # wrong ip
            self.writeLog("Can not find IP, Timeout")
            raise EveconExceptions.ClientWrongPort

        except ConnectionRefusedError:
            # wrong port
            self.writeLog("Can not connect to port, ConnectionRefused")
            raise EveconExceptions.ClientWrongPort

        self.writeLog("Connected with Server")

        self.secu["key"] = randompw(returnpw=True, printpw=False, exclude=["#", "!"])

        infoSend = str(self.useAccount).encode() + b"!" + \
                   self.secu["key"].encode() + b"!" + \
                   str(self.secu["level"]).encode()

        self.send(infoSend, encrypt=False, direct=True, special=0)

        self.send(self.accountName, encrypt=True, direct=True, special=0)
        self.send(self.accountPW, encrypt=True, direct=True, special=0)

        if self.useAccount:
            self.secu["key"] += self.accountKey


        infoServer = self.recieve(0, direct=True).decode("UTF-8").split("!")

        if not infoServer[0] == "#T":
            self.writeLog("Server send wrong Infoconnection")
            raise EveconExceptions.ClientWrongServer()
        else:
            if infoServer[1] == "exit":
                self.writeLog("Server had an error! Code: " + str(infoServer[2]))
                return False
            elif infoServer[1] == "0":
                self.writeLog("Cannot connect to server!")
                return False
            elif infoServer[1] == "1" or infoServer[1] == "-1":
                self.secu["status"] = int(infoServer[1])
            else:
                self.writeLog("Server send wrong Infoconnection")
                raise EveconExceptions.ClientWrongServer()

        self.status = 2
        self.running = True
        self.logStatus()
        self.writeLog("Started Connection with Server")
        self.onStart()

        while self.running:  # MAIN RECIEVING LOOP
            if not self.recieveWorker(self.recieve()):
                self.running = False

        self.exit(sendM=False)

    def send(self, data, special=-1, encrypt=None, direct=False, thisLongMsg=False):
        """
        sends data

        :param data: data
        :param special: special send
        -1: nothing
        0:  special transfer
        1:  special command
        2:  special recieve for the client
        3:  special ?

        :param encrypt: encryption
        :param direct: directly send the msg
        :param thisLongMsg: is the msg a long msg

        :return: success
        """
        if self.running and self.status == 2 or direct:
            # self.status = 3

            if type(data) == str:
                data_send = data.encode()
            elif type(data) == int:
                data_send = str(data).encode()
            elif type(data) == bool:
                data_send = str(data).encode()
            else:
                data_send = data
            longMsg = False
            if special == 0:
                data_send = b"#T!" + data_send
            elif special == 1:
                data_send = b"#C!" + data_send
            elif special == 2:
                data_send = b"#R!" + data_send
            elif special == 3:
                data_send = b"#B!" + data_send
            elif len(data_send) > 1000:  # LONG MSG!!!
                longMsg = True
            else:
                pass
                # data_send = b"startMSG!" + data_send + b"!endMSG"

            if longMsg:
                self.send("longMSGinc", special=0)

                longMsgParts = []
                for i in range(0, len(data) - 1, 1000):
                    longMsgParts.append(data_send[i:i + 1000])

                for partData in longMsgParts:
                    self.send(partData, thisLongMsg=True)

                time.sleep(1)
                self.send("longMSGend", special=0)
            else:
                if encrypt is None:
                    if self.secu["status"] == 1:
                        data_send_de = simplecrypt.encrypt(self.secu["key"], data_send)
                    else:
                        data_send_de = data_send
                elif encrypt:
                    data_send_de = simplecrypt.encrypt(self.secu["key"], data_send)
                else:
                    data_send_de = data_send

                if not thisLongMsg:
                    self.dataSend.append(data)
                    try:
                        self.writeLog(data_send.decode("UTF-8"), dataType=1)
                    except UnicodeDecodeError:
                        self.writeLog(str(data_send), dataType=2)
                else:
                    try:
                        self.writeLog(data_send.decode("UTF-8"), dataType=3)
                    except UnicodeDecodeError:
                        self.writeLog(str(data_send), dataType=4)

                if self.java:
                    data_send_de += b'\r\n'

                self.socket.send(data_send_de)

    def recieve(self, encrypt=999, direct=False):
        if not self.running:
            if not direct:
                return False
        if encrypt == 999:
            encrypt = self.secu["status"]

        try:
            data = self.socket.recv(self.buffersize)
        except ConnectionResetError:
            self.writeLog("Server disconnected without warning")
            return False
        except ConnectionAbortedError:
            self.writeLog("Connection aborted")
            return False
        except OSError:
            return False

        if self.java:
            data = data.rstrip()

        if encrypt == 1:  # yes
            try:
                data = simplecrypt.decrypt(self.secu["key"], data)
            except simplecrypt.DecryptionException:
                return False

        if not data:
            self.writeLog("Server disconnected. If this happens the Server send something courious")
            return False

        return data

    def recieveWorker(self, data):
        if not self.running:
            return False
        if data is False:
            return False

        noByte = True
        try:
            data_form = data.decode("UTF-8")
        except UnicodeDecodeError:
            data_form = str(data)
            noByte = False
        data_form_split = data_form.split("!")
        self.writeLog(data_form, dataType=-1)

        self.dataRec.append(data)
        self.onRecieve(data)

        if self.tmp_longMsg_rec:  # long MSg
            if self.tmp_longMsg_rec[0] is None:
                self.tmp_longMsg_rec = []
            if data_form_split[0] == "#T" and len(data_form_split) == 2:
                if data_form_split[1] == "longMSGend":
                    self.writeLog("Long Message finished!")
                    # LONG MSG WIRD AUS GEWERTET

                    if type(self.tmp_longMsg_rec[0]) == str:
                        msg = ""
                    else:
                        msg = b""

                    for partOfMsg in self.tmp_longMsg_rec:
                        msg += partOfMsg
                    self.writeLog("Long Message: " + msg)
                    self.dataRec.append(msg)
                    # self.tmp_longMSGs_rec = []
                    self.react(msg)

                    self.tmp_longMsg_rec = []
                    return True

            else:
                if noByte:
                    self.tmp_longMsg_rec.append(data_form)
                    self.writeLog("Long Message Part " + str(len(self.tmp_longMsg_rec)) + ": " + data_form)
                else:
                    self.tmp_longMsg_rec.append(data)
                    self.writeLog("Long Message (Byte) Part " + str(len(self.tmp_longMsg_rec)) + ": " + data_form)


        else:
            if data_form_split[0] == "#C" and len(data_form_split) > 1:
                if data_form_split[1] == "getTimeRaw":
                    self.send(str(self.getRunTime()), special=2)
                elif data_form_split[1] == "getTime":
                    self.send(str(self.getRunTime(False)), special=2)
                elif data_form_split[1] == "exit":
                    self.exit()

            elif data_form_split[0] == "#T" and len(data_form_split) > 1:
                if data_form_split[1] == "exit":
                    self.exit(sendM=False)
                    self.writeLog("Server disconnected")

                elif data_form_split[1] == "longMSGinc":
                    self.writeLog("Long Message incoming!")
                    self.tmp_longMsg_rec = [None]

            elif data_form_split[0] == "#B" and len(data_form_split) > 1:
                pass

            else:
                if noByte:
                    self.react(data_form)
                else:
                    self.react(data)
                return True

    def writeLog(self, data, prio=0, dataType=0):
        if dataType == -1:
            prefixx = "Recieved: "
        elif dataType == 1:
            prefixx = "Sent: "
        elif dataType == 2:
            prefixx = "Sent (unencodable): "
        elif dataType == 3:
            prefixx = "Sent (long): "
        elif dataType == 5:
            prefixx = "Sent (long, unencodable): "
        else:
            prefixx = ""

        # noinspection PyTypeChecker
        LogServerless("Client", prefixx + data, prio, self.printLog)

    def exit(self, sendM=True, sendErr=0):
        if sendM:
            self.send("#T!exit")
        elif sendErr:
            self.send("exit!error!" + str(sendErr), special=0)
        self.onExit()

        self.status = 4
        self.running = False
        self.socket.close()

    def logStatus(self):
        self.writeLog("Status:")
        self.writeLog("StatusID: " + str(self.status))
        self.writeLog("running: " + str(self.running))
        self.writeLog("Connected with:")
        self.writeLog("IP: " + str(self.ip))
        self.writeLog("Port: " + str(self.port))
        if not self.useAccount:
            self.writeLog("Account: None")
        else:
            self.writeLog("Account Name: " + self.accountName)
            self.writeLog("Account Password: " + self.accountPW)

        self.writeLog("Secustatus: " + str(self.secu["status"]))
        if self.secu["status"] == 1:
            self.writeLog("Secukey: " + self.secu["key"])

    def getRunTime(self, raw=True):
        if raw:
            return self.timer.getTime()
        else:
            return self.timer.getTimeFor()

    # SCRIPTS

    def onStart(self):
        pass

    def onExit(self):  # begin of exit
        pass

    def onSend(self, data):  # MISS
        pass

    def onRecieve(self, data):  # MISS
        pass

def printer(prit):
    print(prit)

if __name__ == "__main__":
    port = int(input("Port: "))
    #port = int(sys.argv[1])

    cl = Client(ip="192.168.2.102", port=port, react=printer)
    cl.start()
    cl.join()