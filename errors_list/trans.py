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
    if operator == "jmp" or operator == "jnz" or operator == "jz" or operator == "call" or operator == "push":
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

list1 = ["reg,reg", "reg,mem[var]", "reg,imm", "reg,mem[reg]", "reg,mem[var+var]", "reg,mem[reg+var]",
         "reg,mem[var+reg]","reg,mem[reg+reg]","reg,mem[reg*var]","reg,mem[var*var]","reg,mem[var*reg]",
         "reg,mem[reg+reg*var]","reg,mem[var+reg*var]","mem[var],reg","mem[var],imm","mem[reg],reg",
         "mem[reg],imm","mem[reg*var],reg","mem[reg*var],imm","mem[var*reg],reg","mem[var*var],reg",
         "mem[var*var],imm","mem[var*reg],imm","mem[var+var],reg","mem[var+var],imm","mem[reg+var],reg",
         "mem[reg+var],imm", "mem[reg+reg],reg","mem[reg+reg],imm","mem[var+reg],reg", "mem[var+reg],imm",
         "mem[reg+reg*var],reg","mem[reg+reg*var],imm","mem[var+reg*var],reg","mem[var+reg*var],imm"]

list2 = ["reg","mem[reg]","mem[var]","mem[reg+var]","mem[var+var]", "mem[reg+reg]","mem[var+reg]",
         "mem[var+reg*var]","mem[reg+reg*var]"]

list3 = ["reg","mem[reg]","mem[var]","mem[reg+var]","mem[reg+reg]", "mem[var+reg]","mem[reg*var]","mem[var*reg]",
         "mem[var*var]","mem[var+var]","mem[var+reg*var]","mem[reg+reg*var]","imm","label"],

#dictionary of frequently used opcodes along with the type of instruction it can be
op = {  'mov' : list1, 'add' : list1, 'sub' : list1, 'or' :list1, 'cmp' : list1, 'xor' : list1,
        'mul' : list2, 'inc' : list2, 'dec' : list2,
        'jmp' : list3,'jnz' : list3,'jz' :list3,'push' : list3,'call' : list3
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


#dictionary of common errors
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
                         "incorrect_start" : "label or instruction expected at start of line",
                         "op" : "comma, colon, decorator or end of line expected after operand",
                         "syntax" : "expression syntax error",
                         "*" : "impossible segment base multiplier",
                         "sib" : "invalid effective address",
                         "var,var" : "unable to multiply 2 non scalar objects"}
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


#all fields required in symbol table are defined below and also for error table
other_symbols = []
symbol_table = []
errors = [["Instruction","Error"],["----------- ","----- "]]
symbol_name = ""
symbol_section = ""
symbol_def = "U"

i = 0

final_check = []
fin_check = 0
while i < len(file):
    #set default value for each new line
    symbol_name = ""
    temp = file[i]
    error = ""

    #if global or extern functions or labels are defined add them in symbol table
    #also look for errors in them
    if "global" in temp or "extern" in temp:
        l = temp.split()
        for a in l:
            if a.strip() == "":
                l.remove(a)
        if len(l) <= 1:
            error = "no_parameter"
            errors.append([file[i],error_table[symbol_section][error]])
        file.remove(file[i])
        temp = temp.split(" ",1)[1].strip()
        temp = temp.split()
        for q in temp:
            if q.strip() != "":
                other_symbols.append(q)
        continue

    if temp[0].isdigit():
        error = "incorrect_start"
        errors.append([file[i], error_table["text"][error]])
        i = i + 1
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

#if bss value declared in data section,then error
    if symbol_section == "data":
        if "resd " in temp or "resb " in temp or "resw " in temp or "resq " in temp:
            error = "wrong_section"
            errors.append([file[i],error_table["data"][error]])
            i = i+1
            continue

#if data value declared in bss section,then error
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
        #and also it is redefining the symbol
        e = 0
        for k in symbol_table:
            if k[0] == symbol_name:
                if k[2] == 'U':
                    k[2] = 'D'
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



#look for other errors
    operator_yes = 0
    if(is_operator(temp,op)):
        operator_yes = 1

    else:
        symbol_name = temp.split(" ", 1)[0]
        t = temp.split(" ", 1)[1]
        if is_operator(t, op):
            symbol_table.append([symbol_name,symbol_section,"D"])
            operator_yes = 1
            temp = t


