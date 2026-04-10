# Ejemplo sencillo de programa de consola 
#

import ezdxf
from   perfil_I       import *

# -----------------------------------
print("""
            Alma
            +---+
            |   |
                         -+-
       ███████████████    |
            █████         |
            █████         |
            █████         | Alto
            █████         |
    +-      █████         |
Ala |  ███████████████    |
    +-                   -+-
       +-------------+
            Ancho
      """)
# -----------------------------------

def input_float(text):
    try:    return float(input(text))
    except: return input_float(text)

alto  = input_float(" Ingrese Alto  : ")
ancho = input_float(" Ingrese Ancho : ")
ala   = input_float(" Ingrese Ala   : ")
alma  = input_float(" Ingrese Alma  : ")

if alto!=0 and ancho!=0 and ala!=0 and alma!=0:
    objeto = perfil_I()
    objeto.config(ancho,alto,ala,alma)
    # --------------------------------
    try   : objeto.draw()
    except: print("Error al graficar revisar datos")
    # --------------------------------
    doc=objeto.get_doc()
    doc.saveas("test.dxf")
else:
    print("Error un dato es nulo, no se puede graficar.")
