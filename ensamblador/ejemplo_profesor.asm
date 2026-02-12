.model small
.stack
.data
.code

    main PROC 
        ;---------EJEMPLO EN ESTILO DEL PROFESOR---------
        ;Ejercicio: Sumar los primeros N números naturales (N=5)
        ;Usando el registro CX como contador y AX como acumulador
        ;
        ;SINTAXIS:
        ;   LOOP etiqueta
        ;
        ;IDEA CLAVE:
        ;   LOOP decrementa CX y repite mientras CX sea distinto de CERO
        ;
        ;EJEMPLO:
        ;   MOV CX,5D
        ;   INICIO:
        ;       ADD AX,CX
        ;       LOOP INICIO
        ;
        ;Al finalizar, AX contiene la suma 5+4+3+2+1 = 15D
        
        ;-------INICIALIZACIONES-------
        XOR AX,AX       ;AX=0
        MOV CX,5D       ;# de iteraciones
        
        INICIO:
            ADD AX,CX   ;AX=AX+CX
            LOOP INICIO ;repite mientras CX!=0
        
        ;-------CONDICIONALES (DEMO)-------
        ;Si AX >= 10 entonces BH=0FFH, en caso contrario BL=0FFH
        CMP AX,10D
        JGE ES_MAYOR
        JLE ES_MENOR
        
        ES_MAYOR:
            MOV BH,0FFH ;marca caso mayor o igual
            ;JMP FIN    ;(opcional) evitar caida a ES_MENOR
        
        ES_MENOR:
            MOV BL,0FFH ;marca caso menor
        
        ;-------OPERADORES LÓGICOS (DEMO)-------
        ;Enmascarar y activar bits con AND/OR, invertir con NOT
        MOV AL,10111011B
        MOV AH,11001101B
        AND AL,AH       ;AL = AL AND AH
        OR  AL,AH       ;AL = AL OR  AH
        NOT AL          ;complemento
        
        ;Vaciar registros con XOR reg,reg (técnica habitual)
        XOR AX,AX
        XOR BX,BX
        XOR CX,CX
        XOR DX,DX
        
        FIN:
        
    main ENDP