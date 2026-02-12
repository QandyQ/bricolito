.model small
.stack
.data
.code
    main PROC
        
        ;----------OPERADORES LOGICOS-------
        
        ;----OPERADOR AND--------
        
        ;El resultado me da 1 si y solo si las entradas son 1
        ; se usa para ENMASCARAR BITS 
        
        ;SINTAXIS: AND destino, fuente
        
        MOV AL,10111011B
        MOV AH,11001101B
        ;RESL: 10001001B
        
        AND AL,AH
        
        ;----------OR----------
        
        ;SI al menos una entrada es 1 entocnes el resultado es 1
        ;se usa para ACTIVAR bits especificos
        ;sin alterar los bits de entrada
        
        MOV AL,10111011B
        MOV AH,11001101B
        ;RESL: 11111111B
        
        OR AL,AH 
        
        ;---------NOT---------
        ;INVIERTE LOS VALORES DE TODOS LOS BITS
        ;1->0
        ;0->1 
        ;se usa para encontrar el COMPLEMENTO
        ;o para realizar una INVERSAION DE MASCARA
          mov dx,0ffH
        
        NOT AL
        
        ;-----------XOR----------
        ;El resultado es 1 solo cuando los bits de
        ;entrada son DIFERENTES 
        
        ;ME SIRVE PARA VACIAR REGISTROS
        
        ;MOV AL,10111011B
        ;MOV AH,10111011B
        ;resl: 00000000b
        
        XOR ax,ax
        XOR bx,bx
        XOR cx,cx
        XOR dx,dx
        
       
    
    main ENDP