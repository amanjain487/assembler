#tabulate module to print symbol table and literal table in table format
from tabulate import tabulate


#function to check whether passed argument 'temp' contains operator from 'op
#returns true if operator else false
def is_operator(temp,op):
    operator = ""
    j = 0
    while j < len(temp) and temp[j] != ' ':
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
    while j < len(temp) and temp[j] != ' ':
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
      'push' : ["reg",
               "mem[reg]",
               "mem",
               "mem[reg+imm]",
               "mem[var+imm]",
               "mem[var+reg*s]",
               "mem[reg+reg*s]",
                "imm",
                "label"],
      'call' : ["reg",
               "mem[reg]",
               "mem",
               "mem[reg+imm]",
               "mem[var+imm]",
               "mem[var+reg*s]",
               "mem[reg+reg*s]",
                "imm",
                "label"]
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


error_table = {"data" : {"repeat_variable" : "Variable Inconsistently Redefined",
                         "data_type" : "Incorrect Data Type",
                         "no_value" : "No operand for Data Declaration",
                         "wrong_section" : "uninitialized space declared in non - BSS section"},



               "bss" : {"repeat_varible" : "Variable Inconsistently Redefined",
                        "data_type" : "Incorrect Data Type",
                        "no_value" : "Invalid combination of opcode and operands",
                        "wrong_section" : "attempt to initialize memory in BSS Section"},


               "text" : {"only_label" : "label alone without colon might be a error",
                         "no_parameter" : "macro_exists, but not taking 0 parameters",
                         "label" : "Undefined Symbol",
                         "operand" : "invalid combination of opcode and operands",
                         "operator_missing" : "parser: instruction expected",
                         "imm as 1st operand" : "invalid combination of opcode and operands",
                         "label_repeat" : "Label inconsistently redefined",
                         "incorrect_start" : "label or instruction expected at start of line"}
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

symbol_table = []
errors = []
symbol_name = ""
symbol_section = ""
symbol_def = "U"

i = 0

while i < len(file):
    #set default value for each new line
    symbol_name = ""
    temp = file[i]
    error = ""
    if "global" in temp or "extern" in temp:
        l = temp.split()
        for a in l:
            if a.strip() == "":
                l.remove(a)
        if len(l) <= 1:
            error = "no_parameter"
            errors.append([file[i],error_table[symbol_section][error]])
        file.remove(file[i])
        continue

    l = temp.split()
    for a in l:
        if a.strip() == "":
            l.remove(a)
    if len(l) <= 1 and (temp.strip() in symbol_table or temp.strip() not in op) and symbol_section == "text":
        error = "only_label"
        errors.append([file[i], error_table[symbol_section][error]])
        i += 1
        continue

    #if '.' is there in line, it means line is some section
    #find the section name
    if '.' in temp:
        symbol_section = ""
        j = 0
        while temp[j] != '.':
            j += 1
        j += 1
        symbol_section = temp[j:].strip()
        i += 1
        continue


    if symbol_section == "data":
        if "resd " in temp or "resb " in temp or "resw " in temp or "resq " in temp:
            error = "wrong_section"
            errors.append([file[i],error_table["data"][error]])
            i = i+1
            continue


    if symbol_section == "bss":
        if "dd " in temp or "db " in temp or "dw " in temp or "dq " in temp:
            error = "wrong_section"
            errors.append([file[i],error_table["bss"][error]])
            i = i+1
            continue


    #if ':' in instruction, it means the line contains label for sure
    #find the label name and address and store it in symbol table
    if ':' in temp:
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
        e = 0
        for k in symbol_table:
            if k[0] == symbol_name:
                if k[6] == 'U':
                    k[6] = 'D'
                    defined = 1
                else:
                    error = "label_repeat"
                    errors.append([symbol_name + ":" + file[i], error_table["text"][error]])
                    e = 1
                    break

        if e == 1:
            i = i + 1
            continue

        #if label not present aleady, add label in symbol table
        if defined != 1:
            symbol = []
            symbol.append(symbol_name)
            symbol.append(symbol_section)
            symbol.append(symbol_def)
            symbol_table.append(symbol)

    if temp.strip() == "":
        i = i+1
        continue

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
                    symbol_def = "U"
                    symbol = []
                    symbol.append(symbol_name)
                    symbol.append(symbol_section)
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
        temp = new_new_temp


        new_size = op[operator]
        try:
            if address_getter in new_size:
                new_size = 0
        except:
            error = "operator_missing"
            errors.append([file[i], error_table["text"][error]])
            i = i + 1
            continue


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
        if symbol_section == "data":
            j = 0
            while j < len(temp) and temp[j] != ' ':
                symbol_name += temp[j]
                j += 1
            temp = temp[j+1:]

            if symbol_name[0].isdigit():
                error = "incorrect_start"
                errors.append([file[i], error_table["text"][error]])
                i = i+1
                continue

            e = 0
            for n in symbol_table:
                if n[0] == symbol_name and symbol_name.strip() != "":
                    error = "repeat_variable"
                    errors.append([file[i], error_table["data"][error]])
                    e = 1
                    break
            if e == 1:
                i = i + 1
                continue
            l = temp.split()
            for n in l:
                if n.strip() == "":
                    l.remove(n)


            if len(l) ==  1:

                if ("db" in temp or "dd" in temp or "dw" in temp) and ("db" in l or "dd" in l or "dw" in l):
                    error = "no_value"
                    errors.append([file[i], error_table["data"][error]])
                    symbol_table.append([symbol_name])

                elif symbol_name == "dd" or symbol_name == "db" or symbol_name == "dw":
                    z = 1

                else:
                    error = "operator_missing"
                    errors.append([file[i], error_table["text"][error]])
                i = i + 1
                continue

            elif len(l) == 0:
                symbol_name = symbol_name.strip()
                if symbol_name == "dd" or symbol_name == "db" or symbol_name == "dw":
                    error = "no_value"
                    errors.append([file[i], error_table["data"][error]])

                else:
                    error = "only_label"
                    errors.append([file[i], error_table["text"][error]])
                i = i + 1
                continue


            #if byte
            if "db" in temp:
                j = 0
                temp = temp.split("db ",1)[1]
                temp_list = temp.split(",")
                symbol_def = "D"

            #if word, add single word or array of words into symbol table
            elif "dw" in temp:
                temp = temp.split("dw ", 1)[1]
                temp_list = temp.split(",")
                symbol_def = "D"

            #if double, add double word or array of double words into symbol table
            elif "dd" in temp:
                temp = temp.split("dd ", 1)[1]
                temp_list = temp.split(",")
                symbol_def = "D"

            else:
                error = "data_type"
                errors.append([file[i], error_table["data"][error]])
                i = i + 1
                continue


        #if in bss section
        #there are 3 cases
        #1. byte, 2. word, 3.double
        elif symbol_section == "bss" :
            j = 0
            while j < len(temp) and temp[j] != ' ':
                symbol_name += temp[j]
                j += 1
            temp = temp[j + 1:]

            if symbol_name[0].isdigit():
                error = "incorrect_start"
                errors.append([file[i], error_table["text"][error]])
                i = i+1
                continue

            e = 0
            for n in symbol_table:
                if n[0] == symbol_name and symbol_name.strip() != "":
                    error = "repeat_varible"
                    errors.append([file[i], error_table["bss"][error]])
                    e = 1
                    break
            if e == 1:
                i = i + 1
                continue
            l = temp.split()
            for n in l:
                if n.strip() == "":
                    l.remove(n)

            if len(l) == 1:

                if ("resb" in temp or "resd" in temp or "resw" in temp) and ("resd" in l or "resb" in l or "resw" in l):
                    error = "no_value"
                    errors.append([file[i], error_table["bss"][error]])
                    symbol_table.append([symbol_name])

                elif symbol_name == "resb" or symbol_name == "resd" or symbol_name == "resw":
                    z = 1

                else:
                    error = "operator_missing"
                    errors.append([file[i], error_table["text"][error]])
                i = i + 1
                continue

            elif len(l) == 0:
                symbol_name = symbol_name.strip()
                if symbol_name == "resd" or symbol_name == "resb" or symbol_name == "resw":
                    error = "no_value"
                    errors.append([file[i], error_table["bss"][error]])

                else:
                    error = "only_label"
                    errors.append([file[i], error_table["text"][error]])
                i = i + 1
                continue



            #if byte
            #check size and add it in symbol table
            if "resb" or "resd" or "resw" in temp:
                symbol_def = "D"

            else:
                error = "data_type"
                errors.append([file[i], error_table["bss"][error]])
                i = i + 1
                continue


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
                        i = i + 1
                        continue
                except:
                    symbol_def = "U"

            else:
                t = temp.split(" ",1)[1]
                if(check_operator(t,op)):
                    symbol_name = temp.split(" ",1)[0]
                    symbol_def = "D"

                elif ("jmp" in temp or "jnz" in temp or "jz" in temp) and address_getter == "label":
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
                            i = i + 1
                            continue
                    except:
                        symbol_def = "U"


                elif ("jmp" in temp or "jnz" in temp or "jz" in temp):
                    i = i+1
                    continue

                else:
                    error = "operator_missing"
                    errors.append([file[i], error_table["text"][error]])
                    i = i + 1
                    continue
        #if none of the above sections then skip the iteration
        #it may be empty line
        else:
            i += 1
            continue

    #adding symbol along with its attributes at each iteration into symbol table
    symbol = []
    symbol.append(symbol_name)
    symbol.append(symbol_section)
    symbol.append(symbol_def)
    symbol_table.append(symbol)


    i += 1

#print both the tables using tabulate function
#create a new file named output.txt with both the tables

output = open("output.txt","w")

print("\t\t##### ERROR LIST #####")
print(tabulate(errors))
output.write("\t##### ERROR LIST #####")
output.write("\n")
output.write(tabulate(error_table))




