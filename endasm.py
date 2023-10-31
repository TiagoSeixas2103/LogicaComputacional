class FinalizeASM:
    list_init = [
        "\n",
        "; interrupcao de saida ( default )\n",
        "POP EBP\n",
        "MOV EAX, 1\n",
        "INT 0x80\n",
    ]
    def writeEndASM():
        with open("program.asm", "a") as assemblyFile:
            for string in FinalizeASM.list_init:
                assemblyFile.write(string)
            assemblyFile.close()