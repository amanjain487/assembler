section .data
	msg db "%d",10,0
	w1 dw "abcd",10,0
	a dd "abcd",10,1,"abc"
	d5 dd 100

section .bss
	r1 resb "abc"
	r2 resb 10
	r3 resw 2
	r5 resd 1

section .text
	global main
	extern printf
	main: xor eax,ecx
	l1: mov eax,dword[a]
	add eax,1000
	or eax,dword[eax]
    cmp eax,dword[a+1000]
    jmp sib
    mov eax,dword[ecx+1000]
	sib: mov eax,dword[eax+eax*2]
	jmp sib
	cmp dword[a],1000
	mem:    mov dword[eax], eax
	sub dword[a+1000],1000
	jmp mem
	add dword[esi+eax*2],1000
	jnz sib
	jz mem
	inc eax
	inc dword[a]
	dec dword[a+1000]
	inc dword[a+eax*2]
	push eax
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
	end:    call 1000

