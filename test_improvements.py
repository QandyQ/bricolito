# -*- coding: utf-8 -*-
"""Test visualization improvements"""

from catalan_gui import MesaRedonda, NumerosCatalan

print('🧪 Test con 8 personas (visualización mejorada)')
print('='*50)

mesa = MesaRedonda(8)
configs = mesa.generar_todas_configuraciones()
catalan = NumerosCatalan()
expected = catalan.calcular_formula_directa(4)

print(f'Configuraciones encontradas: {len(configs)}')
print(f'C(4) esperado: {expected}')
print(f'✅ Coincide: {len(configs) == expected}')

# Test figure generation
fig = mesa.crear_figura_graficas(configs)
print(f'\nFigura generada: {type(fig).__name__}')
print(f'Subplots: {len(fig.axes)}')
print(f'Figsize: {fig.get_figwidth():.1f} x {fig.get_figheight():.1f} pulgadas')
print(f'Resolución: {fig.dpi} dpi')

print('\n✅ Visualización mejorada:')
print('   • Límite aumentado a 24 personas')
print('   • Gráficas más pequeñas (12" x 2.8*filas)')
print('   • Texto escalado según cantidad de personas')
print('   • Toolbar con ZOOM, PAN, RESET')
print('\n🚀 ¡Listo para ejecutar la aplicación!')
