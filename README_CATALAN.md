# 📊 Números de Catalan - Problema de la Mesa Redonda

Un programa interactivo en Python que genera y visualiza **todas las formas posibles** de que personas alrededor de una mesa redonda se saluden sin que los saludos se crucen.

## 🎯 ¿Qué son los Números de Catalan?

Los **números de Catalan** son una secuencia de números naturales que aparecen en muchos problemas combinatorios:

$$C_n = \frac{(2n)!}{(n+1)! \cdot n!}$$

**Secuencia:** C(0)=1, C(1)=1, C(2)=2, C(3)=5, C(4)=14, C(5)=42, C(6)=132...

## 🤝 El Problema de la Mesa Redonda

Si **n personas** se sientan alrededor de una mesa redonda, ¿**de cuántas formas pueden saludarse SIN que los saludos se crucen?**

**RESPUESTA:** $C(n/2)$ formas (donde n debe ser par)

### Ejemplo con 4 Personas

Personas: 0, 1, 2, 3 alrededor del círculo

| Configuración | Saludos | Válido |
|---------------|---------|--------|
| 1 | 0↔1, 2↔3 | ✅ |
| 2 | 0↔3, 1↔2 | ✅ |
| 3 | 0↔2, 1↔3 | ❌ ¡Se cruzan! |

**Total:** 2 formas = C(2) ✓

## 🚀 Cómo Usar

### Instalación

```bash
# Python 3.8+
pip install matplotlib numpy
```

### Ejecución Modo Interactivo

```bash
python catalan.py
```

Menú interactivo con opciones:
1. **Ver secuencia de números de Catalan** - Muestra los primeros N números
2. **Hallar saludos sin cruces** - Ingresa número de personas y ve todas las configuraciones
3. **Explicación** - Comprende la teoría detrás de los números de Catalan
4. **Salir**

### Ejemplo de Ejecución

```
NÚMEROS DE CATALAN - MESA REDONDA

¿Qué deseas hacer?
1. 📊 Ver secuencia de números de Catalan
2. 🔵 Hallar saludos sin cruces en una mesa redonda
3. ℹ️  Explicación de números de Catalan
4. ❌ Salir

Selecciona una opción (1-4): 2
ℹ️  Los saludos solo funcionan con número PAR de personas
¿Cuántas personas están en la mesa? (2-12, número par): 6

PROBLEMA DE LA MESA REDONDA (6 personas)
============================================================

🔵 Personas alrededor de la mesa: 6
🤝 Saludos que cada persona hace: 3

📊 Número de formas de saludarse SIN que se crucen:
    C(3) = 5 formas

✅ Configuraciones encontradas: 5

DETALLE DE CADA CONFIGURACIÓN:
  1. Saludos: 0↔1, 2↔3, 4↔5
  2. Saludos: 0↔1, 2↔5, 3↔4
  3. Saludos: 0↔3, 1↔2, 4↔5
  4. Saludos: 0↔5, 1↔2, 3↔4
  5. Saludos: 0↔5, 1↔4, 2↔3
```

## 📊 Visualización Gráfica

El programa genera **gráficas automáticas** mostrando:
- Círculo con las personas distribuidas
- Diferentes colores para cada saludo
- Todas las configuraciones posibles sin cruces

## 🔧 Estructura del Programa

### Clases Principales

#### `NumerosCatalan`
Calcula números de Catalan usando:
- **Fórmula directa:** $(2n)! / ((n+1)! \times n!)$
- **Recursión con memoización**
- **Generación de secuencias**

#### `MesaRedonda`
Maneja la lógica de mesa redonda:
- Distribuye personas en círculo
- Detecta si dos saludos se cruzan
- Genera todas las configuraciones válidas
- Visualiza gráficamente

### Algoritmo Principal: Backtracking

El programa usa **búsqueda recursiva (backtracking)** para encontrar todas las combinaciones válidas:

```python
1. Tomar primer elemento disponible
2. Intentar conectarlo con cada otro elemento
3. Verificar que NO se cruza con conexiones existentes
4. Si es válido, recursivamente procesar el resto
5. Deshacer conexión y probar la siguiente
```

## 📈 Rendimiento y Límites

| Personas | Configuraciones | Tiempo |
|----------|-----------------|--------|
| 2 | 1 (C(1)) | < 1ms |
| 4 | 2 (C(2)) | < 1ms |
| 6 | 5 (C(3)) | < 5ms |
| 8 | 14 (C(4)) | < 50ms |
| 10 | 42 (C(5)) | ~ 200ms |
| 12 | 132 (C(6)) | ~ 1s |
| 14 | 429 (C(7)) | ~ 5s |

*Nota: Los tiempos varían según la máquina*

## 💡 Aplicaciones Prácticas

Los números de Catalan aparecen en:
- ✅ Formas de triangular un polígono
- ✅ Expresiones con paréntesis balanceados
- ✅ Caminos en una malla sin cruzarse
- ✅ Emparejamientos en torneos
- ✅ Formas de parentesizar productos de matrices
- ✅ Análisis de genomas (biología computacional)
- ✅ Parsing de expresiones en compiladores

## 📚 Fórmula Recursiva

$$C_n = \sum_{i=0}^{n-1} C_i \cdot C_{n-1-i}$$

Esta fórmula muestra cómo los números más pequeños componen los más grandes.

## 🎓 Explicación Matemática

### ¿Por qué funciona?

Cuando **n personas se saluden de a 2 sin cruces:**

1. La **primera persona (0)** debe saludarse con alguien
2. Si se saluda con la **persona k**, el círculo se divide en:
   - Personas entre 0 y k: pueden hacer (k-1)/2 saludos
   - Personas entre k y 0: pueden hacer (n-k-1)/2 saludos
3. Esto genera la **fórmula recursiva de Catalan**

## 🔗 Referencias

- [Wikipedia - Catalan Numbers](https://en.wikipedia.org/wiki/Catalan_number)
- [OEIS A000108](https://oeis.org/A000108)

## 📝 Autor

Programa educativo para entender números de Catalan de forma interactiva y visual.

## 📄 Licencia

Libre para uso educativo.

---

## ⚙️ Requisitos Técnicos

- Python 3.8+
- matplotlib
- numpy

## 🐛 Troubleshooting

### Error de codificación UTF-8 en PowerShell

```powershell
$env:PYTHONIOENCODING = "utf-8"
python catalan.py
```

### Matplotlib no muestra gráficas

Asegúrate que tienes un backend gráfico disponible (normalmente TkAgg en Windows)

## 🎨 Personalización

Puedes modificar:
- Número máximo de personas: cambiar límite en `resolver_mesa_redonda()`
- Colores de gráficas: editar paleta `plt.cm.Set3`
- Tamaño de visualización: ajustar `figsize` en `visualizar_todas_configuraciones()`

---

**¡Disfruta explorando los números de Catalan!** 🚀
