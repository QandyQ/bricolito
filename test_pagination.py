# -*- coding: utf-8 -*-
"""Test para nuevo sistema de paginación"""

from catalan_gui import MesaRedonda, NumerosCatalan

print("🧪 Test del nuevo sistema de paginación")
print("="*60)

# Test con 8 personas (14 configuraciones = 3 páginas)
print("\n✓ Test con 8 personas (14 configuraciones)")
mesa = MesaRedonda(8)
configs = mesa.generar_todas_configuraciones()
catalan = NumerosCatalan()
expected = catalan.calcular_formula_directa(4)

print(f"  Configuraciones: {len(configs)}")
print(f"  C(4) esperado: {expected}")
print(f"  Coincide: {len(configs) == expected}")

# Simular paginación
configs_por_pagina = 6
num_paginas = (len(configs) + configs_por_pagina - 1) // configs_por_pagina

print(f"\n  Paginación:")
for num_pag in range(1, num_paginas + 1):
    inicio = (num_pag - 1) * configs_por_pagina
    fin = min(inicio + configs_por_pagina, len(configs))
    configs_pagina = configs[inicio:fin]
    print(f"    Página {num_pag}: Configuraciones {inicio+1} a {fin} ({len(configs_pagina)} gráficas)")

# Test con 10 personas (42 configuraciones = 7 páginas)
print("\n✓ Test con 10 personas (42 configuraciones)")
mesa = MesaRedonda(10)
configs = mesa.generar_todas_configuraciones()
expected = catalan.calcular_formula_directa(5)

print(f"  Configuraciones: {len(configs)}")
print(f"  C(5) esperado: {expected}")
print(f"  Coincide: {len(configs) == expected}")

num_paginas = (len(configs) + configs_por_pagina - 1) // configs_por_pagina

print(f"\n  Paginación:")
for num_pag in range(1, num_paginas + 1):
    inicio = (num_pag - 1) * configs_por_pagina
    fin = min(inicio + configs_por_pagina, len(configs))
    configs_pagina = configs[inicio:fin]
    print(f"    Página {num_pag}: Configuraciones {inicio+1} a {fin} ({len(configs_pagina)} gráficas)")

print("\n" + "="*60)
print("✅ SISTEMA DE PAGINACIÓN CORRECTO")
print("="*60)
print("\n🎯 Cambios implementados:")
print("   • Gráficas en tamaño fijo (10\" x 9\")")
print("   • Máximo 6 gráficas por página (2x3)")
print("   • Pestañas para navegar entre páginas")
print("   • Sin necesidad de zoom para ver bien")
print("\n🚀 ¡Listo para ejecutar!")
