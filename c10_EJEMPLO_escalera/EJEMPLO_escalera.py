# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
from Planta_escalera import *
from Corte_escalera  import *

# datos comunes
ancho_esc     = 120
e_losa        = 15
recub         = 2.5
n_barras_long = 5
sep_dist      = 20
diam_long     = 1.27
diam_dist     = 0.95
ancho_apoyo   = 20

# separacion entre filas en el documento
sep_y  = 250    # entre corte y planta
sep_x  = 100
char   = 2
border = False

doc = ezdxf.new()

obj_planta = Planta_escalera()
obj_corte  = Corte_escalera()

obj_planta.set_doc(doc)
obj_corte.set_doc(doc)

# nota, para alinear los dibujos en sentido x 
# se ha planteado una variable de ayuda x
ayuda_x = 0

# iterando sobre distintas geometrias de escalon
# (verificando regla de Blondel: 2ch + h entre 60 y 64 cm)
for n_escalones, huella, contrahuella in [
        (8,  25, 19),   # Blondel = 63 cm
        (10, 28, 18),   # Blondel = 64 cm
        (12, 30, 17),   # Blondel = 64 cm
        ]:

    # corte longitudinal, fila inferior (y=0)
    obj_corte.move_to(y=sep_y,x=ayuda_x)
    obj_corte.config(
            n_escalones   = n_escalones,
            huella        = huella,
            contrahuella  = contrahuella,
            ancho_esc     = ancho_esc,
            e_losa        = e_losa,
            recub         = recub,
            n_barras_long = n_barras_long,
            n_barras_dist = 4,
            diam_long     = diam_long,
            diam_dist     = diam_dist,
            ancho_apoyo   = ancho_apoyo,
            )
    obj_corte.draw(char=char, border=border)
    obj_corte.move(x=sep_x)

    # planta, fila superior
    obj_planta.move_to(y=0,x=ayuda_x)
    obj_planta.config(
            n_escalones   = n_escalones,
            huella        = huella,
            contrahuella  = contrahuella,
            ancho_esc     = ancho_esc,
            e_losa        = e_losa,
            recub         = recub,
            n_barras_long = n_barras_long,
            sep_dist      = sep_dist,
            diam_long     = diam_long,
            diam_dist     = diam_dist,
            )
    obj_planta.draw(char=char, border=border)
    obj_planta.move(x=sep_x)

    # organizando variable x
    ayuda_x = max(obj_corte.x,obj_planta.x)

# guardando dxf
doc.saveas("test.dxf")
print("dibujo dxf generado")
print("Variantes:")
for n, h, ch in [(8,25,19),(10,28,18),(12,30,17)]:
    print(f"  N={n}  h={h}  ch={ch}  Blondel={2*ch+h} cm")