
#
# Ejemplo  hatch (sin polilinea visible)
#
#   https://ezdxf.readthedocs.io/en/stable/tutorials/hatch.html
#

import ezdxf

doc = ezdxf.new()
msp = doc.modelspace()

#------------------------------------------------------
#  contorno del hatch

puntos = [(10, 10),(40, 10),(50, 30),(30, 50),(10,30),]
 
#------------------------------------------------------
#  creando el hatch
hatch = msp.add_hatch()

#------------------------------------------------------
#  agregando el contorno directamente al hatch
hatch.paths.add_polyline_path(
    puntos,
    is_closed=True
)

#------------------------------------------------------
#  configurando el patron
hatch.set_solid_fill()

#------------------------------------------------------

doc.saveas("test.dxf")
print("Archivo DXF creado correctamente")
