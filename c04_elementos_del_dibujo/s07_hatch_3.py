
#
# Ejemplo  hatch (sin polilinea visible)
#
#   https://ezdxf.readthedocs.io/en/stable/tutorials/hatch.html
#

import ezdxf

doc = ezdxf.new()
msp = doc.modelspace()

#------------------------------------------------------
#  creando el hatch
hatch = msp.add_hatch()

#------------------------------------------------------
#  contorno del hatch
puntos_borde  = [(10, 10),(40, 10),(50, 30),(30, 50),(10,30),]
puntos_centro = [(20,10),(15,25),(30,30)]
 
#------------------------------------------------------
#  agregando contornos al hatch
hatch.paths.add_polyline_path( puntos_borde,  is_closed= True)
hatch.paths.add_polyline_path( puntos_centro, is_closed= True)

#------------------------------------------------------
#  configurando el patron
hatch.set_pattern_fill(
    "ar-brstd",   # estilo testeado en LibreCAD
    scale=0.05,
    angle=0
)

#------------------------------------------------------

doc.saveas("test.dxf")
print("Archivo DXF creado correctamente")
