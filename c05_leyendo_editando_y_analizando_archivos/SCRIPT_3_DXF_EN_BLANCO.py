#
# Ejemplo  bloque con dos instancias
#
#

import ezdxf

doc = ezdxf.new()
msp = doc.modelspace()

doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")
