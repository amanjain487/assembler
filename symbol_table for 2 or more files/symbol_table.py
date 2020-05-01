import instruction_set
from instruction_set import registers
from instruction_set import op

#defining node which will behave as a single rocord of symbol table i.e. row
class Node :
	def __init__(self,address=None,section=None,name=None,dtype=None,value=None) :
		
		self.format_address(address)
		self.section=section
		self.name=name
		self.dtype=dtype
		self.value=value 
		self.next=None
	def format_address(self,address) :
		if address!=None :
			address=hex(address)
			address=address[2:]
			address= "0"*(8-len(address)) + address
			self.address=address

# llist class defines a  symbol table
class llist :
	def __init__(self) :
		self.head=None

	#function to enter data  into various attributes of the record
	def insert(self,node) :
		
		if self.head ==None :
			self.head=node

		else :
			ptr=self.head
			while(ptr.next!=None) :
				ptr=ptr.next
			ptr.next=node


	#-----printing and stuffing spaces to get a look of a table-------
	def display(self) :
		if(self.head==None) :
			return
		print('address'," "*8,
			'section'," "*8,
			 'name'," "*11,
			 'dtype'," "*10,
			 'value')

		print("~"*15,"~"*15,"~"*15,"~"*15,"~"*15)

		ptr=self.head
		
		while ptr!=None :
			print(ptr.address ," "*(15-len(ptr.address)), #adding calculative spaces to give a tabular look to the output
				ptr.section[1:]," "*(15-len(ptr.section)),
				ptr.name," "*(15-len(ptr.name)),
				ptr.dtype," "*(15-len(ptr.dtype)),
				ptr.value)
			ptr=ptr.next

#=======================================================================================

#segregate instruction into type as reg,reg || reg,mem[reg+imm]
#this will help us to choose what would be the size if the instruction from the 'op' set that is being imported at the top

def  get_inst_profile(line,addr):

	line=line.strip()
	
	value_set={'label':None,'imm':None,'reg':None,'op':None,'addr':None}
	
	#no need to process line having section , as it neither have instruction nor any label
	if 'section' in line :
		value_set['addr']=0

	if 'extern' in line or 'global' in line :
		ind=line.find(' ')
		records.insert(Node(0,'.text',line[ind+1:],'function','           '))
		value_set['addr']=0


	instructions=['mov','add','sub','mul','xor','or','cmp','inc','dec','jnz','jmp','jz','push','call']
	org_line=line #line will go under change multiple time in this module, org_line will be used where ever original line 
	line=line.strip()							#would be required
	
	# we will replace all the registers in the instruction with 'reg' to step forward in matching indices from 'op' set
	for reg in registers :							
		if reg in line :							
			line=line.replace(reg,'reg') 			
	
	#where ever there is one register, we must note it down as it may later resolve the indices of subset of set 'op'												
	if line.count('reg')==1 :						
		if 'eax' in org_line :						
			value_set['reg']='eax'					
		else :										
			value_set['reg']='oth'						

	#replacing dword with, so as to match indices in set 'op'
	if 'dword' in line :
		line=line.replace('dword','mem') 	

	start_mem=line.find('[') #check if there is dword involves
	end_mem=line.find(']')   
	plus_index = line.find('+')  #check whether displacment or SIB involved

	if start_mem!=-1 :
		
		if plus_index!=-1:	
			
			#replacing immediate value with imm in the memory part '[reg + imm]'
			if 'reg' not in line[plus_index:end_mem+1] :
				if int(line[plus_index+1:end_mem]) <=127 :
					value_set['imm']='127'
				else :
					value_set['imm']='128'
				
				line=line[0:plus_index] + '+imm' + line[end_mem:]

			#replacing scale by 's'
			if '*' in line :
				index1=line.find('*')
				line=line[0:index1]+'*s'+line[end_mem:]

			

	#checking if there exists a variable in bss or data section
	#if it exists then it would be defined variable and we will reolace the variable name with var
	#replacing if variable is in dword block
	ptr=records.head
	if ptr !=None :
		while(ptr!=None) :
			if start_mem != -1 :
				if ptr.name in line[start_mem:end_mem+1] :
					line=line.replace(ptr.name,'var')
					break
			ptr=ptr.next

	# finding imm value 
	count=0
	line=line.split(' ')
	
	#no instruction is there with only one word, so return that line
	if len(line)<2 :
		return
