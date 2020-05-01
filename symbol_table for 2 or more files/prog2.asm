section .data
	array dd 1,2,3,4
	a dd 40
	msg db "ABCDEFGHIJKLMNOPQRSTUVWXYZ",10,0

section .bss
	res resd 3

section .text
	global main

main:	xor ecx,ecx
	xor ebx,ebx
	lp:add ebx,dword[array+ecx*4]
	inc ecx
	cmp ecx,4
	jmp lp
	mov dword[res],ebx
	a:push dword[res]
	push msg
	add esp,8
