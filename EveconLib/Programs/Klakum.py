import EveconLib.Networking.Client

class RelayC:
    def __init__(self, myid, connection):
        self.id = myid
        self.connetion = connection
        self.value = None

    def refresh(self):
        if self.connetion.Connected:
            self.connetion.send("relay_" + str(self.id) + "_get")

    def set(self, value):
        if self.connetion.Connected:
            self.value = value
            self.connetion.send("relay_" + str(self.id) + "_set_" + str(value))

    def switch(self):
        if self.connetion.Connected:
            self.connetion.send("relay_" + str(self.id) + "_switch")


class SRelayC:
    def __init__(self, myid, connection):
        self.id = myid
        self.connetion = connection

    def switch(self):
        if self.connetion.Connected:
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
    global Connected
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
    global Connected
    if Connected:
        connection.exit()
        Connected = False

        return True
    else:
        return False


def refresh():
    for x in relays:
        x.refresh()
        time.sleep(0.05)


connection = EveconLib.Networking.Client(ip="192.168.2.107", port=1007, react=react)
relays = [RelayC(0, connection), RelayC(1, connection), RelayC(2, connection),
          RelayC(3, connection), RelayC(4, connection), RelayC(5, connection),
          RelayC(6, connection)]

srelays = [SRelayC(0, connection)]

Connected = False
