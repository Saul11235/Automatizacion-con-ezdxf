
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
mi_objeto_hatch = msp.add_hatch()

#------------------------------------------------------
#  agregando el contorno directamente al hatch
mi_objeto_hatch.paths.add_polyline_path(
    puntos,
    is_closed=True
)

#------------------------------------------------------
#  mi_objeto_hatch.set_solid_fill()
#  Nota:  relleno solido
#------------------------------------------------------
#  configurando el patron

mi_objeto_hatch.set_pattern_fill(
    "ar-brstd",   # estilo testeado en LibreCAD
    scale=0.1,
    angle=0
)

#------------------------------------------------------

doc.saveas("test.dxf")
print("Archivo DXF creado correctamente")
