.MODEL SMALL
.STACK
.DATA
.CODE

    MAIN PROC
       ;------MULTIPLICACION DE 8 BITS-----
       
     ;EMU8086 realiza multiplicaciones SIN SIGNO
     ;A diferencia de la suma y la resta SOLO NECESITA UN PARAMETRO
     ;Solo se debe elegir el DESTINO, porque el otro 
     ;operando esta IMPLICITO (oculto)
     ;Sintaxis de la multiplicacion: MUL Destino
     ;el Destino puede ser una VARIABLE/RAM/REGISTRO
     
     ;El segundo operando es el IMPLICITO
     ;El resultado puede ocupar EL DOBLE DE BITS que sus operandos  
       
     ;-------MUL DE 8 BITS---------- 
     
     ;EL OPERANDO IMPLICITO ES: AL 
     ;EL OPERANDO EXPLICITO: REG/RAM/VAR
     ;RESULTADO: AX (16 BITS) 
     ;AL x Operando_8bits --> AX (16bits) 
     
     ;Ejemplo: 5x2=10
     
     ;MOV AL,5D ;IMPLICITO
     
     ;MOV AH,2D  ;SEGUNDO OPERANDO Y DESTINO
     
     ;MUL DESTINO:
     ;MUL AH  ;AH=ALxAH  
     
     ;Ejemplo2: 200(8bits)x4(8bits)=800(16bits)
     
     ;MOV BL,200d
     ;MOV AH,4d 
     ;AL x BH/Bl
     
     ;MUL BL; ALxBl=0xBl=AX   
     ;MUL AH; ALxBH=0xBH=AX 
     
     ;------------MULTIPLICACION DE 16 BITS------
     
     ;IMPLICITO: AX
     ;EL RESULTADO--> DX:AX  
     
     ;AX(16bits) x Operando(16bits)= DX:AX (32bits)
     ;MUL operando_16bits
     
     ;EJEMPLO:sin sobrepasar los 16bits--> 1000x20 
     
     
     ;MOV AX,1000D
     ;MOV BX,20D
     
     ;MUL BX ;RESULTADO-->DX:AX 
     
     ;EJEMPLO sobrepasando los 16 bits: 40000Dx2D
     
     MOV AX,40000D
     MOV CX, 2D
     
     MUL CX
     
     
    MAIN ENDP