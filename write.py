class WriteASM:
    program = "program.asm"
    def write(string):
        with open(WriteASM.program, "a") as assemblyFile:
            assemblyFile.write(string)
            assemblyFile.close()