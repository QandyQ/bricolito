# ============================================
# ANÁLISIS ESTADÍSTICO CON R COMMANDER
# Script generado para análisis completo
# ============================================

# Limpiar el entorno
rm(list=ls())

# Configurar para gráficas en español (opcional)
# Sys.setlocale("LC_ALL", "Spanish")

cat("============================================\n")
cat("ANÁLISIS ESTADÍSTICO CON R COMMANDER\n")
cat("============================================\n\n")

# ============================================
# 1. ANÁLISIS DE DISTRIBUCIÓN NORMAL
# ============================================
cat("1. ANÁLISIS DE DISTRIBUCIÓN NORMAL\n")
cat("----------------------------------------\n")

# Generar datos normales
set.seed(42)
datos_normales <- rnorm(1000, mean=100, sd=15)

# Estadísticas descriptivas
cat("ESTADÍSTICAS DESCRIPTIVAS:\n")
cat(sprintf("Media: %.2f\n", mean(datos_normales)))
cat(sprintf("Mediana: %.2f\n", median(datos_normales)))
cat(sprintf("Desviación estándar: %.2f\n", sd(datos_normales)))
cat(sprintf("Varianza: %.2f\n", var(datos_normales)))
cat(sprintf("Mínimo: %.2f\n", min(datos_normales)))
cat(sprintf("Máximo: %.2f\n", max(datos_normales)))
cat("\n")

# Crear ventana de gráficas múltiples
windows()  # En Mac/Linux usar: quartz() o x11()
par(mfrow=c(2,2), mar=c(4,4,3,2))

# Histograma con curva normal
hist(datos_normales, breaks=30, prob=TRUE, 
     col="skyblue", border="black",
     main="Histograma con Curva Normal",
     xlab="Valores", ylab="Densidad")
curve(dnorm(x, mean=mean(datos_normales), sd=sd(datos_normales)), 
      add=TRUE, col="red", lwd=2)
legend("topright", legend="Curva normal teórica", col="red", lwd=2)

# Boxplot
boxplot(datos_normales, col="lightgreen", 
        main="Diagrama de Caja",
        ylab="Valores")
grid()

# Q-Q Plot (prueba de normalidad)
qqnorm(datos_normales, main="Q-Q Plot (Prueba de Normalidad)",
       pch=20, col="blue")
qqline(datos_normales, col="red", lwd=2)

# Gráfica de densidad
plot(density(datos_normales), main="Gráfica de Densidad",
     xlab="Valores", ylab="Densidad", lwd=2, col="darkblue")
polygon(density(datos_normales), col=rgb(0,0,1,0.3), border="darkblue")

# Prueba de normalidad Shapiro-Wilk
cat("PRUEBA DE NORMALIDAD (Shapiro-Wilk):\n")
shapiro_test <- shapiro.test(datos_normales[1:5000])  # máximo 5000 obs
print(shapiro_test)
cat("\n")

# ============================================
# 2. COMPARACIÓN DE GRUPOS (ANOVA)
# ============================================
cat("2. ANÁLISIS DE VARIANZA (ANOVA)\n")
cat("----------------------------------------\n")

# Datos de ejemplo: 3 tratamientos
Grupo_A <- c(3, 2, 1, 1, 4, 2, 4, 3)
Grupo_B <- c(10, 9, 9, 8, 7, 8, 6, 7)
Grupo_C <- c(7, 6, 7, 6, 5, 4, 3, 6)

# Crear data frame
datos_anova <- data.frame(
  Valor = c(Grupo_A, Grupo_B, Grupo_C),
  Grupo = factor(rep(c("Tratamiento_A", "Tratamiento_B", "Tratamiento_C"), 
                     each=8))
)

# Estadísticas por grupo
cat("ESTADÍSTICAS POR GRUPO:\n")
print(tapply(datos_anova$Valor, datos_anova$Grupo, summary))
cat("\n")

cat("MEDIAS Y DESVIACIONES ESTÁNDAR:\n")
medias <- tapply(datos_anova$Valor, datos_anova$Grupo, mean)
desviaciones <- tapply(datos_anova$Valor, datos_anova$Grupo, sd)
print(data.frame(Media=medias, DE=desviaciones))
cat("\n")

# ANOVA
modelo_anova <- aov(Valor ~ Grupo, data=datos_anova)
cat("TABLA ANOVA:\n")
print(summary(modelo_anova))
cat("\n")

# Prueba post-hoc de Tukey (si hay diferencias significativas)
cat("PRUEBA POST-HOC DE TUKEY:\n")
tukey_result <- TukeyHSD(modelo_anova)
print(tukey_result)
cat("\n")

