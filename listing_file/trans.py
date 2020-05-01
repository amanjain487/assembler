
#tabulate module to print symbol table and literal table in table format
from tabulate import tabulate


#function to check whether passed argument 'temp' contains operator from 'op
#returns true if operator else false
def is_operator(temp,op):
    operator = ""
    j = 0
    while temp[j] != ' ':
        operator += temp[j]
        j += 1
    if operator in op:
        return True
    else:
        return False


#function to check whether passed argument 'temp' contains operator from 'op
#returns true if operator other than jmp and jnz else false
def check_operator(temp,op):
    operator = ""
    j = 0
    while temp[j] != ' ':
        operator += temp[j]
        j += 1
    if operator == "jmp" or operator == "jnz" or operator == "jz":
        return False
    if operator in op:
        return True
    else:
        return False


#function to get operator from passed argument
#returns operator
def get_operator(temp,op):
    operator = ""
    j = 0
    while temp[j] != ' ':
        operator += temp[j]
        j += 1
    if operator in op:
        return operator
    else:
        return None


def checkbyte(value):
    while len(value) < 2:
        value = '0' + value
    return value


def checkword(value):
    while len(value) < 4:
        value =  value + '00'
    return value


def checkdouble(value):
    while len(value) < 8:
        value = value + '00'
    return value



def fwd(c,lab):
    symbol_address = "0x0"
    count_size = 0
    while c < len(file):
        temp = file[c]
        if ":" in temp:
            l = temp.split(":",1)[0].strip() + ":"
            if l == lab.strip() + ":":
                return count_size
            else:
                if ':' in temp:
                    symbol_name = ""
                    symbol_address = None
                    symbol_type = "Label"
                    symbol_value = None
                    symbol_size = 0
                    symbol_def = "U"
                    j = 0
                    while temp[j] != ':':
                        symbol_name += temp[j]
                        j += 1
                    modified = temp[j + 1:].strip()
                    temp = modified
                    defined = 0

                    # if label already present in symbol_table and if it is undefined make it as defined
                    for k in symbol_table:
                        if k[0] == symbol_name:
                            defined = 1

                    # if label not present aleady, add label in symbol table
                    if defined != 1:
                        symbol = []
                        symbol.append(symbol_name)
                        symbol.append(symbol_address)
                        symbol.append(symbol_section)
                        symbol.append(symbol_type)
                        symbol.append(symbol_value)
                        symbol.append(symbol_size)
                        symbol.append(symbol_def)
                        symbol_table.append(symbol)

        new_new_temp = temp
        operator = get_operator(temp, op)
        temp = temp.split(operator + ' ', 1)[1]
        op1 = ""
        op2 = ""
        new_temp = temp
        check_address = ""
        # if ',' in instruction, the instruction contains 2 operands for sure
        if ',' in temp:
            j = 0
            while temp[j] != ',':
                op1 += temp[j]
                j += 1
            temp = temp[j + 1:]
            op2 = temp.strip()

        # else only 1 operand, 2nd one is none
        else:
            op1 = temp.strip()
            op2 = None
        address_getter = ""
        op1 = op1.strip()
        if op1 in registers:
            address_getter = "reg"

        elif "*" in op1:
            op1 = op1.split("[", 1)[1][:-1].strip()
            if op1[:3] in registers:
                address_getter = "mem[reg+reg*s]"
            else:
                address_getter = "mem[var+reg*s]"
        elif "dword[" in op1 or "[" in op1:
            if "dword" in op1:
                op1 = op1[6:-1]
            else:
                op1 = op1[1:-1]
            if op1[:3] in registers:
                op1 = op1[3:].strip()
                if op1 != "":
                    address_getter = "mem[reg+imm]"
                else:
                    address_getter = "mem[reg]"
            else:
                if "+" in op1:
                    address_getter = "mem[var+imm]"
                else:
                    address_getter = "mem"

        elif (
                operator == "push" or operator == "call" or operator == "jmp" or operator == "jnz" or operator == "jz") and "[" not in op1 and "imm" not in address_getter and address_getter == "":
            address_getter = ""
            check_address = ""
            for m in symbol_table:
                if m[0] == op1:
                    if operator == "jmp" or operator == "jnz" or operator == "jz":
                        if m[2] == "text":
                            if m[1] == None:
                                if m[3] == "Label":
                                    address_getter = "fwd"
                                elif m[3] == "Function":
                                    address_getter = "label"
                            else:
                                check_address = m[1]
                                address_getter = "bwd"
                        else:
                            address_getter = "label"

                    else:
                        address_getter = "label"
            if address_getter == "":
                try:
                    x = int(op1)
                    address_getter = "imm"
                except:
                    if operator == "jmp" or operator == "jnz" or operator == "jz":
                        address_getter = "fwd"
                    else:
                        address_getter = "label"

        if op2 != None:
            op2 = op2.strip()
            if op2 in registers:
                address_getter += ',reg'

            elif "*" in op2:
                op2 = op2.split("[", 1)[1][:-1].strip()
                if op2[:3] in registers:
                    address_getter += ",mem[reg+reg*s]"
                else:
                    address_getter += ",mem[var+reg*s]"

            elif "dword[" in op2 or "[" in op2:
                if "dword" in op2:
                    op2 = op2[6:-1]
                else:
                    op2 = op2[1:-1]
                if op2[:3] in registers:
                    op2 = op2[3:].strip()
                    if op2 != "":
                        address_getter += ",mem[reg+imm]"
                    else:
                        address_getter += ",mem[reg]"
                else:
                    if "+" in op2:
                        address_getter += ",mem[var+imm]"
                    else:
                        address_getter += ",mem"

            else:
                address_getter += ",imm"

        # get instruction size from dictionary "op"
        current_address = op[operator][address_getter]
        if operator == "mov" and (
                address_getter == "mem,reg" or address_getter == "reg,mem" or address_getter == "reg,mem[var+imm]" or address_getter == "mem[var+imm],reg"):
            if op2 == "eax" or op1 == "eax":
                current_address = current_address["eax"]
            else:
                current_address = current_address["oth"]
        elif (operator == "jmp" or operator == "jnz" or operator == "jz"):
            if address_getter == "bwd":
                validate_address = ""
                if abs(int(symbol_address, 0) - int(check_address, 0)) <= 127:
                    current_address = current_address["127"]
                else:
                    current_address = current_address["128"]

            elif address_getter == "fwd":
                    current_address = current_address["128"]




        elif "imm" in address_getter and operator != "mov" and "imm]" not in address_getter:
            for s in symbol_table:
                if op2 != None and s[0].strip() == op2.strip():
                    current_address = 6
                    break
            if current_address == 6:
                j = 0
            elif address_getter == "imm":
                if int(op1) <= 127:
                    current_address = current_address["127"]
                else:
                    current_address = current_address["128"]
            elif int(op2) <= 127:
                current_address = current_address["127"]
            else:
                current_address = current_address["128"]
                if operator != "mov" and op1 == "eax" and address_getter == "reg,imm":
                    current_address = current_address["eax"]
                elif operator != "mov" and address_getter == "reg,imm":
                    current_address = current_address["oth"]
        elif "imm]" in address_getter:
            count = address_getter.count("imm")
            if count == 1:
                if op2 != None:
                    if "imm]," in address_getter:
                        if address_getter != "mem[var+imm],reg":
                            if int(op1) <= 127:
                                current_address = current_address["127"]
                            else:
                                current_address = current_address["128"]
                    else:
                        if address_getter != "reg,mem[var+imm]":
                            op2 = op2.split("+", 1)[1].strip()
                            if int(op2) <= 127:
                                current_address = current_address["127"]
                            else:
                                current_address = current_address["128"]
                else:
                    if type(current_address) == type({}):
                        if int(op1) <= 127:
                            current_address = current_address["127"]
                        else:
                            current_address = current_address["128"]
            elif count == 2:
                if address_getter != "mem[var+imm],imm" or operator != "mov":
                    op1 = op1.split("+", 1)[1].strip()
                    if "var" not in address_getter:
                        if int(op1) <= 127:
                            current_address = current_address["127"]
                        else:
                            current_address = current_address["128"]
                        if int(op2) <= 127:
                            current_address = current_address["127"]
                        else:
                            current_address = current_address["128"]
                    else:
                        if int(op2) <= 127:
                            current_address = current_address["127"]
                        else:
                            current_address = current_address["128"]

        count_size += current_address
        c += 1









