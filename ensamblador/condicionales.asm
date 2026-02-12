.model small
.stack
.data
.code

    main PROC 
        ;--------BLOQUES CONDICIONALES (IF)--------
       
       
        ;IF (CONDICION) ENTONCES
        ;INSTRUCCCION1
        ;END IF
        
        inicio:
        MOV AH,50D
        MOV AL,50D
        
        CMP AH,AL ; 50<100 
        
        ;JNE NO_SON_IGUALES 
        ;JE  SON_IGUALES
        
        ;JGE es_mayor
        
        JLE es_menor
        
        MOV CX,2D
        MOV DX,3D
        MOV AX,1D
        
        
        SON_IGUALES:
         MOV BL,0FFH
         
         
        NO_SON_IGUALES:
            MOV BH,0FFH 
            
        
        es_mayor:
        
            mov cl,0ffh
                 
   
        es_menor:
        
            mov ch,0ffh
            
        
        
       
        
    
    main ENDP