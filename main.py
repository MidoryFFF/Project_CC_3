import sys

_argsSet = {"ProgrammPath": "-", "FilePath": "-", "Mode": "-"}
_commandsSet = {"CreateConst": 1, "Read": 2, "Write": 3, "Bswap": 4}
_acamulator = 0
_RAMmemory = [0] * 64
_application = []

def CommandStringPars():
    flag = True
    args = sys.argv[1:]
    for key in list(_argsSet.keys()):
        commandParametr =  "-" + key[0]
        if commandParametr in args:
            pos = args.index(commandParametr)
            _argsSet[key] = args.pop(pos + 1)
            args.pop(pos)
        else:
            print(f"Error: argument {commandParametr} isn't set")
            flag = False
    if (len(args) > 0):
        for i in args:
            if (i[0] == "-"):
                print(f"Error: wrong parameter {i} was added")
        flag = False
    return flag

def CheckInputedArguments():
    try:
        open(_argsSet["FilePath"])
    except:
        print(f"Error: can't find memory file in " + str(_argsSet["FilePath"]) + ", it will be created")
        open(_argsSet["FilePath"], "x")
    if (not (_argsSet["Mode"] in ["Test", "Normal"])):
        print(f"Error: " + str(_argsSet["Mode"]) + " isn't correct run mode, it will be set to Normal mode")
        _argsSet["Mode"] = "Normal"
    try:
        open(_argsSet["ProgrammPath"])
    except:
        print(f"Error: can't find program file in " + str(_argsSet["ProgrammPath"]))
        return False
    return True

def Read(adress):
    global _acamulator
    if (0 <= adress < len(_RAMmemory)):
        _acamulator = _RAMmemory[adress]
    else:
        print("Error: invalid access to memory location")
    # with open(_argsSet["FilePath"]) as f:
    #     memory = f.readlines()
    #     if len(memory) < adress or not memory[adress].isdigit:
    #         print("Error: invalid access to memory location")
    #         return 1
    #     else:
    #         _acamulator = memory[adress]
    # return 0

def CreateConstant(value):
    global _acamulator
    _acamulator = value 

def Write(adress, value):
    if (0 <= adress < len(_RAMmemory)):
        _RAMmemory[adress] = value
    else:
        print("Error: invalid access to memory location")

def BSWP(adress):
    global _acamulator
    #print(bin(_acamulator), bin(_acamulator)[6:] + bin(_acamulator)[2:5], int(bin(_acamulator)[6:] + bin(_acamulator)[2:5], 2))
    _RAMmemory[adress] = int(bin(_acamulator)[8:] + bin(_acamulator)[2:7], 2)

def WriteInFile():
    with open(_argsSet["FilePath"], "w") as f:
        if (f.writable()):
            for i in _RAMmemory:
                f.write(str(i) + " ")
        else:
            return 1
    return 0

def BinPresent(command, argument):
    return [bin(command), bin(argument)]

def ReadProgram():
    with open(_argsSet["ProgrammPath"]) as f:
        ParsProgramm(f.read())

def MinorPars(argsPars: str, nameAction: str):
    temp = [nameAction[:-3], [j[:-2].replace(" ", "") if j[-1] in ["{", "}"] else j.replace(" ", "") for j in argsPars.split(", ")]]
    # temp = []
    # for j in argsPars.split(", "):
    #     if j[-1] in ["{", "}", " "]:
    #         temp.append([nameAction[:-3], [j[:-2].replace(" ", "")]])
    #     else:
    #         j.replace(" ", "")
    # temp = temp[0]
    for a in range(len(temp[1])):
        if (":" in temp[1][a]):
            temp[1][a] = temp[1][a].split(":")
            try:
                temp[1][a][1] = int(temp[1][a][1])
            except:
                print("Error: invalid syntax")
                return
    return temp

def ParsProgramm(ProgramString: str):
    prog = ProgramString.split("\n")
    func = prog[0]
    buf = ""
    for i in range(1, len(prog)):
        if len(prog[i]) > 0: 
            if not (prog[i][0] in [" ", "\t"]):
                _application.append(MinorPars(buf, func))
                func = prog[i]
                buf = ""
            else:
                buf += prog[i]
    _application.append(MinorPars(buf, func))
    if (None in _application):
        return
    #[print(i) for i in _application]
    return _application

def RunProgam():
    for i in _application:
        try:
            i[0], i[1]
            #print(i[0], i[1])
        except:
            return
        buf = dict()
        for a in i[1]:
            if (len(a) > 0):
                buf[a[0]] = a[1]
        if i[0] == "const":
            CreateConstant(buf["value"])
            print(*BinPresent(_commandsSet["CreateConst"], buf["value"]))
        elif i[0] == "read":
            Read(buf["adress"])
            print(*BinPresent(_commandsSet["Read"], buf["adress"]))
        elif i[0] == "write":
            Write(buf["adress"], _acamulator)
            print(*BinPresent(_commandsSet["Write"], buf["adress"]))
        elif i[0] == "bswap":
            BSWP(buf["adress"])
            print(*BinPresent(_commandsSet["Bswap"], buf["adress"]))
        else:
            print("Error: unkown " + i[0] + " command, this command will be skiped")

def TestRunMode():
    ReadProgram()
    RunProgam()
    WriteInFile()

def main():
    if (CommandStringPars() and CheckInputedArguments()):
        if (_argsSet["Mode"] == "Test"):
            TestRunMode()

if (__name__ == "__main__"):
    main()
    input("Press 'Enter' to exit.")
