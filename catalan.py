"""
Números de Catalan: Problema de la Mesa Redonda
================================================

Este programa genera todas las formas posibles de que personas
alrededor de una mesa redonda se saluden sin que los saludos se crucen.

MENÚ INTERACTIVO:
- Ver secuencia de números de Catalan
- Ingresar número de personas y ver todas las configuraciones
- Explicación completa de números de Catalan
"""

import math
from dataclasses import dataclass
from typing import List, Tuple
import matplotlib
matplotlib.use('TkAgg')  # Backend sin bloqueos
import matplotlib.pyplot as plt
import numpy as np


@dataclass
class Punto:
    """Representa una persona en la mesa redonda"""
    id: int
    x: float
    y: float


class NumerosCatalan:
    """Clase para calcular números de Catalan"""
    
    @staticmethod
    def calcular_formula_directa(n: int) -> int:
        """
        Calcula el n-ésimo número de Catalan usando la fórmula:
        C(n) = (2n)! / ((n+1)! * n!)
        """
        return math.comb(2*n, n) // (n + 1)
    
    @staticmethod
    def calcular_recursivo(n: int, memo: dict = None) -> int:
        """
        Calcula el n-ésimo número de Catalan recursivamente con memoización
        C(0) = 1
        C(n) = suma de C(i) * C(n-1-i) para i de 0 a n-1
        """
        if memo is None:
            memo = {}
        
        if n in memo:
            return memo[n]
        
        if n <= 1:
            return 1
        
        resultado = 0
        for i in range(n):
            resultado += NumerosCatalan.calcular_recursivo(i, memo) * \
                        NumerosCatalan.calcular_recursivo(n-1-i, memo)
        
        memo[n] = resultado
        return resultado
    
    @staticmethod
    def generar_secuencia(n: int) -> List[int]:
        """Genera los primeros n números de Catalan"""
        return [NumerosCatalan.calcular_formula_directa(i) for i in range(n)]


class MesaRedonda:
    """Genera y maneja mesas redondas con conexiones (saludos)"""
    
    def __init__(self, n_personas: int):
        """
        Inicializa una mesa redonda
        n_personas: número de personas (debe ser par para saludos)
        """
        self.n = n_personas
        self.puntos = self._generar_puntos()
        self.conexiones = []
    
    def _generar_puntos(self) -> List[Punto]:
        """Genera los puntos (personas) distribuidos en círculo"""
        puntos = []
        for i in range(self.n):
            angulo = 2 * math.pi * i / self.n
            x = math.cos(angulo)
            y = math.sin(angulo)
            puntos.append(Punto(id=i, x=x, y=y))
        return puntos
    
    @staticmethod
    def se_cruzan(conexion1: Tuple[int, int], conexion2: Tuple[int, int], 
                  n: int) -> bool:
        """
        Verifica si dos saludos se cruzan en un círculo
        n: número de personas
        """
        a, b = conexion1
        c, d = conexion2
        
        # Si comparten un punto, no se cruzan
        if a == b or c == d:
            return False
        
        # Normalizamos para que a < b y c < d
        if a > b:
            a, b = b, a
        if c > d:
            c, d = d, c
        
        # Si comparten un extremo, no se cruzan
        if a == c or a == d or b == c or b == d:
            return False
        
        # Verificamos si un intervalo contiene exactamente uno de los puntos del otro
        return (a < c < b < d) or (c < a < d < b)
    
    def generar_todas_configuraciones(self) -> List[List[Tuple[int, int]]]:
        """
        Genera todas las configuraciones posibles de saludos
        sin que se crucen (si n es par)
        """
        if self.n % 2 != 0:
            return []
        
        configuraciones = []
        self._backtrack(list(range(self.n)), [], configuraciones)
        return configuraciones
    
    def _backtrack(self, disponibles: List[int], 
                   saludos_actuales: List[Tuple[int, int]], 
                   configuraciones: List):
        """
        Búsqueda recursiva para encontrar todas las configuraciones válidas
        """
        if not disponibles:
            configuraciones.append(saludos_actuales.copy())
            return
        
        # Tomar el primer elemento disponible
        primer = disponibles[0]
        resto = disponibles[1:]
        
        # Intentar saludarse (conectarse) con cada otro elemento disponible
        for i, segundo in enumerate(resto):
            nuevo_saludo = (min(primer, segundo), max(primer, segundo))
            
            # Verificar que no se cruza con saludos existentes
            valida = True
            for saludo_existente in saludos_actuales:
                if self.se_cruzan(nuevo_saludo, saludo_existente, self.n):
                    valida = False
                    break
            
            if valida:
                nuevo_disponible = resto[:i] + resto[i+1:]
                saludos_actuales.append(nuevo_saludo)
                self._backtrack(nuevo_disponible, saludos_actuales, configuraciones)
                saludos_actuales.pop()
    
    def visualizar_todas_configuraciones(self, saludos_lista: List[List[Tuple[int, int]]]):
        """Visualiza todas las configuraciones de manera clara"""
        num_configs = len(saludos_lista)
        
        # Determinar layout
        cols = 3
        filas = (num_configs + cols - 1) // cols
        
        fig = plt.figure(figsize=(18, 5*filas))
        fig.suptitle(f'Formas de Saludarse sin Cruces - {self.n} Personas\n' + 
                     f'Total: {num_configs} configuraciones = C({self.n//2})',
                     fontsize=16, fontweight='bold', y=0.995)
        
        for config_idx, saludos in enumerate(saludos_lista):
            ax = fig.add_subplot(filas, cols, config_idx+1)
            
            # Dibujar círculo (mesa)
            circulo = plt.Circle((0, 0), 1, fill=False, color='navy', linewidth=3, linestyle='--')
            ax.add_patch(circulo)
            
            # Dibujar personas como círculos grandes
            xs = [p.x for p in self.puntos]
            ys = [p.y for p in self.puntos]
            ax.scatter(xs, ys, s=500, c='#FF6B6B', zorder=5, edgecolors='darkred', linewidth=2)
            
            # Etiquetar personas con números
            for p in self.puntos:
                ax.text(p.x, p.y, str(p.id), 
                       ha='center', va='center', fontsize=11, fontweight='bold', color='white')
            
            # Dibujar saludos (conexiones) con colores diferentes
            colors = plt.cm.Set3(np.linspace(0, 1, len(saludos)))
            for saludo_idx, (a, b) in enumerate(saludos):
                pa = self.puntos[a]
                pb = self.puntos[b]
                ax.plot([pa.x, pb.x], [pa.y, pb.y], 
                       color=colors[saludo_idx], linewidth=3, alpha=0.8, 
                       label=f'{a}↔{b}')
            
            # Configurar eje
            ax.set_xlim(-1.6, 1.6)
            ax.set_ylim(-1.6, 1.6)
            ax.set_aspect('equal')
            ax.axis('off')
            
            # Título con información
            title = f'Configuración {config_idx+1}\n'
            title += f'Saludos: {", ".join([f"{a}↔{b}" for a, b in saludos])}'
            ax.set_title(title, fontsize=10, fontweight='bold', pad=10)
        
        plt.tight_layout()
        return fig


