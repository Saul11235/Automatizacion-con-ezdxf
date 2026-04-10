# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
import numpy as np
from Superficie_curvas_nivel import *

# datos simulados de levantamiento topografico
# (en la practica se cargan de un CSV, Excel o archivo de campo)

def cargar_desde_csv(archivo):
    """ejemplo de como cargar puntos reales desde un CSV"""
    import csv
    puntos = []
    with open(archivo, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # saltar encabezado
        for fila in reader:
            puntos.append([float(fila[0]),
                           float(fila[1]),
                           float(fila[2])])
    return puntos

# Generamos datos simulados para el ejemplo
obj_base = Superficie_curvas_nivel()

puntos_colina  = obj_base._generar_puntos_colina (n=60, seed=42)
puntos_valle   = obj_base._generar_puntos_valle  (n=70, seed=7 )
puntos_terreno = obj_base._generar_puntos_terreno(n=80, seed=13)

# creamos un solo documento con las tres superficies

doc = ezdxf.new()

# --- superficie 1: colina (equidistancia automatica 10 curvas) ---
sup1 = Superficie_curvas_nivel()
sup1.set_doc(doc)
sup1.config(
    puntos        = puntos_colina,
    n_curvas      = 10,
    metodo_interp = 'cubic',
    resolucion    = 200,
    n_maestra     = 5,
    mostrar_puntos= True,
    dec_cotas     = 2,
)
sup1.draw(x=0, y=0, char=3)

# --- superficie 2: valle (equidistancia fija 2 m) ---
sup2 = Superficie_curvas_nivel()
sup2.set_doc(doc)
sup2.config(
    puntos        = puntos_valle,
    equidistancia = 2.0,
    metodo_interp = 'cubic',
    resolucion    = 200,
    n_maestra     = 5,
    mostrar_puntos= True,
    dec_cotas     = 1,
)
sup2.draw(x=0, y=400, char=3)   # desplazada en Y

# --- superficie 3: terreno con gradiente (equidistancia 5 m) ---
sup3 = Superficie_curvas_nivel()
sup3.set_doc(doc)
sup3.config(
    puntos        = puntos_terreno,
    equidistancia = 5.0,
    metodo_interp = 'linear',   # linear para datos con cambios bruscos
    resolucion    = 150,
    n_maestra     = 4,
    mostrar_puntos= True,
    dec_cotas     = 1,
)
sup3.draw(x=0, y=800, char=3)   # desplazada en Y

# guardando
doc.saveas("test.dxf")
print("\nDXF generado")