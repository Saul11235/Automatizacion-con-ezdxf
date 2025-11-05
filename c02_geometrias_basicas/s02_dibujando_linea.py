#  
# Ejemplo 1 - dibujo simple
#

import ezdxf

# nuevo documento DXF
doc = ezdxf.new() 

# Crear modelspace
msp = doc.modelspace()

# dibujarndo lineas 
msp.add_line( [1,1] , [5,5] )

# Guardar el archivo DXF
doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")