#if the instruction starts with operator
    if operator_yes == 1:
        new_new_temp = temp
        operator = get_operator(temp, op)
        temp = temp.split(operator+' ', 1)[1]
        op1 = ""
        op2 = ""
        new_temp = temp
        check_address = ""
        #if ',' in instruction, the instruction contains 2 operands for sure
        if ',' in temp:
            op1 = temp.split(",",1)[0].strip()
            op2 = temp.split(",",1)[1].strip()

        #else only 1 operand, 2nd one is none
        else:
            op1 = temp.strip()
            op2 = None
        address_getter = ""
        op1 = op1.strip()

#find the type of instruction
        #address_getter stores the type of instruction
        operand1 = op1
        operand2 = op2
        if op1 in registers:
            address_getter = "reg"

        elif "[" in op1:
            end = 1
            op1 = op1.strip()
            if op1[0] == "[":
                address_getter += "mem["

            else:
                check = op1.split("[",1)[0]
                if check == "dword" or check == "dword ":
                    address_getter += "mem["


                else:
                    error = "op"
                    errors.append([file[i], error_table["text"][error]])
                    end = 0
                    break

            op1 = op1.split("[", 1)[1].strip()
            while op1 != "":
                if op1[0].isdigit() == True:
                    j = 0
                    while op1[j].isdigit():
                        j = j + 1
                    op1 = op1[j:].strip()
                    j = 0
                    if op1[j] == "d" or op1[j] == "q" or op1[j] == "b":
                        address_getter += "var"
                        j = j+1

                    elif op1[j] == "+" or op1[j] == "]" or op1[0] == "*":
                        address_getter += "var"

                    op1 = op1[j:]
                    j = 0
                    if op1[j] == "+" or op1[j] == "]" or op1[0] == "*":
                        if op1[j] == "+":
                            address_getter += "+"

                        elif op1[j] == "*":
                            address_getter += "*"

                        else:
                            op1 = op1[j:].strip()
                            if op1 == "]":
                                address_getter += "]"

                    else:
                        error = "syntax"
                        errors.append([file[i], error_table["text"][error]])
                        end = 0
                        break


                elif op1[:3] in registers:
                    address_getter += "reg"
                    op1 = op1[3:].strip()
                    if op1 == "]":
                        address_getter += "]"
                    elif op1[0] == "+":
                        address_getter += "+"
                    elif op1[0] == "*":
                        address_getter += "*"
                    else:
                        error = "syntax"
                        errors.append([file[i], error_table["text"][error]])
                        end = 0
                        break

                else:
                    check = ""
                    j = 0
                    while op1[j].isalnum():
                        check += op1[j]
                        j = j+1
                    q = 0
                    for x in symbol_table:
                        if x[0].strip() == check.strip():
                            address_getter += "var"
                            op1 = op1.split(check,1)[1].strip()

                            if op1 == "]":
                                address_getter += "]"

                            elif op1[0] == "+" or op1[0] == "*":
                                address_getter += op1[0]
                            q = 1
                            break

                    if q == 0:
                        error = "label"
                        errors.append([file[i], error_table["text"][error]])
                        break


                op1 = op1.strip()
                if op1.strip() == "]":
                    op1 = ""
                else:
                    op1 = op1[1:].strip()

            if "+reg*var" in address_getter:
                op1 = operand1
                op1 = op1.split("*",1)[1].strip()[:-1].strip()
                if op1 == "2" or op1 == "4" or op1 == "8":
                    end = 1
                else:
                    error = "sib"
                    errors.append([file[i], error_table["text"][error]])
                    i = i+1
                    continue

            elif "[reg*var]" in address_getter:
                op1 = operand1
                op1 = op1.split("[",1)[1].strip().strip()
                op1 = op1.split("*", 1)[1].strip()[:-1].strip()
                if op1 == "2" or op1 == "4" or op1 == "8":
                    end = 1
                else:
                    error = "sib"
                    errors.append([file[i], error_table["text"][error]])
                    i = i + 1
                    continue

            elif "[var*reg]" in address_getter:
                op1 = operand1
                op1 = op1.split("[",1)[1].strip().strip()
                op1 = op1.split("*", 1)[0].strip().strip()
                if op1 == "2" or op1 == "4" or op1 == "8":
                    end = 1
                else:
                    error = "sib"
                    errors.append([file[i], error_table["text"][error]])
                    i = i + 1
                    continue

            elif "var*var" in address_getter:
                op1 = operand1
                op1 = op1.split("[", 1)[1].strip()[:-1].strip()
                var1 = op1.split("*", 1)[0].strip()
                var2 = op1.split("*", 1)[1].strip()
                sym1 = 0
                sym2 = 0
                for z in symbol_table:
                    if var1.strip() == z[0].strip():
                        sym1 = 1
                    if var2.strip() == z[0].strip():
                        sym2 = 1
                    if sym1 == 1 and sym2 == 1:
                        break

                if sym1 == 1 and sym2 == 1:
                    error = "var,var"
                    errors.append([file[i], error_table["text"][error]])
                    i = i + 1
                    continue

                elif var1.isdigit() != True or var2.isdigit() != True:
                    error = "sib"
                    errors.append([file[i], error_table["text"][error]])
                    i = i + 1
                    continue

            elif "[var+var]" in address_getter:
                op1 = operand1
                op1 = op1.split("[", 1)[1].strip()[:-1].strip()
                var1 = op1.split("+", 1)[0].strip()
                var2 = op1.split("+", 1)[1].strip()
                if var1.isdigit() or var2.isdigit():
                    no_problem = 1

                else:
                    error = "sib"
                    errors.append([file[i], error_table["text"][error]])
                    i = i + 1
                    continue

            elif "reg*reg" in address_getter:
                error = "var,var"
                errors.append([file[i], error_table["text"][error]])
                i = i + 1
                continue

            if end == 0:
                i = i + 1
                continue

        elif op1[0].isdigit():
            if check_operator(new_new_temp,op):
                error = "incorrect_start"
                errors.append([file[i], error_table["text"][error]])
                i = i + 1
                continue

            else:
                address_getter = "imm"


        #address_getter if instruction has only 1 operand is found.
        #but if instruction has 2 operands, type of instruction is modified accordingly
        if op2 != None:
            if op2 in registers:
                address_getter += ",reg"

            elif "[" in op2:
                end = 1
                op2 = op2.strip()
                if op2[0] == "[":
                    address_getter += ",mem["

                else:
                    check = op2.split("[", 1)[0]
                    if check == "dword" or check == "dword ":
                        address_getter += ",mem["

                    else:
                        error = "op"
                        errors.append([file[i], error_table["text"][error]])
                        end = 0
                        i = i+1
                        continue

                op2 = op2.split("[", 1)[1].strip()
                while op2 != "":
                    if op2[0].isdigit() == True:
                        j = 0
                        while op2[j].isdigit():
                            j = j + 1
                        op2 = op2[j:].strip()
                        j = 0
                        if op2[j] == "d" or op2[j] == "q" or op2[j] == "b":
                            address_getter += "var"
                            j = j + 1

                        elif op2[j] == "+" or op2[j] == "]" or op2[0] == "*":
                            address_getter += "var"

                        op2 = op2[j:]
                        j = 0
                        if op2[j] == "+" or op2[j] == "]" or op2[0] == "*":
                            if op2[j] == "+":
                                address_getter += "+"

                            elif op2[j] == "*":
                                address_getter += "*"

                            else:
                                op2 = op2[j:].strip()
                                if op2 == "]":
                                    address_getter += "]"

                        else:
                            error = "syntax"
                            errors.append([file[i], error_table["text"][error]])
                            end = 0
                            break

                    elif op2[:3] in registers:
                        address_getter += "reg"
                        op2 = op2[3:].strip()
                        if op2 == "]":
                            address_getter += "]"
                        elif op2[0] == "+":
                            address_getter += "+"
                        elif op2[0] == "*":
                            address_getter += "*"
                        else:
                            error = "syntax"
                            errors.append([file[i], error_table["text"][error]])
                            end = 0
                            break

                    else:
                        check = ""
                        j = 0
                        while op2[j].isalnum():
                            check += op2[j]
                            j = j + 1
                        q = 0
                        for x in symbol_table:
                            if x[0].strip() == check.strip():
                                address_getter += "var"
                                op2 = op2.split(check, 1)[1].strip()

                                if op2 == "]":
                                    address_getter += "]"

                                elif op2[0] == "+" or op2[0] == "*":
                                    address_getter += op2[0]
                                q = 1
                                break

                        if q == 0:
                            error = "label"
                            errors.append([file[i], error_table["text"][error]])
                            break

                    op2 = op2.strip()
                    if op2.strip() == "]":
                        op2 = ""
                    else:
                        op2 = op2[1:].strip()

                if "+reg*var" in address_getter:
                    op2 = operand2
                    op2 = op2.split("*", 1)[1].strip()[:-1].strip()
                    if op2 == "2" or op2 == "4" or op2 == "8":
                        end = 1
                    else:
                        error = "sib"
                        errors.append([file[i], error_table["text"][error]])
                        i = i + 1
                        continue

                elif "[reg*var]" in address_getter:
                    op2 = operand2
                    op2 = op2.split("[", 1)[1].strip().strip()
                    op2 = op2.split("*", 1)[1].strip()[:-1].strip()
                    if op2 == "2" or op2 == "4" or op2 == "8":
                        end = 1
                    else:
                        error = "sib"
                        errors.append([file[i], error_table["text"][error]])
                        i = i + 1
                        continue

                elif "[var*reg]" in address_getter:
                    op2 = operand2
                    op2 = op2.split("[", 1)[1].strip().strip()
                    op2 = op2.split("*", 1)[0].strip().strip()
                    if op2 == "2" or op2 == "4" or op2 == "8":
                        end = 1
                    else:
                        error = "sib"
                        errors.append([file[i], error_table["text"][error]])
                        i = i + 1
                        continue

                elif "var*var" in address_getter:
                    op2 = operand2
                    op2 = op2.split("[", 1)[1].strip()[:-1].strip()
                    var1 = op2.split("*", 1)[0].strip()
                    var2 = op2.split("*", 1)[1].strip()
                    sym1 = 0
                    sym2 = 0
                    for z in symbol_table:
                        if var1.strip() == z[0].strip():
                            sym1 = 1
                        if var2.strip() == z[0].strip():
                            sym2 = 1
                        if sym1 == 1 and sym2 == 1:
                            break

                    if sym1 == 1 and sym2 == 1:
                        error = "var,var"
                        errors.append([file[i], error_table["text"][error]])
                        i = i + 1
                        continue

                    elif var1.isdigit() != True or var2.isdigit() != True:
                        error = "sib"
                        errors.append([file[i], error_table["text"][error]])
                        i = i + 1
                        continue

                elif "[var+var]" in address_getter:
                    op2 = operand2
                    op2 = op2.split("[", 1)[1].strip()[:-1].strip()
                    var1 = op2.split("+", 1)[0].strip()
                    var2 = op2.split("+", 1)[1].strip()
                    if var1.isdigit() or var2.isdigit():
                        no_problem = 1

                    else:
                        error = "sib"
                        errors.append([file[i], error_table["text"][error]])
                        i = i + 1
                        continue

                if end == 0:
                    i = i + 1
                    continue

            elif op2[0].isdigit():
                address_getter += ",imm"

        temp = new_new_temp

        #if instructions contain label add them in separate list. we will check them later.
        if not check_operator(temp,op) and address_getter == "":
            final_check.append([file[i],op1])
            i = i+1
            continue


        temp = new_new_temp

    #find if the type of instruction is valid or not by looking into op dictionary which further uses 3 lists
        new_size = op[operator]
        if address_getter in new_size:
            new_size = 0

        else:
            error = "operator_missing"
            errors.append([file[i], error_table["text"][error]])
            i = i + 1
            continue

    #if instruction did not start with operator or label and if section is text then it is an error
    elif symbol_section == "text":
        error = "operator_missing"
        errors.append([file[i], error_table["text"][error]])
        i = i + 1
        continue

    else:
        #if section is data
        #then there are 3 cases:
        #1.byte, 2.word, 3.double
        if symbol_section == "data":
            symbol_name = ""
            j = 0
            while j < len(temp) and temp[j] != ' ':
                symbol_name += temp[j]
                j += 1
            temp = temp[j+1:]

            #if variable is already defined, then redefine error
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

            #if none of the above types then it is invalid data type error
            else:
                error = "data_type"
                errors.append([file[i], error_table["data"][error]])
                i = i + 1
                continue

        #if in bss section
        #there are 3 cases
        #1. byte, 2. word, 3.double
        elif symbol_section == "bss" :
            symbol_name =""
            j = 0
            while j < len(temp) and temp[j] != ' ':
                symbol_name += temp[j]
                j += 1
            temp = temp[j + 1:]


            # if variable is already defined, then redefine error
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
            if "resb" in temp or "resd" in temp or "resw" in temp:
                symbol_def = "D"

            else:
                error = "data_type"
                errors.append([file[i], error_table["bss"][error]])
                i = i + 1
                continue

        #if section is text and does not contain operator then it is an error
        elif symbol_section == "text" :
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

#checking those instructions which had labels or instructions
#by now all the labels and functions are added in symbol table
#so if a function from any instruction is not in symbol table, then it is undefined symbol error
for i in final_check:
    final = 0
    for x in symbol_table:
        if x[0].strip() == i[1].strip():
            final = 1
            break

    if final == 0:
        if i[1].strip() not in other_symbols:
            error = "label"
            errors.append([i[0], error_table["text"][error]])

#print errors using tabulate function
#create a new file named output.txt with both the tables

output = open("output.txt","w")

print("\t\t##### ERROR LIST #####")
print(tabulate(errors))
output.write("\t##### ERROR LIST #####")
output.write("\n")
output.write(tabulate(errors))




