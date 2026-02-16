#  
# Ejemplo geometrias basicas
# 
# https://ezdxf.readthedocs.io/en/stable/tasks/add_dxf_entities.html
#

import ezdxf

doc = ezdxf.new() 
msp = doc.modelspace()

#------------------------------------------------------
# dibujarndo lineas respecto a coordenadas

msp.add_line([0, 0], [50, 0])  # linea
                               # circulo
msp.add_circle(center=[60, 10], radius=10) 
                               # arco
msp.add_arc(center=[100, 10], radius=10, start_angle=0, end_angle=180)
                               # elipse
msp.add_ellipse(center=[140, 10], major_axis=[20, 0], ratio=0.5)
                               # Polilinea 2D abierta
msp.add_lwpolyline([[0, 30], [20, 50], [40, 30]])
                               # Polilinea 2D cerrada
msp.add_lwpolyline([[0, 40], [20, 60], [40, 40]], close=True)
msp.add_point([50, 50])        # Punto

#------------------------------------------------------

# Guardar el archivo DXF
doc.saveas("test.dxf")
print("Archivo DXF creado correctamente")

