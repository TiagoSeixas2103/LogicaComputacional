class FinalizeASM:
    list_init = []
    with open("end.asm") as file:
        for line in file:
            list_init.append(line)
    def writeEndASM(program):
        with open(program, "a") as assemblyFile:
            for string in FinalizeASM.list_init:
                assemblyFile.write(string)
            assemblyFile.close()