#if every char of last word lies in range (48,58) then in must be an immediate value in original instruction  
	for char in line[-1]:
		if  ord(char) not in range(48,58) :
				break
		count+=1
	

	if count==len(line[-1].strip()) :
		
		#checking whether imm was greater than 127 or not
		if int(line[-1].strip()) <=127 :
			value_set['imm']='127'
		else :
			value_set['imm']='128'

		line=line[0:len(line)-1]
		line.append('imm')

	line=' '.join(line)
	line=line.strip()

	#find if instruction contains a label , ':' specifies tht instruction contains a label
	if ':' in line and 'main' not in line:
		index=line.find(':')
		value_set['label']=line[0:index]
		line=line[index+1:]
	
	# check if there is any operator in instruction
	for inst in instructions :
		if inst in line :
			value_set['op']=inst
	
	
	line=line.split(' ')
	if value_set['label']==None :
		line=line[1:]
	else : 
		line=line[2:]

	line=','.join(line)
	profile=line.strip()

	if 'mem[var]' in profile:
		profile=profile.replace('mem[var]','mem')

	if value_set['op'] in ['jnz','jmp','jz'] : 
		value_set['addr']=2

	if value_set['op']!=None :
		if profile in op[value_set['op']] :
			
			# if the value is integer then its the required value we need to add in prev addr, else go deep into the subset
			if str(type(op[value_set['op']][profile]) ) != "<class 'dict'>" :
				value_set['addr']=op[value_set['op']][profile]
			else: 
				if op[value_set['op']][profile] == {'eax':5,'oth':6} :
					value_set['addr']= op[value_set['op']][profile]['reg']
 
				elif str(type(op[value_set['op']][profile][value_set['imm']])) != "<class 'dict'>" :
					value_set['addr']= op[value_set['op']][profile][value_set['imm']]
				
				else :
					value_set['addr']= op[value_set['op']][profile][value_set['imm']][value_set['reg']]
	
		else:
			#for instructions such as push msg call printf, etc
			if value_set['addr']==None :
				value_set['addr']=5	

	if value_set['label']!=None :
		records.insert(Node(addr,'.text',value_set['label'],'label','  '))
	
	new_addr=addr+value_set['addr']
	return new_addr
	#print(org_line + '  ---> ' + str(value_set['addr']))
	#return [value_set['label'],value_set['addr']]

#==================================================================================================

def is_integer(s) :
	for i in s :
		if ord(i) not in range(48,58) and i!=' ' :
			return 0
	int_arr=list(map(int,s.split(' ')))
	return len(int_arr)

#==============================================================================
#to handle the variables that are strings as it is diff the way address is calculated for them
def handle_string(s,dtype) :
	
	s=s[::-1]
	actual_len=0
	if s[0]=='\"' :
		actual_len=len(s)-2

		if section=='.data' :
			if dtype=='db'  :
				return actual_len
			
			elif dtype=='dw' :
				if actual_len%2==0 :
					return actual_len
				else :
					return actual_len+ 2- actual_len%2

			elif dtype=='dd' :
				if actual_len%4==0 :
					return actual_len
				else :
					return actual_len+ 4- actual_len%4

			else :
				if actual_len%8==0 :
					return actual_len
				else :
					return actual_len+ 8- actual_len%8		

		if section == '.bss' :
			str_addr=""
			s=s[1:len(s)-1]

			for ch in s :
				
				if dtype=='resb' and s!='': 
					str_addr=str_addr+ hex( ord(ch) )[2:]

				elif dtype=='resw' : 
					str_addr=str_addr+ hex(ord(ch) * 2)[2:]

				elif dtype=='resd' : 
					str_addr=str_addr+ hex( ord(ch)*4 )[2:]
				
				else : 
					str_addr=str_addr+ hex( ord(ch)*8 )[2:]
			
			return int(str_addr,16)


	
	else :
		index=s.find('\"')
		extra_bytes=len(list(s[:index-1	].split(' ')))
		actual_len=len(s[:len(s)-index])-2

		if dtype=='db' :
			return actual_len + extra_bytes

		elif dtype=='dw' :
			total=actual_len + 2*extra_bytes
			if total%2==0 :
				return total
			else :
				return total + 2- total%8
		elif dtype=='dd' :
			total=actual_len + 4*extra_bytes
			if total%4==0 :
				return total
			else :
				return total + 4- total%4

		else :
			total=actual_len + 8*extra_bytes
			if total%8==0 :
				return total
			else :
				return total + 8- total%8
