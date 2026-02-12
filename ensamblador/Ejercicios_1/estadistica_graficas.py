# Análisis Estadístico con Gráficas - Similar a R Commander
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

# Configuración para gráficas en español
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)

print("=" * 60)
print("ANÁLISIS ESTADÍSTICO CON GRÁFICAS")
print("=" * 60)
print()

# ============================================
# EJEMPLO 1: DISTRIBUCIÓN NORMAL
# ============================================
print("1. DISTRIBUCIÓN NORMAL")
print("-" * 40)

# Generar datos
np.random.seed(42)
datos_normales = np.random.normal(loc=100, scale=15, size=1000)

# Estadísticas
print(f"Media: {np.mean(datos_normales):.2f}")
print(f"Desviación estándar: {np.std(datos_normales):.2f}")
print(f"Mediana: {np.median(datos_normales):.2f}")
print()

# Crear figura con múltiples gráficas
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Análisis de Distribución Normal', fontsize=16, fontweight='bold')

# Histograma
axes[0, 0].hist(datos_normales, bins=30, density=True, alpha=0.7, color='skyblue', edgecolor='black')
x = np.linspace(datos_normales.min(), datos_normales.max(), 100)
axes[0, 0].plot(x, stats.norm.pdf(x, np.mean(datos_normales), np.std(datos_normales)), 
                'r-', linewidth=2, label='Curva normal teórica')
axes[0, 0].set_title('Histograma con Curva Normal')
axes[0, 0].set_xlabel('Valores')
axes[0, 0].set_ylabel('Densidad')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Boxplot
axes[0, 1].boxplot(datos_normales, vert=True)
axes[0, 1].set_title('Diagrama de Caja')
axes[0, 1].set_ylabel('Valores')
axes[0, 1].grid(True, alpha=0.3)

# Q-Q Plot
stats.probplot(datos_normales, dist="norm", plot=axes[1, 0])
axes[1, 0].set_title('Q-Q Plot (Normalidad)')
axes[1, 0].grid(True, alpha=0.3)

# Gráfica de densidad
axes[1, 1].hist(datos_normales, bins=50, density=True, alpha=0.5, color='lightgreen', edgecolor='black')
axes[1, 1].set_title('Gráfica de Densidad')
axes[1, 1].set_xlabel('Valores')
axes[1, 1].set_ylabel('Densidad')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('c:/Users/ASUS/Documents/PAGINA/ensamblador/Ejercicios_1/grafica_normal.png', dpi=300, bbox_inches='tight')
print("✓ Gráfica guardada: grafica_normal.png")
print()

# ============================================
# EJEMPLO 2: COMPARACIÓN DE GRUPOS (ANOVA)
# ============================================
print("2. COMPARACIÓN DE GRUPOS (ANOVA)")
print("-" * 40)

# Datos de ejemplo: Efecto de 3 tratamientos
grupo_A = np.array([3, 2, 1, 1, 4, 2, 4, 3])
grupo_B = np.array([10, 9, 9, 8, 7, 8, 6, 7])
grupo_C = np.array([7, 6, 7, 6, 5, 4, 3, 6])

# Realizar ANOVA
f_stat, p_value = stats.f_oneway(grupo_A, grupo_B, grupo_C)

print(f"Estadístico F: {f_stat:.4f}")
print(f"Valor p: {p_value:.6f}")
if p_value < 0.05:
    print("✓ HAY diferencias significativas entre los grupos (p < 0.05)")
else:
    print("✗ NO hay diferencias significativas entre los grupos (p >= 0.05)")
print()

# Gráficas comparativas
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Análisis ANOVA - Comparación de Grupos', fontsize=16, fontweight='bold')

# Boxplot comparativo
datos_box = [grupo_A, grupo_B, grupo_C]
axes[0, 0].boxplot(datos_box, labels=['Grupo A', 'Grupo B', 'Grupo C'])
axes[0, 0].set_title('Diagrama de Caja por Grupo')
axes[0, 0].set_ylabel('Valores')
axes[0, 0].grid(True, alpha=0.3)

# Gráfica de barras con medias
medias = [np.mean(grupo_A), np.mean(grupo_B), np.mean(grupo_C)]
errores = [np.std(grupo_A), np.std(grupo_B), np.std(grupo_C)]
x_pos = np.arange(len(medias))
axes[0, 1].bar(x_pos, medias, yerr=errores, capsize=5, 
               color=['#ff9999', '#66b3ff', '#99ff99'], edgecolor='black', alpha=0.7)
axes[0, 1].set_xticks(x_pos)
axes[0, 1].set_xticklabels(['Grupo A', 'Grupo B', 'Grupo C'])
axes[0, 1].set_title('Medias por Grupo con Desviación Estándar')
axes[0, 1].set_ylabel('Media')
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Gráfica de puntos individuales
for i, grupo in enumerate([grupo_A, grupo_B, grupo_C]):
    x = np.full(len(grupo), i)
    axes[1, 0].scatter(x, grupo, alpha=0.6, s=100)
axes[1, 0].set_xticks([0, 1, 2])
axes[1, 0].set_xticklabels(['Grupo A', 'Grupo B', 'Grupo C'])
axes[1, 0].set_title('Valores Individuales por Grupo')
axes[1, 0].set_ylabel('Valores')
axes[1, 0].grid(True, alpha=0.3)

