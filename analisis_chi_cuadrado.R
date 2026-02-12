tab <- matrix(c(28,2,
                28,2,
                23,7,
                30,0,
                26,4), nrow=5, byrow=TRUE)
dimnames(tab) <- list(Pregunta=paste0("P",1:5),
                      Respuesta=c("Acuerdo","Desacuerdo"))

# Imprimir tabla original
print("Tabla con valores observados:")
print(tab)

prueba <- chisq.test(tab, correct=FALSE)
prueba

# Imprimir tabla con valores esperados
print("Tabla con valores esperados:")
print(prueba$expected)

# Calcular y mostrar el valor crítico
alpha <- 0.05
critico <- qchisq(1-alpha, df=prueba$parameter)
print(paste("Valor crítico con alpha =", alpha, ":", critico))
