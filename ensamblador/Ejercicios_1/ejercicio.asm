.model small
.stack
.data 
    msg1 db 10d, 13d, 'Mi dia de nacimiento es: $'
    msg2 db 10d, 13d, 'Mi divisor es: $'
    msg3 db 10d, 13d, 'EL resultado de 1536/$'
    msg4 db 10d, 13d, ' : $'
    msg5 db 10d, 13d, 'Cociente: $'
    msg6 db 10d, 13d, 'Residuo: $'
    
    
    base_valor  dw  1536d
    dia_nacimiento  dw 2d
    ultimo_digito   dw ?
    divisor dw  ?
    cociente    dw   ?
    residuo dw  ?



.code

main proc  
          
    mov ax, @data
    mov ds, ax
    xor ax, ax
    
    mov ah, 09h
    mov dx, offset msg1
    int 21h
    
    mov ax, dia_nacimiento
    add ax, 30h
    mov ah, 02h
    mov dx, ax
    int 21h
    
    
    
    
    mov ah, 09h
    mov dx, offset msg2
    int 21h
    
    
    mov ah, 09h
    mov dx, offset msg3
    int 21h  
    mov ax, dia_nacimiento
    add ax, 30h
    mov ah, 02h
    mov dx, ax
    int 21h
    
    ;obtener ultimo digito
    xor dx, dx
    mov ax, dia_nacimiento
    mov bx, 10d
    div bx
    
    mov ultimo_digito, dx 
    
    cmp dx, 0d
    je cambiar_divisor
    
    cmp dx, 1d
    je cambiar_divisor
    
    mov divisor, dx
    jmp continuar
    
    
    cambiar_divisor:
    mov divisor, 8d   
                    
                    
    continuar: 
    
    ;verificar si base_valor es par o impar
    xor dx, dx
    mov ax, base_valor
    mov bx, 2d
    div bx 
    
    cmp dx, 0d
    je par
    
    sub base_valor, 2d
    jmp continuar2
    
    
    
    par:
    add base_valor, 3d
    
    
    continuar2:
    
    
    ;5.division base_valor/divisor
    xor dx, dx
    mov ax, base_valor
    mov bx, divisor
    div bx
    
    mov cociente, ax
    mov residuo, dx
      
    
                          


main endp