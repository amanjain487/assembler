from sys import argv
import sys
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

#makes the size of value = size of byte
def checkbyte(value):
    while len(value) < 2:
        value = '0' + value
    return value

#makes size of value(argument) = size of word
def checkword(value):
    while len(value) < 4:
        value =  value + '00'
    return value

#makes size of value(argument) = size of double
def checkdouble(value):
    while len(value) < 8:
        value = value + '00'
    return value



def fwd(c,lab,file):
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
                check = fwd(c+1,op1,file_name)
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

#each files is passed in this function which generates symbol table
def symbol_table_generator(file_name,last_add):

    # dictionary of frequently used opcodes along with their instruction size
    op = {'mov': {"reg,reg": 2,
                  "reg,mem": {"eax": 5,
                              "oth": 6},
                  "reg,imm": 5,
                  "reg,mem[reg]": 2,

                  "reg,mem[var+imm]": {'eax': 5,
                                       'oth': 6},

                  "reg,mem[reg+imm]": {'127': 3,
                                       '128': 6},

                  "reg,mem[reg+reg*s]": 3,
                  "reg,mem[var+reg*s]": 7,

                  "mem,reg": {'eax': 5,
                              'oth': 6},
                  "mem,imm": 10,

                  "mem[reg],reg": 2,
                  "mem[reg],imm": 6,

                  "mem[var+imm],reg": {"eax": 5,
                                       "oth": 6},
                  "mem[var+imm],imm": 10,

                  "mem[reg+imm],reg": {'127': 3,
                                       '128': 6},
                  "mem[reg+imm],imm": {'127': {'127': 7,
                                               '128': 7},
                                       '128': {'127': 10,
                                               '128': 10}
                                       },

                  "mem[reg+reg*s],reg": 3,
                  "mem[reg+reg*s],imm": 7,

                  "mem[var+reg*s],reg": 7,
                  "mem[var+reg*s],imm": 11
                  },
          'add': {"reg,reg": 2,
                  "reg,mem": 6,
                  "reg,imm": {'127': 3,
                              '128': {"eax": 5,
                                      "oth": 6}
                              },
                  "reg,mem[reg]": 2,

                  "reg,mem[var+imm]": 6,

                  "reg,mem[reg+imm]": {'127': 3,
                                       '128': 6},

                  "reg,mem[reg+reg*s]": 3,
                  "reg,mem[var+reg*s]": 7,

                  "mem,reg": 6,
                  "mem,imm": {'127': 7,
                              '128': 10},

                  "mem[reg],reg": 2,
                  "mem[reg],imm": {'127': 3,
                                   '128': 6},

                  "mem[var+imm],reg": 6,
                  "mem[var+imm],imm": {'127': 7,
                                       '128': 10},

                  "mem[reg+imm],reg": {'127': 3,
                                       '128': 6},
                  "mem[reg+imm],imm": {'127': {'127': 4,
                                               '128': 7},
                                       '128': {'127': 7,
                                               '128': 10}
                                       },

                  "mem[reg+reg*s],reg": 3,
                  "mem[reg+reg*s],imm": {'127': 4,
                                         '128': 7},

                  "mem[var+reg*s],reg": 7,
                  "mem[var+reg*s],imm": {'127': 8,
                                         '128': 11
                                         }
                  },
          'sub': {"reg,reg": 2,
                  "reg,mem": 6,
                  "reg,imm": {'127': 3,
                              '128': {"eax": 5,
                                      "oth": 6}
                              },
                  "reg,mem[reg]": 2,

                  "reg,mem[var+imm]": 6,

                  "reg,mem[reg+imm]": {'127': 3,
                                       '128': 6},

                  "reg,mem[reg+reg*s]": 3,
                  "reg,mem[var+reg*s]": 7,

                  "mem,reg": 6,
                  "mem,imm": {'127': 7,
                              '128': 10},

                  "mem[reg],reg": 2,
                  "mem[reg],imm": {'127': 3,
                                   '128': 6},

                  "mem[var+imm],reg": 6,
                  "mem[var+imm],imm": {'127': 7,
                                       '128': 10},

                  "mem[reg+imm],reg": {'127': 3,
                                       '128': 6},
                  "mem[reg+imm],imm": {'127': {'127': 4,
                                               '128': 7},
                                       '128': {'127': 7,
                                               '128': 10}
                                       },

                  "mem[reg+reg*s],reg": 3,
                  "mem[reg+reg*s],imm": {'127': 4,
                                         '128': 7},

                  "mem[var+reg*s],reg": 7,
                  "mem[var+reg*s],imm": {'127': 8,
                                         '128': 11
                                         }
                  },
          'or': {"reg,reg": 2,
                 "reg,mem": 6,
                 "reg,imm": {'127': 3,
                             '128': {"eax": 5,
                                     "oth": 6}
                             },
                 "reg,mem[reg]": 2,

                 "reg,mem[var+imm]": 6,

                 "reg,mem[reg+imm]": {'127': 3,
                                      '128': 6},

                 "reg,mem[reg+reg*s]": 3,
                 "reg,mem[var+reg*s]": 7,

                 "mem,reg": 6,
                 "mem,imm": {'127': 7,
                             '128': 10},

                 "mem[reg],reg": 2,
                 "mem[reg],imm": {'127': 3,
                                  '128': 6},

                 "mem[var+imm],reg": 6,
                 "mem[var+imm],imm": {'127': 7,
                                      '128': 10},

                 "mem[reg+imm],reg": {'127': 3,
                                      '128': 6},
                 "mem[reg+imm],imm": {'127': {'127': 4,
                                              '128': 7},
                                      '128': {'127': 7,
                                              '128': 10}
                                      },

                 "mem[reg+reg*s],reg": 3,
                 "mem[reg+reg*s],imm": {'127': 4,
                                        '128': 7},

                 "mem[var+reg*s],reg": 7,
                 "mem[var+reg*s],imm": {'127': 8,
                                        '128': 11
                                        }
                 },
          'cmp': {"reg,reg": 2,
                  "reg,mem": 6,
                  "reg,imm": {'127': 3,
                              '128': {"eax": 5,
                                      "oth": 6}
                              },
                  "reg,mem[reg]": 2,

                  "reg,mem[var+imm]": 6,

                  "reg,mem[reg+imm]": {'127': 3,
                                       '128': 6},

                  "reg,mem[reg+reg*s]": 3,
                  "reg,mem[var+reg*s]": 7,

                  "mem,reg": 6,
                  "mem,imm": {'127': 7,
                              '128': 10},

                  "mem[reg],reg": 2,
                  "mem[reg],imm": {'127': 3,
                                   '128': 6},

                  "mem[var+imm],reg": 6,
                  "mem[var+imm],imm": {'127': 7,
                                       '128': 10},

                  "mem[reg+imm],reg": {'127': 3,
                                       '128': 6},
                  "mem[reg+imm],imm": {'127': {'127': 4,
                                               '128': 7},
                                       '128': {'127': 7,
                                               '128': 10}
                                       },

                  "mem[reg+reg*s],reg": 3,
                  "mem[reg+reg*s],imm": {'127': 4,
                                         '128': 7},

                  "mem[var+reg*s],reg": 7,
                  "mem[var+reg*s],imm": {'127': 8,
                                         '128': 11
                                         }
                  },
          'xor': {"reg,reg": 2,
                  "reg,mem": 6,
                  "reg,imm": {'127': 3,
                              '128': {"eax": 5,
                                      "oth": 6}
                              },
                  "reg,mem[reg]": 2,

                  "reg,mem[var+imm]": 6,

                  "reg,mem[reg+imm]": {'127': 3,
                                       '128': 6},

                  "reg,mem[reg+reg*s]": 3,
                  "reg,mem[var+reg*s]": 7,

                  "mem,reg": 6,
                  "mem,imm": {'127': 7,
                              '128': 10},

                  "mem[reg],reg": 2,
                  "mem[reg],imm": {'127': 3,
                                   '128': 6},

                  "mem[var+imm],reg": 6,
                  "mem[var+imm],imm": {'127': 7,
                                       '128': 10},

                  "mem[reg+imm],reg": {'127': 3,
                                       '128': 6},
                  "mem[reg+imm],imm": {'127': {'127': 4,
                                               '128': 7},
                                       '128': {'127': 7,
                                               '128': 10}
                                       },

                  "mem[reg+reg*s],reg": 3,
                  "mem[reg+reg*s],imm": {'127': 4,
                                         '128': 7},

                  "mem[var+reg*s],reg": 7,
                  "mem[var+reg*s],imm": {'127': 8,
                                         '128': 11
                                         }
                  },
          'mul': {"reg": 2,
                  "mem[reg]": 2,
                  "mem": 6,
                  "mem[reg+imm]": {'127': 3,
                                   '128': 6},
                  "mem[var+imm]": 6,
                  "mem[var+reg*s]": 7,
                  "mem[reg+reg*s]": 3
                  },
          'inc': {"reg": 1,
                  "mem[reg]": 2,
                  "mem": 6,
                  "mem[reg+imm]": {'127': 3,
                                   '128': 6},
                  "mem[var+imm]": 6,
                  "mem[var+reg*s]": 7,
                  "mem[reg+reg*s]": 3
                  },
          'dec': {"reg": 1,
                  "mem[reg]": 2,
                  "mem": 6,
                  "mem[reg+imm]": {'127': 3,
                                   '128': 6},
                  "mem[var+imm]": 6,
                  "mem[var+reg*s]": 7,
                  "mem[reg+reg*s]": 3
                  },
          'jmp': {"fwd": {"127": 2,
                          "128": 5},
                  "bwd": {"127": 2,
                          "128": 5},
                  "reg": 2,
                  "mem[reg]": 2,
                  "mem": 6,
                  "mem[reg+imm]": {'127': 3,
                                   '128': 6},
                  "mem[var+imm]": 6,
                  "mem[var+reg*s]": 7,
                  "mem[reg+reg*s]": 3,
                  "imm": {"127": 5,
                          "128": 5
                          },
                  "label": 5
                  },
          'jnz': {"fwd": {"127": 2,
                          "128": 6},
                  "bwd": {"127": 2,
                          "128": 6},
                  "imm": {"127": 6,
                          "128": 6
                          },
                  "label": 6
                  },
          'jz': {"fwd": {"127": 2,
                         "128": 6},
                 "bwd": {"127": 2,
                         "128": 6},
                 "imm": {"127": 6,
                         "128": 6
                         },
                 "label": 6
                 },
          'push': {"reg": 1,
                   "mem[reg]": 2,
                   "mem": 6,
                   "mem[reg+imm]": {'127': 3,
                                    '128': 6},
                   "mem[var+imm]": 6,
                   "mem[var+reg*s]": 7,
                   "mem[reg+reg*s]": 3,
                   "imm": {"127": 2,
                           "128": 5
                           },
                   "label": 5
                   },
          'call': {"reg": 2,
                   "mem[reg]": 2,
                   "mem": 6,
                   "mem[reg+imm]": {'127': 3,
                                    '128': 6},
                   "mem[var+imm]": 6,
                   "mem[var+reg*s]": 7,
                   "mem[reg+reg*s]": 3,
                   "imm": {"127": 5,
                           "128": 5
                           },
                   "label": 5
                   }
          }
    z = 0
    # dictionary of registers along with their number in modrm
    registers = {"eax": "000",
                 "ecx": "001",
                 "edx": "010",
                 "ebx": "011",
                 "esp": "100",
                 "ebp": "101",
                 "esi": "110",
                 "edi": "111"
                 }

    # read file
    file = open(file_name, "r")

    # remove leading and trailing spaces and tabs:
    temp_file = file
    file = []
    for i in temp_file:
        temp = i.lstrip()
        if temp == '':
            continue
        file.append(temp)

    # pass 1

    # all fields required in symbol table are defined below
    # same are used in literal table as required
    symbol_name = ""
    symbol_section = ""
    symbol_type = ""
    symbol_size = 0
    symbol_def = "U"
    next_symbol_address = "0x0"

    i = 0

    while i < len(file):

        # set default value for each new line
        current_address = ""
        symbol_address = next_symbol_address
        new_symbol_name = ""
        symbol_name = ""
        symbol_type = ""
        symbol_value = 0
        symbol_size = 0
        temp = file[i]
        if "global" in temp or "extern" in temp:
            file.remove(file[i])
            continue

        # if '.' is there in line, it means line is some section
        # find the section name
        if '.' in temp:
            symbol_section = ""
            j = 0
            while temp[j] != '.':
                j += 1
            j += 1
            symbol_section = temp[j:-1]
            symbol_section = symbol_section.strip()

            if symbol_section == "text":
                symbol_address = last_add
                next_symbol_address = last_add

            elif argv[1] == file_name:
                symbol_address = "0x0"
                next_symbol_address = "0x0"
            else:
                z = 0
                while z < len(symbol_table) and symbol_table[z][3] != symbol_section:
                    z = z+1
                while z < len(symbol_table) and symbol_table[z][3] == symbol_section:
                    z = z+1
                if z < len(symbol_table):
                    if symbol_section == "text":
                        z = z - 1
                    else:
                        z = z-1
                        symbol_address = symbol_table[z][2]
                        next_symbol_address = int(symbol_address.strip(), 0) + int(symbol_table[z][6])
                        next_symbol_address = hex(next_symbol_address)
                else:
                    symbol_address == "0x0"
                    next_symbol_address = "0x0"
                z = z + 1
            i += 1
            continue
        # if ':' in instruction, it means the line contains label for sure
        # find the label name and address and store it in symbol table
        if ':' in temp:
            symbol_type = "Label"
            symbol_value = None
            symbol_size = 0
            symbol_def = "D"
            j = 0
            while temp[j] != ':':
                symbol_name += temp[j]
                j += 1
            modified = temp[j + 1:].strip()
            file[i] = modified
            temp = modified
            defined = 0

            # if label already present in symbol_table and if it is undefined make it as defined
            for k in symbol_table:
                if k[1] == symbol_name:
                    if k[7] != "D":
                        k[7] = 'D'
                        k[2] = symbol_address
                        defined = 1
                    else:
                        index = file_name.split(".", 1)[0].strip()
                        new_symbol_name = symbol_name + "_" + index
                    break

            # if label not present aleady, add label in symbol table
            if defined != 1:
                if new_symbol_name == "":
                    new_symbol_name = symbol_name
                symbol = []
                symbol.append(new_symbol_name)
                symbol.append(symbol_name)
                symbol.append(symbol_address)
                symbol.append(symbol_section)
                symbol.append(symbol_type)
                symbol.append(symbol_value)
                symbol.append(symbol_size)
                symbol.append(symbol_def)
                symbol_table.append(symbol)

        # calculate the size of each instruction to calculate address of label if any
        if (is_operator(temp, op)):

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

            elif (operator == "push" or operator == "call" or operator == "jmp" or operator == "jnz" or operator == "jz") and "[" not in op1 and "imm" not in address_getter and address_getter == "":
                address_getter = ""
                check_address = ""
                for m in symbol_table:
                    if m[1] == op1:
                        if operator == "jmp" or operator == "jnz" or operator == "jz":
                            if m[3] == "text":
                                if m[2] == None:
                                    if m[4] == "Label":
                                        address_getter = "fwd"
                                    elif m[4] == "Function":
                                        address_getter = "label"
                                else:
                                    check_address = m[2]
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
                    check = fwd(i + 1, op1,file_name)
                    if check <= 127:
                        current_address = current_address["127"]
                    else:
                        current_address = current_address["128"]



            elif "imm" in address_getter and operator != "mov" and "imm]" not in address_getter:
                for s in symbol_table:
                    if op2 != None and s[1].strip() == op2.strip():
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


            # calculate new address by adding previous address + current instruction size
            next_symbol_address = int(symbol_address, 0) + current_address
            next_symbol_address = hex(next_symbol_address)
            # find any undefined function used or called in the program
            # if present add it to symbol table
            temp = new_temp
            if operator == 'call':
                temp = temp.strip()
                if address_getter == "label":
                    check = 0
                    for s in symbol_table:
                        if s[1] == temp:
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
                        symbol.append(symbol_name)
                        symbol.append(symbol_address)
                        symbol.append(symbol_section)
                        symbol.append(symbol_type)
                        symbol.append(symbol_value)
                        symbol.append(symbol_size)
                        symbol.append(symbol_def)
                        symbol_table.append(symbol)

            # if not then see if the instruction contains any immediate value
            # if yes add it to literal table
            else:
                j = 0
                while j < len(temp) and temp[j] != ",":
                    j = j + 1
                temp = temp[j + 1:]
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

        # to check if given instruction contains operators
        # if yes skip because immediate value added already
        if (check_operator(temp, op)):
            i = i + 1
            continue

        # if no then check if it contains any constants or user declared data
        else:

            # if section is data
            # then there are 3 cases:
            # 1.byte, 2.word, 3.double
            if symbol_section == "data":
                j = 0
                while temp[j] != ' ':
                    symbol_name += temp[j]
                    j += 1
                temp = temp[j + 1:]

                # if byte
                if "db" in temp:
                    symbol_type = "Byte"
                    j = 0
                    temp = temp.split("db ", 1)[1]
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
                            while j < len(temp) and temp[j] != '"' and temp[j] != "'":
                                symbol_size += 1
                                j += 1
                        # else it contains single byte data, so add that in symbol table
                        else:
                            symbol_size += 1
                    next_symbol_address = int(symbol_address, 0) + symbol_size
                    next_symbol_address = hex(next_symbol_address)
                    symbol_def = "D"

                # if word, add single word or array of words into symbol table
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

                # if double, add double word or array of double words into symbol table
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

            # if in bss section
            # there are 3 cases
            # 1. byte, 2. word, 3.double
            elif symbol_section == "bss":
                j = 0
                while temp[j] != ' ':
                    symbol_name += temp[j]
                    j += 1
                temp = temp[j + 1:]

                # if byte
                # check size and add it in symbol table
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
                            symbol_size = int(current_address, 0)
                    else:
                        temp = temp.split("resb ", 1)[1]
                        j = 0
                        temp = temp[:-1]
                        symbol_value = None
                        symbol_size = 1 * int(temp)
                        next_symbol_address = hex(symbol_size + int(symbol_address, 0))
                    symbol_def = "D"

                # if word
                elif "resw" in temp:
                    symbol_type = "Word"
                    temp = temp.split("resw ", 1)[1]
                    j = 0
                    temp = temp[:-1]
                    symbol_value = None
                    symbol_size = 2 * int(temp)
                    next_symbol_address = hex(symbol_size + int(symbol_address, 0))

                # if double
                elif "resd" in temp:
                    symbol_type = "Double"
                    temp = temp.split("resd ", 1)[1]
                    j = 0
                    temp = temp[:-1]
                    symbol_value = None
                    symbol_size = 4 * int(temp)
                    next_symbol_address = hex(symbol_size + int(symbol_address, 0))
                literal = []
                literal.append(symbol_name)
                literal.append(symbol_section)
                literal.append(symbol_type)
                literal.append(symbol_value)
                literal_table.append(literal)

            # if section is text
            # to counter labels which are declared after jmp or jnz operators
            # extract label and its attributes and add it in symbol_table
            elif symbol_section == "text":
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
                        if k[1] == symbol_name:
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
                        if k[1] == symbol_name:
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
                        if k[1] == symbol_name:
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

                # if not jmp and jnz, skip the iteration
                else:
                    i = i + 1
                    continue
            # if none of the above sections then skip the iteration
            # it may be empty line
            else:
                i += 1
                continue

        for s in symbol_table:
            if s[1] == symbol_name:
                index = file_name.split(".",1)[0].strip()
                new_symbol_name = symbol_name + "_" + index
                break
        if new_symbol_name == "":
            new_symbol_name = symbol_name





        # adding symbol along with its attributes at each iteration into symbol table
        symbol = []
        symbol.append(new_symbol_name)
        symbol.append(symbol_name)
        symbol.append(symbol_address)
        symbol.append(symbol_section)
        symbol.append(symbol_type)
        symbol.append(symbol_value)
        symbol.append(symbol_size)
        symbol.append(symbol_def)

        if file_name == argv[1]:
            symbol_table.append(symbol)
        else:
            symbol_table.insert(z,symbol)
            z = z+1

        i += 1

    return next_symbol_address


#################################################
##beginning of program

#variables declared as global as they will be accessed by each file
symbol_address = "0x0"
literal_table = []
literal_table.append(["Name", "Section", "Type", "Value"])
symbol_table = []
symbol_table.append(["New Name","Name", "Address", "Section", "Type", "Value", "Size", "Defined/Undefined"])

#reads file names which are passes as arguments
files = argv[1:]
last_address = "0x0"

#for each file call symbol_table_generator address
for i in files:
    last_address = symbol_table_generator(i,last_address)



# print both the tables using tabulate function
# create a new file named output.txt with both the tables
print("\t\t\t\t\t\t#####COMBINED SYMBOL TABLE #####")
print(tabulate(symbol_table))
output = open("output.txt","w")
output.write("\t\t\t\t#####COMBINED SYMBOL TABLE #####")
output.write("\n")

output.write(tabulate(symbol_table))

print("\n")
