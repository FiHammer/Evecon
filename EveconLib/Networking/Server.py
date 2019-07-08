import threading
import socket

import EveconLib.EveconExceptions as EveconExceptions
from EveconLib.Networking.ConnectionHandler import ConnectionHandler
import EveconLib.Tools

class Server(threading.Thread):
    def __init__(self, port: int, stdReact=None, ip=socket.gethostbyname(socket.gethostname()), buffersize=1024,
                 maxConnections=10, accounts=None, forcePort=False, printLog=True, secuLevel=0, java=False):
        """
        Init the Variables

        :param port: the port which the server listens (do not use usedPorts, only if forcePort)
        :type port: int

        :param forcePort: forces the use of the port (no usedPorts)
        :type forcePort: bool

        :param stdReact: the standard react funktion, use THIS param or use the accounts if they connect with an account
        :type stdReact: function

        :param ip: the ip of the server
        :type ip: str

        :param buffersize: buffersize of the connection
        :type buffersize: int

        :param maxConnections: max similar connections
        :type maxConnections: int

        :param accounts: all accounts, in the list is a tuple with the (0) name and (1) password, optional the (2) encryption key (empty string for none) and (3) special react
        :type accounts: list

        :param printLog: prints the log
        :type printLog: bool

        """
        super().__init__()

        if forcePort:
            self.port = port
        else:
            self.port = EveconLib.Tools.UsedPorts.givePort(port)
        self.stdReact = stdReact
        self.ip = ip
        self.buffersize = buffersize
        self.maxConnections = maxConnections
        self.printLog = printLog
        self.secuLevel = secuLevel
        self.java = java

        okAccs = []
        if accounts:  # validating
            for acc in accounts:
                if len(acc) == 4:
                    okAccs.append(acc)

        self.accounts = okAccs
        self.timer = EveconLib.Tools.Timer()  # server timer

        self.connections = {}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.bind((self.ip, self.port))
        except OSError:
            raise EveconExceptions.ServerPortUsed(self.port)

        self.running = False
        self.status = 0
        """
        status definition

        0   not running
        1   setup
        2   listen for client
        3   starting connection handler
        """

    def __del__(self):
        self.exit()
        EveconLib.Tools.UsedPorts.remPort(self.port)

    def writeLog(self, data, connectionID=-1, prio=0, dataType=0):
        if connectionID == -1:
            prefix = "Server"
        else:
            prefix = "ConnectionHandler (%s)" % connectionID
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

        try:
            # noinspection PyTypeChecker
            EveconLib.Tools.Log(prefix, prefixx + data, prio, self.printLog)
        except NameError:
            # noinspection PyTypeChecker
            EveconLib.Tools.LogServerless(prefix, prefixx + data, prio, self.printLog)

    def logStatus(self, full=False):
        self.writeLog("Status:")
        if full:
            self.writeLog("Ip: " + str(self.ip))
            self.writeLog("Port: " + str(self.port))
            self.writeLog("MaxConnections: " + str(self.maxConnections))
            self.writeLog("Accounts: " + str(len(self.accounts)))

        self.writeLog("Current connections: " + str(len(self.connections)))

    def run(self):
        self.running = True
        self.status = 1

        self.logStatus(full=True)
        self.onStart()
        while self.running:  # MAIN LOOP
            self.listenForClient()

    def listenForClient(self):
        self.status = 2

        self.onStartListen()

        self.socket.listen(self.maxConnections)
        try:
            con, conAddress = self.socket.accept()
        except OSError:
            self.running = False
            return

        self.writeLog("Found Client with IP: %s, Port: %s" % (conAddress[0], conAddress[1]))
        self.startConnectionHandler(con, conAddress)

    def startConnectionHandler(self, con, conAddress):
        self.status = 3

        newID = len(self.connections)
        conData = {"id": newID, "ip": conAddress[0], "port": conAddress[1], "conAddress": conAddress, "con": con,
                   "running": False}

        conHandler = ConnectionHandler(conData=conData, server=self)

        conData["conHandler"] = conHandler
        self.connections[newID] = conData

        conHandler.start()

    def sendToID(self, data, conID):
        if conID in self.connections.keys():
            if self.connections[conID]["running"]:
                return self.connections[conID]["conHandler"].send(data)
            else:
                return False  # connection not running
        else:
            return False  # wrong ID

    def sendToIDs(self, data, conIDs):
        for conID in conIDs:
            if self.connections[conID]["running"]:
                self.sendToID(data, conID)

    def sendToIP(self, data, conIP):
        theIPs = []
        theIP_ID = {}
        for conID in self.connections:
            if self.connections[conID]["running"]:
                theIP_ID[self.connections[conID]["ip"]] = []
        for conID in self.connections:
            if self.connections[conID]["running"]:
                theIPs.append(self.connections[conID]["ip"])
                theIP_ID[self.connections[conID]["ip"]].append(self.connections[conID]["id"])

        if not conIP in theIPs:
            return False

        self.sendToIDs(data, theIP_ID[conIP])

    def sendToAll(self, data):
        for conID in self.connections:
            self.sendToID(data, conID)

    def exit(self, sendM=True):
        if self.status != 0:
            self.onExit()
            self.closeConnectionAll()
            self.socket.close()
            EveconLib.Tools.UsedPorts.remPort(self.port)

    def closeConnectionAll(self):
        for conID in self.connections:
            self.closeConnectionByID(conID)

    def closeConnectionByID(self, conID):
        if conID in self.connections.keys():
            if self.connections[conID]["running"]:
                return self.connections[conID]["conHandler"].exit()
            else:
                return False  # connection not running
        else:
            return False  # wrong ID

    def getRunTime(self, raw=True):
        if raw:
            return self.timer.getTime()
        else:
            return self.timer.getTimeFor()

    # SCRIPTS

    def onStart(self):
        pass

    def onStartListen(self):
        pass

    def onConnect(self, conID):
        pass

    def onDisconnect(self, conID):
        pass

    def onExit(self):  # begin of exit
        pass

    def onSend(self, data, conID):
        pass

    def onRecieve(self, data, conID):
        pass


