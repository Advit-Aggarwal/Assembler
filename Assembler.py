with open("testcases.txt", "r") as file:
    lines = file.readlines()
def twos_compliment(value):
    pass
def num_to_binary(value, ):
    binary = []
    temp = value
    while num > 0:
        binary.append(str(value % 2))
        value = value // 2
        num -= 1
    if value != "0":
        return "Illegal"
    binary = binary[::-1]
    str1 = "".join(binary)
    if temp < 0:
        str1 = twos_compliment(str1)
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
    pass
def S_type(lst):
    pass
def B_type(lst):
    pass
def J_type(lst, labels, Pc):    
    parts = lst[1].split(",")
    if len(parts) != 2:
        return "Error: Incorrect operand count for J-type instruction"
    
    rd = reg_to_binary(parts[0].strip())
    if rd == "Error":
        return "Error: Invalid destination register"
    
    label = parts[1].strip()
    if label not in labels.keys():
        return "Error: Undefined label"
    imm = (labels[label] - Pc - 1) 
def Bonus_type(lst):
    pass

def main(lines):
    labels = {}
    Pc = -1
    R_type_list = {"add", "sub", "slt", "srl", "or", "and"}
    I_type_list = {"lw", "addi", "jarl"}
    S_type_list = {"sw"}
    B_type_list = {"beq", "bne", "blt"}
    J_type_list = {"jal"}
    Bonus_type_list = {"halt", "rst"}
    for line in lines:
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
            print("The given instruction is not supported/is incorrect.")
        if final_line != "":
            final_lines += final_line + "\n"
    
    with open("output code.txt", "w") as file:
        file.write(final_lines)