#dictionary of frequently used opcodes along with their instruction size
op = {'mov' : {"reg,reg" : 2,
               "reg,mem" : {"eax" : 5,
                            "oth" : 6},
               "reg,imm" : 5,
               "reg,mem[reg]" : 2,

               "reg,mem[var+imm]" : {'eax' : 5,
                                     'oth' : 6},

               "reg,mem[reg+imm]" : {'127' : 3,
                                     '128' : 6},

               "reg,mem[reg+reg*s]" : 3,
               "reg,mem[var+reg*s]": 7,

               "mem,reg" : {'eax' : 5,
                            'oth' : 6},
               "mem,imm" : 10,

               "mem[reg],reg" : 2,
               "mem[reg],imm" : 6,

               "mem[var+imm],reg" : {"eax" : 5,
                                     "oth" : 6},
               "mem[var+imm],imm" : 10,

               "mem[reg+imm],reg" : {'127' : 3,
                                     '128' : 6},
               "mem[reg+imm],imm" : {'127' : {'127' : 7,
                                              '128' : 7},
                                     '128' : {'127' : 10,
                                              '128' : 10}
                                     },


               "mem[reg+reg*s],reg" : 3,
               "mem[reg+reg*s],imm" : 7,

               "mem[var+reg*s],reg" : 7,
               "mem[var+reg*s],imm" : 11
               },
      'add' : {"reg,reg" : 2,
               "reg,mem" : 6,
               "reg,imm" : {'127' : 3,
                            '128' : {"eax" : 5,
                                     "oth" : 6}
                            },
               "reg,mem[reg]" : 2,

               "reg,mem[var+imm]" : 6,

               "reg,mem[reg+imm]" : {'127' : 3,
                                     '128' : 6},

               "reg,mem[reg+reg*s]" : 3,
               "reg,mem[var+reg*s]": 7,

               "mem,reg" : 6,
               "mem,imm" : {'127' : 7,
                            '128' : 10},

               "mem[reg],reg" : 2,
               "mem[reg],imm" : {'127' : 3,
                                 '128' : 6},

               "mem[var+imm],reg" : 6,
               "mem[var+imm],imm" : {'127' : 7,
                                     '128' : 10},

               "mem[reg+imm],reg" : {'127' : 3,
                                     '128' : 6},
               "mem[reg+imm],imm" : {'127' : {'127' : 4,
                                              '128' : 7},
                                     '128' : {'127' : 7,
                                              '128' : 10}
                                     },


               "mem[reg+reg*s],reg" : 3,
               "mem[reg+reg*s],imm" : {'127' : 4,
                                       '128' : 7},

               "mem[var+reg*s],reg" : 7,
               "mem[var+reg*s],imm" : {'127' : 8,
                                       '128' : 11
                                       }
               },
      'sub' : {"reg,reg" : 2,
               "reg,mem" : 6,
               "reg,imm" : {'127' : 3,
                            '128' : {"eax" : 5,
                                     "oth" : 6}
                            },
               "reg,mem[reg]" : 2,

               "reg,mem[var+imm]" : 6,

               "reg,mem[reg+imm]" : {'127' : 3,
                                     '128' : 6},

               "reg,mem[reg+reg*s]" : 3,
               "reg,mem[var+reg*s]": 7,

               "mem,reg" : 6,
               "mem,imm" : {'127' : 7,
                            '128' : 10},

               "mem[reg],reg" : 2,
               "mem[reg],imm" : {'127' : 3,
                                 '128' : 6},

               "mem[var+imm],reg" : 6,
               "mem[var+imm],imm" : {'127' : 7,
                                     '128' : 10},

               "mem[reg+imm],reg" : {'127' : 3,
                                     '128' : 6},
               "mem[reg+imm],imm" : {'127' : {'127' : 4,
                                              '128' : 7},
                                     '128' : {'127' : 7,
                                              '128' : 10}
                                     },


               "mem[reg+reg*s],reg" : 3,
               "mem[reg+reg*s],imm" : {'127' : 4,
                                       '128' : 7},

               "mem[var+reg*s],reg" : 7,
               "mem[var+reg*s],imm" : {'127' : 8,
                                       '128' : 11
                                       }
               },
      'or' : {"reg,reg" : 2,
               "reg,mem" : 6,
               "reg,imm" : {'127' : 3,
                            '128' : {"eax" : 5,
                                     "oth" : 6}
                            },
               "reg,mem[reg]" : 2,

               "reg,mem[var+imm]" : 6,

               "reg,mem[reg+imm]" : {'127' : 3,
                                     '128' : 6},

               "reg,mem[reg+reg*s]" : 3,
               "reg,mem[var+reg*s]": 7,

               "mem,reg" : 6,
               "mem,imm" : {'127' : 7,
                            '128' : 10},

               "mem[reg],reg" : 2,
               "mem[reg],imm" : {'127' : 3,
                                 '128' : 6},

               "mem[var+imm],reg" : 6,
               "mem[var+imm],imm" : {'127' : 7,
                                     '128' : 10},

               "mem[reg+imm],reg" : {'127' : 3,
                                     '128' : 6},
               "mem[reg+imm],imm" : {'127' : {'127' : 4,
                                              '128' : 7},
                                     '128' : {'127' : 7,
                                              '128' : 10}
                                     },


               "mem[reg+reg*s],reg" : 3,
               "mem[reg+reg*s],imm" : {'127' : 4,
                                       '128' : 7},

               "mem[var+reg*s],reg" : 7,
               "mem[var+reg*s],imm" : {'127' : 8,
                                       '128' : 11
                                       }
               },
      'cmp' : {"reg,reg" : 2,
               "reg,mem" : 6,
               "reg,imm" : {'127' : 3,
                            '128' : {"eax" : 5,
                                     "oth" : 6}
                            },
               "reg,mem[reg]" : 2,

               "reg,mem[var+imm]" : 6,

               "reg,mem[reg+imm]" : {'127' : 3,
                                     '128' : 6},

               "reg,mem[reg+reg*s]" : 3,
               "reg,mem[var+reg*s]": 7,

               "mem,reg" : 6,
               "mem,imm" : {'127' : 7,
                            '128' : 10},

               "mem[reg],reg" : 2,
               "mem[reg],imm" : {'127' : 3,
                                 '128' : 6},

               "mem[var+imm],reg" : 6,
               "mem[var+imm],imm" : {'127' : 7,
                                     '128' : 10},

               "mem[reg+imm],reg" : {'127' : 3,
                                     '128' : 6},
               "mem[reg+imm],imm" : {'127' : {'127' : 4,
                                              '128' : 7},
                                     '128' : {'127' : 7,
                                              '128' : 10}
                                     },


               "mem[reg+reg*s],reg" : 3,
               "mem[reg+reg*s],imm" : {'127' : 4,
                                       '128' : 7},

               "mem[var+reg*s],reg" : 7,
               "mem[var+reg*s],imm" : {'127' : 8,
                                       '128' : 11
                                       }
               },
      'xor' : {"reg,reg" : 2,
               "reg,mem" : 6,
               "reg,imm" : {'127' : 3,
                            '128' : {"eax" : 5,
                                     "oth" : 6}
                            },
               "reg,mem[reg]" : 2,

               "reg,mem[var+imm]" : 6,

               "reg,mem[reg+imm]" : {'127' : 3,
                                     '128' : 6},

               "reg,mem[reg+reg*s]" : 3,
               "reg,mem[var+reg*s]": 7,

               "mem,reg" : 6,
               "mem,imm" : {'127' : 7,
                            '128' : 10},

               "mem[reg],reg" : 2,
               "mem[reg],imm" : {'127' : 3,
                                 '128' : 6},

               "mem[var+imm],reg" : 6,
               "mem[var+imm],imm" : {'127' : 7,
                                     '128' : 10},

               "mem[reg+imm],reg" : {'127' : 3,
                                     '128' : 6},
               "mem[reg+imm],imm" : {'127' : {'127' : 4,
                                              '128' : 7},
                                     '128' : {'127' : 7,
                                              '128' : 10}
                                     },


               "mem[reg+reg*s],reg" : 3,
               "mem[reg+reg*s],imm" : {'127' : 4,
                                       '128' : 7},

               "mem[var+reg*s],reg" : 7,
               "mem[var+reg*s],imm" : {'127' : 8,
                                       '128' : 11
                                       }
               },
      'mul' : {"reg" : 2,
               "mem[reg]" : 2,
               "mem" : 6,
               "mem[reg+imm]" : {'127' : 3,
                                 '128' : 6},
               "mem[var+imm]" : 6,
               "mem[var+reg*s]" : 7,
               "mem[reg+reg*s]" : 3
               },
      'inc' : {"reg" : 1,
               "mem[reg]" : 2,
               "mem" : 6,
               "mem[reg+imm]" : {'127' : 3,
                                 '128' : 6},
               "mem[var+imm]" : 6,
               "mem[var+reg*s]" : 7,
               "mem[reg+reg*s]" : 3
               },
      'dec' : {"reg" : 1,
               "mem[reg]" : 2,
               "mem" : 6,
               "mem[reg+imm]" : {'127' : 3,
                                 '128' : 6},
               "mem[var+imm]" : 6,
               "mem[var+reg*s]" : 7,
               "mem[reg+reg*s]" : 3
               },
      'jmp' : {"fwd" : {"127" : 2,
                        "128" : 5},
               "bwd" : {"127" : 2,
                        "128" : 5},
               "reg" : 2,
               "mem[reg]" : 2,
               "mem" : 6,
               "mem[reg+imm]" : {'127' : 3,
                                 '128' : 6},
               "mem[var+imm]" : 6,
               "mem[var+reg*s]" : 7,
               "mem[reg+reg*s]" : 3,
                "imm": {"127": 5,
                        "128": 5
                        },
                "label": 5
               },
      'jnz' : {"fwd" : {"127" : 2,
                        "128" : 6},
               "bwd" : {"127" : 2,
                        "128" : 6},
                "imm": {"127": 6,
                        "128": 6
                        },
                "label": 6
               },
      'jz' : {"fwd" : {"127" : 2,
                        "128" : 6},
               "bwd" : {"127" : 2,
                        "128" : 6},
                "imm": {"127": 6,
                        "128": 6
                        },
                "label": 6
              },
      'push' : {"reg" : 1,
               "mem[reg]" : 2,
               "mem" : 6,
               "mem[reg+imm]" : {'127' : 3,
                                 '128' : 6},
               "mem[var+imm]" : 6,
               "mem[var+reg*s]" : 7,
               "mem[reg+reg*s]" : 3,
                "imm": {"127": 2,
                        "128": 5
                        },
                "label": 5
                },
      'call' : {"reg" : 2,
               "mem[reg]" : 2,
               "mem" : 6,
               "mem[reg+imm]" : {'127' : 3,
                                 '128' : 6},
               "mem[var+imm]" : 6,
               "mem[var+reg*s]" : 7,
               "mem[reg+reg*s]" : 3,
                "imm": {"127": 5,
                        "128": 5
                        },
                "label": 5
                }
      }



#dictionary of registers along with their number in modrm
registers = { "eax": "000",
              "ecx": "001",
              "edx": "010",
              "ebx": "011",
              "esp": "100",
              "ebp": "101",
              "esi": "110",
              "edi": "111"
              }

#read file
file = open("prog.asm","r")

#remove leading and trailing spaces and tabs:
temp_file = file
file = []
for i in temp_file:
    temp = i.lstrip()
    if temp == '':
        continue
    file.append(temp)


#pass 1


#all fields required in symbol table are defined below
#same are used in literal table as required
literal_table = []
literal_table.append(["Name","Section","Type","Value"])
symbol_table = []
symbol_table.append(["Name","Address","Section","Type","Value","Size","Defined/Undefined"])
symbol_name = ""
symbol_address = "0x0"
symbol_section = ""
symbol_type = ""
symbol_size = 0
symbol_def = "U"
next_symbol_address = "0x0"

i = 0

