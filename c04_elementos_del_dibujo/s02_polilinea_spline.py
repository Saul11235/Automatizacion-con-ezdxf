
#
# Ejemplo  polilinea y spline
#   https://ezdxf.readthedocs.io/en/stable/tutorials/polyline.html

import ezdxf

doc = ezdxf.new()
msp = doc.modelspace()

#------------------------------------------------------
#  ejemplo de polilinea 2D

puntos = [(10, 10),(40, 10),(50, 30),(30, 50),(10,30),]

#------------------------------------------------------
#  dibujando la polilinea
msp.add_lwpolyline(
    puntos,
    dxfattribs={
        "color"     : 3,     # color verde (ACI)
        "closed"    : True,  # cerrar la polilinea
        "lineweight": 25     # grosor de linea
    }
)

#------------------------------------------------------
doc.saveas("test.dxf")
print("Archivo DXF creado correctamente")
