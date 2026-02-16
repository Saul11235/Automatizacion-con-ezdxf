#  
# Ejemplo  texto
#

import ezdxf

doc = ezdxf.new() 
msp = doc.modelspace()

#------------------------------------------------------

# creando TEXT

msp.add_text( "hola mundo" )

#------------------------------------------------------

doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")

