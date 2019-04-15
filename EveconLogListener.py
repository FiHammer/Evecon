import simplecrypt
import socket
import datetime
import EveconExceptions
from EveconTools import *

class Client(threading.Thread):
    def __init__(self, ip: str, port: int, react, buffersize=1024, loginName=None, loginPW=None, Seculevel=0, showLog=False):
        """
        port
        the port where the server schould listen on

        reac
        the function with will be executed when the client sent data

        ip
        normaly the ip of your pc
        ip of your pc

        buffersize
        normaly 1024
        byte limit of your get data

        loginName
        if you want the client should login in the server you should define here the username

        loginPW
        if you want the client should login in the server you should define here the password

        Seculevel
        normaly 0 if both uses 0 no secu will be used
        -2: the encryption will be deactivated, but if the client has enabled Secu, the connection will be refuesd
        -1: the encryption will be deactivated
        0:  the client decide if the encryption is enabled
        1:  you force the client to generate a encryption code, but if the client has deactivated Secu, no Secu will be used
        2:  you force the client to generate a encryption code, but if the client has deactivated Secu, the connection will be refuesd

        BigServerBuffersize
        normaly 536870912 (maybe 512MB)
        if this Buffersize is less then the normal buffersize the BigServer will be deactivated
        you can set the Buffersize of the Bigserver

        BigServerPort
        set the Port of the BigServer if it is 0 the port is the normal port+1

        showLog
        show Log entries

        Keywords:
        #C! for a command
        #T! do not use, this will be used to talk to the client directly, like login in

        """
        super().__init__()


        self.port = port
        self.react = react
        self.ip = ip
        self.buffersize = buffersize
        self.showLog = showLog


        if loginName and loginPW:
            self.login = True
        else:
            self.login = False
        self.loginName = loginName
        self.loginPW = loginPW

        self.Seculevel = Seculevel

        self.tmp_longMSG_rec = False
        self.tmp_longMSGs_rec = []
        self.tmp_longMSG_sen = False
        self.tmp_longMSGs_sen = []

        self.Logsend = []
        self.Logsend_long = []
        self.Logrece = []
        self.Logrece_long = []

        self.s = socket.socket()

        self.Running = False # between start and end
        self.Connected = False # while connected

        self.conAddress = None
        self.conInfo = {}

        self.Info = {"login" : {"status" : self.login, "name" : self.loginName, "password" : self.loginPW},
                     "secu" : {"level" : self.Seculevel}}

        self.Log = []
        self.Status = "Starting"

    def run(self):
        self.Running = True

        self.Status = "Setup"
        self.writeLog("Status:")
        self.writeLog("Ip: " + str(self.ip))
        self.writeLog("Port: " + str(self.port))
        self.writeLog("Login: " + str(self.login))
        self.writeLog("LoginName: " + str(self.loginName))
        self.writeLog("LoginPW: " + str(self.loginPW))
        self.writeLog("Seculevel: " + str(self.Seculevel))

        self.Status = "Connecting"

        try:
            self.s.connect((self.ip, self.port))

        except TimeoutError:
            # wrong ip
            self.writeLog("Can not find IP, Timeout")
            raise EveconExceptions.ClientWrongPort

        except ConnectionRefusedError:
            # wrong port
            self.writeLog("Can not connect to port, ConnectionRefused")
            raise EveconExceptions.ClientWrongPort

        self.Connected = True
        self.Status = "Connected"
        self.writeLog("Connected with Server")

        try:
            InfoServer_raw = self.s.recv(1024)
        except ConnectionResetError:
            self.writeLog("Server disconnected without warning")
            raise EveconExceptions.ClientConnectionLost()

        InfoServer = InfoServer_raw.decode("UTF-8").split("!")
        if not InfoServer[0] == "#T":
            self.writeLog("Server send wrong Infoconnection")
            raise EveconExceptions.ClientWrongServer()

        elif InfoServer[0] == "#T" and InfoServer[1] == "Test":
            self.conInfo = {"secu": {"status": -1}, "key": "None"}
            self.writeLog("== uses the 'Test'-Version")

        else:
            if InfoServer[1] == "True":
                # noinspection PyTypeChecker
                InfoServer[1] = True
            else:
                # noinspection PyTypeChecker
                InfoServer[1] = False
            if InfoServer[2] == "True":
                # noinspection PyTypeChecker
                InfoServer[2] = True
            else:
                # noinspection PyTypeChecker
                InfoServer[2] = False
            self.conInfo = {"login": {"status" : InfoServer[1]},
                            "bigserver" : {"status" : InfoServer[2], "port" : int(InfoServer[3])},
                            "secu": {"level" : int(InfoServer[4])}}

        S = int(self.conInfo["secu"]["level"])
        C = int(self.Seculevel)

        if not -3 < S < 3:
            self.writeLog("Server send a wrong Seculevel")
            raise EveconExceptions.ClientWrongServer

        elif S == -2:
            if C == 2:
                self.Info["secu"]["status"] = 0
            else:
                self.Info["secu"]["status"] = -1
        elif S == -1:
            if C == 2:
                self.Info["secu"]["status"] = 1
            else:
                self.Info["secu"]["status"] = -1
        elif S == 0:
            if C < 1:
                self.Info["secu"]["status"] = -1
            else:
                self.Info["secu"]["status"] = 1
        elif S == 1:
            if C == -2:
                self.Info["secu"]["status"] = -1
            else:
                self.Info["secu"]["status"] = 1
        elif S == 2:
            if C == -2:
                self.Info["secu"]["status"] = 0
            else:
                self.Info["secu"]["status"] = 1

        if self.Info["secu"]["status"] == 1:
            self.Info["secu"]["key"] = randompw(returnpw=True, printpw=False, exclude=["#", "!"])
        else:
            self.Info["secu"]["key"] = None

        InfoSend = b'#T!' + str(self.Info["login"]["status"]).encode() + b'!' + \
                   str(self.Info["login"]["name"]).encode() + b'!' + \
                   str(self.Info["login"]["password"]).encode() + b'!' + \
                   str(self.Info["secu"]["status"]).encode() + b'!' + \
                   str(self.Info["secu"]["level"]).encode() + b'!' + \
                   str(self.Info["secu"]["key"]).encode()

        self.send(InfoSend, encrypt=False, direct=True)

        try:
            conAccept = self.s.recv(self.buffersize).decode("UTF-8")
        except ConnectionResetError:
            self.writeLog("Server disconnected without warning")
            raise EveconExceptions.ClientConnectionLost()
        #print(conAccept, InfoSend)

        if conAccept:

            if self.Info["secu"]["status"] == 1:
                self.writeLog("Started Connection with Server. Decryption Key: " + self.Info["secu"]["key"])

                while self.Running and self.Connected and self.Status != "Ended" and self.Status == "Connected":
                    try:
                        data_en = self.s.recv(self.buffersize)
                    except ConnectionResetError:
                        self.writeLog("Server disconnected without warning")
                        break
                    except ConnectionAbortedError:
                        self.writeLog("Connection aborted")
                        break
                    #print(data_en)
                    data = simplecrypt.decrypt(self.Info["secu"]["key"], data_en)

                    self.receive(data)

            elif self.Info["secu"]["status"] == -1:
                self.writeLog("Started Connection with Server. No Decryption")

                while self.Running and self.Connected and self.Status != "Ended" and self.Status == "Connected":
                    try:
                        data = self.s.recv(self.buffersize)
                    except ConnectionResetError:
                        self.writeLog("Server disconnected without warning")
                        break
                    except ConnectionAbortedError:
                        self.writeLog("Connection aborted")
                        break

                    self.receive(data)
            else:
                self.writeLog("Wrong status")
        else:
            self.writeLog("Wrong Password")

        self.s.close()
        self.Running = False
        self.Connected = False
        self.Status = "Ended"


    def send(self, data, encrypt=None, direct=False):
        if self.Running and self.Connected and self.Status != "Ended" and self.Status == "Connected" or direct:
            if type(data) == str:
                data_send = data.encode()
            elif type(data) == int:
                data_send = str(data).encode()
            elif type(data) == bool:
                data_send = str(data).encode()
            else:
                data_send = data

            if len(data_send) > 1000:  # LONG MSG!!!
                self.send("#T!longMSGinc")

                self.tmp_longMSG_sen = True
                self.tmp_longMSGs_sen = []
                for i in range(0, len(data) - 1, 1000):
                    self.tmp_longMSGs_sen.append(data_send[i:i + 1000])
                    self.Logsend_long.append(data_send[i:i + 1000])

                for partData in self.tmp_longMSGs_sen:
                    self.send(partData)

                self.tmp_longMSG_sen = False
                self.tmp_longMSGs_sen = []
                self.send("#T!longMSGend")

            else:
                if encrypt is None:
                    if self.Info["secu"]["status"] == 1:
                        data_send_de = simplecrypt.encrypt(self.Info["secu"]["key"], data_send)
                    else:
                        data_send_de = data_send
                elif encrypt:
                    data_send_de = simplecrypt.encrypt(self.Info["secu"]["key"], data_send)
                else:
                    data_send_de = data_send

                if type(data) == str:
                    data_str = data
                elif type(data) == bytes:
                    try:
                        data_str = data.decode("UTF-8")
                    except UnicodeDecodeError:
                        data_str = str(data)
                else:
                    data_str = str(data)
                if not self.tmp_longMSG_sen:
                    self.Logsend.append(data_str)

                    try:
                        self.writeLog("Sent: " + data_send.decode("UTF-8"))
                    except UnicodeDecodeError:
                        self.writeLog("Sent something uncodeable!: " + str(data_send))
                else:
                    try:
                        self.writeLog("Long Message: " + data_send.decode("UTF-8"))
                    except UnicodeDecodeError:
                        self.writeLog("Long Message (uncodeable): " + str(data_send))

                self.s.send(data_send_de)

        else:
            return False

    def receive(self, data):
        if self.Running and self.Connected and self.Status != "Ended" and self.Status == "Connected":
            noByte = True
            try:
                data_form = data.decode("UTF-8")
            except UnicodeDecodeError:
                noByte = False
                data_form = str(data)
            data_form_split = data_form.split("!")
            self.writeLog("Receive: " + data_form)

            if not self.tmp_longMSG_rec:
                self.Logrece.append(data)

                if data_form_split[0] == "#C" and len(data_form_split) > 1:
                    if data_form_split[1] == "exit":
                        self.exit()
                elif data_form_split[0] == "#T" and len(data_form_split) > 1:
                    if data_form_split[1] == "exit":
                        self.exit(sendM=False)
                        self.writeLog("Server disconnected")

                    elif data_form_split[1] == "longMSGinc":
                        self.writeLog("Long Message incoming!")
                        self.tmp_longMSG_rec = True
                        self.tmp_longMSGs_rec = []
                else:
                    if noByte:
                        self.react(data_form)
                    else:
                        self.react(data)
            else:  # LONG MESSAGE
                if data_form_split[0] == "#T" and len(data_form_split) > 1:
                    if data_form_split[1] == "longMSGend":
                        self.writeLog("Long Message finished!")
                        # LONG MSG WIRD AUS GEWERTET
                        self.tmp_longMSG_rec = False

                        if type(self.tmp_longMSGs_rec[0]) == str:
                            msg = ""
                        else:
                            msg = b""

                        for partOfMsg in self.Logrece_long:
                            msg += partOfMsg
                        if type(self.tmp_longMSGs_rec[0]) == str:
                            self.writeLog("Long Message: " + msg)
                        else:
                            self.writeLog("Long (Byte) Message: " + str(msg))

                        self.Logrece.append(msg)
                        #self.tmp_longMSGs_rec = []
                        self.react(msg)

                else:
                    if noByte:
                        self.tmp_longMSGs_rec.append(data_form)
                        self.Logrece_long.append(data_form)
                        self.writeLog("Long Message Part " + str(len(self.tmp_longMSGs_rec)) + ": " + data_form)
                    else:
                        self.tmp_longMSGs_rec.append(data)
                        self.Logrece_long.append(data)
                        self.writeLog("Long Message (Byte) Part " + str(len(self.tmp_longMSGs_rec)) + ": " + data_form)


    def save(self, directory:str):
        file_log_raw = open("Log.txt", "w")
        for x in self.Log:
            file_log_raw.write(x)
        file_log_raw.close()

        file_logsend_raw = open("LogSend.txt", "w")
        for x in self.Logsend:
            if type(x) == str:
                file_logsend_raw.write(x)
            elif type(x) == bytes:
                file_logsend_raw.write(x.decode("UTF-8"))
            elif type(x) == bool:
                file_logsend_raw.write(str(x))
        file_logsend_raw.close()

        file_logrece_raw = open("LogReceive.txt", "w")
        for x in self.Logrece:
            if type(x) == str:
                file_logrece_raw.write(x)
            elif type(x) == bytes:
                file_logrece_raw.write(x.decode("UTF-8"))
            elif type(x) == bool:
                file_logrece_raw.write(str(x))
        file_logrece_raw.close()

    def writeLog(self, data):
        write = "(" + datetime.datetime.now().strftime("%H:%M:%S:%f") + ") " + "(" + self.Status + ") " + data
        self.Log.append(write)
        if self.showLog:
            print("[Log] " + write)

    def exit(self, sendM=True):
        if sendM:
            self.send("#T!exit")
        self.s.close()
        self.Connected = False
        self.Status = "Lost Connection"

    def getStatus(self):
        curStatus = {"status" : {"status" : self.Status, "running" : self.Running, "connected" : self.Connected},
                     "log": self.Log, "info" : self.Info}
        return curStatus

def printer(prit):
    print(prit)

if __name__ == "__main__":
    port = int(input("Port: "))
    #port = int(sys.argv[1])

    cl = Client(ip="192.168.2.102", port=port, react=printer)
    cl.start()
    cl.join()