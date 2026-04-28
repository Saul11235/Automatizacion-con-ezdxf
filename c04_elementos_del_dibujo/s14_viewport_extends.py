#
# Ejemplo  de elementos de dibujo 
#

import ezdxf

doc = ezdxf.new('R2018')
msp = doc.modelspace()

#------------------------------------------------------
# definiendo capas

doc.layers.new(name="miCapa", dxfattribs={"color":4,"lineweight":200} )
       
#------------------------------------------------------
# dibujando elementos

msp.add_text("Texto1", dxfattribs={"insert": (105,201),"layer":"miCapa"})
msp.add_text("Texto2", dxfattribs={"insert": (125,201),"layer":"miCapa"})
msp.add_text("Texto3", dxfattribs={"insert": (145,201),"layer":"miCapa"})

msp.add_lwpolyline( [ [100,200],[100,204],[120,204],[120,200] ] ,  dxfattribs = {"layer":"miCapa","closed":True} )
msp.add_lwpolyline( [ [120,200],[120,204],[140,204],[140,200] ] ,  dxfattribs = {"layer":"miCapa","closed":True} )
msp.add_lwpolyline( [ [140,200],[140,204],[160,204],[160,200] ] ,  dxfattribs = {"layer":"miCapa","closed":True} )


# Nota, este dibujo será del tipo
#
#  (100,204)                             (160,204)
#     +-----------+----------+-----------+
#     |  TEXTO 1  | TEXTO 2  |  TEXTO 3  |
#     +-----------+----------+-----------+
#   (100,200)                            (160,200)
#
#
#  Centro de la vista  (130,202)
#  Altura vista 4  unidades
#  Ancho  vista 60 unidades
#
#------------------------------------------------------
# Definiendo viewport de archivo DXF

vports   = doc.viewports.get('*ACTIVE')

if vports: vport = vports[0] if isinstance(vports, list) else vports
else     : vport = doc.viewports.new('*ACTIVE')

    # colocando centro y altura de la vista
vport.dxf.center = (82,107 )    # ojo no es en el centro de coord
vport.dxf.height = 30           # es la altura de la vista

#------------------------------------------------------

doc.saveas("test.dxf")
print("Archivo 'test.dxf' creado con exito")


