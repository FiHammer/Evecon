import EveconLib.Networking.Client
import time

class RelayC:
    def __init__(self, myid, connection):
        self.id = myid
        self.connetion = connection
        self.value = None

    def refresh(self):
        if self.connetion.status == 2 or self.connetion.status == 3:
            self.connetion.send("relay_" + str(self.id) + "_get")

    def set(self, value):
        if self.connetion.status == 2 or self.connetion.status == 3:
            self.value = value
            self.connetion.send("relay_" + str(self.id) + "_set_" + str(value))

    def switch(self):
        if self.connetion.status == 2 or self.connetion.status == 3:
            self.connetion.send("relay_" + str(self.id) + "_switch")


class SRelayC:
    def __init__(self, myid, connection):
        self.id = myid
        self.connetion = connection

    def switch(self):
        if self.connetion.status == 2 or self.connetion.status == 3:
            self.connetion.send("srelay_" + str(self.id) + "_switch")



def react(msg):
    msg_split = msg.split("_")

    if msg_split[0] == "relay":

        relay_id = int(msg_split[1])
        if msg_split[2] == "return":
            relays[relay_id].value = msg_split[3]

    elif msg_split[0] == "srelay":
        relay_id = int(msg_split[1])


def connect():
    if not Started:
        startup()
    global Connected, connection
    if not Connected:
        connection.start()
        while not connection.running:
            time.sleep(0.05)
        time.sleep(0.15)
        Connected = True
        refresh()
        time.sleep(0.05)
        return True
    else:
        return False


def disconnect():
    if not Started:
        startup()
    global Connected
    if Connected:
        connection.exit()
        Connected = False

        return True
    else:
        return False


def refresh():
    if not Started:
        startup()
    for x in relays:
        x.refresh()
        time.sleep(0.05)

def startup():
    global connection, relays, srelays
    connection = EveconLib.Networking.Client(ip="192.168.2.107", port=2343, react=react)
    relays = [RelayC(0, connection), RelayC(1, connection), RelayC(2, connection),
              RelayC(3, connection), RelayC(4, connection), RelayC(5, connection),
              RelayC(6, connection)]

    srelays = [SRelayC(0, connection)]

Connected = False
Started = False

relays = []
srelays = []
connection = None