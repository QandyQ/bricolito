"""
Script de demostración del programa de Números de Catalan
Muestra todo automáticamente sin entrada interactiva
"""

import math
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple


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
        """Calcula C(n) = (2n)! / ((n+1)! * n!)"""
        return math.comb(2*n, n) // (n + 1)
    
    @staticmethod
    def generar_secuencia(n: int) -> List[int]:
        """Genera los primeros n números de Catalan"""
        return [NumerosCatalan.calcular_formula_directa(i) for i in range(n)]


class MesaRedonda:
    """Genera y maneja mesas redondas con saludos sin cruces"""
    
    def __init__(self, n_personas: int):
        self.n = n_personas
        self.puntos = self._generar_puntos()
    
    def _generar_puntos(self) -> List[Punto]:
        """Genera los puntos distribuidos en círculo"""
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
        """Verifica si dos saludos se cruzan en un círculo"""
        a, b = conexion1
        c, d = conexion2
        
        if a == b or c == d:
            return False
        
        if a > b:
            a, b = b, a
        if c > d:
            c, d = d, c
        
        if a == c or a == d or b == c or b == d:
            return False
        
        return (a < c < b < d) or (c < a < d < b)
    
    def generar_todas_configuraciones(self) -> List[List[Tuple[int, int]]]:
        """Genera todas las configuraciones de saludos sin cruces"""
        if self.n % 2 != 0:
            return []
        
        configuraciones = []
        self._backtrack(list(range(self.n)), [], configuraciones)
        return configuraciones
    
    def _backtrack(self, disponibles: List[int], 
                   saludos_actuales: List[Tuple[int, int]], 
                   configuraciones: List):
        """Búsqueda recursiva para encontrar todas las configuraciones"""
        if not disponibles:
            configuraciones.append(saludos_actuales.copy())
            return
        
        primer = disponibles[0]
        resto = disponibles[1:]
        
        for i, segundo in enumerate(resto):
            nuevo_saludo = (min(primer, segundo), max(primer, segundo))
            
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
        """Visualiza todas las configuraciones"""
        num_configs = len(saludos_lista)
        
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
            
            # Dibujar personas
            xs = [p.x for p in self.puntos]
            ys = [p.y for p in self.puntos]
            ax.scatter(xs, ys, s=500, c='#FF6B6B', zorder=5, edgecolors='darkred', linewidth=2)
            
            # Etiquetar personas
            for p in self.puntos:
                ax.text(p.x, p.y, str(p.id), 
                       ha='center', va='center', fontsize=11, fontweight='bold', color='white')
            
            # Dibujar saludos con colores diferentes
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
            
            # Título
            title = f'Configuración {config_idx+1}\n'
            title += f'Saludos: {", ".join([f"{a}↔{b}" for a, b in saludos])}'
            ax.set_title(title, fontsize=10, fontweight='bold', pad=10)
        
        plt.tight_layout()
        return fig


def demostrar():
    """Función de demostración"""
    
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "DEMOSTRACIÓN - NÚMEROS DE CATALAN".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    # Mostrar secuencia
    print("\n" + "="*60)
    print("NÚMEROS DE CATALAN - SECUENCIA")
    print("="*60)
    
    catalan = NumerosCatalan()
    secuencia = catalan.generar_secuencia(10)
    
    print(f"\nPrimeros 10 números de Catalan:")
    print("-" * 60)
    print(f"{'n':>3} | {'C(n)':>15} | {'Personas': >10}")
    print("-" * 60)
    for i, c in enumerate(secuencia):
        personas = 2*i if i > 0 else 0
        print(f"{i:3d} | {c:15,d} | {personas:>10}")
    print("-" * 60)
    
    # Demostración con 4 personas
    print("\n" + "="*60)
    print("DEMOSTRACIÓN 1: MESA REDONDA CON 4 PERSONAS")
    print("="*60)
    
    n_personas = 4
    k = n_personas // 2
    num_catalan = catalan.calcular_formula_directa(k)
    
    print(f"\n🔵 Personas alrededor de la mesa: {n_personas}")
    print(f"🤝 Cada persona se saluda con: {k} personas")
    print(f"\n📊 Número de formas de saludarse SIN que se crucen:")
    print(f"    C({k}) = {num_catalan} formas")
    
    mesa1 = MesaRedonda(n_personas)
    config1 = mesa1.generar_todas_configuraciones()
    
    print(f"\n✅ Configuraciones encontradas: {len(config1)}")
    print("\nDetalles:")
    for idx, saludos in enumerate(config1):
        pares = ", ".join([f"{a}↔{b}" for a, b in saludos])
        print(f"  {idx+1}. {pares}")
    
    fig1 = mesa1.visualizar_todas_configuraciones(config1)
    
    # Demostración con 6 personas
    print("\n" + "="*60)
    print("DEMOSTRACIÓN 2: MESA REDONDA CON 6 PERSONAS")
    print("="*60)
    
    n_personas = 6
    k = n_personas // 2
    num_catalan = catalan.calcular_formula_directa(k)
    
    print(f"\n🔵 Personas alrededor de la mesa: {n_personas}")
    print(f"🤝 Cada persona se saluda con: {k} personas")
    print(f"\n📊 Número de formas de saludarse SIN que se crucen:")
    print(f"    C({k}) = {num_catalan} formas")
    
    mesa2 = MesaRedonda(n_personas)
    config2 = mesa2.generar_todas_configuraciones()
    
    print(f"\n✅ Configuraciones encontradas: {len(config2)}")
    print("\nPrimeras 5 configuraciones:")
    for idx, saludos in enumerate(config2[:5]):
        pares = ", ".join([f"{a}↔{b}" for a, b in saludos])
        print(f"  {idx+1}. {pares}")
    print(f"  ... (y {len(config2)-5} más)")
    
    fig2 = mesa2.visualizar_todas_configuraciones(config2)
    
    # Información final
    print("\n" + "="*60)
    print("¡LISTO! Mostrando gráficas...")
    print("="*60)
    print("\n💡 Puedes cerrar las ventanas de gráficas para ver más información")
    
    plt.show()
    
    print("\n✨ Demostración completada exitosamente!")
    print("📌 Nota: Ejecuta 'python catalan.py' para el menú interactivo")


if __name__ == "__main__":
    demostrar()
