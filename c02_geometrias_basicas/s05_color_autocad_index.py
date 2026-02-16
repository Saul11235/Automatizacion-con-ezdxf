#  
# Ejemplo lineas y color
# https://ezdxf.readthedocs.io/en/stable/concepts/aci.html
#
# ---------------------------------------------

import ezdxf

doc = ezdxf.new()       # nuevo documento DXF
msp = doc.modelspace()  # crear modelspace

#------------------------------------------------------
# definir una funcion que dibuja una linea respecto a un indice

def dibuja_linea(indice):
    deltaY = 1     # variables
    longX  = 150
    # coordenadas de puntos
    x1 = 0      ; y1 = indice*deltaY
    x2 = longX  ; y2 = y1
    # dibujando linea
    msp.add_line([x1,y1] , [x2,y2] , dxfattribs = {"color":indice})

#------------------------------------------------------
#  dibujando varias lineas una por cada color, hay 255 en total

for i in range(255): dibuja_linea(i)

#------------------------------------------------------

# Guardar el archivo DXF
doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")

