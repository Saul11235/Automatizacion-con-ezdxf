#  
# Ejemplo  texto
#
#   https://ezdxf.readthedocs.io/en/stable/tutorials/text.html
#

import ezdxf
from ezdxf.enums import TextEntityAlignment as algn

doc = ezdxf.new() 
msp = doc.modelspace()

#------------------------------------------------------
#
#  haciendo una prueba de alineamiento
#  se hara respecto a un punto rojo
#  

def punto(x,y):  # esta funcion muestra un punto de forma vistosa
    msp.add_circle((x,y),radius=0.1,dxfattribs={"color":1})
    msp.add_circle((x,y),radius=0.2,dxfattribs={"color":1})
    msp.add_circle((x,y),radius=0.3,dxfattribs={"color":1})
    msp.add_circle((x,y),radius=1  ,dxfattribs={"color":1})


#  Vert/Horiz  | Left        | Center        | Right
#  ------------|-------------|---------------|----------
#  Top         | TOP_LEFT    | TOP_CENTER    | TOP_RIGHT
#  Middle      | MIDDLE_LEFT | MIDDLE_CENTER | MIDDLE_RIGHT
#  Bottom      | BOTTOM_LEFT | BOTTOM_CENTER | BOTTOM_RIGHT
#  Baseline    | LEFT        | CENTER        | RIGHT
#

msp.add_text("TOP_LEFT").set_placement((100,100),align=algn.TOP_LEFT) 
punto(100,100)

msp.add_text("TOP_CENTER").set_placement((150,100),align=algn.TOP_CENTER) 
punto(150,100)

msp.add_text("TOP_RIGHT").set_placement((200,100),align=algn.TOP_RIGHT) 
punto(200,100)




msp.add_text("MIDDLE_LEFT").set_placement((100,80),align=algn.MIDDLE_LEFT) 
punto(100,80)

msp.add_text("MIDDLE_CENTER").set_placement((150,80),align=algn.MIDDLE_CENTER) 
punto(150,80)

msp.add_text("MIDDLE_RIGHT").set_placement((200,80),align=algn.MIDDLE_RIGHT) 
punto(200,80)




msp.add_text("BOTTOM_LEFT").set_placement((100,60),align=algn.BOTTOM_LEFT) 
punto(100,60)

msp.add_text("BOTTOM_CENTER").set_placement((150,60),align=algn.BOTTOM_CENTER) 
punto(150,60)

msp.add_text("BOTTOM_RIGHT").set_placement((200,60),align=algn.BOTTOM_RIGHT) 
punto(200,60)



msp.add_text("LEFT").set_placement((100,40),align=algn.LEFT) 
punto(100,40)

msp.add_text("CENTER").set_placement((150,40),align=algn.CENTER) 
punto(150,40)

msp.add_text("RIGHT").set_placement((200,40),align=algn.RIGHT) 
punto(200,40)


# --------------------------------------------------

doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")



