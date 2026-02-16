#  
# Ejemplo  texto
#

import ezdxf

doc = ezdxf.new() 
msp = doc.modelspace()

#------------------------------------------------------
#
#  otro metodo de posicionar los elementos TEXT
#  sera utilizando el método set_placement
#

# sin metodo placement (se coloca en el inicio
obj1 = msp.add_text("hola")
 
# set_placement solo con ubicacion
obj2 = msp.add_text("adios")
obj2.set_placement((20,20))

# set_placement solo con ubicacion
from ezdxf.enums import TextEntityAlignment  #<--- parte de ezdxf para alineamientos de texto

obj3 = msp.add_text("hasta luego")
obj3.set_placement((10,20),align=TextEntityAlignment.TOP_CENTER) 

# --------------------------------------------------

doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")



