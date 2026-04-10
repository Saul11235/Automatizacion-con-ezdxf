#
# Ejemplo sencillo de script
#

import ezdxf
from   perfil_I       import *
from   perfil_Hueco   import *

# -----------------------------------
#
# En esta seccion se dibujaran varias 
# secciones variando los espesores
#
#  este ejemplo utilizara varias clases
#  de perfil para dibujar todos estos elementos
#
# -----------------------------------

# Datos para geometria

alto            = 50
ancho           = 40

espesor_inicial = 2
espesor_final   = 12

espesor_step    = 1  # este valor servira par iterar

# datos para graficar

separacion_x    = 1
separacion_y    = 160

char            = 4
# -----------------------------------

doc = ezdxf.new()

# creando objetos
obj_perfil_I = perfil_I()
obj_perfil_O = perfil_Hueco()

# configurando obj_perfil_Ieto doc
obj_perfil_I.set_doc( doc )
obj_perfil_O.set_doc( doc )

# Nota: este ejemplo vamos a crear varios ejemplos analizando

for e in range(espesor_inicial,espesor_final,espesor_step):

    # perfil I, iterado para un espesor e
    obj_perfil_I.move_to(y=0)
    obj_perfil_I.config(alto=alto,ancho=ancho,ala=e,alma=e)
    obj_perfil_I.draw(char=char)
    obj_perfil_I.move(x= separacion_x)

    # Perfil hueco, iterado para un espesor e
    obj_perfil_O.move_to(y=separacion_y)
    obj_perfil_O.config(alto=alto,ancho=ancho,espesor=e)
    obj_perfil_O.draw(char=char)
    obj_perfil_O.move(x= separacion_x)

# guardando dxf
doc.saveas("test.dxf")
print("dibujo dxf generado")


