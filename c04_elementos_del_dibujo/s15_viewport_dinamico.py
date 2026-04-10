#
# Ejemplo  de elementos de dibujo 
#

import ezdxf

doc = ezdxf.new('R2018')
msp = doc.modelspace()

#------------------------------------------------------
# definiendo coordenadas a hacer encuadre
#
#    +-------------------+ x2 y2 
#    |                   |
#    |                   |
#    |       xc yc       |  h viewport
#    |                   |  
#    |                   |
#    |                   |
#    +-------------------+
#    x1,y1

xc,yc  = 12292,12332
hview  = 250

#------------------------------------------------------
x1,y1  = xc-hview/2,yc-hview/2
x2,y2  = xc+hview/2,yc+hview/2

#------------------------------------------------------
# realizando dibujo

doc.layers.new(name="miCapa", dxfattribs={"color":4,"lineweight":200} )
msp.add_lwpolyline( [[x1,y1],[x1,y2],[x2,y2],[x2,y1],[x1,y1],[x2,y2],[x2,y1],[x1,y2]] ,
                   dxfattribs = {"layer":"miCapa","closed":True} )

#--------------------------------------------------------
# Definiendo viewport de archivo DXF

vports   = doc.viewports.get('*ACTIVE')

if vports: vport = vports[0] if isinstance(vports, list) else vports
else     : vport = doc.viewports.new('*ACTIVE')

#
# Nota: testeado en LibreCAD
#
vport.dxf.center =  ( xc/2 +0.5767*hview -0.06826, yc/2 +0.25901*hview -0.021 )
vport.dxf.target =  0,0,0
vport.dxf.height =  hview*1.05

#------------------------------------------------------
# muestra las coordenadas del punto

print(f"x1 : {x1}\t y1 : {y1} \nx2 : {x2}\t y2 : {y2}")

#------------------------------------------------------

doc.saveas("test.dxf")
print("Archivo 'test.dxf' creado con exito")


