.MODEL SMALL
.STACK
.DATA
	;---------VARIABLES DECLARADAS (SIN ENTRADA DE DATOS)---------
	;dividendo, divisor, ultimo_digito, cociente, residuo
	dividendo      DW 1024D     ;inic. solicitada: 1024
	ultimo_digito  DW 3D        ;CAMBIA ESTE VALOR por tu ultimo digito de cedula (0..9)
	divisor        DW 0D        ;se determina segun reglas
	cociente       DW 0D
	residuo        DW 0D

	;---------MENSAJES EXACTOS DE SALIDA---------
	; Estas etiquetas son cadenas terminadas en '$' para INT 21h/AH=9.
	; Se imprimen con: LEA DX, msgX  -> MOV AH, 9 -> INT 21h
	msgLinea1      DB 'Mi ultimo digito de cedula es: ', '$'
	msgLinea2a     DB 13,10, 'El resultado de 1024/', '$'
	msgLinea2b     DB ' es:', 13,10, '$'
	msgCociente    DB 'Cociente: ', '$'
	msgResiduo     DB 13,10, 'Residuo: ', '$'
	msgNuevaLinea  DB 13,10, '$'

.CODE
	main PROC
		;Inicializar segmento de datos
		MOV AX, @DATA
		MOV DS, AX

		;---------DETERMINAR EL VALOR DE divisor SEGUN REGLAS---------
		;si ultimo_digito es 0 o 1, divisor = 9; en otro caso, divisor = ultimo_digito
		MOV AX, ultimo_digito
		CMP AX, 0
		JE set_div_9
		CMP AX, 1
		JE set_div_9
		MOV divisor, AX
		JMP div_ready
	set_div_9:
		MOV divisor, 9
	div_ready:

		;---------AJUSTE DEL DIVIDENDO SEGUN PARIDAD DEL ultimo_digito---------
		; Regla: si ultimo_digito es PAR -> dividendo = 1026; si es IMPAR -> 1023
		MOV AX, ultimo_digito
		TEST AX, 1              ;bit 0 = 0 (par), 1 (impar)
		JZ set_dividendo_1026   ;si es par
		MOV dividendo, 1023
		JMP dividendo_ready
	set_dividendo_1026:
		MOV dividendo, 1026
	dividendo_ready:

		;---------REALIZAR LA DIVISION: dividendo / divisor---------
		XOR DX, DX          ;parte alta en 0 antes de DIV
		MOV AX, dividendo   ;AX = dividendo
		MOV BX, divisor     ;BX = divisor
		DIV BX              ;DX:AX / BX -> AX(cociente), DX(residuo)
		MOV cociente, AX
		MOV residuo, DX

		;---------SALIDA EN CONSOLA (FORMATO EXACTO)---------
		;Linea 1: Mi ultimo digito de cedula es: D
		LEA DX, msgLinea1
		MOV AH, 9
		INT 21H
		; Nota: aqui se imprime 'divisor'. Si deseas mostrar el ultimo digito
		; real de cedula, cambia a: MOV AX, ultimo_digito
		MOV AX, divisor     ;D corresponde al valor del divisor utilizado
		CALL print_u16
		LEA DX, msgNuevaLinea
		MOV AH, 9
		INT 21H

		;Linea 2: El resultado de 1024/D es:
		LEA DX, msgLinea2a
		MOV AH, 9
		INT 21H
		MOV AX, divisor
		CALL print_u16
		LEA DX, msgLinea2b
		MOV AH, 9
		INT 21H

		;Linea 3: Cociente: Q
		LEA DX, msgCociente
		MOV AH, 9
		INT 21H
		MOV AX, cociente
		CALL print_u16

		;Linea 4: Residuo: R
		LEA DX, msgResiduo
		MOV AH, 9
		INT 21H
		MOV AX, residuo
		CALL print_u16
		LEA DX, msgNuevaLinea
		MOV AH, 9
		INT 21H

		;Terminar programa DOS
		MOV AX, 4C00H
		INT 21H

	main ENDP

	;------------------------------------------------------------
	;Rutina: print_u16
	;Imprime en DECIMAL un entero SIN SIGNO de 16 bits pasado en AX
	;------------------------------------------------------------
	print_u16 PROC
		PUSH AX
		PUSH BX
		PUSH CX
		PUSH DX

		MOV BX, 10          ;base decimal
		XOR CX, CX          ;contador de digitos

		;Caso especial: AX == 0 -> imprimir '0'
		CMP AX, 0
		JNE pu16_loop
		MOV DL, '0'
		MOV AH, 2
		INT 21H
		JMP pu16_done

	pu16_loop:
		;Mientras AX != 0
		XOR DX, DX          ;DX debe estar en 0 antes de DIV 10
		DIV BX              ;AX / 10 -> AX=cociente, DX=residuo
		PUSH DX             ;guardar residuo (digito)
		INC CX              ;aumentar # de digitos
		CMP AX, 0
		JNE pu16_loop

	pu16_print:
		CMP CX, 0
		JE pu16_done
		POP DX              ;recuperar digito
		DEC CX
		ADD DL, '0'        ;convertir a ASCII
		MOV AH, 2
		INT 21H             ;imprimir caracter
		JMP pu16_print

	pu16_done:
		; Punto unico de salida de print_u16: restaura registros y retorna.
		; Tanto el caso AX==0 como el flujo del bucle saltan aqui.
		POP DX
		POP CX
		POP BX
		POP AX
		RET
	print_u16 ENDP

END main
