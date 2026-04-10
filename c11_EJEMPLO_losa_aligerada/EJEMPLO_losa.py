# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
from Planta_losa import *
from Corte_losa  import *

# datos comunes
largo_losa   = 500
ancho_losa   = 400
b_vig        = 12
h_losa       = 5
recub        = 2
diam_vig     = 0.95
n_barras_vig = 2
sep_temp     = 25
diam_temp    = 0.64

# separacion entre filas
sep_y = 200    # entre planta y corte
sep_x = 100
char  = 2
border = False

doc = ezdxf.new()

obj_planta = Planta_losa()
obj_corte  = Corte_losa()

obj_planta.set_doc(doc)
obj_corte.set_doc(doc)

# nota, para alinear los dibujos en sentido x 
# se ha planteado una variable de ayuda x
ayuda_x = 0

# iterando sobre distintos tipos de bloque / altura de losa
for claro_bloque, h_total in [(23, 17), (28, 20), (33, 25)]:

    # planta, fila superior
    obj_planta.move_to(y=sep_y, x= ayuda_x)
    obj_planta.config(
            largo_losa   = largo_losa,
            ancho_losa   = ancho_losa,
            b_vig        = b_vig,
            claro_bloque = claro_bloque,
            h_total      = h_total,
            h_losa       = h_losa,
            recub        = recub,
            diam_vig     = diam_vig,
            n_barras_vig = n_barras_vig,
            sep_temp     = sep_temp,
            diam_temp    = diam_temp,
            )
    obj_planta.draw(char=char, border=border)
    obj_planta.move(x=sep_x)

    # corte transversal, fila inferior (y=0)
    obj_corte.move_to(y=0, x= ayuda_x)
    obj_corte.config(
            ancho_losa   = ancho_losa,
            b_vig        = b_vig,
            claro_bloque = claro_bloque,
            h_total      = h_total,
            h_losa       = h_losa,
            recub        = recub,
            diam_vig     = diam_vig,
            n_barras_vig = n_barras_vig,
            diam_temp    = diam_temp,
            sep_temp     = sep_temp,
            )
    obj_corte.draw(char=char, border=border)
    obj_corte.move(x=sep_x)

    # actualizando valor ayuda_x
    ayuda_x = max(obj_planta.x,obj_corte.x)

# guardando dxf
doc.saveas("test.dxf")

print("dibujo dxf generado")