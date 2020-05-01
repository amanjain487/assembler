section .data
	array dd 10,20,30,40
	a dd 4
	msg db "abcdefghijklmnopqrstuvwxyz",10,0

section .bss
	a7 resd 1
	b15 resb 1

section .text
	global main

main:	xor edx,edx
    jmp end
	mov ebx,35
	mov dword[a],ebx
	add edx,dword[ebx+ecx*2]
	mov edi,edx
	b:	inc dword[edx]
	dec dword[ebx]
	jmp c
	inc edx
	d:inc edi
	jmp b
	xor dword[a],10
	add dword[a],10
	or ecx,[ecx]
	sub dword[a],10
	cmp dword[a],10
	dec dword[ebx]
	jmp c
	inc edx
	inc edi
	jmp b
	add edx,dword[ebx+ecx*2]
	mov edi,edx
	inc dword[edx]
	dec dword[ebx]
	jmp c
	inc edx
	inc edi
	jmp b
	c:xor dword[a],10
	add dword[a],10
	or ecx,[ecx]
	sub dword[a],10
	cmp dword[a],10
	end: xor eax,15
