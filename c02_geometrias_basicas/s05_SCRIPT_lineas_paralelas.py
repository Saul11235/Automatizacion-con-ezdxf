#  
# Ejemplo geometrias basicas
#

import ezdxf

# nuevo documento DXF
doc = ezdxf.new() 

# Crear modelspace
msp = doc.modelspace()

#------------------------------------------------------
# definir una funcion que dibuja una linea respecto a un indice

def dibuja_linea(indice):
    # variables
    deltaY = 1
    longX  = 150
    # coordenadas de puntos
    x1 = 0      ; y1 = indice*deltaY
    x2 = longX  ; y2 = y1
    # dibujando linea
    msp.add_line([x1,y1] , [x2,y2] )

#------------------------------------------------------

for i in range(100): dibuja_linea(i)

#------------------------------------------------------

# Guardar el archivo DXF
doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")

