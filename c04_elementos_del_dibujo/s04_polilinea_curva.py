
#
# Ejemplo  polilinea con curvas
#
#   https://ezdxf.readthedocs.io/en/stable/tutorials/polyline.html
#

import ezdxf

doc = ezdxf.new()
msp = doc.modelspace()

#------------------------------------------------------
#
#  puntos de la polilinea con bulge (curvatura)
#  cada tupla es (x, y, bulge)
#  bulge > 0: curva hacia la izquierda
#  bulge < 0: curva hacia la derecha
#

puntos = [
    (10, 10, 0),    # linea recta
    (40, 10, 0.5),  # curva suave hacia arriba
    (50, 30, -0.3), # curva hacia abajo
    (30, 50, 0),    # linea recta
    (10, 30, 0.2),  # curva leve
]

#------------------------------------------------------
#  dibujando la polilinea con curvas
msp.add_lwpolyline(
    puntos,
    format="xyb",  # indica que cada tupla tiene x, y, bulge
    dxfattribs={
        "color"     : 6,     # magenta
        "closed"    : True,  # cerrar la polilinea
        "lineweight": 25
    }
)

#------------------------------------------------------

doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")
