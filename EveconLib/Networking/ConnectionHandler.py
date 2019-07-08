import threading
import time
import simplecrypt

import EveconLib.Tools


class ConnectionHandler(threading.Thread):
    def __init__(self, conData, server):
        """
        handles the connection

        :param conData: connection Data
        :type conData: dict
        :param server: the main server
        :type server: Server
        """
        super().__init__()

        self.conData = conData
        self.server = server
        self.react = None

        self.java = server.java
        self.accounts = server.accounts
        self.buffersize = server.buffersize
        self.useAccount = False
        self.accountName = ""
        self.accountPW = ""
        self.accountKey = ""

        self.secu = {"status": 0, "level": self.server.secuLevel, "key": ""}
        self.secuClient = {"status": 0, "level": 0}

        self.id = conData["id"]
        self.con = conData["con"]

        self.dataRec = []
        self.dataSend = []
        self.timer = EveconLib.Tools.Timer()

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

    def run(self):
        self.status = 1

        infoClient_raw = self.recieve(0, direct=True)
        if infoClient_raw is None:
            return

        # noinspection PyUnresolvedReferences
        infoClient = infoClient_raw.decode("UTF-8").split("!")

        if not infoClient[0] == "#T":
            self.writeLog("Client send wrong Infoconnection")
            self.exit(sendErr=2)
            return

        elif infoClient[0] == "#T" and infoClient[1] == "Test":
            self.secu["status"] = -1
            self.writeLog("Client uses the 'Test'-Version")

        else:
            if infoClient[1] == "True":
                infoClient[1] = True
            else:
                infoClient[1] = False

            self.useAccount = infoClient[1]
            self.secu["key"] = infoClient[2] # auf zwei liegt jetz der encryption key
            self.secuClient = {"level": int(infoClient[3])}

            self.accountName = self.recieve(1, direct=True).decode("UTF-8").lstrip('#T!')
            self.accountPW = self.recieve(1, direct=True).decode("UTF-8").lstrip('#T!')


            # compute the secu level
            cl = self.secuClient["level"]
            se = self.secu["level"]

            noEncryption = -1
            yesEncryption = 1
            errorEnryption = 0

            sumSecu = cl + se

            if cl == 0 and se == 0:
                secuStatus = noEncryption
            elif sumSecu < 0:
                secuStatus = noEncryption
            elif sumSecu == 0:
                if (cl == 2 and se == 2) or (cl == -2 and se == -2):
                    secuStatus = errorEnryption
                elif se <= 0:
                    secuStatus = noEncryption
                else:
                    secuStatus = yesEncryption
            elif sumSecu > 0:
                secuStatus = yesEncryption
            else:
                self.writeLog("Error computing secu level (Cl: %s, Se: %s, Sum: %s)" % (cl, se, sumSecu))
                self.exit(sendErr=3)
                return False

            self.secu["status"] = secuStatus
            #if secuStatus == 1:
            #    self.secu["key"] = randompw(returnpw=True, printpw=False, exclude=["#", "!"])

        if self.useAccount:
            self.useAccount = False
            for aAccount in self.accounts:
                if aAccount[0] == self.accountName and aAccount[1] == self.accountPW:
                    self.useAccount = True
                    if aAccount[2]:
                        self.react = aAccount[2]
                    else:
                        self.react = self.server.stdReact
                    if aAccount[3]:
                        self.secu["status"] = 1
                        self.secu["key"] += aAccount[3] # PLUS
                        self.accountKey = aAccount[3]
                        if self.secuClient["level"] == -2:  # if client says no, he will disconnect
                            self.secu["status"] = 0
            if not self.useAccount:
                if self.server.stdReact:
                    self.react = self.server.stdReact
                else:
                    self.writeLog("Wrong Username or Password")
                    self.exit(sendErr=5)
                    return False

        elif not self.server.stdReact:
            self.writeLog("Client did not login")
            self.exit(sendErr=4)
            return False
        else:
            self.react = self.server.stdReact

        infoSend = str(self.secu["status"]).encode()
        #if not self.accountKey:
        #    infoClient += b"!" + str(self.secu["key"]).encode()

        self.send(infoSend, encrypt=False, direct=True, special=0)

        if self.secu["status"] == 0:
            self.writeLog("Could not match secu levels")
            self.exit(sendM=False)
            return False

        self.server.connections[self.id]["running"] = True
        self.status = 2
        self.running = True
        self.logStatus()
        self.writeLog("Started Connection with Client")

        self.server.onConnect(self.id)
        while self.running:  # MAIN RECIEVING LOOP
            if not self.recieveWorker(self.recieve()):
                self.running = False

        self.exit(sendM=False)

    def recieve(self, encrypt=999, direct=False):
        if not self.running:
            if not direct:
                return False
        if encrypt == 999:
            encrypt = self.secu["status"]

        try:
            data = self.con.recv(self.buffersize)
        except ConnectionResetError:
            self.writeLog("Client disconnected without warning")
            return False
        except ConnectionAbortedError:
            self.writeLog("Connection aborted")
            return False
        except OSError:
            return False

        if self.java:
            data = data.rstrip()

        if encrypt == 1:  # yes
            data = simplecrypt.decrypt(self.secu["key"], data)

        if not data:
            self.writeLog("Client disconnected. If this happens the Client send something courious")
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
        self.server.onRecieve(data, self.id)

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
                    self.send(str(self.server.getRunTime()), special=2)
                elif data_form_split[1] == "getTime":
                    self.send(str(self.server.getRunTime(False)), special=2)
                elif data_form_split[1] == "exit":
                    self.exit()

            elif data_form_split[0] == "#T" and len(data_form_split) > 1:
                if data_form_split[1] == "exit":
                    self.exit(sendM=False)
                    self.writeLog("Client disconnected")

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
            self.server.onSend(data, self.id)

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

                self.con.send(data_send_de)

    def exit(self, sendM=True, sendErr=0):
        if sendM and not sendErr:
            self.send("exit", special=0)
        elif sendErr:
            self.send("exit!error!" + str(sendErr), special=0)
        self.server.onDisconnect(self.id)
        self.con.close()
        self.running = False
        self.server.connections[self.id]["running"] = False
        self.status = 4

    def writeLog(self, data, prio=0, dataType=0):
        self.server.writeLog(data=data, connectionID=self.id, prio=prio, dataType=dataType)

    def logStatus(self):
        self.writeLog("Status:")
        self.writeLog("StatusID: " + str(self.status))
        self.writeLog("Running: " + str(self.running))
        self.writeLog("Connected with:")
        self.writeLog("IP: " + str(self.conData["ip"]))
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
