# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
from Perfil_muro import *
from Planta_muro  import *
from Corte_muro   import *

#
# En este ejemplo se dibujaran muros de diferente altura
# variando el alto_m.  Para cada variante se genera:
#   - fila 1 (y=0):        perfil lateral
#   - fila 2 (y=sep_1):    planta
#   - fila 3 (y=sep_2):    corte transversal
#

# datos comunes
largo_muro = 600
largo_z    = 150
puntera    = 40
alto_z     = 35
e_base     = 30
e_corona   = 20
recub      = 7.5
diam_vert  = 1.59
diam_horiz = 1.27
diam_zap   = 1.27

# separacion entre filas
sep_1 = 500    # entre perfil y planta
sep_2 = 750    # entre planta y corte
sep_x = 100

char  = 3
border = False

doc = ezdxf.new()

obj_perfil = Perfil_muro()
obj_planta = Planta_muro()
obj_corte  = Corte_muro()

obj_perfil.set_doc(doc)
obj_planta.set_doc(doc)
obj_corte.set_doc(doc)

# nota, para alinear los dibujos en sentido x 
# se ha planteado una variable de ayuda x
ayuda_x = 0

# iterando sobre distintos altos de muro
for alto_m in [200, 270, 340]:

    # calculo de separacion transversal proporcional al alto
    sep_vert  = 20
    sep_horiz = max(30, alto_m // 7)
    n_vert    = max(6, largo_muro // sep_vert)
    n_horiz   = max(4, alto_m // sep_horiz)

    # perfil lateral
    obj_perfil.move_to(y=0,x=ayuda_x)
    obj_perfil.config(
            largo_z   = largo_z,
            puntera   = puntera,
            alto_z    = alto_z,
            alto_m    = alto_m,
            e_base    = e_base,
            e_corona  = e_corona,
            recub     = recub,
            n_vert    = 8,
            n_horiz   = n_horiz,
            diam_vert = diam_vert,
            diam_horiz= diam_horiz,
            diam_zap  = diam_zap,
            )
    obj_perfil.draw(char=char, border=border)
    obj_perfil.move(x=sep_x)

    # planta
    obj_planta.move_to(y=sep_1,x=ayuda_x)
    obj_planta.config(
            largo_muro = largo_muro,
            largo_z    = largo_z,
            puntera    = puntera,
            e_base     = e_base,
            alto_z     = alto_z,
            alto_m     = alto_m,
            recub      = recub,
            n_long     = 10,
            sep_trans  = 20,
            diam_long  = diam_vert,
            diam_trans = diam_horiz,
            )
    obj_planta.draw(char=char, border=border)
    obj_planta.move(x=sep_x)

    # corte transversal
    obj_corte.move_to(y=sep_2,x=ayuda_x)
    obj_corte.config(
            largo_muro = largo_muro,
            largo_z    = largo_z,
            alto_z     = alto_z,
            alto_m     = alto_m,
            e_base     = e_base,
            recub      = recub,
            sep_vert   = sep_vert,
            sep_horiz  = sep_horiz,
            diam_vert  = diam_vert,
            diam_horiz = diam_horiz,
            diam_zap   = diam_zap,
            )
    obj_corte.draw(char=char, border=border)
    obj_corte.move(x=sep_x)

    # actualizando ayuda_x
    ayuda_x=max(obj_corte.x,obj_planta.x,obj_perfil.x)

# guardando dxf
doc.saveas("test.dxf")
print("dibujo dxf generado")