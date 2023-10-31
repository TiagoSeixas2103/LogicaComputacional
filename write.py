class WriteASM:
    def write(string):
        with open("program.asm", "a") as assemblyFile:
            assemblyFile.write(string)
            assemblyFile.close()