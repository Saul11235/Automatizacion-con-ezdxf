#
# Ejemplo  bloque con dos instancias
#
#   https://ezdxf.readthedocs.io/en/stable/tutorials/blocks.html
#

import ezdxf

doc = ezdxf.new()
msp = doc.modelspace()

#------------------------------------------------------
#  Creando un bloque
block = doc.blocks.new(name="MI_BLOQUE")

#  creando contenido del bloque
block.add_lwpolyline( [ (0,0),(20,0),(20,10),(0,10),(0,0)], dxfattribs={"color": 3} )
block.add_line      ( (0,0),  (20,10),  dxfattribs={"color":1} )
  
#------------------------------------------------------
#  colocando instancias del bloque en el modelspace

msp.add_blockref( "MI_BLOQUE", insert=(10,10) )
msp.add_blockref( "MI_BLOQUE", insert=(50,20) )
msp.add_blockref( "MI_BLOQUE", insert=(40,30) )

#------------------------------------------------------
doc.saveas("test.dxf")
print("Archivo DXF creado correctamente")
