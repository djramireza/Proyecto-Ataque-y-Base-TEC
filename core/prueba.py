from entities import Tower, Unidad, Pared, Base
from data_definitions import TOWERS_CATALOG, UNITS_CATALOG
from combat import CombatEngine
 
# Crear la base, ubicada en la casilla (9, 9)
base = Base(hp=200, position=(9, 9))
 
# Crear una torre básica, ubicada en (5, 5)
datos_torre = TOWERS_CATALOG["basica"]
torre = Tower(**datos_torre)
torre.position = (5, 5)
 
# Crear una unidad atacante (soldado), cerca de la torre
datos_unidad = UNITS_CATALOG["soldado"]
unidad = Unidad(**datos_unidad)
unidad.position = (5, 6)
 
paredes = []
 
combate = CombatEngine(towers=[torre], paredes=paredes, unidades=[unidad], base=base)
resultado = combate.ejecutar_ronda()
 
print("Resultado de la ronda:")
print(resultado)
print(f"HP de la torre al final: {torre.hp}")
print(f"HP de la unidad al final: {unidad.hp}")
print(f"HP de la base al final: {base.hp}")
 