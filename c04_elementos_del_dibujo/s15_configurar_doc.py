#
# Ejemplo configuracion
#

import ezdxf

doc = ezdxf.new('R2018')
msp = doc.modelspace()

#------------------------------------------------------
# definiendo capas

doc.layers.new(name="miCapa", dxfattribs={"color":1,"lineweight":200} )
       
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


#========================================================
# CONFIGURACIÓN GENERAL DE UNIDADES (DXF / AutoCAD)
#========================================================

# $INSUNITS → unidades del dibujo (1 unidad del modelo = ?)
# 0  = Sin unidades (NO recomendado)
# 1  = Pulgadas
# 2  = Pies
# 3  = Millas
# 4  = Milímetros
# 5  = Centímetros
# 6  = Metros              <-- recomendado ingeniería / arquitectura
# 7  = Kilómetros
# 8  = Microinches
# 9  = Mils
# 10 = Yardas

doc.header['$INSUNITS'] = 6


#--------------------------------------------------------

# $MEASUREMENT → sistema métrico o imperial
# 0 = Imperial
# 1 = Métrico              <-- recomendado
#
doc.header['$MEASUREMENT'] = 1


#--------------------------------------------------------

# $LUNITS → formato de unidades lineales
# 1 = Científico
# 2 = Decimal              <-- más común
# 3 = Ingeniería
# 4 = Arquitectónico
# 5 = Fraccionario
#
doc.header['$LUNITS'] = 2


#--------------------------------------------------------

# $LUPREC → precisión decimal lineal
# 0 = 10
# 1 = 10.0
# 2 = 10.00
# 3 = 10.000               <-- típico
# 4 = 10.0000
#
doc.header['$LUPREC'] = 3


#--------------------------------------------------------

# $AUNITS → unidades angulares
# 0 = Grados decimales     <-- típico
# 1 = Grados / Min / Seg
# 2 = Gradianes
# 3 = Radianes
# 4 = Topográfico
#
doc.header['$AUNITS'] = 0


#--------------------------------------------------------

# $AUPREC → precisión angular
# 0 = 0
# 1 = 0.0
# 2 = 0.00                <-- típico
# 3 = 0.000
#
doc.header['$AUPREC'] = 2

#------------------------------------------------------

doc.saveas("test.dxf")
print("Archivo 'test.dxf' creado con exito")


