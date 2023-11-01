class InitializeASM:
    list_init = []
    with open("init.asm") as file:
        for line in file:
            list_init.append(line)
    def writeInitASM(program):
        with open(program, "a") as assemblyFile:
            for string in InitializeASM.list_init:
                assemblyFile.write(string)
            assemblyFile.close()