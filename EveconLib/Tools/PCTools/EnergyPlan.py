import subprocess

import EveconLib.EveconExceptions as EveconExceptions


cEP = None
cEP_code = None
cEP_id = None

Plans = ["381b4222-f694-41f0-9685-ff5bb260df2e", "a1841308-3541-4fab-bc81-f71556f20b4a",
         "472405ce-5d19-4c83-94d7-a473c87dedad"]
Plans_Dic = {"Ausbalanciert": "381b4222-f694-41f0-9685-ff5bb260df2e",
             "Energiesparmodus": "a1841308-3541-4fab-bc81-f71556f20b4a",
             "0Sys": "472405ce-5d19-4c83-94d7-a473c87dedad"}


def getEP(printit=False):
    global cEP, cEP_code, cEP_id
    p = subprocess.Popen(["powercfg", "/GETACTIVESCHEME"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    try:
        eplan_tmp = output.decode("utf-8")
    except UnicodeDecodeError:
        eplan_tmp = 'GUID des Energieschemas: a1841308-3541-4fab-bc81-f71556f20b4a  (Energiesparmodus)'

    eplan_tmp2 = eplan_tmp.lstrip("GUID des Energieschemas").lstrip(": ")
    eplan_code = ""
    for x in range(36):
        eplan_code += eplan_tmp2[x]

    cEP_code = eplan_code

    if eplan_code == '381b4222-f694-41f0-9685-ff5bb260df2e':
        cEP = "Ausbalanciert"
        cEP_id = 0
    elif eplan_code == 'a1841308-3541-4fab-bc81-f71556f20b4a':
        cEP = "Energiesparmodus"
        cEP_id = 1
    elif eplan_code == '472405ce-5d19-4c83-94d7-a473c87dedad':
        cEP = "0Sys"
        cEP_id = 2
    else:
        raise EveconExceptions.EnergyPlanNotFound

    if printit:
        print("Current Plan:")
        print(cEP)
        print("Code: " + cEP_code)

    return cEP_id


def Change(ID):
    subprocess.call(["powercfg", "/s", str(Plans[ID])])


def Switch():
    getEP()
    if cEP_id == 0:
        Change(1)
    elif cEP_id == 1:
        Change(0)
    elif cEP_id == 2:
        Change(1)
