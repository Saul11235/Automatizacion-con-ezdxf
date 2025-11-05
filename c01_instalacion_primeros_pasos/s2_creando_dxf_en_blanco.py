#  # Ejemplo que crea un nuevo archivo dxf en blanco #

import ezdxf

# nuevo documento DXF
doc = ezdxf.new() 

# Crear modelspace
msp = doc.modelspace()

# Guardar el archivo DXF
doc.saveas("test.dxf")
print("Archivo DXF creado correctamente")

