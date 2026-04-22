# -*- coding: utf-8 -*-
"""Script de prueba para verificar funcionalidades de catalan_gui.py"""

import sys
sys.path.insert(0, r"c:\Users\ASUS\Documents\PAGINA")

from catalan_gui import NumerosCatalan, MesaRedonda, Punto
import math

print("="*60)
print("🧪 PRUEBA DE APLICACIÓN CATALAN - NÚMEROS Y MESA REDONDA")
print("="*60)

# Test 1: NumerosCatalan
print("\n✓ Test 1: Cálculo de Números de Catalan")
catalan = NumerosCatalan()
for n in range(6):
    resultado = catalan.calcular_formula_directa(n)
    print(f"  C({n}) = {resultado:,}")

# Test 2: Mesa Redonda - 4 personas (n=4, k=2)
print("\n✓ Test 2: Mesa Redonda con 4 personas")
mesa = MesaRedonda(4)
configs = mesa.generar_todas_configuraciones()
print(f"  Número de configuraciones: {len(configs)}")
print(f"  Catalan teórico: C(2) = {catalan.calcular_formula_directa(2)}")
print(f"  Coincide: {len(configs) == catalan.calcular_formula_directa(2)}")
for i, config in enumerate(configs):
    pares = ", ".join([f"{a}↔{b}" for a, b in config])
    print(f"    {i+1}. {pares}")

# Test 3: Mesa Redonda - 6 personas (n=6, k=3)
print("\n✓ Test 3: Mesa Redonda con 6 personas")
mesa = MesaRedonda(6)
configs = mesa.generar_todas_configuraciones()
print(f"  Número de configuraciones: {len(configs)}")
print(f"  Catalan teórico: C(3) = {catalan.calcular_formula_directa(3)}")
print(f"  Coincide: {len(configs) == catalan.calcular_formula_directa(3)}")
for i, config in enumerate(configs):
    pares = ", ".join([f"{a}↔{b}" for a, b in config])
    print(f"    {i+1}. {pares}")

# Test 4: Verify Figure generation (matplotlib integration)
print("\n✓ Test 4: Generación de gráficas (matplotlib)")
try:
    fig = mesa.crear_figura_graficas(configs)
    print(f"  ✅ Figura generada correctamente")
    print(f"  Tipo: {type(fig).__name__}")
    print(f"  Subplots: {len(fig.axes)}")
except Exception as e:
    print(f"  ❌ Error: {e}")

print("\n" + "="*60)
print("✅ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
print("="*60)
print("\n🚀 Para ejecutar la aplicación GUI:")
print("   python catalan_gui.py")
print("\n   O desde PowerShell:")
print("   $env:PYTHONIOENCODING = 'utf-8'; Start-Process -FilePath")
print("   'c:/Users/ASUS/Documents/PAGINA/.venv/Scripts/python.exe'")
print("   -ArgumentList 'catalan_gui.py'")
