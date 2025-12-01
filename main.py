import sys

argsSet = {"ProgrammPath": "-", "FilePath": "-", "Mode": "-"}

acamulator = 0
RAMmemory = [0] * 64
application = []

def CommandStringPars():
    flag = True
    args = sys.argv[1:]
    for key in list(argsSet.keys()):
        commandParametr =  "-" + key[0]
        if commandParametr in args:
            pos = args.index(commandParametr)
            argsSet[key] = args.pop(pos + 1)
            args.pop(pos)
            #print(f"arg {commandParametr} has been set to {argsSet[key]}")
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
        open(argsSet["FilePath"])
    except:
        print(f"Error: can't find memory file in {argsSet["FilePath"]}, it will be created")
        open(argsSet["FilePath"], "x")
        
    if (not (argsSet["Mode"] in ["Test", "Normal"])):
        print(f"Error: {argsSet["Mode"]} isn't correct run mode, it will be set to Normal mode")
        argsSet["Mode"] = "Normal"

    try:
        open(argsSet["ProgrammPath"])
    except:
        print(f"Error: can't find program file in {argsSet["ProgrammPath"]}")
        return False
    
    return True

def Read(adress):
    global acamulator
    if (adress < len(RAMmemory)):
        acamulator = RAMmemory[adress]
    else:
        print("Error: invalid access to memory location")
    # with open(argsSet["FilePath"]) as f:
    #     memory = f.readlines()
    #     if len(memory) < adress or not memory[adress].isdigit:
    #         print("Error: invalid access to memory location")
    #         return 1
    #     else:
    #         acamulator = memory[adress]
    # return 0

def Write(adress, value):
    if (adress < len(RAMmemory)):
        RAMmemory[adress] = value
    else:
        print("Error: invalid access to memory location")
    # with open(argsSet["FilePath"]) as f:
    #     f.wr

def BSWP():
    global acamulator
    #print(bin(acamulator)[6:] + bin(acamulator)[:5], int(bin(acamulator)[6:] + bin(acamulator)[:5], 2))
    acamulator = int(bin(acamulator)[6:] + bin(acamulator)[:5], 2)

def WriteInFile():
    with open(argsSet["FilePath"], "w") as f:
        if (f.writable()):
            for i in RAMmemory:
                f.write(str(i) + " ")
        else:
            return 1
    return 0

def ReadProgram():
    with open(argsSet["ProgrammPath"]) as f:
        ParsProgramm(f.read())

def ParsProgramm(ProgramString: str):
    prog = ProgramString.split("\n")
    func = prog[0]
    buf = ""
    for i in range(1, len(prog)):
        if not prog[i][0] in [" ", "\t"]:
            application.append([func[:-3], [j[:-2].replace(" ", "") if j[-1] in ["{", "}", " "] else j.replace(" ", "") for j in buf.split(", ")]])
            func = prog[i]
            buf = ""
        else:
            buf += prog[i]
    application.append([func[:-3], [j[:-2].replace(" ", "") if j[-1] in ["{", "}"] else j.replace(" ", "") for j in buf.split(", ")]])
    [print(i) for i in application]
    return application

def RunProgam():
    for i in application:
        if i[0] == "const":
            buf = dict()
            for a in i[1]:
                a = a.split(":")
                buf[a[0]] = int(a[1])
            Write(buf["adress"], buf["value"])
        elif i[0] == "read":
            Read(int(i[1][0].split(":")[1]))
        elif i[0] == "write":
            Write(int(i[1][0].split(":")[1]), acamulator)
        elif i[0] == "bswap":
            BSWP()

def TestRunMode():
    ReadProgram()
    RunProgam()
    WriteInFile()

def main():
    if (CommandStringPars() and CheckInputedArguments()):
        if (argsSet["Mode"] == "Test"):
            TestRunMode()

if (__name__ == "__main__"):
    main()
    input("Press 'Enter' to exit.")
