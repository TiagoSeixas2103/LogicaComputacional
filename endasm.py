class FinalizeASM:
    list_init = [
        "\n",
        "; depois que terminar de gerar o código:\n",
        "PUSH DWORD [stdout]\n",
        "CALL fflush\n",
        "ADD ESP, 4\n",
        "MOV ESP, EBP\n",
        "POP EBP\n",
        "MOV EAX, 1\n",
        "XOR EBX, EBX\n",
        "INT 0x80\n",
    ]
    def writeEndASM(program):
        with open(program, "a") as assemblyFile:
            for string in FinalizeASM.list_init:
                assemblyFile.write(string)
            assemblyFile.close()