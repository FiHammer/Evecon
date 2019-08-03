CurColor = "07"
colors = {"0": "black", "1": "blue", "2": "green", "3": "cyan", "4": "red", "5": "purple",
               "6": "yellow", "7": "light gray", "8": "gray", "9": "light blue", "A": "light green",
               "B": "light cyan", "C": "light red", "D": "light purple", "E": "light yellow", "F": "white"}
colorsinv = {"black": "0", "blue": "1", "green": "2", "cyan": "3", "red": "4", "purple": "5",
                  "yellow": "6", "light gray": "7", "gray": "8", "light blue": "9", "light green": "A",
                  "light cyan": "B", "light red": "C", "light purple": "D", "light yellow": "E", "white": "F"}
colorKeys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]


def encode(code, printit=False):
    background = colors[code[0]]
    foreground = colors[code[1]]
    if printit:
        pass
    return background, foreground


def decode(background, foreground, printit=False):
    code = ""
    code += colorsinv[background]
    code += colorsinv[foreground]
    if printit:
        pass
    return code


def change(code):
    pass


def switch():
    if CurColor == "07":
        change("F0")
    elif CurColor == "F0":
        change("07")


def Man():
    pass
