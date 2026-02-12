# ANOVA DE UNA VÍA - Efecto de pastillas en presión arterial
# H0: No hay diferencia en la presión arterial entre los grupos
# H1: Al menos un grupo tiene diferencia significativa

# Datos de presión arterial (escala 1-10) para 3 grupos con diferentes pastillas
set.seed(123)  # Para reproducibilidad
Grupo_A <- c(3, 2, 1, 1, 4, 2, 4, 3)
Grupo_B <- c(10, 9, 9, 8, 7, 8, 6, 7)
Grupo_C <- c(7, 6, 7, 6, 5, 4, 3, 6)

# Crear data frame
datos <- data.frame(
  Presion = c(Grupo_A, Grupo_B, Grupo_C),
  Grupo = factor(rep(c("Pastilla_A", "Pastilla_B", "Pastilla_C"), each=8))
)

# Mostrar datos
print("=== DATOS DEL EXPERIMENTO ===")
print(datos)
print("")

# Estadísticas descriptivas por grupo
print("=== ESTADÍSTICAS DESCRIPTIVAS POR GRUPO ===")
tapply(datos$Presion, datos$Grupo, summary)
print("")

# ANOVA de una vía
print("=== ANOVA DE UNA VÍA ===")
modelo_anova <- aov(Presion ~ Grupo, data=datos)
resumen <- summary(modelo_anova)
print(resumen)
print("")

# CÁLCULOS MANUALES PASO A PASO
print("=== CÁLCULOS MANUALES ===")

# Medias por grupo
media_A <- mean(Grupo_A)
media_B <- mean(Grupo_B)
media_C <- mean(Grupo_C)
media_total <- mean(datos$Presion)

print(paste("Media Grupo A:", round(media_A, 4)))
print(paste("Media Grupo B:", round(media_B, 4)))
print(paste("Media Grupo C:", round(media_C, 4)))
print(paste("Media Total:", round(media_total, 4)))
print("")

# Tamaños de muestra
n <- 8  # por grupo
k <- 3   # número de grupos
N <- n * k  # total de observaciones

# Grados de libertad
gl_entre <- k - 1  # grados de libertad entre grupos
gl_dentro <- N - k  # grados de libertad dentro de grupos
gl_total <- N - 1

print(paste("Grados de libertad entre grupos (k-1):", gl_entre))
print(paste("Grados de libertad dentro de grupos (N-k):", gl_dentro))
print(paste("Grados de libertad totales (N-1):", gl_total))
print("")

# Suma de cuadrados entre grupos (SCE)
SCE <- n * sum((c(media_A, media_B, media_C) - media_total)^2)
print(paste("Suma de Cuadrados Entre grupos (SCE):", round(SCE, 4)))

# Suma de cuadrados dentro de grupos (SCD)
SCD <- sum((Grupo_A - media_A)^2) + 
       sum((Grupo_B - media_B)^2) + 
       sum((Grupo_C - media_C)^2)
print(paste("Suma de Cuadrados Dentro de grupos (SCD):", round(SCD, 4)))

# Cuadrados medios
CME <- SCE / gl_entre  # Varianza entre grupos
CMD <- SCD / gl_dentro  # Varianza dentro de grupos

print(paste("Cuadrado Medio Entre grupos (CME - Varianza entre):", round(CME, 4)))
print(paste("Cuadrado Medio Dentro de grupos (CMD - Varianza dentro):", round(CMD, 4)))
print("")

# Estadístico F
F_calculado <- CME / CMD
print(paste("Estadístico F calculado = CME/CMD =", round(F_calculado, 4)))
print("")

# Valor crítico y p-value
alpha <- 0.05
F_critico <- qf(1-alpha, gl_entre, gl_dentro)
p_value <- pf(F_calculado, gl_entre, gl_dentro, lower.tail=FALSE)

print(paste("Valor crítico F(", gl_entre, ",", gl_dentro, ") con alpha=0.05:", round(F_critico, 4)))
print(paste("P-value:", format(p_value, scientific=TRUE)))
print("")

# Decisión
print("=== CONCLUSIÓN ===")
if (p_value < alpha) {
  print("RECHAZAMOS H0: Hay diferencias significativas entre al menos un grupo")
} else {
  print("NO RECHAZAMOS H0: No hay diferencias significativas entre los grupos")
}
print("")

# Configurar para mostrar ambos gráficos juntos
par(mfrow=c(1,2))  # 1 fila, 2 columnas

# GRÁFICO 1: Diagrama de Caja y Bigotes
print("Generando gráfico de caja y bigotes...")
boxplot(Presion ~ Grupo, data=datos,
        main="Efecto de Pastillas en Presión Arterial",
        xlab="Tipo de Pastilla",
        ylab="Presión Arterial (escala 1-10)",
        col=c("lightblue", "lightgreen", "lightcoral"),
        border="darkblue",
        notch=FALSE)

# Agregar las medias al gráfico
points(1:3, c(media_A, media_B, media_C), 
       col="red", pch=19, cex=1.5)
legend("topright", legend="Media", col="red", pch=19)

# GRÁFICO 2: Distribución F (Campana de Gauss)
print("Generando gráfico de distribución F...")
x <- seq(0, 20, length=1000)
y <- df(x, gl_entre, gl_dentro)

plot(x, y, type="l", lwd=2, col="blue",
     main=paste("Distribución F(", gl_entre, ",", gl_dentro, ")"),
     xlab="Valor F",
     ylab="Densidad",
     xlim=c(0, max(F_calculado + 5, F_critico + 5)))

# Área de rechazo
x_rechazo <- seq(F_critico, max(x), length=100)
y_rechazo <- df(x_rechazo, gl_entre, gl_dentro)
polygon(c(F_critico, x_rechazo, max(x)), 
        c(0, y_rechazo, 0), 
        col=rgb(1,0,0,0.3), border=NA)

# Líneas verticales
abline(v=F_critico, col="red", lwd=2, lty=2)
abline(v=F_calculado, col="darkgreen", lwd=2, lty=1)

# Leyenda
legend("topright", 
       legend=c(paste("F crítico =", round(F_critico, 2)),
                paste("F calculado =", round(F_calculado, 2)),
                paste("Área de rechazo (alpha=", alpha, ")", sep="")),
       col=c("red", "darkgreen", rgb(1,0,0,0.3)),
       lwd=c(2, 2, 10),
       lty=c(2, 1, 1))

print("¡Análisis ANOVA completado!")
