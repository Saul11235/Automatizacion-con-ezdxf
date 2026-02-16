#
# Ejemplo  de elementos de dibujo 
#

import ezdxf

doc = ezdxf.new('R2018')
msp = doc.modelspace()

#------------------------------------------------------
# definiendo capas

doc.layers.new(name="miCapa", dxfattribs={"color":4,"lineweight":25} )
       
#------------------------------------------------------
# dibujando elementos

msp.add_text("Texto1", dxfattribs={"insert": (105,201),"layer":"miCapa"})
msp.add_text("Texto2", dxfattribs={"insert": (125,201),"layer":"miCapa"})
msp.add_text("Texto3", dxfattribs={"insert": (145,201),"layer":"miCapa"})

msp.add_lwpolyline( [ [100,200],[100,205],[120,205],[120,200] ] ,  dxfattribs = {"layer":"miCapa","closed":True} )
msp.add_lwpolyline( [ [120,200],[120,205],[140,205],[140,200] ] ,  dxfattribs = {"layer":"miCapa","closed":True} )
msp.add_lwpolyline( [ [140,200],[140,205],[160,205],[160,200] ] ,  dxfattribs = {"layer":"miCapa","closed":True} )


# Nota, este dibujo será del tipo
#
#  (100,205)                             (160,205)
#     +-----------+----------+-----------+
#     |           |          |           |
#     |  TEXTO 1  | TEXTO 2  |  TEXTO 3  |
#     |           |          |           |
#     +-----------+----------+-----------+
#   (100,200)                            (160,200)
#
#  Nota: este script no ajusta la visibilidad de las vars

#------------------------------------------------------

doc.saveas("test.dxf")
print("Archivo 'test.dxf' creado con exito")
