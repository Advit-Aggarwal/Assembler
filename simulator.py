with open("file.txt", "r") as file:
    lines = file.readlines()

memory = {
        "0" : "", "1" : "", "2" : "", "3" : "", "4" : "", "5" : "", "6" : "", "7" : "", "8" : "", "9" : "", "10" : "", "11" : "",
        "12" : "", "13" : "", "14" : "", "15" : "", "16" : "", "17" : "", "18" : "", "19" : "", "20" : "", "21" : "",
        "22" : "", "23" : "", "24" : "", "25" : "", "26" : "", "27" : "", "28" : "", "29" : "", "30" : "", "31" : ""
    }

register_map = {
        "00000": "", "00001": "", "00010": "", "00011": "", "00100": "",
        "00101": "", "00110": "", "00111": "", "01000": "", "01001": "",
        "01010": "", "01011": "", "01100": "", "01101": "", "01110": "",
        "01111": "", "10000": "", "10001": "", "10010": "", "10011": "",
        "10100": "", "10101": "", "10110": "", "10111": "", "11000": "",
        "11001": "", "11010": "", "11011": "", "11100": "", "11101": "", 
        "11110": "", "11111": ""
    }

def reg(register_map, rd, reg1, operation, reg2 = None, immi = False):
    if operation.lower() == "add":
        if immi:
            register_map[rd] = int(register_map[reg1]) + int(reg2)
        else:
            register_map[rd] = int(register_map[reg1]) + int(register_map[reg2])
    elif operation.lower() == "sub":
        register_map[rd] = int(register_map[reg1]) - int(register_map[reg2])
    elif operation.lower() == "slt":
        if int(register_map[reg1]) < int(register_map[reg2]):
            register_map[rd] = "1"
    elif operation.lower() == "srl":
        rd =  int(register_map[reg1]) >> int(register_map[reg2]) % 32
    elif operation.lower() == "or":
        register_map[rd] = int(register_map[reg1]) | int(register_map[reg2])
    elif operation.lower() == "and":
        register_map[rd] = int(register_map[reg1]) & int(register_map[reg2])
    
def memory_map(memory, address, value = None, store = False, retrieve = False):
    if store:
        memory[address] = str(value)
        return 
    if retrieve:
        return memory.get(str(address), "Memory Call Error")

def R_type(register_map, line):
    if line[:7] == "0000000":
        rd = int(line[20:25])
        reg1 = int(line[12:17])
        reg2 = int(line[7:12])
        if line[17:20] == "000":
            reg(register_map, rd, reg1, "add", reg2)
        elif line[17:20] == "010":
            reg(register_map, rd, reg1, "slt", reg2)
        elif line[17:20] == "101":
            reg(register_map, rd, reg1, "srl", reg2)
        elif line[17:20] == "110":
            reg(register_map, rd, reg1, "or", reg2)
        elif line[17:20] == "111":
            reg(register_map, rd, reg1, "and", reg2)
    elif line[:7] == "0100000":
        if line[17:20] == "000":
            reg(register_map, rd, reg1, "sub", reg2)
    return

def I_type(register_map, memory, line):
    global Pc
    rd = int(line[20:25])
    reg1 = int(line[12:17])
    immi = int(line[:12])
    if line[26:] == "0000011":
        int(register_map[rd]) = int(memory_map(memory, int(register_map[reg1]) + immi, retrieve = True))
    elif line[26:] == "0010011":
        reg(register_map, rd, reg1, "add", immi, immi = True)
    elif line[26:] == "1100111":
        register_map[rd] = Pc
        Pc = int(register_map[reg1]) + immi
    return

def S_type(register_map, memory, line):
    reg1 = int(line[12:17])
    reg2 = int(line[7:12])
    immi = int(line[:7] + line[20:25])
    memory_map(memory, int(register_map[reg1]) + immi, register_map[reg2], store = True)
    
# done till here    
    
def B_type(register_map, line):
    global Pc
    reg1 = int(line[12:17])
    reg2 = int(line[7:12])
    immi = int(line[0] + line[24] + line[1:7] + line[20:24] + "0")
    if line[17:20] == "000":
        if int(register_map[reg1]) == int(register_map[reg2]):
            Pc += immi
    elif line[17:20] == "001":  
        if int(register_map[reg1]) != int(register_map[reg2]):
            Pc += immi
    elif line[17:20] == "100":  
        if int(register_map[reg1]) < int(register_map[reg2]):
            Pc += immi
    elif line[17:20] == "101": 
        if int(register_map[reg1]) >= int(register_map[reg2]):
            Pc += immi

def J_Type(register_map, line):
    global Pc
    rd = int(line[20:25])
    immi = int(line[0] + line[12:20] + line[11] + line[1:11] + "0")
    register_map[rd] = str(Pc + 4)
    Pc += immi
    

#main
Pc = 0
line = lines[Pc // 4]
while line != "Virtual Halt is not present" and line != "00000000000000000000000001100011":
    Pc += 4
    if line[26:] == "0110011":
        R_type(register_map, line)
    elif line[26:] == "0000011" or line[26:] == "0010011" or line[26:] == "1100111":
        I_type(register_map, memory, line)
    elif line[26:] == "0100011":
        S_type(register_map, memory, line)
    elif line[26:] == "1100011":
        B_type(register_map, line)
    elif line[26:] == "1101111":
        J_Type(register_map, line)
