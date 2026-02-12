.model small
.stack
.data
.code
    main PROC 
        
       ;OPERACIONES ARITMETICAS
       
       ;--------SUMA-----------
       
       ;ADD destino,fuente 
       ;Destino y la fuente pueden ser: registro/variable/ram
       ;El resultado siempre se almacena en el DESTINO
       ;ADD X,Y --> X=X+Y 
       
       ;EJEMPLO: 5+2=7
       
       ;SUMA DE 8 BITS: ENTRE REGISTROS
       
       MOV AH,5D ;CARGANDO VALORES EN AH
       MOV AL,2D ;CARGANDO VALORES EN AL
       
       ADD AH,AL ;SUMA: AH=AH+AL 
       
       ;SUMA DE 8 BITS: SUMA CON VALOR INMEDIATO
       
       ADD AH,3D ;SUMA CON VALOR INMEDIATO
       
       ;SUMA DE 8 BITS: DESBORDAMIENTO
       
       MOV BL,255D
       MOV BH,1D
                       
       ADD BL,BH ;BL=BL+BH
       
       ;SUMA DE 16 BITS:
       
       MOV CX,65534D
       MOV DX,1D
       
       ADD CX,DX ;CX=CX+DX

                
    main ENDP