while i < len(file):
    #set default value for each new line
    current_address = ""
    symbol_address = next_symbol_address
    symbol_name = ""
    symbol_type = ""
    symbol_value = 0
    symbol_size = 0
    temp = file[i]
    if "global" in temp or "extern" in temp:
        file.remove(file[i])
        continue

    #if '.' is there in line, it means line is some section
    #find the section name
    if '.' in temp:
        symbol_section = ""
        symbol_address = "0x0"
        next_symbol_address = "0x0"
        j = 0
        while temp[j] != '.':
            j += 1
        j += 1
        symbol_section = temp[j:].strip()
        i += 1
        continue

    #if ':' in instruction, it means the line contains label for sure
    #find the label name and address and store it in symbol table
    if ':' in temp:
        symbol_type = "Label"
        symbol_value = None
        symbol_size = 0
        symbol_def = "D"
        j = 0
        while temp[j] != ':':
            symbol_name += temp[j]
            j += 1
        modified = temp[j+1:].strip()
        file[i] = modified
        temp = modified
        defined = 0

        #if label already present in symbol_table and if it is undefined make it as defined
        for k in symbol_table:
            if k[0] == symbol_name:
                k[6] = 'D'
                k[1] = symbol_address
                defined = 1

        #if label not present aleady, add label in symbol table
        if defined != 1:
            symbol = []
            symbol.append(symbol_name)
            symbol.append(symbol_address)
            symbol.append(symbol_section)
            symbol.append(symbol_type)
            symbol.append(symbol_value)
            symbol.append(symbol_size)
            symbol.append(symbol_def)
            symbol_table.append(symbol)

    #calculate the size of each instruction to calculate address of label if any
    if(is_operator(temp,op)):
        new_new_temp = temp
        operator = get_operator(temp,op)
        temp = temp.split(operator+' ',1)[1]
        op1 = ""
        op2 = ""
        new_temp = temp
        check_address = ""
        #if ',' in instruction, the instruction contains 2 operands for sure
        if ',' in temp:
            j= 0
            while temp[j] != ',':
                op1 += temp[j]
                j += 1
            temp = temp[j+1:]
            op2 = temp.strip()

        #else only 1 operand, 2nd one is none
        else:
            op1 = temp.strip()
            op2 = None
        address_getter = ""
        op1 = op1.strip()
        if op1 in registers:
            address_getter = "reg"

        elif "*" in op1:
            op1 = op1.split("[",1)[1][:-1].strip()
            if op1[:3] in registers:
                address_getter = "mem[reg+reg*s]"
            else:
                address_getter = "mem[var+reg*s]"
        elif "dword[" in op1 or "[" in op1:
            if "dword" in op1:
                op1 = op1[6:-1]
            else:
                op1 = op1[1:-1]
            if op1[:3] in registers:
                op1 = op1[3:].strip()
                if op1 != "" :
                    address_getter = "mem[reg+imm]"
                else:
                    address_getter = "mem[reg]"
            else:
                if "+" in op1:
                    address_getter = "mem[var+imm]"
                else:
                    address_getter = "mem"

        elif (operator == "push" or operator == "call" or operator == "jmp" or operator == "jnz" or operator == "jz" ) and "[" not in op1 and "imm" not in address_getter and address_getter == "":
            address_getter = ""
            check_address = ""
            for m in symbol_table:
                if m[0] == op1:
                    if operator == "jmp" or operator == "jnz" or operator == "jz":
                        if m[2] == "text":
                            if m[1] == None:
                                if m[3] == "Label":
                                    address_getter = "fwd"
                                elif m[3] == "Function":
                                    address_getter = "label"
                            else:
                                check_address = m[1]
                                address_getter = "bwd"
                        else:
                            address_getter = "label"

                    else:
                        address_getter = "label"
            if address_getter == "":
                try:
                    x = int(op1)
                    address_getter = "imm"
                except:
                    if operator == "jmp" or operator == "jnz" or operator == "jz":
                        address_getter = "fwd"
                    else:
                        address_getter = "label"





        if op2 != None:
            op2 = op2.strip()
            if op2 in registers:
                address_getter += ',reg'

            elif "*" in op2:
                op2 = op2.split("[", 1)[1][:-1].strip()
                if op2[:3] in registers:
                    address_getter += ",mem[reg+reg*s]"
                else:
                    address_getter += ",mem[var+reg*s]"

            elif "dword[" in op2 or "[" in op2:
                if "dword" in op2:
                    op2 = op2[6:-1]
                else:
                    op2 = op2[1:-1]
                if op2[:3] in registers:
                    op2 = op2[3:].strip()
                    if op2 != "":
                        address_getter += ",mem[reg+imm]"
                    else:
                        address_getter += ",mem[reg]"
                else:
                    if "+" in op2:
                        address_getter += ",mem[var+imm]"
                    else:
                        address_getter += ",mem"

            else:
                address_getter += ",imm"



        #get instruction size from dictionary "op"
        current_address = op[operator][address_getter]
        if operator == "mov" and (address_getter == "mem,reg" or address_getter == "reg,mem" or address_getter == "reg,mem[var+imm]" or address_getter == "mem[var+imm],reg"):
                if op2 == "eax" or op1 == "eax":
                    current_address = current_address["eax"]
                else:
                    current_address = current_address["oth"]
        elif (operator == "jmp" or operator == "jnz" or operator == "jz"):
            if address_getter == "bwd":
                validate_address = ""
                if abs(int(symbol_address, 0) - int(check_address, 0)) <= 127:
                    current_address = current_address["127"]
                else:
                    current_address = current_address["128"]

            elif address_getter == "fwd":
                c = i
                check = fwd(c + 1, op1)
                if check < 128:
                    current_address = current_address["127"]
                else:
                    current_address = current_address["128"]


        elif "imm" in address_getter and operator != "mov" and "imm]" not in address_getter:
            for s in symbol_table:
                if op2 != None and s[0].strip() == op2.strip():
                    current_address = 6
                    break
            if current_address == 6:
                j = 0
            elif address_getter == "imm":
                if int(op1) <= 127:
                    current_address = current_address["127"]
                else:
                    current_address = current_address["128"]
            elif int(op2) <= 127:
                current_address = current_address["127"]
            else:
                current_address = current_address["128"]
                if operator != "mov" and op1 == "eax" and address_getter == "reg,imm":
                    current_address = current_address["eax"]
                elif operator != "mov" and address_getter == "reg,imm":
                    current_address = current_address["oth"]
        elif "imm]" in address_getter:
            count = address_getter.count("imm")
            if count == 1:
                if op2 != None:
                    if "imm]," in address_getter:
                        if address_getter != "mem[var+imm],reg":
                            if int(op1) <= 127:
                                current_address = current_address["127"]
                            else:
                                current_address = current_address["128"]
                    else:
                        if address_getter != "reg,mem[var+imm]":
                            op2 = op2.split("+",1)[1].strip()
                            if int(op2) <= 127:
                                current_address = current_address["127"]
                            else:
                                current_address = current_address["128"]
                else:
                    if type(current_address) == type({}):
                        if int(op1) <= 127:
                            current_address = current_address["127"]
                        else:
                            current_address = current_address["128"]
            elif count == 2:
                if address_getter != "mem[var+imm],imm" or operator !="mov":
                    op1 = op1.split("+",1)[1].strip()
                    if "var" not in address_getter:
                        if int(op1) <= 127:
                            current_address = current_address["127"]
                        else:
                            current_address = current_address["128"]
                        if int(op2) <= 127:
                            current_address = current_address["127"]
                        else:
                            current_address = current_address["128"]
                    else:
                        if int(op2) <= 127:
                            current_address = current_address["127"]
                        else:
                            current_address = current_address["128"]

        #calculate new address by adding previous address + current instruction size
        next_symbol_address = int(symbol_address, 0) + current_address
        next_symbol_address = hex(next_symbol_address)
        #find any undefined function used or called in the program
        #if present add it to symbol table
        temp = new_temp
        if operator == 'call':
            temp = temp.strip()
            if address_getter == "label":
                check = 0
                for s in symbol_table:
                    if s[0] == temp:
                        check = 1
                        break
                if check == 0:
                    symbol_name = temp
                    symbol_address = None
                    symbol_type = "Function"
                    symbol_value = None
                    symbol_size = 0
                    symbol_def = "U"
                    symbol = []
                    symbol.append(symbol_name)
                    symbol.append(symbol_address)
                    symbol.append(symbol_section)
                    symbol.append(symbol_type)
                    symbol.append(symbol_value)
                    symbol.append(symbol_size)
                    symbol.append(symbol_def)
                    symbol_table.append(symbol)

        #if not then see if the instruction contains any immediate value
        #if yes add it to literal table
        else:
            j = 0
            while j < len(temp) and temp[j] != ",":
                j = j+1
            temp = temp[j+1:]
            temp = temp.strip()
            if temp in registers:
                i = i + 1
                continue
            elif "dword[" in temp:
                i = i + 1
                continue
            elif len(temp.strip()) > 0:
                symbol_name = None
                symbol_type = "Immediate Value"
                symbol_value = temp
                literal = []
                literal.append(symbol_name)
                literal.append(symbol_section)
                literal.append(symbol_type)
                literal.append(symbol_value)
                literal_table.append(literal)
        temp = new_new_temp


    #to check if given instruction contains operators
    #if yes skip because immediate value added already
    if(check_operator(temp,op)):
        i = i+1
        continue

    #if no then check if it contains any constants or user declared data
    else:

        #if sectio is data
        #then there are 3 cases:
        #1.byte, 2.word, 3.double
        if symbol_section == "data" :
            j = 0
            while temp[j] != ' ':
                symbol_name += temp[j]
                j += 1
            temp = temp[j+1:]

            #if byte
            if "db" in temp:
                symbol_type = "Byte"
                j = 0
                temp = temp.split("db ",1)[1]
                symbol_value = temp
                temp_list = temp.split(",")
                symbol_size = 0

                for temp in temp_list:
                    temp = temp.strip()
                    if temp == "":
                        continue
                    #check if it is array of characters
                    #if yes add the array in symbol table along with all of its attributes
                    elif "'" in temp or '"' in temp:
                        temp = temp[1:]
                        while j < len(temp) and temp[j] != '"' and temp[j] != "'":
                            symbol_size += 1
                            j += 1
                    #else it contains single byte data, so add that in symbol table
                    else:
                        symbol_size += 1
                next_symbol_address = int(symbol_address, 0) + symbol_size
                next_symbol_address = hex(next_symbol_address)
                symbol_def = "D"

            #if word, add single word or array of words into symbol table
            elif "dw" in temp:
                symbol_type = "Word"
                temp = temp.split("dw ", 1)[1]
                symbol_value = temp
                temp_list = temp.split(",")
                symbol_size = 0
                for temp in temp_list:
                    temp = temp.strip()
                    if temp == "":
                        continue
                    # check if it is array of characters
                    # if yes add the array in symbol table along with all of its attributes
                    elif "'" in temp or '"' in temp:
                        temp = temp[1:]
                        j = 0
                        while j < len(temp) and temp[j] != '"' and temp[j] != "'":
                            symbol_size += 1
                            j += 1
                        if symbol_size % 2 != 0:
                            symbol_size += 1
                    # else it contains single byte data, so add that in symbol table
                    else:
                        symbol_size += 2
                next_symbol_address = int(symbol_address, 0) + symbol_size
                next_symbol_address = hex(next_symbol_address)
                symbol_def = "D"

            #if double, add double word or array of double words into symbol table
            elif "dd" in temp:
                symbol_type = "Double"
                temp = temp.split("dd ", 1)[1]
                symbol_value = temp
                temp_list = temp.split(",")
                symbol_size = 0
                for temp in temp_list:
                    temp = temp.strip()
                    if temp == "":
                        continue
                    # check if it is array of characters
                    # if yes add the array in symbol table along with all of its attributes
                    elif "'" in temp or '"' in temp:
                        temp = temp[1:]
                        j = 0
                        while j < len(temp) and temp[j] != '"' and temp[j] != "'":
                            symbol_size += 1
                            j += 1
                        while symbol_size % 4 != 0:
                            symbol_size += 1
                    # else it contains single byte data, so add that in symbol table
                    else:
                        symbol_size += 4
                next_symbol_address = int(symbol_address, 0) + symbol_size
                next_symbol_address = hex(next_symbol_address)
                symbol_def = "D"
            literal = []
            literal.append(symbol_name)
            literal.append(symbol_section)
            literal.append(symbol_type)
            literal.append(symbol_value)
            literal_table.append(literal)

        #if in bss section
        #there are 3 cases
        #1. byte, 2. word, 3.double
        elif symbol_section == "bss" :
            j = 0
            while temp[j] != ' ':
                symbol_name += temp[j]
                j += 1
            temp = temp[j + 1:]

            #if byte
            #check size and add it in symbol table
            if "resb" in temp:
                symbol_type = "Byte"
                j = 0
                if "'" in temp or '"' in temp:
                    while j < len(temp) and temp[j] != "'" and temp[j] != '"':
                        j = j + 1
                    temp = temp[j:]
                    symbol_value = None
                    j = 1
                    symbol_size = 0
                    while j < len(temp) and temp[j] != '"' and temp[j] != "'":
                        current_address = (hex(ord(temp[j])) + current_address[2:])
                        next_symbol_address = hex(int(symbol_address, 0) + int(current_address, 0))
                        j += 1
                        symbol_size = int(current_address,0)
                else:
                    temp = temp.split("resb ", 1)[1]
                    j = 0
                    temp = temp[:-1]
                    symbol_value = None
                    symbol_size = 1 * int(temp)
                    next_symbol_address = hex(symbol_size + int(symbol_address, 0))
                symbol_def = "D"

            #if word
            elif "resw" in temp:
                symbol_type = "Word"
                temp = temp.split("resw ", 1)[1]
                j = 0
                temp = temp[:-1]
                symbol_value = None
                symbol_size = 2 * int(temp)
                next_symbol_address = hex(symbol_size + int(symbol_address, 0))

            #if double
            elif "resd" in temp:
                symbol_type = "Double"
                temp = temp.split("resd ", 1)[1]
                j = 0
                temp = temp[:-1]
                symbol_value = None
                symbol_size = 4*int(temp)
                next_symbol_address = hex(symbol_size + int(symbol_address,0))
            literal = []
            literal.append(symbol_name)
            literal.append(symbol_section)
            literal.append(symbol_type)
            literal.append(symbol_value)
            literal_table.append(literal)

        #if section is text
        #to counter labels which are declared after jmp or jnz operators
        #extract label and its attributes and add it in symbol_table
        elif symbol_section == "text" :
            if ("jmp" in temp or "jnz" in temp or "jz" in temp) and address_getter == "label":
                if "jmp" in temp:
                    temp = temp.split("jmp ", 1)[1]
                if "jnz" in temp:
                    temp = temp.split("jnz ", 1)[1]
                if "jz" in temp:
                    temp = temp.split("jz ", 1)[1]
                symbol_name = temp.strip()
                defined = 0
                for k in symbol_table:
                    if k[0] == symbol_name:
                        defined = 1
                if defined == 1:
                    i = i + 1
                    continue

                try:
                    if type(int(temp.strip())) == type(0):
                        symbol_address = None
                        symbol_type = "Immediate Value"
                        symbol_value = None
                        symbol_size = 0
                        literal = []
                        literal.append(symbol_name)
                        literal.append(symbol_section)
                        literal.append(symbol_type)
                        literal.append(symbol_value)
                        literal_table.append(literal)
                        i = i + 1
                        continue
                except:
                    symbol_address = None
                    symbol_type = "Label"
                    symbol_value = None
                    symbol_size = 0
                    symbol_def = "U"


            elif "jnz" in temp:
                temp = temp.split("jnz ", 1)[1]
                symbol_name = temp.strip()
                defined = 0
                for k in symbol_table:
                    if k[0] == symbol_name:
                        defined = 1
                if defined == 1:
                    i = i + 1
                    continue
                try:
                    if type(int(temp.strip())) == type(0):
                        symbol_address = None
                        symbol_type = "Immediate Value"
                        symbol_value = None
                        symbol_size = 0
                        literal = []
                        literal.append(symbol_name)
                        literal.append(symbol_section)
                        literal.append(symbol_type)
                        literal.append(symbol_value)
                        literal_table.append(literal)
                        i = i + 1
                        continue
                except:
                    symbol_address = None
                    symbol_type = "Label"
                    symbol_value = None
                    symbol_size = 0
                    symbol_def = "U"

            elif "jz" in temp:
                temp = temp.split("jz ", 1)[1]
                symbol_name = temp.strip()
                defined = 0
                for k in symbol_table:
                    if k[0] == symbol_name:
                        defined = 1
                if defined == 1:
                    i = i + 1
                    continue
                try:
                    if type(int(temp.strip())) == type(0):
                        symbol_address = None
                        symbol_type = "Immediate Value"
                        symbol_value = None
                        symbol_size = 0
                        literal = []
                        literal.append(symbol_name)
                        literal.append(symbol_section)
                        literal.append(symbol_type)
                        literal.append(symbol_value)
                        literal_table.append(literal)
                        i = i + 1
                        continue
                except:
                    symbol_address = None
                    symbol_type = "Label"
                    symbol_value = None
                    symbol_size = 0
                    symbol_def = "U"

            #if not jmp and jnz, skip the iteration
            else:
                i = i+1
                continue
        #if none of the above sections then skip the iteration
        #it may be empty line
        else:
            i += 1
            continue

    #adding symbol along with its attributes at each iteration into symbol table
    symbol = []
    symbol.append(symbol_name)
    symbol.append(symbol_address)
    symbol.append(symbol_section)
    symbol.append(symbol_type)
    symbol.append(symbol_value)
    symbol.append(symbol_size)
    symbol.append(symbol_def)
    symbol_table.append(symbol)


    i += 1






