#
# Ejemplo sencillo de script
#

import ezdxf
from   perfil_I       import *
from   perfil_Hueco   import *

# -----------------------------------
#
# En este caso los datos se sacaran de un archivo
# input.txt leyendo ancho, alto y espesor
#
# -----------------------------------

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

# en este ejemplo vamos a generar funciones para generar los dibujos

def dibujar_elementos(ancho, alto, espesor):    

    # perfil I, iterado para un espesor e
    obj_perfil_I.move_to(y=0)
    obj_perfil_I.config(alto=alto,ancho=ancho,ala=espesor,alma=espesor)
    obj_perfil_I.draw(char=char)
    obj_perfil_I.move(x= separacion_x)

    # Perfil hueco, iterado para un espesor e
    obj_perfil_O.move_to(y=separacion_y)
    obj_perfil_O.config(alto=alto,ancho=ancho,espesor=espesor)
    obj_perfil_O.draw(char=char)
    obj_perfil_O.move(x= separacion_x)

def get_data():
    # devuelve la data del archivo input.txt
    data = []
    try:
        with open('input.txt','r') as file:
            for linea in file.read().split("\n"):
                linea = linea.split("\t")
                if len(linea) == 3:
                    data.append(
                            [float(linea[0]),
                             float(linea[1]),
                             float(linea[2])]
                            )
    except: pass
    print("puntos leidos:",len(data))
    return data


# dibujando ---------------------------------------

for x in get_data():
    dibujar_elementos(*x)


# guardando dxf -----------------------------------
doc.saveas("test.dxf")
print("dibujo dxf generado")