class ServerJava(threading.Thread):
    def __init__(self, ip, port, react, allowPrint=False, giveJava=True, sendIP=True):
        super().__init__()
        self.host = ip
        self.allowPrint = allowPrint
        self.port = EveconLib.Tools.UsedPorts.givePort(port)
        self.giveJava = giveJava
        self.sendIP = sendIP

        self.Running = False
        self.Connected = False
        self.End = False
        self.allDataSend = []
        self.allDataRec = []
        self.s = socket.socket()
        self.conAddress = None
        self.con = None

        self.reac = react

    def stop(self):
        self.Running = False
        self.End = True
        self.Connected = False
        if self.con:
            self.con.close()

    def send(self, data):
        if self.Running and self.Connected and not self.End:
            if type(data) == str:
                data = data.encode()
            else:
                data = str(data).encode()
            data += b'\r\n'
            if self.allowPrint:
                print("[Log] Sending:" + str(data))
            self.con.send(data)
            self.allDataSend.append(data)

    def react(self, curData):
        if self.allowPrint:
            print("[Log] Recieving:" + str(curData))
        data = curData.decode("UTF-8").lstrip().rstrip()
        if self.giveJava:
            self.reac(data, java=True)
        else:
            self.reac(data)

    def run(self):
        self.Running = True
        self.bind()

        if self.allowPrint:
            print("[Log] Started!")
        while self.Running:
            self.s.listen(1)
            self.con, self.conAddress = self.s.accept()
            if self.allowPrint:
                print("[Log] Connected:" + str(self.conAddress))
            if self.sendIP:
                self.reac(self.conAddress)
            self.Connected = True
            while self.Connected:
                try:
                    data = self.con.recv(1024)
                except ConnectionResetError:
                    self.Connected = False
                    break
                if not data:
                    break
                self.allDataRec.append(data)
                self.react(data)

        self.stop()

    def bind(self):
        self.s.bind((self.host, self.port))
