with open("testcases.txt", "r") as file:
    lines = file.readlines()

def twos_complement(binary_str):
    n = len(binary_str)
    num = int(binary_str, 2)
    if num == 0:
        return binary_str  
    twos_comp = (1 << n) - num
    return bin(twos_comp)[2:].zfill(n)[-n:]

def num_to_binary(value, num):
    num = num - 1
    binary = []
    value = int(value)
    temp = value
    if value < 0:
        value = -value
    while num > 0:
        binary.append(str(value % 2))
        value = value // 2
        num -= 1
    if value != 0:
        return "Illegal"
    binary = binary[::-1]
    str1 = "".join(binary)
    if temp < 0:
        str1 = twos_complement(str1)
        str1 = "1" + str1
    else:
        str1 = "0" + str1
    return str1
def reg_to_binary(name):
    register_map = {
        "zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011", "tp": "00100",
        "t0": "00101", "t1": "00110", "t2": "00111", "s0": "01000", "fp": "01000",
        "s1": "01001", "a0": "01010", "a1": "01011", "a2": "01100", "a3": "01101",
        "a4": "01110", "a5": "01111", "a6": "10000", "a7": "10001", "s2": "10010",
        "s3": "10011", "s4": "10100", "s5": "10101", "s6": "10110", "s7": "10111",
        "s8": "10110", "s9": "11000", "s10": "11001", "s11": "11010", "t3": "11011",
        "t4": "11100", "t5": "11101", "t6": "11110"
    }
    return register_map.get(name, "Error")
def R_type(lst):
    reg = list(map(str, lst[1].split(",")))
    if reg_to_binary(reg[2]) == "Error" or  reg_to_binary(reg[1]) == "Error" or reg_to_binary(reg[0]) == "Error":
        return "Register Error"
    else:
        if lst[0] == "add":
            str1 =  "0000000" + reg_to_binary(reg[2]) + reg_to_binary(reg[1]) + "000" + reg_to_binary(reg[0]) + " 0110011"
        if lst[0] == "sub":
            str1 =  "0100000" + reg_to_binary(reg[2]) + reg_to_binary(reg[1]) + "000" + reg_to_binary(reg[0]) + " 0110011"
        if lst[0] == "slt":
            str1 =  "0000000" + reg_to_binary(reg[2]) + reg_to_binary(reg[1]) + "010" + reg_to_binary(reg[0]) + " 0110011"
        if lst[0] == "srl":
            str1 =  "0000000" + reg_to_binary(reg[2]) + reg_to_binary(reg[1]) + "101" + reg_to_binary(reg[0]) + " 0110011"
        if lst[0] == "or":
            str1 =  "0000000" + reg_to_binary(reg[2]) + reg_to_binary(reg[1]) + "110" + reg_to_binary(reg[0]) + " 0110011"
        if lst[0] == "and":
            str1 =  "0000000" + reg_to_binary(reg[2]) + reg_to_binary(reg[1]) + "111" + reg_to_binary(reg[0]) + " 0110011"
    return str1
def I_type(lst):
    reg = list(map(str, lst[1].split(",")))
    if "(" in reg:
        reg[2],reg[1]=map(str,reg[1].split("("))
        reg[2]=reg[2].strip(")")
    immediate=num_to_binary(reg[2],12)
    if reg_to_binary(reg[1]) == "Error" or reg_to_binary(reg[0]) == "Error":
        return "Register Error"
    if lst[0] == "lw":
        str1 = immediate+reg_to_binary[reg[1]]+"010"+reg_to_binary[reg[0]]+"0000011"
    elif lst[0] == "jalr":
        str1 = immediate+reg_to_binary[reg[1]]+"000"+reg_to_binary[reg[0]]+"1100111"
    elif lst[0] == "addi":
        str1 = immediate+reg_to_binary[reg[1]]+"000"+reg_to_binary[reg[0]]+"0010011"
    return str1
            
def S_type(lst):
    reg = list(map(str, lst[1].split(",")))
    reg[2],reg[1]=map(str,reg[1].split("("))
    reg[2]=reg[2].strip(")")
    immediate=num_to_binary(reg[2],12)
    if lst[0] == "sw":
        str1 = immediate[-12:-5]+reg_to_binary[reg[0]]+reg_to_binary[reg[1]]+"010"+immediate[-5:]+"0100011"
    return str1
def B_type(lst, labels, Pc):
    pass
def J_type(lst, labels, Pc):    
    parts = lst[1].split(",")
    if len(parts) != 2:
        return "Error: Incorrect operand count for J-type instruction."
    
    rd = reg_to_binary(parts[0].strip())
    if rd == "Error":
        return "Error: Invalid destination register"
    
    label = parts[1].strip()
    if label in labels.keys():
        str01 = num_to_binary(labels[label] - Pc - 1)
    else:
        try:    
            str01 = num_to_binary(int(label), 20)
            if str01 == "Illegal":
                return "Immediate is illegal."
        except:
            return "label is not defined"
    if lst[0] == "jal":
        str1 = str01[0]+ str01[10:] + str01[9] + str01[1:9] + reg_to_binary(rd) +"000" + str01[8:] + str01[1] + "1100011" 
    return str1
def Bonus_type(lst):
    if lst == "rst":
        str1 = I_type(["addi", "zero,zero,0"])
    elif lst == "halt":
        str1 = B_type(["beq", "zero,zero,0"])
    return str1

virtual_halt = False
labels = {}
Pc = -1
R_type_list = {"add", "sub", "slt", "srl", "or", "and"}
I_type_list = {"lw", "addi", "jalr"}
S_type_list = {"sw"}
B_type_list = {"beq", "bne", "blt"}
J_type_list = {"jal"}
Bonus_type_list = {"halt", "rst"}
for line in lines:
    if virtual_halt:
        final_line += "Virtual Halt is not the last instruction" + "\n"
    Pc += 1
    final_line = ""
    final_lines= ""
    line = line.strip("\n")
    line.strip()
    if ":" in line:
        lst1 = line.split(":")
        lst1 = [s.lstrip() for s in lst1]
        labels[lst1[0]] = Pc
        lst = list(map(str, lst1[1].split(maxsplit = 1)))
    else:
        lst = list(map(str, line.split(maxsplit = 1)))
    if lst == ["beq", "zero,zero,0"]:
        virtual_halt = True
    if lst[0] in R_type_list:
        final_line = R_type(lst)
    elif lst[0] in I_type_list:
        final_line = I_type(lst)
    elif lst[0] in S_type_list:
        final_line = S_type(lst)
    elif lst[0] in B_type_list:
        final_line = B_type(lst, labels, Pc)
    elif lst[0] in J_type_list:
        final_line = J_type(lst, labels, Pc)
    elif line in Bonus_type_list:
        final_line = Bonus_type(lst)
    else:
        final_line = "The given instruction is not supported/is incorrect."
    final_lines += final_line + "\n"
if virtual_halt == False:
    final_lines += "Virtual Halt is not present" + "\n"
with open("output code.txt", "w") as file:
    file.write(final_lines)
        