#================================================================


#=======THE PROGRAM STARTS HERE===================================
datatypes=['db','dw','dd','dq','dt','resb','resw','resd','resq']
section=None
records=llist()

#file_name=input("enter file name : ")
fp=open('prog1.asm')


prev_addr=0
new_addr=0
text_prev_addr=0

#----removing extra space which may behave as list element------------
for line in fp :
	line=line.strip()
	inst=line.split(' ')	
	
	for i in inst  :
		i=i.strip()

	#------------setting the section for reading lines-----------------
	
	if 'section' in inst :
		section = inst[-1]
		prev_addr=0
		new_addr=0

	if section == '.data' or section == '.bss' :

		#--------now looking for datatypes in line which will guarantee an associated variable----------- 
		
		temp_dtype=''
		for dtype in datatypes  :
			if dtype in inst :
				temp_dtype=dtype

				#getting the variables from the inst set now
				for i in inst :
					if i != '' and i!=' ' :
						var=inst[0]
						break
				
		#-------------assigning value of a variable-------------------------------

				value =  ' '.join(inst[2:])
				value=value.strip()
				string_flag=0
				string_addon_in_addr=0
				addon=0

				if is_integer(value) > 0 : #getting how many values, if more than one then its array
					addon=is_integer(value)

				else :
					string_flag=1
					string_addon_in_addr=handle_string(value,temp_dtype)
		
		#------------getting address of the variable-----------------------
				
				if temp_dtype== 'db' or temp_dtype== 'resb' :
					
					if temp_dtype=='db'  and string_flag!=1:
						new_addr= prev_addr + 1*addon
					
					elif string_flag==1:
						new_addr=prev_addr + string_addon_in_addr 
					
					else :
						
						new_addr = prev_addr + 1 * int(value)

				if temp_dtype== 'dw' or temp_dtype== 'resw' :
					
					if temp_dtype=='dw'   and string_flag!=1 :
						new_addr = prev_addr  + addon*2
					
					elif string_flag==1:
						new_addr=prev_addr + string_addon_in_addr 
					
					else :
						new_addr = prev_addr + 2 * int(value)

				if temp_dtype== 'dd' or temp_dtype== 'resd' :
					
					if temp_dtype=='dd'   and string_flag!=1 :
						new_addr = prev_addr + addon*4

					elif string_flag==1:
						new_addr=prev_addr + string_addon_in_addr 
					
					else :
						new_addr = prev_addr + 4 * int(value)

				if temp_dtype== 'dq' or temp_dtype== 'resq' :
					
					if temp_dtype=='dq' and string_flag!=1 :
						new_addr = prev_addr  + addon*8

					elif string_flag==1:
						new_addr=prev_addr + string_addon_in_addr 
					
					else :
						new_addr = prev_addr + 8 * int(value)
					
		#-------------------------------------------------------------------
				
				if temp_dtype not in ['resb','resw','resd'] :
				 	records.insert(Node(prev_addr,section,var,temp_dtype,value))		
				
				else : #bss section only reserves memory , it has only uninitialized variables,so no value attribute provided
					records.insert(Node(prev_addr,section,var,temp_dtype,' '))		
				prev_addr=new_addr	
				
	else :

		new_addr=get_inst_profile(line,text_prev_addr)
		text_prev_addr=new_addr
		
	
records.display()

#========================================================= THANK YOU !! =======================
