# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
from Seccion_columna import *
from Corte_columna   import *

# datos comunes
recub       = 4
d_estribo   = 0.95
h_losa      = 20
h_zapata    = 50
l_desarrollo= 40

# separacion entre filas
sep_y  = 100
sep_x  = 50
char   = 2
border = False

doc = ezdxf.new()

obj_seccion = Seccion_columna()
obj_corte   = Corte_columna()

obj_seccion.set_doc(doc)
obj_corte.set_doc(doc)

# tres variantes: seccion y pisos crecientes
variantes = [
    # b_col, h_col, n_pisos, h_piso, nx, ny, diam_long
    (25, 25, 2, 260, 3, 3, 1.27),
    (30, 30, 3, 280, 4, 4, 1.59),
    (40, 40, 4, 300, 5, 5, 1.91),
]

# nota, para alinear los dibujos en sentido x 
# se ha planteado una variable de ayuda x
ayuda_x = 0

for b_col, h_col, n_pisos, h_piso, nx, ny, dl in variantes:

    az = max(b_col * 3, 100)   # ancho zapata proporcional

    # seccion transversal (fila superior)
    obj_seccion.move_to(y=0,x=ayuda_x)
    obj_seccion.config(
            b_col      = b_col,
            h_col      = h_col,
            recub      = recub,
            d_estribo  = d_estribo,
            n_barras_x = nx,
            n_barras_y = ny,
            diam_long  = dl,
            )
    obj_seccion.draw(char=char, border=border)
    obj_seccion.move(x=sep_x)

    # desarrollo longitudinal (fila inferior)
    obj_corte.move_to(y=sep_y,x=ayuda_x)
    obj_corte.config(
            b_col        = b_col,
            h_col        = h_col,
            h_piso       = h_piso,
            n_pisos      = n_pisos,
            h_losa       = h_losa,
            h_zapata     = h_zapata,
            ancho_zapata = az,
            recub        = recub,
            d_estribo    = d_estribo,
            diam_long    = dl,
            n_barras     = nx,
            l_desarrollo = l_desarrollo,
            )
    obj_corte.draw(char=char, border=border)
    obj_corte.move(x=sep_x)

    # ajustando variable ayuda_x
    ayuda_x=max(obj_seccion.x,obj_corte.x)

# guardando dxf
doc.saveas("test.dxf")
print("dibujo dxf generado")
print()
for b, h, np, hp, nx, ny, dl in variantes:
    Lc   = max(h, hp/6, 50)
    sc   = min(b/4, 8*dl, 10)
    sm   = min(b/2, 16*dl, 30)
    rho  = round((2*nx+2*ny-4)*3.14159*(dl**2)/4/(b*h)*100, 2)
    print(f"  Col {b}x{h} / {np} pisos: Lc={Lc:.0f}cm  s_conf={sc:.1f}cm  s_cent={sm:.1f}cm  rho={rho}%")