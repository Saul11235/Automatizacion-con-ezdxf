#  
# Ejemplo 1 - dibujo simple
#

import ezdxf

# nuevo documento DXF
doc = ezdxf.new() 

# Crear modelspace
msp = doc.modelspace()

# dibujarndo lineas 
msp.add_line( [1,1] , [5,5] , dxfattribs = {"color":3} )

#  ----------------------------------
#
# Nota: dxfatribs es un atributo de un diccionario
#       indicando con los atributos de un objeto
#
#       En este caso color 3 = verde
#
#  ----------------------------------

# Guardar el archivo DXF
doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")