#function used durin 2nd pass

#makes each address of size 8
def makeaddress(value):
    while len(value) < 8:
        value = "0" + value
    return value

#makes each memory variable in address format and also in little endian format
def makememory(memory):
    memory = memory[2:]
    if len(memory) % 2 != 0:
        memory = "0" + memory
    while len(memory) != 8:
        memory = "00" + memory

    memory = bytearray.fromhex(memory)
    memory.reverse()
    memory = ''.join(format(x, '02x') for x in memory)

    memory = "[" + memory + "]"
    return memory


#find twos complement incase of backward jump
def twoscomp(value):
    max = ""
    for i in range(len(value)):
        max += "1111"
    onescomp = int(max,2) - int(value,16)
    value = hex(onescomp + 1)

    value = bytearray.fromhex(value[2:])
    vaule = value.reverse()
    value = ''.join(format(x, '02x') for x in value)
    return value


#makes value size = 1 byte
def makebvalue(value):
    value = value[2:]
    if len(value) %2 != 0:
        value = "0" + value
    return value


#makes value size = 4 bytes
def makedvalue(value):
    value = value[2:]
    if len(value) % 2 != 0:
        value = "0" + value
    while len(value) != 8:
        value = "00" + value

    return value




#makes value size = 1 byte and in little endian format
def makebytevalue(value):
    value = value[2:]
    if len(value) %2 != 0:
        value = "0" + value
    return value

#makes value size = 4 byte in little endian format
def makedoublevalue(value):
    value = value[2:]
    if len(value) % 2 != 0:
        value = "0" + value
    while len(value) != 8:
        value = "00" + value

    value = bytearray.fromhex(value)
    vaule = value.reverse()
    value = ''.join(format(x, '02x') for x in value)

    return value


#pass 2
#generate listing file

#to find middle 3 bits of modrm based on operators
mid_mod = {"add" : "000",
           "or" : "001",
           "adc" : "010",
           "sbb" : "011",
           "and" : "100",
           "sub" : "101",
           "xor" : "110",
           "cmp" : "111",
           "mov" : "000",
           "inc" : "000",
           "dec" : "001",
           "push" : "110",
           "mul" : "100",
           "call" : "010",
           "jmp" : "100"
           }


#strip all lines in file
temp_file = []
for i in file:
    temp_file.append(i.strip())
file = temp_file




i = 0


#table which will contain all fields of listing file
address_table = []


#all variables which will be used to hold temporary information of each instruction
section = ""
address = ""
next_add = "00000000"
current_address = ""
opcode = ""