# Gráficas para ANOVA
windows()
par(mfrow=c(2,2), mar=c(5,4,3,2))

# Boxplot por grupos
boxplot(Valor ~ Grupo, data=datos_anova, 
        col=c("#ff9999", "#66b3ff", "#99ff99"),
        main="Comparación de Grupos (Boxplot)",
        xlab="Grupo", ylab="Valores",
        las=2)  # las=2 para etiquetas verticales

# Gráfica de barras con error
barplot(medias, col=c("#ff9999", "#66b3ff", "#99ff99"),
        main="Medias por Grupo",
        ylab="Media", las=2,
        ylim=c(0, max(medias)+3))
arrows(x0=c(0.7, 1.9, 3.1), y0=medias-desviaciones,
       x1=c(0.7, 1.9, 3.1), y1=medias+desviaciones,
       angle=90, code=3, length=0.1)

# Gráfica de puntos
stripchart(Valor ~ Grupo, data=datos_anova, 
           vertical=TRUE, method="jitter",
           pch=19, col=c("red", "blue", "green"),
           main="Valores Individuales por Grupo",
           xlab="Grupo", ylab="Valores")

# Gráfica de interacción (línea de medias)
plot(1:3, medias, type="b", pch=19, col="darkblue", lwd=2,
     main="Gráfica de Medias",
     xlab="Grupo", ylab="Media",
     xaxt="n", ylim=c(0, max(medias)+1))
axis(1, at=1:3, labels=names(medias), las=2)
grid()

# ============================================
# 3. REGRESIÓN LINEAL
# ============================================
cat("3. ANÁLISIS DE REGRESIÓN LINEAL\n")
cat("----------------------------------------\n")

# Generar datos con relación lineal
set.seed(123)
x <- seq(0, 10, length.out=50)
y <- 2.5*x + 5 + rnorm(50, sd=2)

# Modelo de regresión
modelo_regresion <- lm(y ~ x)

cat("RESUMEN DEL MODELO:\n")
print(summary(modelo_regresion))
cat("\n")

# Coeficientes
coef <- coef(modelo_regresion)
cat(sprintf("Ecuación: y = %.4f * x + %.4f\n", coef[2], coef[1]))
cat(sprintf("R²: %.4f\n", summary(modelo_regresion)$r.squared))
cat(sprintf("R² ajustado: %.4f\n", summary(modelo_regresion)$adj.r.squared))
cat("\n")

# Gráficas de regresión
windows()
par(mfrow=c(2,2), mar=c(4,4,3,2))

# Gráfica de dispersión con línea de regresión
plot(x, y, pch=19, col="blue", 
     main="Regresión Lineal",
     xlab="Variable X", ylab="Variable Y")
abline(modelo_regresion, col="red", lwd=2)
legend("topleft", 
       legend=sprintf("y = %.2fx + %.2f\nR² = %.4f", 
                     coef[2], coef[1], summary(modelo_regresion)$r.squared),
       bty="n")
grid()

# Gráfica de residuos vs valores ajustados
plot(fitted(modelo_regresion), residuals(modelo_regresion),
     pch=19, col="darkgreen",
     main="Residuos vs Valores Ajustados",
     xlab="Valores Ajustados", ylab="Residuos")
abline(h=0, col="red", lwd=2, lty=2)
grid()

# Q-Q Plot de residuos
qqnorm(residuals(modelo_regresion), pch=19, col="purple",
       main="Q-Q Plot de Residuos")
qqline(residuals(modelo_regresion), col="red", lwd=2)

# Histograma de residuos
hist(residuals(modelo_regresion), breaks=15, 
     col="lightblue", border="black",
     main="Histograma de Residuos",
     xlab="Residuos", ylab="Frecuencia")

# ============================================
# 4. PRUEBA CHI-CUADRADO
# ============================================
cat("4. PRUEBA DE CHI-CUADRADO\n")
cat("----------------------------------------\n")

# Crear tabla de contingencia
tabla <- matrix(c(28, 2,
                  28, 2,
                  23, 7,
                  30, 0,
                  26, 4), 
                nrow=5, byrow=TRUE)
dimnames(tabla) <- list(
  Pregunta=paste0("P", 1:5),
  Respuesta=c("Acuerdo", "Desacuerdo")
)

cat("TABLA DE CONTINGENCIA (Valores Observados):\n")
print(tabla)
cat("\n")

# Realizar prueba chi-cuadrado
prueba_chi <- chisq.test(tabla, correct=FALSE)

cat("RESULTADOS DE LA PRUEBA CHI-CUADRADO:\n")
print(prueba_chi)
cat("\n")

cat("VALORES ESPERADOS:\n")
print(round(prueba_chi$expected, 2))
cat("\n")

