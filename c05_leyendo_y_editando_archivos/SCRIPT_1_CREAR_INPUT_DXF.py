#
# Ejemplo  bloque con dos instancias
#
#

import ezdxf

doc = ezdxf.new()
msp = doc.modelspace()

#------------------------------------------------------

ptos = [ [100,100], [150,100], [150,0], [250,70], [220,150], [150,150]]

lim = len(ptos)

ptos.append(ptos[0])

for x in range(lim):
    msp.add_line(ptos[x],ptos[x+1])


#------------------------------------------------------
# creando marco

vports   = doc.viewports.get('*ACTIVE')

if vports: vport = vports[0] if isinstance(vports, list) else vports
else     : vport = doc.viewports.new('*ACTIVE')

vport.dxf.center =  (189,83)
vport.dxf.target =  0,0,0
vport.dxf.height =  194

#------------------------------------------------------


doc.saveas("test.dxf")
print("Archivo DXF creado correctamente")
