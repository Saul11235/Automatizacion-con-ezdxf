# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
from Perfil_zapata import *
from Planta_zapata  import *

#
# En este ejemplo se dibujaran varias zapatas
# variando las dimensiones en planta.
# Cada variante muestra su perfil (fila inferior)
# y su planta (fila superior) en el mismo documento.
#

# datos fijos
alto_z       = 40
largo_col    = 30
ancho_col    = 30
alto_col     = 60
recub        = 7.5
n_barras_x   = 6
n_barras_y   = 6
diam_barra   = 1.27
diam_estribo = 0.95

# datos para graficar
separacion_y = 200   # separacion entre fila perfil y fila planta
char         = 3
border       = False

doc = ezdxf.new()

# creando objetos
obj_perfil = Perfil_zapata()
obj_planta = Planta_zapata()

# configurando al mismo doc
obj_perfil.set_doc(doc)
obj_planta.set_doc(doc)

# nota, para alinear los dibujos en sentido x 
# se ha planteado una variable de ayuda x
ayuda_x = 0

# iterando sobre dimensiones en planta
for lado in [100, 130, 160]:

    # perfil, fila inferior
    obj_perfil.move_to(y=0,x=ayuda_x)
    obj_perfil.config(
            largo_z      = lado,
            ancho_z      = lado,
            alto_z       = alto_z,
            largo_col    = largo_col,
            ancho_col    = ancho_col,
            alto_col     = alto_col,
            recub        = recub,
            n_barras_x   = n_barras_x,
            n_barras_y   = n_barras_y,
            diam_barra   = diam_barra,
            diam_estribo = diam_estribo,
            )
    obj_perfil.draw(char=char, border=border)
    obj_perfil.move(x=10)

    # planta, fila superior
    obj_planta.move_to(y=separacion_y,x=ayuda_x)
    obj_planta.config(
            largo_z    = lado,
            ancho_z    = lado,
            largo_col  = largo_col,
            ancho_col  = ancho_col,
            recub      = recub,
            n_barras_x = n_barras_x,
            n_barras_y = n_barras_y,
            diam_barra = diam_barra,
            )
    obj_planta.draw(char=char, border=border)
    obj_planta.move(x=10)

    # actualizando variable de ayuda
    ayuda_x=max(obj_perfil.x,obj_planta.x)

# guardando dxf
doc.saveas("test.dxf")
print("test dxf generado")