def mostrar_estadisticas(n: int = 10):
    """Muestra estadísticas de números de Catalan"""
    print("\n" + "="*60)
    print("NÚMEROS DE CATALAN - SECUENCIA")
    print("="*60)
    
    catalan = NumerosCatalan()
    secuencia = catalan.generar_secuencia(n)
    
    print(f"\nPrimeros {n} números de Catalan:")
    print("-" * 60)
    print(f"{'n':>3} | {'C(n)':>15} | {'Significado'}") 
    print("-" * 60)
    for i, c in enumerate(secuencia):
        if i == 0:
            significado = "Valor base"
        elif i == 1:
            significado = "1 o 2 personas"
        else:
            significado = f"Saludos sin cruces ({2*i} personas)"
        print(f"{i:3d} | {c:15,d} | {significado}")
    print("-" * 60)


def resolver_mesa_redonda(n_personas: int, mostrar_graficas: bool = True):
    """
    Resuelve el problema de la mesa redonda
    
    n_personas: número de personas (debe ser par)
    mostrar_graficas: si mostrar gráficas al final
    """
    print("\n" + "="*60)
    print(f"PROBLEMA DE LA MESA REDONDA ({n_personas} personas)")
    print("="*60)
    
    if n_personas % 2 != 0:
        print(f"❌ Error: {n_personas} es impar. Use un número par.")
        return None
    
    # Calcular número de Catalan esperado
    k = n_personas // 2
    catalan = NumerosCatalan()
    num_catalan = catalan.calcular_formula_directa(k)
    
    print(f"\n🔵 Personas alrededor de la mesa: {n_personas}")
    print(f"🤝 Saludos que cada persona hace: {k}")
    print(f"\n📊 Número de formas de saludarse SIN que se crucen:")
    print(f"    C({k}) = {num_catalan:,} formas")
    
    # Generar mesa redonda
    mesa = MesaRedonda(n_personas)
    
    print(f"\n⏳ Generando todas las configuraciones posibles...")
    
    configuraciones = mesa.generar_todas_configuraciones()
    
    print(f"\n✓ Total de configuraciones encontradas: {len(configuraciones)}")
    print(f"✓ Validación: C({k}) = {num_catalan} (esperado)")
    
    if len(configuraciones) == num_catalan:
        print("✅ ¡CORRECTO! El número de configuraciones coincide con C(n)")
    
    # Mostrar una pequeña descripción de cada configuración
    print("\n" + "-"*60)
    print("DETALLE DE CADA CONFIGURACIÓN:")
    print("-"*60)
    for idx, saludos in enumerate(configuraciones):
        pares = ", ".join([f"{a}↔{b}" for a, b in saludos])
        print(f"  {idx+1}. Saludos: {pares}")
    
    # Visualizar todas las configuraciones
    if mostrar_graficas:
        print(f"\n📊 Generando gráficas de todas las {len(configuraciones)} configuraciones...")
        fig = mesa.visualizar_todas_configuraciones(configuraciones)
        return fig
    else:
        return None


