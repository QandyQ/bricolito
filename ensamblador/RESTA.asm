.model small
.stack
.data
.code
    main PROC
      
      ;---------RESTA----------
      
      ;SUB DESTINO,FUENTE
      ;RESULTADO: se almacena en el destino
      
      ;Ejemplo: 10-4=+6
      
      MOV BH,10D
      MOV BL,4D
      
      ;SUB BH,BL ;BH=BH-BL=10-4 ;RESTA ENTRE REGISTRO
      
      ;4-10=-6
      
      SUB BL,BH  ;RESTA ENTRE REGISTRO
      
      ;RESTA CON VALOR INMEDIATO
      
      MOV AH,12D
      
      SUB AH,10D ; RESTA CON VALOR INMEDIATO 
             
    main ENDP