import threading
#import click
from click import getchar as click_getchar
#import click

class Scanner(threading.Thread):
    def __init__(self, action, raw=False):
        """
        :type action: object
        react
        """
        super().__init__()
        self.action = action


        self.running = True
        self.raw = raw

    def run(self):
        while self.running:
            #char = click.getchar()
            char = click_getchar()
            if self.running:
                if self.raw:
                    self.action(char)
                else:
                    if char == "\x1b":
                        self.action("escape")
                    elif char == "\x00;":
                        self.action("F1")
                    elif char == "\x00<":
                        self.action("F2")
                    elif char == "\x00=":
                        self.action("F3")
                    elif char == "\x00>":
                        self.action("F4")
                    elif char == "\x00?":
                        self.action("F5")
                    elif char == "\x00@":
                        self.action("F6")
                    elif char == "\x00A":
                        self.action("F7")
                    elif char == "\x00B":
                        self.action("F8")
                    elif char == "\x00C":
                        self.action("F9")
                    elif char == "\x00D":
                        self.action("F10")
                    elif char == 'à\x85':
                        self.action("F11")
                    elif char == 'à\x86':
                        self.action("F12")
                    elif char == "\x08":
                        self.action("backspace")
                    elif char == "\x7f":
                        self.action("strg_backspace")
                    elif char == "àR":
                        self.action("insert")
                    elif char == "àG":
                        self.action("home") #pos1
                    elif char == "àI":
                        self.action("pageup")
                    elif char == "àS":
                        self.action("del")
                    elif char == "àO":
                        self.action("end")
                    elif char == "àQ":
                        self.action("pagedown")
                    elif char == "àH":
                        self.action("arrowup")
                    elif char == "àK":
                        self.action("arrowleft")
                    elif char == "àP":
                        self.action("arrowdown")
                    elif char == "àM":
                        self.action("arrowright")
                    elif char.encode() == b'\xc3\xa0\xc2\x8d':
                        self.action("strg_arrowup")
                    elif char == "às":
                        self.action("strg_arrowleft")
                    elif char.encode() == b'\xc3\xa0\xc2\x91':
                        self.action("strg_arrowdown")
                    elif char == "àt":
                        self.action("strg_arrowright")
                    elif char == "\x00R":
                        self.action("num0")
                    elif char == "\x00O":
                        self.action("num1")
                    elif char == "\x00P":
                        self.action("num2")
                    elif char == "\x00Q":
                        self.action("num3")
                    elif char == "\x00K":
                        self.action("num4")
                    elif char == "\x00M":
                        self.action("num6")
                    elif char == "\x00G":
                        self.action("num7")
                    elif char == "\x00H":
                        self.action("num8")
                    elif char == "\x00I":
                        self.action("num9")
                    elif char == "\r":
                        self.action("return")
                    else:
                        self.action(char)
