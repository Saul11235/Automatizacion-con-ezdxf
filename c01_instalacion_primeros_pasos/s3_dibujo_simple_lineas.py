#  
# Ejemplo 1 - dibujo simple
#

import ezdxf

# nuevo documento DXF
doc = ezdxf.new() 

# Crear modelspace
msp = doc.modelspace()

# dibujarndo lineas respecto a coordenadas
msp.add_line( [0,3] , [7,7] )
msp.add_line( [7,7] , [7,3] )
msp.add_line( [7,3] , [0,3] )

# Guardar el archivo DXF
doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")