# Valor crítico
alpha <- 0.05
valor_critico <- qchisq(1-alpha, df=prueba_chi$parameter)
cat(sprintf("Valor crítico (α = %.2f): %.4f\n", alpha, valor_critico))
cat("\n")

# Interpretación
if(prueba_chi$p.value < alpha) {
  cat("CONCLUSIÓN: Se rechaza H0. Hay diferencias significativas.\n")
} else {
  cat("CONCLUSIÓN: No se rechaza H0. No hay diferencias significativas.\n")
}
cat("\n")

# Gráficas para Chi-cuadrado
windows()
par(mfrow=c(2,2), mar=c(5,4,3,2))

# Gráfica de barras agrupadas
barplot(t(tabla), beside=TRUE, 
        col=c("lightblue", "pink"),
        main="Distribución de Respuestas",
        xlab="Pregunta", ylab="Frecuencia",
        legend.text=TRUE,
        args.legend=list(x="topright", bty="n"))

# Gráfica de barras apiladas
barplot(t(tabla), 
        col=c("lightblue", "pink"),
        main="Respuestas Apiladas",
        xlab="Pregunta", ylab="Frecuencia",
        legend.text=TRUE,
        args.legend=list(x="topright", bty="n"))

# Mosaico
mosaicplot(tabla, color=c("lightblue", "pink"),
           main="Gráfica de Mosaico",
           xlab="Pregunta", ylab="Respuesta")

# Gráfica de proporciones
proporciones <- prop.table(tabla, margin=1)
barplot(t(proporciones), 
        col=c("lightblue", "pink"),
        main="Proporciones por Pregunta",
        xlab="Pregunta", ylab="Proporción",
        legend.text=TRUE,
        args.legend=list(x="topright", bty="n"),
        ylim=c(0, 1))

 y_val <- dchisq(chi_calc, df=df)
 points(chi_calc, y_val, pch=19, col="blue")
 text(chi_calc, y_val, labels=paste("Chi^2 =", chi_calc), pos=4, col="blue")

# ============================================
# 5. CORRELACIÓN
# ============================================
cat("5. ANÁLISIS DE CORRELACIÓN\n")
cat("----------------------------------------\n")

# Generar datos correlacionados
set.seed(456)
var1 <- rnorm(100)
var2 <- 0.7*var1 + rnorm(100, sd=0.5)
var3 <- -0.5*var1 + rnorm(100, sd=0.5)

# Crear data frame
datos_cor <- data.frame(Variable1=var1, Variable2=var2, Variable3=var3)

# Matriz de correlación
cat("MATRIZ DE CORRELACIÓN:\n")
matriz_cor <- cor(datos_cor)
print(round(matriz_cor, 4))
cat("\n")

# Pruebas de correlación
cat("CORRELACIÓN Variable1 vs Variable2:\n")
cor_test1 <- cor.test(var1, var2)
print(cor_test1)
cat("\n")

# Gráfica de correlaciones
windows()
par(mfrow=c(2,2), mar=c(4,4,3,2))

# Gráficas de dispersión
plot(var1, var2, pch=19, col="blue",
     main=sprintf("Correlación = %.3f", cor(var1, var2)),
     xlab="Variable 1", ylab="Variable 2")
abline(lm(var2 ~ var1), col="red", lwd=2)
grid()

plot(var1, var3, pch=19, col="red",
     main=sprintf("Correlación = %.3f", cor(var1, var3)),
     xlab="Variable 1", ylab="Variable 3")
abline(lm(var3 ~ var1), col="blue", lwd=2)
grid()

plot(var2, var3, pch=19, col="green",
     main=sprintf("Correlación = %.3f", cor(var2, var3)),
     xlab="Variable 2", ylab="Variable 3")
abline(lm(var3 ~ var2), col="purple", lwd=2)
grid()

# Matriz de pares
pairs(datos_cor, pch=19, col="darkblue",
      main="Matriz de Gráficas de Dispersión")

# ============================================
# RESUMEN FINAL
# ============================================
cat("============================================\n")
cat("ANÁLISIS COMPLETADO\n")
cat("============================================\n")
cat("Se han generado 5 ventanas de gráficas:\n")
cat("  1. Análisis de Distribución Normal\n")
cat("  2. Comparación de Grupos (ANOVA)\n")
cat("  3. Regresión Lineal\n")
cat("  4. Prueba Chi-Cuadrado\n")
cat("  5. Análisis de Correlación\n")
cat("\n")
cat("Presiona Enter para cerrar todas las ventanas...\n")
readline()

# Cerrar todas las ventanas de gráficas
graphics.off()

cat("\n¡Análisis finalizado!\n")
