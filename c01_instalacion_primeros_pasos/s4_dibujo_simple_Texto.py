#  
# Ejemplo 2 - dibujo simple
#

import ezdxf

# nuevo documento DXF
doc = ezdxf.new() 

# MODELSPACE ---------------------------
msp = doc.modelspace()

msp.add_line( [0,3] , [7,7] )
msp.add_line( [7,7] , [7,3] )
msp.add_line( [7,3] , [0,3] )
msp.add_text("Hola")



# --- Ahora trabajamos en el PAPERSPACE ---




# Guardar el archivo DXF
doc.saveas("test.dxf")

print("nuevoArchivo DXF creado correctamente")