# Histograma superpuesto
axes[1, 1].hist(grupo_A, alpha=0.5, label='Grupo A', bins=8, color='red')
axes[1, 1].hist(grupo_B, alpha=0.5, label='Grupo B', bins=8, color='blue')
axes[1, 1].hist(grupo_C, alpha=0.5, label='Grupo C', bins=8, color='green')
axes[1, 1].set_title('Distribución de Valores por Grupo')
axes[1, 1].set_xlabel('Valores')
axes[1, 1].set_ylabel('Frecuencia')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('c:/Users/ASUS/Documents/PAGINA/ensamblador/Ejercicios_1/grafica_anova.png', dpi=300, bbox_inches='tight')
print("✓ Gráfica guardada: grafica_anova.png")
print()

# ============================================
# EJEMPLO 3: REGRESIÓN LINEAL
# ============================================
print("3. REGRESIÓN LINEAL")
print("-" * 40)

# Generar datos con relación lineal
x = np.linspace(0, 10, 50)
y = 2.5 * x + 5 + np.random.normal(0, 2, 50)

# Calcular regresión
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

print(f"Ecuación: y = {slope:.4f}x + {intercept:.4f}")
print(f"R² (coeficiente de determinación): {r_value**2:.4f}")
print(f"Correlación (r): {r_value:.4f}")
print(f"Valor p: {p_value:.6f}")
print()

# Gráficas de regresión
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Análisis de Regresión Lineal', fontsize=16, fontweight='bold')

# Gráfica de dispersión con línea de regresión
axes[0].scatter(x, y, alpha=0.6, s=50, label='Datos observados')
axes[0].plot(x, slope * x + intercept, 'r-', linewidth=2, label=f'y = {slope:.2f}x + {intercept:.2f}')
axes[0].set_title(f'Regresión Lineal (R² = {r_value**2:.4f})')
axes[0].set_xlabel('Variable X')
axes[0].set_ylabel('Variable Y')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Residuos
residuos = y - (slope * x + intercept)
axes[1].scatter(x, residuos, alpha=0.6, s=50)
axes[1].axhline(y=0, color='r', linestyle='--', linewidth=2)
axes[1].set_title('Gráfica de Residuos')
axes[1].set_xlabel('Variable X')
axes[1].set_ylabel('Residuos')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('c:/Users/ASUS/Documents/PAGINA/ensamblador/Ejercicios_1/grafica_regresion.png', dpi=300, bbox_inches='tight')
print("✓ Gráfica guardada: grafica_regresion.png")
print()

# ============================================
# EJEMPLO 4: PRUEBA CHI-CUADRADO
# ============================================
print("4. PRUEBA CHI-CUADRADO")
print("-" * 40)

# Tabla de contingencia
tabla = np.array([[28, 2],
                  [28, 2],
                  [23, 7],
                  [30, 0],
                  [26, 4]])

chi2, p_value, dof, expected = stats.chi2_contingency(tabla)

print(f"Chi-cuadrado: {chi2:.4f}")
print(f"Grados de libertad: {dof}")
print(f"Valor p: {p_value:.6f}")
print()
print("Valores observados:")
print(tabla)
print()
print("Valores esperados:")
print(expected.round(2))
print()

# Gráfica de chi-cuadrado
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Análisis Chi-Cuadrado', fontsize=16, fontweight='bold')

# Gráfica de barras agrupadas
x_pos = np.arange(5)
width = 0.35
axes[0].bar(x_pos - width/2, tabla[:, 0], width, label='Acuerdo', alpha=0.7)
axes[0].bar(x_pos + width/2, tabla[:, 1], width, label='Desacuerdo', alpha=0.7)
axes[0].set_xlabel('Pregunta')
axes[0].set_ylabel('Frecuencia')
axes[0].set_title('Distribución de Respuestas')
axes[0].set_xticks(x_pos)
axes[0].set_xticklabels([f'P{i+1}' for i in range(5)])
axes[0].legend()
axes[0].grid(True, alpha=0.3, axis='y')

# Heatmap de valores observados
im = axes[1].imshow(tabla, cmap='YlOrRd', aspect='auto')
axes[1].set_xticks([0, 1])
axes[1].set_xticklabels(['Acuerdo', 'Desacuerdo'])
axes[1].set_yticks(range(5))
axes[1].set_yticklabels([f'P{i+1}' for i in range(5)])
axes[1].set_title('Mapa de Calor - Frecuencias')
# Añadir valores en las celdas
for i in range(5):
    for j in range(2):
        axes[1].text(j, i, str(tabla[i, j]), ha='center', va='center', color='black', fontweight='bold')
plt.colorbar(im, ax=axes[1])

plt.tight_layout()
plt.savefig('c:/Users/ASUS/Documents/PAGINA/ensamblador/Ejercicios_1/grafica_chicuadrado.png', dpi=300, bbox_inches='tight')
print("✓ Gráfica guardada: grafica_chicuadrado.png")
print()

# ============================================
# MOSTRAR TODAS LAS GRÁFICAS
# ============================================
print("=" * 60)
print("ANÁLISIS COMPLETADO")
print("=" * 60)
print("Se han generado 4 archivos de gráficas en la carpeta:")
print("  - grafica_normal.png")
print("  - grafica_anova.png")
print("  - grafica_regresion.png")
print("  - grafica_chicuadrado.png")
print()
print("Mostrando gráficas...")
plt.show()
