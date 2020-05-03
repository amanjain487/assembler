section .data
	
msg db "%d",10,0

	a dd "abcd","ab"
	d5 dd 100

section .bss
	

	 
	r3 resq 2

section .text
	global main
	extern printf
	main: xor eax,ecx
	jmp end
	l1 mov eax,dword[a]
	add eax,1000
	or eax,dword[eax]
    	cmp eax,dword[a+1000]
    	jmp sib
    	mov eax,dword[ecx+1000]
	sib: mov eax,dword[eax+eax*4]
	cmp dword[a],1000
	mem:   mov dword[eax], eax
	sub eax,1000
	add dword[100+eax*3],1000
	jnz l1
	jz mem
	inc eax
	inc dword[a]
	dec dword[a+1000]
	inc dword[a+eax*2]
	push esi
	push dword[a+1000]
	push msg
	push 1000
	mul ecx
	mul dword[a]
	mul dword[ecx+100]
	mul dword[a+ecx*4]
	call printf
	call dword[ecx+eax*4]
	call msg
	end:  call 1000



