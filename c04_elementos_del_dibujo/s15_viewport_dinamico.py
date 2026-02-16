#
# Ejemplo  de elementos de dibujo 
#

import ezdxf

doc = ezdxf.new('R2018')
msp = doc.modelspace()

#------------------------------------------------------
# definiendo coordenadas a hacer encuadre
#
#                     x2 y2
#    +-------------------+
#    |                   |
#    |                   |
#    |       xc yc       |
#    |                   |
#    |                   |
#    |                   |
#    +-------------------+
#   x1 y1

x1,y1  = 8882,33

lado1 = 500
lado2 = 200

x2,y2  =  x1+lado1, y1+lado2


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
# Nota: estas son aproximaciones testeadas en LibreCAD
#       los viewport utilizan otro sistema de coordenadas, distinto a las coordenadas
#       de los objetos, esto es parte del formato DXF
#
vport.dxf.center =  ((x1+x2)/4+57.25, (y1+y2)/4+25.88)
vport.dxf.target =  0,0,0
vport.dxf.height =  (y2-y1)*1.5

#------------------------------------------------------
# muestra las coordenadas del punto

print(f"x1 : {x1}\t y1 : {y1} \nx2 : {x2}\t y2 : {y2}")

#------------------------------------------------------

doc.saveas("test.dxf")
print("Archivo 'test.dxf' creado con exito")


