#  
# Ejemplo  TEXT
#

import ezdxf

doc = ezdxf.new() 
msp = doc.modelspace()

#------------------------------------------------------

# probando hacer un texto de varias lineas 

t = 'Hola mundo\nsoy un texto\nde varias\nlineas'

print(t)            # <-- mostrando en la consola

msp.add_text( t )   # <-- creando TEXT

#------------------------------------------------------

doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")

# 
# Nota: en este caso se hara en una sola linea
#