#iterate over the file line by line
while i < len(file):
    temp = file[i]

    #if '.' is in line, it means its beginning of new section
    #find which section and reset address to "00000000"
    if '.' in temp:
        j = 0
        while temp[j] != '.':
            j = j + 1
        temp = temp[j+1:]
        section = temp.strip()
        address = "0x0"
        address_table.append(["","",""])
        address_table.append(["","",file[i]])

        if section == "text":
            # read file
            temp_file = open("prog.asm", "r")

            # remove leading and trailing spaces and tabs:
            temp_t_file = temp_file
            temp_file = []
            for l in temp_t_file:
                temp = l.strip()
                if temp == '':
                    continue
                temp_file.append(temp)
            l = 0
            while ".text" not in temp_file[l]:
                l = l+1
            i = i + 1
            l = l + 1

            #to add lines like
            #"global main"
            #"extern printf" which does not have address in the address_table
            while file[i] not in temp_file[l]:
                address_table.append(["","",temp_file[l]])
                l = l+1
            i = i - 1

        i = i + 1
        continue

    #if section is data
    #find hex representation of whatever variable defined
    #also find its address
    if section == "data":
        current_address = ""
        new_temp = temp
        name = ""
        j = 0
        while temp[j] != " ":
            name += temp[j]
            j += 1
        for a in symbol_table:
            if a[0] == name and a[2] == "data":
                current_address = a[1]
                break
        current_value = ""

        #for byte datatype
        if "db" in temp:
            temp = temp.split("db ", 1)[1]
            temp = temp.split(",")
            for k in temp:
                k = k.strip()
                if k == "":
                    continue
                else:
                    if "'" in k or '"' in k:
                        temp_value = ""
                        k = k[1:]
                        j = 0
                        while k[j] != "'" and k[j] != '"':
                            temp_value = temp_value + checkbyte(hex(ord(k[j]))[2:])
                            j += 1
                        current_value = current_value + temp_value
                    else:
                        current_value = current_value + checkbyte(hex(int(k))[2:])

        #for word data type
        if "dw" in temp:
            temp = temp.split("dw ", 1)[1]
            temp = temp.split(",")
            for k in temp:
                k = k.strip()
                if k == "":
                    continue
                else:
                    if "'" in k or '"' in k:
                        temp_value = ""
                        k = k[1:]
                        j = 0
                        while k[j] != "'" and k[j] != '"':
                            temp_value = temp_value + checkbyte(hex(ord(k[j]))[2:])
                            j += 1
                        temp_value = checkword(temp_value)
                        current_value = current_value + temp_value
                    else:
                        current_value = current_value + checkword(checkbyte(hex(int(k))[2:]))

        #for double data type
        if "dd" in temp:
            temp = temp.split("dd ", 1)[1]
            temp = temp.split(",")
            for k in temp:
                k = k.strip()
                if k == "":
                    continue
                else:
                    if "'" in k or '"' in k:
                        temp_value = ""
                        k = k[1:]
                        j = 0
                        while k[j] != "'" and k[j] != '"':
                            temp_value = temp_value + checkbyte(hex(ord(k[j]))[2:])
                            j += 1
                        temp_value = checkdouble(temp_value)
                        current_value = current_value + temp_value
                    else:
                        current_value = current_value + checkdouble(checkbyte(hex(int(k))[2:]))

        current_address = current_address[2:]
        current_address = makeaddress(current_address)

        address_table.append([current_address,current_value,file[i]])

    # if section is bss
    # find hex representation of whatever variable defined
    # also find its address
    if section == "bss":
        current_address = ""
        next_address = ""
        current_value = ""
        new_temp = temp
        name = ""
        j = 0
        while temp[j] != " ":
            name += temp[j]
            j += 1
        for a in range(len(symbol_table)):
            a1 = symbol_table[a]
            if a1[0] == name and a1[2] == "bss":
                current_address = a1[1]
                current_value = hex(a1[5])
                break
        current_address = makeaddress(current_address[2:])
        current_value = makeaddress(current_value[2:])
        current_value = "<res " + current_value + ">"

        address_table.append([current_address, current_value,file[i]])

    #is section is text:
    if section == "text":
        actual_address = next_add
        address_getter = ""
        operator = ""
        op1 = ""
        op2 = ""
        imm = ""
        j = 0

        #split operator operand 1 and operand 2 if any
        while temp[j] != " ":
            operator += temp[j]
            j += 1
        temp = temp[j:].strip()
        temp = temp.split(",")
        if len(temp) == 2:
            op1 = temp[0].strip()
            op2 = temp[1].strip()
        elif len(temp) == 1:
            op1 = temp[0].strip()
            op2 = None


        #find address_getter
        #address_getter tells what type of instruction it is
        #few examples are :
        #reg,reg _ mem,reg _ reg,imm _ reg,mem[var+off]....and so on
        if op1 in registers:
            address_getter = "reg"

        elif "*" in op1:
            op1 = op1.split("[", 1)[1][:-1].strip()
            if op1[:3] in registers:
                address_getter = "mem[reg+reg*s]"
            else:
                address_getter = "mem[var+reg*s]"

        elif "dword[" in op1 or "[" in op1:
            temp = op1.split("[",1)[1][:-1]
            if temp[:3] in registers:
                if temp[3:] != "":
                    temp = temp[3:].strip()
                    temp = temp[1:].strip()
                    imm = temp
                    address_getter = "mem[reg+imm]"
                else:
                    address_getter = "mem[reg]"
            else:
                if "+" in temp:
                    j = 0
                    while temp[j] != "+":
                        j = j+1
                    temp = temp[j+1:].strip()
                    address_getter = "mem[var+imm]"
                else:
                    address_getter = "mem"
        if op2 != None:
            if op2 in registers:
                address_getter += ",reg"

            elif "*" in op2:
                op2 = op2.split("[", 1)[1][:-1].strip()
                if op2[:3] in registers:
                    address_getter += ",mem[reg+reg*s]"
                else:
                    address_getter += ",mem[var+reg*s]"

            elif "dword[" in op2 or "[" in op2:
                temp = op2.split("[", 1)[1][:-1]
                if temp[:3] in registers:
                    if temp[3:] != "":
                        temp = temp[3:].strip()
                        temp = temp[1:].strip()
                        imm = temp
                        address_getter += ",mem[reg+imm]"
                    else:
                        address_getter += ",mem[reg]"
                else:
                    if "+" in temp:
                        j = 0
                        while temp[j] != "+":
                            j = j + 1
                        temp = temp[j + 1:].strip()
                        address_getter += ",mem[var+imm]"
                    else:
                        address_getter += ",mem"
            else:
                address_getter += ",imm"

        #now based on address getter find modrm
        #find sib if required
        #convert immediate value into little endian format in hex if any
        #find memory address of variables and convert them in little endian format
        check_address = ""
        mod_rm = ""
        memory = ""
        value = ""
        base = ""
        remaining = ""
        if address_getter == "reg,reg":
            mod_rm = "11" + registers[op2] + registers[op1]
            mod_rm = checkbyte(hex(int(mod_rm,2))[2:])

            remaining = mod_rm

        elif address_getter == "reg,mem":
            if operator == "mov" and op1 == "eax":
                mod_rm = ""

            else:
                mod_rm = "00" + registers[op1] + "101"
                mod_rm = checkbyte(hex(int(mod_rm,2))[2:])

            memory = ""
            var = op2.split("[",1)[1][:-1].strip()
            for s in symbol_table:
                if s[0] == var and (s[2] == "bss" or s[[2] == "data"]):
                    memory = s[1]
                    memory = makememory(memory)

            remaining = mod_rm + memory

        elif address_getter == "reg,imm":
            if operator != "mov":
                mod_rm = "11" + mid_mod[operator] + registers[op1]
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                value = ""

                for s in symbol_table:
                    if s[0] == op2:
                        value = makememory(s[1])
                        break

                if value == "":
                    if int(op2) <= 127:
                        value = hex(int(op2))
                        value = makebytevalue(value)

                    else:
                        value = hex(int(op2))
                        value = makedoublevalue(value)
                        if op1 == "eax":
                            mod_rm = ""
                remaining = mod_rm + value

            else:
                base = "b8"
                base = int(base,16) + int(registers[op1],2)
                base = hex(base)[2:]

                value = ""

                for s in symbol_table:
                    if s[0] == op2:
                        value = makememory(s[1])

                if value == "":
                    value = hex(int(op2))
                    value = makedoublevalue(value)
                remaining = base + value

        elif address_getter == "reg,mem[reg]":
            op2 = op2.split("[",1)[1][:-1].strip()
            mod_rm = "00" + registers[op1] + registers[op2]
            mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

            remaining = mod_rm

        elif address_getter == "reg,mem[reg+imm]":
            reg = op2.split("[",1)[1][:-1].strip()[:3]
            value = op2.split("+",1)[1][:-1].strip()
            if int(value) <= 127:
                mod_rm = "01" + registers[op1] + registers[reg]
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

                value = hex(int(value))
                value = makebytevalue(value)

            else:
                mod_rm = "10" + registers[op1] + registers[reg]
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

                value = hex(int(value))
                value = makedoublevalue(value)

            remaining = mod_rm + value


        elif address_getter == "reg,mem[var+imm]":
            if operator == "mov" and op1 == "eax":
                mod_rm = ""

            else:
                mod_rm = "00" + registers[op1] + "101"
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

            var = op2.split("[",1)[1][:-1].strip()
            var = var.split("+",1)[0].strip()
            value = op2.split("+", 1)[1][:-1].strip()
            for s in symbol_table:
                if s[0].strip() == var.strip():
                    var = s[1]
                    break

            memory = hex(int(var,0) + int(value))
            memory = makememory(memory)
            remaining = mod_rm + memory


        elif address_getter == "mem,reg":
            if operator == "mov" and op2 == "eax":
                mod_rm = ""

            else:
                mod_rm = "00" + registers[op2] + "101"
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

            memory = ""
            var = op1.split("[", 1)[1][:-1].strip()
            for s in symbol_table:
                if s[0] == var and (s[2] == "bss" or s[[2] == "data"]):
                    memory = s[1]
                    memory = makememory(memory)
            remaining = mod_rm + memory

        elif address_getter == "mem,imm":
            mod_rm = "00" + mid_mod[operator] + "101"
            mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

            memory = ""
            var = op1.split("[", 1)[1][:-1].strip()
            for s in symbol_table:
                if s[0] == var and (s[2] == "bss" or s[[2] == "data"]):
                    memory = s[1]
                    memory = makememory(memory)

            value = ""

            for s in symbol_table:
                if s[0] == op2:
                    value = makememory(s[1])

            if value == "":
                if int(op2) <= 127 and operator != "mov":
                    value = hex(int(op2))
                    value = makebytevalue(value)

                else:
                    value = hex(int(op2))
                    value = makedoublevalue(value)
            remaining = mod_rm + memory + value

        elif address_getter == "mem[reg],reg":
            reg = op1.split("[",1)[1].strip()[:3]
            mod_rm = "00" + registers[op2] + registers[reg]
            mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
            remaining = mod_rm

        elif address_getter == "mem[reg],imm":
            reg = op1.split("[", 1)[1].strip()[:3]
            mod_rm = "00" + mid_mod[operator] + registers[reg]
            mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
            value = ""

            for s in symbol_table:
                if s[0] == op2:
                    value = makememory(s[1])

            if value == "":
                if int(op2) <= 127 and operator != "mov":
                    value = hex(int(op2))
                    value = makebytevalue(value)

                else:
                    value = hex(int(op2))
                    value = makedoublevalue(value)
            remaining = mod_rm + value

        elif address_getter == "mem[reg+imm],reg":
            reg = op1.split("[", 1)[1][:-1].strip()[:3]
            value = op1.split("+", 1)[1][:-1].strip()
            if int(value) <= 127:
                mod_rm = "01" + registers[op2] + registers[reg]
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

                value = hex(int(value))
                value = makebytevalue(value)

            else:
                mod_rm = "10" + registers[op2] + registers[reg]
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

                value = hex(int(value))
                value = makedoublevalue(value)

            remaining = mod_rm + value

        elif address_getter == "mem[reg+imm],imm":
            reg = op1.split("[", 1)[1].strip()[:3]
            imm = op1.split("+", 1)[1][:-1].strip()
            offset = ""
            if int(imm) <= 127:
                mod_rm = "01" + mid_mod[operator] + registers[reg]
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                offset = makebytevalue(hex(int(imm)))
            elif int(imm) > 127:
                mod_rm = "10" + mid_mod[operator] + registers[reg]
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                offset = makedoublevalue(hex(int(imm)))

            value = ""

            for s in symbol_table:
                if s[0] == op2:
                    value = makememory(s[1])

            if value == "":
                if int(op2) <= 127 and operator != "mov":
                    value = hex(int(op2))
                    value = makebytevalue(value)

                else:
                    value = hex(int(op2))
                    value = makedoublevalue(value)

            remaining = mod_rm + offset + value

        elif address_getter == "mem[var+imm],reg" :
            if operator == "mov" and op2 == "eax":
                mod_rm = ""
            else:
                mod_rm = "00" + registers[op2] + "101"
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

            var = op1.split("[", 1)[1][:-1].strip()
            var = var.split("+", 1)[0].strip()
            value = op1.split("+", 1)[1][:-1].strip()
            for s in symbol_table:
                if s[0] == var:
                    var = s[1]
                    break

            memory = hex(int(var, 0) + int(value))
            memory = makememory(memory)
            remaining = mod_rm + memory


        elif address_getter == "mem[var+imm],imm" :
            mod_rm = "00" + mid_mod[operator] + "101"
            mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

            var = op1.split("[", 1)[1][:-1].strip()
            var = var.split("+", 1)[0].strip()
            value = op1.split("+", 1)[1][:-1].strip()
            for s in symbol_table:
                if s[0] == var:
                    var = s[1]
                    break

            memory = hex(int(var, 0) + int(value))
            memory = makememory(memory)

            value = ""

            for s in symbol_table:
                if s[0] == op2:
                    value = makememory(s[1])

            if value == "":
                if int(op2) <= 127 and operator != "mov":
                    value = hex(int(op2))
                    value = makebytevalue(value)

                else:
                    value = hex(int(op2))
                    value = makedoublevalue(value)
            remaining = mod_rm + memory  + value

        elif address_getter == "reg":
            if operator == "mul":
                mod_rm = "11" + "100" + registers[op1]
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

                remaining = mod_rm

            elif operator == "call" or operator == "jmp" :
                mod_rm = "11" + mid_mod[operator] + registers[op1]
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

                remaining = mod_rm

            elif operator == "inc" or operator == "dec" or operator == "push":
                if operator == "inc":
                    base = "40"
                elif operator == "dec":
                    base = "48"
                else:
                    base = "50"

                base = int(base, 16) + int(registers[op1], 2)
                base = hex(base)[2:]

                remaining = base

            else:
                remaining = ""

        elif address_getter == "mem":
            if operator == "mul" or operator == "inc" or operator == "dec" or operator == "push" or operator == "call" or operator == "jmp" :
                mod_rm = "00" + mid_mod[operator] + "101"
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

                var = op1.split("[",1)[1][:-1].strip()
                for s in symbol_table:
                    if s[0] == var:
                        var = s[1]
                        break

                memory = hex(int(var, 0))
                memory = makememory(memory)
                remaining = mod_rm + memory

            else:
                remaining = ""

        elif address_getter == "mem[reg]":
            if operator == "mul":
                reg = op1.split("[", 1)[1].strip()[:3]
                mod_rm = "00" + "100" + registers[reg]
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                remaining = mod_rm

            elif operator == "inc" or operator == "dec" or operator == "push" or operator == "call" or operator == "jmp" :
                reg = op1.split("[", 1)[1].strip()[:3]
                mod_rm = "00" + mid_mod[operator] + registers[reg]
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                remaining = mod_rm

            else:
                remaining = ""


        elif address_getter == "mem[reg+imm]":
            if operator == "mul":
                reg = op1.split("[", 1)[1].strip()[:3]
                imm = op1.split("+", 1)[1][:-1].strip()
                offset = ""
                if int(imm) <= 127:
                    mod_rm = "01" + "100" + registers[reg]
                    mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                    offset = makebytevalue(hex(int(imm)))

                elif int(imm) > 127:
                    mod_rm = "10" + "100" + registers[reg]
                    mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                    offset = makedoublevalue(hex(int(imm)))

                remaining = mod_rm + offset

            elif operator == "inc" or operator == "dec" or operator == "push" or operator == "call" or operator == "jmp" :
                reg = op1.split("[", 1)[1].strip()[:3]
                imm = op1.split("+", 1)[1][:-1].strip()
                offset = ""
                if int(imm) <= 127:
                    mod_rm = "01" + mid_mod[operator] + registers[reg]
                    mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                    offset = makebytevalue(hex(int(imm)))

                elif int(imm) > 127:
                    mod_rm = "10" + mid_mod[operator] + registers[reg]
                    mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                    offset = makedoublevalue(hex(int(imm)))

                remaining = mod_rm + offset



        elif address_getter == "mem[var+imm]":
            if operator == "mul":
                mod_rm = "00" + "100" + "101"
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                var = op1.split("[", 1)[1][:-1].strip()
                var = var.split("+", 1)[0].strip()
                value = op1.split("+", 1)[1][:-1].strip()
                for s in symbol_table:
                    if s[0] == var:
                        var = s[1]
                        break

                memory = hex(int(var, 0) + int(value))
                memory = makememory(memory)

                remaining = mod_rm + memory


            elif operator == "inc" or operator == "dec" or operator == "push" or operator == "call" or operator == "jmp" :
                mod_rm = "00" + mid_mod[operator] + "101"
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                var = op1.split("[", 1)[1][:-1].strip()
                var = var.split("+", 1)[0].strip()
                value = op1.split("+", 1)[1][:-1].strip()
                for s in symbol_table:
                    if s[0] == var:
                        var = s[1]
                        break

                memory = hex(int(var, 0) + int(value))
                memory = makememory(memory)

                remaining = mod_rm + memory

            else:
                remaining = ""


        elif address_getter == "mem[reg+reg*s]":
            if operator == "mul":
                mod_rm = "00" + "100" + "100"
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

                base = op1[:3]
                index = op1.split("+", 1)[1].strip()[:3]
                scale = op1.split("*", 1)[1].strip()
                if int(scale) == 2:
                    scale = "01"
                elif int(scale) == 4:
                    scale = "10"
                elif int(scale) == 8:
                    scale = "11"
                sib = scale + registers[index] + registers[base]
                sib = checkbyte(hex(int(sib, 2))[2:])

                remaining = mod_rm + sib

            elif operator == "inc" or operator == "dec" or operator == "push" or operator == "call" or operator == "jmp" :
                mod_rm = "00" + mid_mod[operator] + "100"
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

                base = op1[:3]
                index = op1.split("+", 1)[1].strip()[:3]
                scale = op1.split("*", 1)[1].strip()
                if int(scale) == 2:
                    scale = "01"
                elif int(scale) == 4:
                    scale = "10"
                elif int(scale) == 8:
                    scale = "11"
                sib = scale + registers[index] + registers[base]
                sib = checkbyte(hex(int(sib, 2))[2:])

                remaining = mod_rm + sib

            else:
                remaining = ""


        elif address_getter == "mem[var+reg*s]":
            if operator == "mul":
                index = op1.split("+", 1)[1].strip()[:3]
                scale = op1.split("*", 1)[1].strip()
                sib = ""
                if int(scale) == 2:
                    mod_rm = "10" + "100" + "100"
                    mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                    scale = "00"
                    sib = scale + registers[index] + registers[index]
                elif int(scale) == 4:
                    mod_rm = "00" + "100" + "100"
                    mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                    scale = "10"
                    sib = scale + registers[index] + "101"
                elif int(scale) == 8:
                    mod_rm = "00" + "100" + "100"
                    mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                    scale = "11"
                    sib = scale + registers[index] + "101"

                sib = checkbyte(hex(int(sib, 2))[2:])

                var = op1.split("+", 1)[0].strip()
                for s in symbol_table:
                    if s[0] == var:
                        var = s[1]
                        break

                memory = hex(int(var, 0))
                memory = makememory(memory)

                remaining = mod_rm + sib + memory

            elif operator == "inc" or operator == "dec" or operator == "push" or operator == "call" or operator == "jmp" :
                index = op1.split("+", 1)[1].strip()[:3]
                scale = op1.split("*", 1)[1].strip()
                sib = ""
                if int(scale) == 2:
                    mod_rm = "10" + mid_mod[operator] + "100"
                    mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                    scale = "00"
                    sib = scale + registers[index] + registers[index]
                elif int(scale) == 4:
                    mod_rm = "00" + mid_mod[operator] + "100"
                    mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                    scale = "10"
                    sib = scale + registers[index] + "101"
                elif int(scale) == 8:
                    mod_rm = "00" + mid_mod[operator] + "100"
                    mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                    scale = "11"
                    sib = scale + registers[index] + "101"

                sib = checkbyte(hex(int(sib, 2))[2:])

                var = op1.split("+", 1)[0].strip()
                for s in symbol_table:
                    if s[0] == var:
                        var = s[1]
                        break

                memory = hex(int(var, 0))
                memory = makememory(memory)

                remaining = mod_rm + sib + memory

            else:
                remaining = ""

        elif address_getter == "mem[reg+reg*s],reg":
            mod_rm = "00" + registers[op2] + "100"
            mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
            base = op1[:3]
            index = op1.split("+",1)[1].strip()[:3]
            scale = op1.split("*",1)[1].strip()
            if int(scale) == 2:
                scale = "01"
            elif int(scale) == 4:
                scale = "10"
            elif int(scale) == 8:
                scale = "11"
            sib = scale + registers[index] + registers[base]
            sib = checkbyte(hex(int(sib, 2))[2:])

            remaining = mod_rm + sib



        elif address_getter ==  "mem[reg+reg*s],imm":
            mod_rm = "00" + mid_mod[operator] + "100"
            mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

            base = op1[:3]
            index = op1.split("+", 1)[1].strip()[:3]
            scale = op1.split("*", 1)[1].strip()
            if int(scale) == 2:
                scale = "01"
            elif int(scale) == 4:
                scale = "10"
            elif int(scale) == 8:
                scale = "11"
            sib = scale + registers[index] + registers[base]
            sib = checkbyte(hex(int(sib, 2))[2:])

            value = ""

            for s in symbol_table:
                if s[0] == op2:
                    value = makememory(s[1])

            if value == "":
                if int(op2) <= 127 and operator != "mov":
                    value = hex(int(op2))
                    value = makebytevalue(value)

                else:
                    value = hex(int(op2))
                    value = makedoublevalue(value)

            remaining = mod_rm + sib + value



        elif address_getter == "reg,mem[reg+reg*s]" :
            mod_rm = "00" + registers[op1] + "100"
            mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

            base = op2[:3]
            index = op2.split("+", 1)[1].strip()[:3]
            scale = op2.split("*", 1)[1].strip()
            if int(scale) == 2:
                scale = "01"
            elif int(scale) == 4:
                scale = "10"
            elif int(scale) == 8:
                scale = "11"
            sib = scale + registers[index] + registers[base]
            sib = checkbyte(hex(int(sib, 2))[2:])

            remaining = mod_rm + sib

        elif address_getter == "mem[var+reg*s],reg" :
            mod_rm = "00" + registers[op2] + "100"
            mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])

            index = op1.split("+", 1)[1].strip()[:3]
            scale = op1.split("*", 1)[1].strip()
            if int(scale) == 2:
                scale = "01"
            elif int(scale) == 4:
                scale = "10"
            elif int(scale) == 8:
                scale = "11"
            sib = scale + registers[index] + "101"
            sib = checkbyte(hex(int(sib, 2))[2:])
            var = op1.split("+", 1)[0].strip()
            for s in symbol_table:
                if s[0] == var:
                    var = s[1]
                    break

            memory = hex(int(var, 0))
            memory = makememory(memory)

            remaining = mod_rm + sib + memory



        elif address_getter == "mem[var+reg*s],imm" :

            index = op1.split("+", 1)[1].strip()[:3]
            scale = op1.split("*", 1)[1].strip()
            sib = ""
            if int(scale) == 2:
                mod_rm = "10" + mid_mod[operator] + "100"
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                scale = "00"
                sib = scale + registers[index] + registers[index]
            elif int(scale) == 4:
                mod_rm = "00" + mid_mod[operator] + "100"
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                scale = "10"
                sib = scale + registers[index] + "101"
            elif int(scale) == 8:
                mod_rm = "00" + mid_mod[operator] + "100"
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                scale = "11"
                sib = scale + registers[index] + "101"

            sib = checkbyte(hex(int(sib, 2))[2:])

            var = op1.split("+", 1)[0].strip()
            for s in symbol_table:
                if s[0] == var:
                    var = s[1]
                    break

            memory = hex(int(var, 0))
            memory = makememory(memory)

            value = ""

            for s in symbol_table:
                if s[0] == op2:
                    value = makememory(s[1])

            if value == "":
                if int(op2) <= 127 and operator != "mov":
                    value = hex(int(op2))
                    value = makebytevalue(value)

                else:
                    value = hex(int(op2))
                    value = makedoublevalue(value)

            remaining = mod_rm + sib + memory + value


        elif address_getter == "reg,mem[var+reg*s]" :

            sib = ""
            index = op2.split("+", 1)[1].strip()[:3]
            scale = op2.split("*", 1)[1].strip()
            if int(scale) == 2:
                mod_rm = "10" + registers[op1] + "100"
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                scale = "00"
                sib = scale + registers[index] + registers[index]

            elif int(scale) == 4:
                mod_rm = "00" + registers[op1] + "100"
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                scale = "10"
                sib = scale + registers[index] + "101"

            elif int(scale) == 8:
                mod_rm = "00" + registers[op1] + "100"
                mod_rm = checkbyte(hex(int(mod_rm, 2))[2:])
                scale = "11"
                sib = scale + registers[index] + "101"

            sib = checkbyte(hex(int(sib, 2))[2:])

            var = op2.split("+", 1)[0].strip()
            for s in symbol_table:
                if s[0] == var:
                    var = s[1]
                    break

            memory = hex(int(var, 0))
            memory = makememory(memory)

            remaining = mod_rm + sib + memory


        elif (operator == "push" or operator == "call" or operator == "jmp" or operator == "jnz" or operator == "jz") and "[" not in op1 and "imm" not in address_getter and address_getter == "":
            address_getter = ""
            check_address = ""
            for m in symbol_table:
                if m[0] == op1:
                    if operator == "jmp" or operator == "jnz" or operator == "jz":
                        if m[2] == "text":
                            if m[1] == None:
                                if m[3] == "Label":
                                    address_getter = "label"
                            else:
                                check_address = m[1]
                                if int(actual_address,16) <= int(check_address,16):
                                    address_getter = "fwd"
                                else:
                                    address_getter = "bwd"
                        else:
                            address_getter = "label"

                    else:
                        address_getter = "label"


            if address_getter == "":
                try:
                    x = int(op1)
                    address_getter = "imm"
                except:
                    if operator == "jmp" or operator == "jnz" or operator == "jz":
                        address_getter = "fwd"
                    else:
                        address_getter = "label"

            if address_getter == "label":
                var = op1
                check = 0
                for s in symbol_table:
                    if s[0] == var:
                        check = 1
                        var = s[1]
                        break
                if check == 1 and var != None:
                    memory = hex(int(var, 0))
                    memory = makememory(memory)
                    if operator == "call"  or operator == "jmp" or operator == "jnz" or operator == "jz" :
                        memory = "(" + memory[1:-1] + ")"
                else:
                    memory = "(00000000)"

                remaining = memory

            elif address_getter == "imm":
                if operator == "call"  or operator == "jmp" or operator == "jnz" or operator == "jz" :
                    value = "(" + makedoublevalue(hex(int(op1))) + ")"

                else:
                    if int(op1) <= 127:
                        value = hex(int(op1))
                        value = makebytevalue(value)

                    else:
                        value = hex(int(op1))
                        value = makedoublevalue(value)

                remaining = value

            elif address_getter == "fwd":
                validate_address = abs(int(actual_address, 16) - int(check_address, 16))

                if validate_address <= 127:
                    remaining = makebytevalue(hex(validate_address-2))
                else:
                    remaining = makedoublevalue(hex(validate_address-5))


            elif address_getter == "bwd":
                validate_address = abs(int(actual_address, 16) - int(check_address, 16))
                if validate_address <= 127:
                    remaining = makebvalue(hex(validate_address + 2))
                else:
                    remaining = makedvalue(hex(validate_address + 2))

                remaining = twoscomp(remaining)

        #till here all the code was to find address getter and based on the address getter calculate mod_rm,value,memory and sib if any

        #find the instruction size using operator and address getter usinf the same dictionary which was used to generate symbol table
        current_address = op[operator][address_getter]
        if operator == "mov" and (
                address_getter == "mem,reg" or address_getter == "reg,mem" or address_getter == "reg,mem[var+imm]" or address_getter == "mem[var+imm],reg"):
            if op2 == "eax" or op1 == "eax":
                current_address = current_address["eax"]
            else:
                current_address = current_address["oth"]
        elif (operator == "jmp" or operator == "jnz" or operator == "jz"):
            if address_getter == "bwd":
                if abs(int(actual_address, 16) - int(check_address, 0)) <= 127:
                    current_address = current_address["127"]
                else:
                    current_address = current_address["128"]

            elif address_getter == "fwd":

                if abs(int(actual_address, 16) - int(check_address, 0)) <= 127:
                    current_address = current_address["127"]
                else:
                    current_address = current_address["128"]



        elif "imm" in address_getter and operator != "mov" and "imm]" not in address_getter:
            for s in symbol_table:
                if op2 != None and s[0].strip() == op2.strip():
                    current_address = 6
                    break
            if current_address == 6:
                j = 0
            elif address_getter == "imm":
                if int(op1) <= 127:
                    current_address = current_address["127"]
                else:
                    current_address = current_address["128"]
            elif int(op2) <= 127:
                current_address = current_address["127"]
            else:
                current_address = current_address["128"]
                if operator != "mov" and op1 == "eax" and address_getter == "reg,imm":
                    current_address = current_address["eax"]
                elif operator != "mov" and address_getter == "reg,imm":
                    current_address = current_address["oth"]
        elif "imm]" in address_getter:
            count = address_getter.count("imm")
            if count == 1:
                if op2 != None:
                    if "imm]," in address_getter:
                        if address_getter != "mem[var+imm],reg":
                            op1 = op1.split("+", 1)[1][:-1].strip()
                            if int(op1) <= 127:
                                current_address = current_address["127"]
                            else:
                                current_address = current_address["128"]
                    else:
                        if address_getter != "reg,mem[var+imm]":
                            op2 = op2.split("+", 1)[1][:-1].strip()
                            if int(op2) <= 127:
                                current_address = current_address["127"]
                            else:
                                current_address = current_address["128"]
                else:
                    if type(current_address) == type({}):
                        if "+" in op1:
                            op1 = op1.split("+", 1)[1][:-1].strip()
                        if int(op1) <= 127:
                            current_address = current_address["127"]
                        else:
                            current_address = current_address["128"]
            elif count == 2:
                if address_getter != "mem[var+imm],imm" or operator != "mov":
                    op1 = op1.split("+", 1)[1][:-1].strip()
                    if "var" not in address_getter:
                        if int(op1) <= 127:
                            current_address = current_address["127"]
                        else:
                            current_address = current_address["128"]
                        if int(op2) <= 127:
                            current_address = current_address["127"]
                        else:
                            current_address = current_address["128"]
                    else:
                        if int(op2) <= 127:
                            current_address = current_address["127"]
                        else:
                            current_address = current_address["128"]

        # calculate new address by adding previous address + current instruction size

        next_add = int(actual_address, 16) + current_address
        next_add = hex(next_add)
        next_add = makeaddress(next_add[2:])

        for s in symbol_table:
            if s[3] == "Label":
                if s[1] != None and makeaddress(s[1][2:]) == actual_address:
                    file[i] = s[0] + " : " + file[i]
                    break

        #this dictionary contains operators and their opcodes
        #it can be accessed by same operator and address getter
        opcode_table = {'mov': {"reg,reg": "89",
                                "reg,mem": {"eax" : "a1",
                                           "oth" : "8b"},
                                "reg,imm": "",
                                "reg,mem[reg]": "8b",
                                "reg,mem[var+imm]": {'eax': "a1",
                                                    'oth': "8b"},
                                "reg,mem[reg+imm]": "8b",
                                "reg,mem[reg+reg*s]": "8b",
                                "reg,mem[var+reg*s]": "8b",
                                "mem,reg": {'eax': "a3",
                                            'oth': "89"},
                                "mem,imm": "c7",
                                "mem[reg],reg": "89",
                                "mem[reg],imm": "c7",
                                "mem[var+imm],reg": {"eax": "a3",
                                                     "oth": "89"},
                                "mem[var+imm],imm": "c7",
                                "mem[reg+imm],reg": "89",
                                "mem[reg+imm],imm": "c7",
                                "mem[reg+reg*s],reg": "89",
                                "mem[reg+reg*s],imm": "89",
                                "mem[var+reg*s],reg": "c7",
                                "mem[var+reg*s],imm": "c7"
                                },
                        'add': {"reg,reg": "01",
                                "reg,mem": "03",
                                "reg,imm": {'127': "83",
                                            '128': {"eax": "05",
                                                    "oth": "81"}
                                            },
                                "reg,mem[reg]": "03",

                                "reg,mem[var+imm]": "03",

                                "reg,mem[reg+imm]": "03",

                                "reg,mem[reg+reg*s]": "03",
                                "reg,mem[var+reg*s]": "03",

                                "mem,reg": "01",
                                "mem,imm": {'127': "83",
                                            '128': "81"},

                                "mem[reg],reg": "01",
                                "mem[reg],imm": {'127': "83",
                                                 '128': "81"},

                                "mem[var+imm],reg": "01",
                                "mem[var+imm],imm": {'127': "83",
                                                     '128': "81"},

                                "mem[reg+imm],reg": "01",
                                "mem[reg+imm],imm": {'127': "83",
                                                     '128': "81"
                                                     },

                                "mem[reg+reg*s],reg": "01",
                                "mem[reg+reg*s],imm": {'127': "83",
                                                       '128': "81"},

                                "mem[var+reg*s],reg": "01",
                                "mem[var+reg*s],imm": {'127': "83",
                                                       '128': "81"
                                                       }
                                },
                        'sub': {"reg,reg": "29",
                                "reg,mem": "2b",
                                "reg,imm": {'127': "83",
                                            '128': {"eax": "2d",
                                                    "oth": "81"}
                                            },
                                "reg,mem[reg]": "2b",

                                "reg,mem[var+imm]": "2b",

                                "reg,mem[reg+imm]": "2b",

                                "reg,mem[reg+reg*s]": "2b",
                                "reg,mem[var+reg*s]": "2b",

                                "mem,reg": "29",
                                "mem,imm": {'127': "83",
                                            '128': "81"},

                                "mem[reg],reg": "29",
                                "mem[reg],imm": {'127': "83",
                                                 '128': "81"},

                                "mem[var+imm],reg": "29",
                                "mem[var+imm],imm": {'127': "83",
                                                     '128': "81"},

                                "mem[reg+imm],reg": "29",
                                "mem[reg+imm],imm": {'127': "83",
                                                     '128': "81"
                                                     },

                                "mem[reg+reg*s],reg": "29",
                                "mem[reg+reg*s],imm": {'127': "83",
                                                       '128': "81"},

                                "mem[var+reg*s],reg": "29",
                                "mem[var+reg*s],imm": {'127': "83",
                                                       '128': "81"
                                                       }
                                },
                        'or': {"reg,reg": "09",
                                "reg,mem": "0b",
                                "reg,imm": {'127': "83",
                                            '128': {"eax": "0d",
                                                    "oth": "81"}
                                            },
                                "reg,mem[reg]": "0b",

                                "reg,mem[var+imm]": "0b",

                                "reg,mem[reg+imm]": "0b",

                                "reg,mem[reg+reg*s]": "0b",
                                "reg,mem[var+reg*s]": "0b",

                                "mem,reg": "09",
                                "mem,imm": {'127': "83",
                                            '128': "81"},

                                "mem[reg],reg": "09",
                                "mem[reg],imm": {'127': "83",
                                                 '128': "81"},

                                "mem[var+imm],reg": "09",
                                "mem[var+imm],imm": {'127': "83",
                                                     '128': "81"},

                                "mem[reg+imm],reg": "09",
                                "mem[reg+imm],imm": {'127': "83",
                                                     '128': "81"
                                                     },

                                "mem[reg+reg*s],reg": "09",
                                "mem[reg+reg*s],imm": {'127': "83",
                                                       '128': "81"},

                                "mem[var+reg*s],reg": "09",
                                "mem[var+reg*s],imm": {'127': "83",
                                                       '128': "81"
                                                       }
                                },
                        'xor': {"reg,reg": "31",
                                "reg,mem": "33",
                                "reg,imm": {'127': "83",
                                            '128': {"eax": "35",
                                                    "oth": "81"}
                                            },
                                "reg,mem[reg]": "33",

                                "reg,mem[var+imm]": "33",

                                "reg,mem[reg+imm]": "33",

                                "reg,mem[reg+reg*s]": "33",
                                "reg,mem[var+reg*s]": "33",

                                "mem,reg": "31",
                                "mem,imm": {'127': "83",
                                            '128': "81"},

                                "mem[reg],reg": "31",
                                "mem[reg],imm": {'127': "83",
                                                 '128': "81"},

                                "mem[var+imm],reg": "31",
                                "mem[var+imm],imm": {'127': "83",
                                                     '128': "81"},

                                "mem[reg+imm],reg": "31",
                                "mem[reg+imm],imm": {'127': "83",
                                                     '128': "81"
                                                     },

                                "mem[reg+reg*s],reg": "31",
                                "mem[reg+reg*s],imm": {'127': "83",
                                                       '128': "81"},

                                "mem[var+reg*s],reg": "31",
                                "mem[var+reg*s],imm": {'127': "83",
                                                       '128': "81"
                                                       }
                                },
                        'cmp': {"reg,reg": "39",
                                "reg,mem": "3b",
                                "reg,imm": {'127': "83",
                                            '128': {"eax": "3d",
                                                    "oth": "81"}
                                            },
                                "reg,mem[reg]": "3b",

                                "reg,mem[var+imm]": "3b",

                                "reg,mem[reg+imm]": "3b",

                                "reg,mem[reg+reg*s]": "3b",
                                "reg,mem[var+reg*s]": "3b",

                                "mem,reg": "39",
                                "mem,imm": {'127': "83",
                                            '128': "81"},

                                "mem[reg],reg": "39",
                                "mem[reg],imm": {'127': "83",
                                                 '128': "81"},

                                "mem[var+imm],reg": "39",
                                "mem[var+imm],imm": {'127': "83",
                                                     '128': "81"},

                                "mem[reg+imm],reg": "39",
                                "mem[reg+imm],imm": {'127': "83",
                                                     '128': "81"
                                                     },

                                "mem[reg+reg*s],reg": "39",
                                "mem[reg+reg*s],imm": {'127': "83",
                                                       '128': "81"},

                                "mem[var+reg*s],reg": "39",
                                "mem[var+reg*s],imm": {'127': "83",
                                                       '128': "81"
                                                       }
                                },
                        'mul' : {"reg" : "f7",
                                 "mem[reg]" : "f7",
                                 "mem" : "f7",
                                 "mem[reg+imm]" : {'127' : "f7",
                                                   '128' : "f7"},
                                 "mem[var+imm]" : "f7",
                                 "mem[reg+reg*s]" : "f7",
                                 "mem[var+reg*s]" : "f7"
                                 },
                        'inc' : {"reg" : "",
                                 "mem[reg]" : "ff",
                                 "mem" : "ff",
                                 "mem[reg+imm]" : {'127' : "ff",
                                                   '128' : "ff"},
                                 "mem[var+imm]" : "ff",
                                 "mem[var+reg*s]" : "ff",
                                 "mem[reg+reg*s]" : "ff"
                                 },
                        'dec' : {"reg" : "",
                                 "mem[reg]" : "ff",
                                 "mem" : "ff",
                                 "mem[reg+imm]" : {'127' : "ff",
                                                   '128' : "ff"},
                                 "mem[var+imm]" : "ff",
                                 "mem[var+reg*s]" : "ff",
                                 "mem[reg+reg*s]" : "ff"
                                 },
                        'jmp' : {"fwd" : {"127" : "eb",
                                          "128" : "e9"},
                                 "bwd" : {"127" : "eb",
                                          "128" : "e9"},
                                 "reg" : "ff",
                                 "mem[reg]" : "ff",
                                 "mem" : "ff",
                                 "mem[reg+imm]" : {'127' : "ff",
                                                   '128' : "ff"},
                                 "mem[var+imm]" : "ff",
                                 "mem[var+reg*s]" : "ff",
                                 "mem[reg+reg*s]" : "ff",
                                 "imm": {"127": "e9",
                                         "128": "e9"
                                         },
                                 "label": "e9"
                                 },
                        'jnz' : {"fwd" : {"127" : "75",
                                          "128" : "0f85"},
                                 "bwd" : {"127" : "75",
                                          "128" : "0f85"},
                                 "label": "0f85",
                                 "imm": {"127": "0f85",
                                         "128": "0f85"
                                         }
                                 },
                        'jz' : {"fwd" : {"127" : "74",
                                         "128" : "0f84"},
                                "bwd" : {"127" : "74",
                                         "128" : "0f84"},
                                "imm": {"127": "0f84",
                                        "128": "0f84"
                                        },
                                "label": "0f84"
                                },
                        'push' : {"reg" : "",
                                  "mem[reg]" : "ff",
                                  "mem" : "ff",
                                  "mem[reg+imm]" : {'127' : "ff",
                                                    '128' : "ff"},
                                  "mem[var+imm]" : "ff",
                                  "mem[var+reg*s]" : "ff",
                                  "mem[reg+reg*s]" : "ff",
                                  "imm" : {"127" : "6a",
                                           "128" : "68"
                                           },
                                  "label" : "68"
                                  },
                        'call' : {"reg" : "ff",
                                  "mem[reg]" : "ff",
                                  "mem" : "ff",
                                  "mem[reg+imm]" : {'127' : "ff",
                                                    '128' : "ff"},

                                  "mem[var+imm]" : "ff",
                                  "mem[var+reg*s]" : "ff",
                                  "mem[reg+reg*s]" : "ff",
                                  "imm": {"127": "e8",
                                          "128": "e8"
                                          },
                                  "label": "e8"
                                  }
                        }


        #find opcode using operator and address getter
        opcode = opcode_table[operator][address_getter]

        if type(opcode) == type({}):
            if operator == "mov":
                if "eax" in file[i]:
                    opcode = opcode["eax"]
                else:
                    opcode = opcode["oth"]

            elif address_getter == "mem[reg+imm]" and operator == "mul":
                if int(op1) <= 127:
                    opcode = opcode["127"]
                else:
                    opcode = opcode["128"]

            elif operator == "inc" or operator == "dec" or operator == "push" or operator == "call" or ((operator == "jmp" or operator == "jnz" or operator == "jz") and (address_getter != "fwd" and address_getter != "bwd")):
                if int(op1) <= 127:
                    opcode = opcode["127"]
                else:
                    opcode = opcode["128"]


            elif (operator == "jmp" or operator == "jnz" or operator == "jz"):
                if address_getter == "bwd":
                    validate_address = abs(int(actual_address, 16) - int(check_address, 16))
                    if validate_address <= 127:
                        opcode = opcode["127"]
                    else:
                        opcode = opcode["128"]

                elif address_getter == "fwd":
                    validate_address = abs(int(actual_address, 16) - int(check_address, 16))
                    if validate_address <= 127:
                        opcode = opcode["127"]
                    else:
                        opcode = opcode["128"]



            else:
                if ",imm" in address_getter:
                    if int(op2) <= 127:
                        opcode = opcode["127"]
                    else:
                        opcode = opcode["128"]
                        if address_getter == "reg,imm":
                            if "eax" in file[i]:
                                opcode = opcode["eax"]
                            else:
                                opcode = opcode["oth"]


        #join opcode with modrm,sib,immediate value and memory if any
        #remaining contains modrm,memory,value or sib if any
        opcode = opcode + remaining

        #append it to the address table
        address_table.append([actual_address, opcode, file[i]])

    i = i+1


for i in address_table:
    i[0] = i[0].upper()
    i[1] = i[1].upper()
    if "<RES" in i[1]:
        i[1] = i[1].replace("<RES","<res")


#print the table using tabulate function from tabulate module
print("\t\t\t\t\t\t##### LISTING FILE #####")
print(tabulate(address_table))
output = open("output.txt","w")
output.write(tabulate(address_table))



