class InitializeASM:
    list_init = [
        "; constantes\n", "SYS_EXIT equ 1\n", 
        "SYS_READ equ 3\n", 
        "SYS_WRITE equ 4\n", 
        "STDIN equ 0\n", 
        "STDOUT equ 1\n", 
        "True equ 1\n", 
        "False equ 0\n", 
        "\n", 
        "segment .data\n", 
        'formatin: db "%d", 0\n', 
        'formatout: db "%d", 10, 0 ; newline, null terminator\n', 
        "scanint: times 4 db 0 ; 32-bit integer = 4 bytes\n", 
        "\n", 
        "segment .bss ; variáveis\n", 
        "res RESB 1\n", 
        "\n", 
        "section .text\n", 
        "global main ; linux\n", 
        "; global _main ; windows\n", 
        "extern scanf ; linux\n", 
        "extern printf ; linux\n", 
        "; extern _scanf ; windows\n", 
        "extern _printf ; windows\n", 
        "\n", 
        "; subrotinas if/while\n", 
        "binop_je:\n", 
        "    JE binop_true\n", 
        "    JMP binop_false\n", 
        "binop_jg:\n", 
        "    JG binop_true\n", 
        "    JMP binop_false\n", 
        "binop_jl:\n", 
        "    JL binop_true\n", 
        "    JMP binop_false\n", 
        "binop_false:\n", 
        "    MOV EAX, False\n", 
        "    JMP binop_exit\n", 
        "binop_true:\n", 
        "    MOV EAX, True\n", 
        "binop_exit:\n", 
        "    RET\n", 
        "\n", 
        "main:\n", 
        "\n" 
    ]
    def writeInitASM():
        with open("program.asm", "a") as assemblyFile:
            for string in InitializeASM.list_init:
                assemblyFile.write(string)
            assemblyFile.close()