def mostrar_explicacion():
    """Muestra explicación de números de Catalan"""
    explicacion = """
╔════════════════════════════════════════════════════════════╗
║         ¿QUÉ SON LOS NÚMEROS DE CATALAN?                  ║
╚════════════════════════════════════════════════════════════╝

🔢 DEFINICIÓN:
Los números de Catalan (C_n) son una secuencia de números naturales
que aparecen en muchos problemas combinatorios:

   C_n = (2n)! / ((n+1)! × n!)

📊 SECUENCIA:
C(0)=1, C(1)=1, C(2)=2, C(3)=5, C(4)=14, C(5)=42, C(6)=132...


🤝 EL PROBLEMA DE LA MESA REDONDA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Si n personas se sientan alrededor de una mesa redonda,
¿DE CUÁNTAS FORMAS PUEDEN SALUDARSE SIN QUE LOS SALUDOS SE CRUCEN?

RESPUESTA: C(n/2) maneras

📌 EJEMPLO CON 4 PERSONAS (Personas 0, 1, 2, 3):

   FORMA 1 ✅                    FORMA 2 ✅
   Saludos: 0↔1, 2↔3           Saludos: 0↔3, 1↔2
   
   Círculo:                      Círculo:
       0 ------- 1                   0 ----- 1
      /           \\                 / \\     / \\
     3 ------- 2    (⚪)           3   (⚪)   2
     
     LAS 4 PERSONAS              LAS 4 PERSONAS
     se saludan sin              se saludan sin
     que cruces ocurran          que cruces ocurran

   ❌ ¿FORMA 3? Saludos: 0↔2, 1↔3 → ¡SE CRUZAN LAS LÍNEAS!
   
   Total: 2 formas = C(2) ✓


🎯 APLICACIONES PRÁCTICAS:
• Formas de triangular un polígono (dividir en triángulos)
• Expresiones matemáticas válidas con paréntesis balanceados
• Caminos en una malla sin cruzarse
• Emparejamientos en un torneo sin conflictos
• Formas de parentesizar un producto de matrices
• Análisis de genomas (biología computacional)
• ¡Y muchas más!


💡 OBSERVACIONES INTERESANTES:
• C(n) crece EXPONENCIALMENTE: C(10) = 16,796
• C(20) = 6,564,120,420 (¡más de 6 mil millones!)
• Los números de Catalan aparecen en la naturaleza frecuentemente
• Tienen MÚLTIPLES fórmulas e interpretaciones equivalentes
• Son fundamentales en combinatoria, teoría de grafos y programación


📐 FÓRMULA RECURSIVA:
C(0) = 1
C(n) = C(0)×C(n-1) + C(1)×C(n-2) + ... + C(n-1)×C(0)

Esta fórmula muestra cómo los números más pequeños componen los más grandes.
"""
    print(explicacion)


def menu_interactivo():
    """Menú interactivo para explorar números de Catalan"""
    
    while True:
        print("\n" + "█"*60)
        print("█" + " "*58 + "█")
        print("█" + "NÚMEROS DE CATALAN - MESA REDONDA".center(58) + "█")
        print("█" + " "*58 + "█")
        print("█"*60)
        
        print("\n¿Qué deseas hacer?")
        print("-" * 60)
        print("1. 📊 Ver secuencia de números de Catalan")
        print("2. 🔵 Hallar saludos sin cruces en una mesa redonda")
        print("3. ℹ️  Explicación de números de Catalan")
        print("4. ❌ Salir")
        print("-" * 60)
        
        opcion = input("Selecciona una opción (1-4): ").strip()
        
        if opcion == "1":
            try:
                n = int(input("\n¿Cuántos números de Catalan deseas ver? (1-20): "))
                if n < 1 or n > 20:
                    print("❌ Rango inválido. Usando 10.")
                    n = 10
                mostrar_estadisticas(n)
            except ValueError:
                print("❌ Debes ingresar un número válido.")
        
        elif opcion == "2":
            try:
                print("\nℹ️  Los saludos solo funcionan con número PAR de personas")
                n_personas = int(input("¿Cuántas personas están en la mesa? (2-12, número par): "))
                
                if n_personas % 2 != 0:
                    print("❌ El número debe ser PAR para hacer saludos pareados.")
                    continue
                
                if n_personas < 2 or n_personas > 12:
                    print("❌ Por favor, usa un número entre 2 y 12.")
                    continue
                
                fig = resolver_mesa_redonda(n_personas, mostrar_graficas=True)
                
                # Preguntar si visualizar
                if fig:
                    mostrar = input("\n¿Deseas ver las gráficas? (s/n): ").strip().lower()
                    if mostrar == 's':
                        plt.show()
                
            except ValueError:
                print("❌ Debes ingresar un número válido.")
        
        elif opcion == "3":
            mostrar_explicacion()
        
        elif opcion == "4":
            print("\n¡Hasta luego! 👋")
            break
        
        else:
            print("❌ Opción inválida. Intenta de nuevo.")


if __name__ == "__main__":
    menu_interactivo()
