.model small
.stack
.data
.code

    main PROC
        
        ;----CICLO FOR USANDO -->LOOP-----
        ;Como funciona LOOP:
        ;1.Decrementa CX en 1 (CX=CX-1)
        ;2.Si el nuevo valor de CX no es cero,
        ;hace un salto al INICIO del BUCLE
        ;3.Si CX llega a CERO, no salta y el promgrama
        ;continua con las instrucciones siguientes
        
        ;IDEA CLAVE: LOOP es equivalente a repite mientras
        ;CX sea distinto de CERO 
        
        ;SINTAXIS: LOOP etiqueta
        
            ;etiqueta es el punto al que se quiere
            ;volver mientras CX sea distinto de CERO
            ;Antesde de usar LOOP, se debe cargar 
            ;CX con el numero de iteraciones que necesitemos
            
        
        ;MOV CX,6D ;repetir la accion 6 veces
        
        ;INICIO:
            ;ADD AL, 5D ; AL=AL+5 (6 veces)
            
            ;LOOP INICIO  
            
            
        ;----- WHILE --> LOOP--------
        
        ;LOOP por si solo no EVALUA NINGUNA CONDICION
        ;Por esta razon para simular un WHILE tenemos
        ;que combinar:
            ;1.Una comparacion inicial
            ;2.con LOOP como mecanismo de repeticion
        
        ;Ejemplo:
        
        ;MOV CX, 10D ; limite de seguridad
         
        ;INICIO:
           ; CMP AX, 6D  ;# de veces que queremos repetir
            ;JGE FIN     ;CONDICION DEL WHILE
            
            ;----instrucciones del while----
            
                ;ADD AX,1D ;Instruccion que se repite
            
           ; LOOP INICIO
            
            ;FIN:
                ;MOV DX, 0FFH  
                
                
                
          ;---- DO-WHILE -->LOOP-----
          
          ;MOV CX, N
          ;INICIO:
            ;-----INSTRUCCIONES DEL BUCLE----
            
               ;INSTRUCCION_1
               ;INSTRUCCION_2
               
               ;INSTRUCCION_N
               
            ;CMP REGISTRO, LIMITE
            ;JGE FIN
            
            
            ;LOOP INICIO
            
            
            ;FIN:
            
         ;-------EJEMPLO------------- 
         
          MOV CX, 10D
          
          INICIO:
            
            INC AX ;AX=AX+1
            
            CMP AX,5D ;NUMERO DE VECES A REPETIR
            JGE FIN
            
            LOOP INICIO
            
            
            FIN:
            
            MOV DX, 0FFH 
            
            
   
    main ENDP