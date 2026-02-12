.MODEL SMALL
.STACK
.DATA
.CODE
    MAIN PROC
        
        ;--------DIVISION------
        
        ;Es una instruccion de un SOLO OPERANDO
        ;El DIVIDENDO se encuentra en un registro IMPLICITO
        ;El DIVISOR es EXPLICITO
        ;El RESULTADO:
                ;COCIENTE:AL
                ;RESIDUO: AH 
                
                
        ;------DIVISION 8 BITS------
        ;DIVIDENDO: AX (IMPLICITO)
        ;DIVISOR: REG/RAM/VAR 8 BITS
        
        ;SINTAXIS: DIV operando_explicito 
        
        ; dividendo/divisor = cociente y residuo
        
        ;AX / Operando_8bits --> AL (Cociente) y En AH el RESIDUO
        
        
        ;EJEMPLO:DIVISION EXACTA DE 8 BITS
        
        ;100/5
        
        ;MOV AX,100D
        ;MOV BL,5D 
        
        ;DIV BL
        
        ;EJEMPLO: DIVISION NO EXACTA DE 8 BITS
        
        ;MOV AX,20D
        ;MOV CH,3D
        
        ;DIV CH
        
        ;-----------DIVISION DE 16 BITS---------
        
        
        ;REGISTROS INVOLUCRADOS:
            ;Dividendo--> DX:AX (32bits)
            ;Divisor: reg/var/ram 16 bits
            ;Cociente: AX
            ;Residuo: DX  
         ;DX:AX / Operando_16bits --> AX(cociente) y en DX (Residuo) 
         
         
         ;Ejemplo: 1000/2
         
         ;MOV DX,0D ;ME ASEGURO QUE LA PARTE ALTA ESTE VACIA
         
         ;MOV AX,1000D
         ;MOV BX,2D
         
         ;DIV BX
                 
                 
         ;Ejemplo: 1000/3
         
         ;MOV DX,0D ;ME ASEGURO QUE LA PARTE ALTA ESTE VACIA
         
         ;MOV AX,1000D
         ;MOV CX,3D
         
         ;DIV CX
         
         ;ERRORES COMUNES:
         
         ;No limpiar DX antes de la division
         ;Divisiones por cero
         ;Cociente sea demasiado GRANDE
         
         
         ;implicito: AX dividendo
         
         ;cociente->Al
         ;Residuo->Ah
         
          ;600/2 
          
         ;Ejemplo de cociente demasiado GRANDE 
          ;MOV AX,600D
          ;MOV BL,2D
          
          ;DIV BL 
          
          
         ;80000/10000
         
         MOV DX,1B
         MOV AX,11100010000000B ;COLOCO EL 80MIL EN BINARIO
         
         MOV BX,1001D
         
         DIV BX
         
            
    MAIN ENDP