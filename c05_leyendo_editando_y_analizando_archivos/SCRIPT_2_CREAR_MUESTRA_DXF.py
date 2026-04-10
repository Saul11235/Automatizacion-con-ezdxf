#
# Ejemplo  bloque con dos instancias
#
#

import ezdxf

doc = ezdxf.new()
msp = doc.modelspace()

#------------------------------------------------------
# creando capas
doc.layers.new( name="dibujos",      dxfattribs={"color": 1, "lineweight":50})
doc.layers.new( name="anotaciones",  dxfattribs={"color": 2, "lineweight":50})
doc.layers.new( name="sketch",       dxfattribs={"color": 3, "lineweight":50})
doc.layers.new( name="dimensiones",  dxfattribs={"color": 4, "lineweight":50})
doc.layers.new( name="marco",        dxfattribs={"color": 5, "lineweight":50})

#------------------------------------------------------
#  Creando bloques
blockA = doc.blocks.new(name="Bloque A")
blockA.add_text(" A",dxfattribs={"height":0.75,"insert":[1,1]})
blockA.add_lwpolyline( [ (0,0),(3,0),(3,3),(0,3),(0,0)], dxfattribs={"color": 6} )

blockB = doc.blocks.new(name="Bloque B")
blockB.add_text(" B",dxfattribs={"height":0.75,"insert":[1,1]})
blockB.add_lwpolyline( [ (0,0),(3,0),(3,3),(0,3),(0,0)], dxfattribs={"color": 8} )

blockC = doc.blocks.new(name="Bloque C")
blockC.add_text(" C",dxfattribs={"height":0.75,"insert":[1,1]})
blockC.add_lwpolyline( [ (0,0),(3,0),(3,3),(0,3),(0,0)], dxfattribs={"color": 9} )
 
#  colocando instancias del bloque en el modelspace
for x in range(20,60,5) : msp.add_blockref("Bloque A", insert=(170,x))
for x in range(15,70,8) : msp.add_blockref("Bloque B", insert=(180,x))
for x in range( 5,80,10): msp.add_blockref("Bloque C", insert=(190,x))

#------------------------------------------------------
# creando marco

xmarco, ymarco, hmarco, vmarco = 20,0, 90,180
msp.add_lwpolyline( [ (xmarco,ymarco),(xmarco,ymarco+hmarco),(xmarco+vmarco,ymarco+hmarco),(xmarco+vmarco,ymarco),(xmarco,ymarco)], dxfattribs={"layer": "marco"} )

vports   = doc.viewports.get('*ACTIVE')

if vports: vport = vports[0] if isinstance(vports, list) else vports
else     : vport = doc.viewports.new('*ACTIVE')

vport.dxf.center =  (106,45)
vport.dxf.target =  0,0,0
vport.dxf.height =  91

#------------------------------------------------------
# creando texto
def crear_txt(txt,x,y,height=1):
    msp.add_text(txt,dxfattribs={"insert": (x, y),"height": height,"layer" : "anotaciones"})

def crear_mtxt(txt,x,y,height=1):
    msp.add_mtext(txt,dxfattribs={"insert": (x, y),"char_height": height,"layer" : "anotaciones"})

for x in range(5,80,2): crear_txt(f"texto en {x}",25,x)
crear_txt("PRUEBA DE OBJETOS DXF",73,84,4)
txt = "texto varias lineas\notra linea\ny una linea mas\ny otra."
for x in range(40,180,20):crear_mtxt(txt,x, 80)

#------------------------------------------------------
# dibujarndo lineas respecto a coordenadas

msp.add_line([100,65], [150,65], dxfattribs={"layer":"dibujos"})  
msp.add_line([100,66], [150,66], dxfattribs={"layer":"dibujos"})  
msp.add_line([100,67], [150,67], dxfattribs={"layer":"dibujos"})  
msp.add_lwpolyline([[100, 30], [120, 50], [140, 30]] , dxfattribs={"layer":"dibujos"})
msp.add_lwpolyline([[100, 40], [120, 60], [140, 40]], close=True , dxfattribs={"layer":"dibujos"})
msp.add_point([120, 30])     

msp.add_circle(center=[60, 15], radius=10 , dxfattribs={"layer":"sketch"}) 
msp.add_arc(center=[100, 15], radius=10, start_angle=0, end_angle=180, dxfattribs={"layer":"sketch"})
msp.add_ellipse(center=[140, 15], major_axis=[20, 0], ratio=0.5 , dxfattribs={"layer":"sketch"})

#------------------------------------------------------
# creando un hatch

puntos = [(50, 30),(80, 30),(90, 60),(70, 70),(50,50),]
 
hatch = msp.add_hatch()

hatch.paths.add_polyline_path(
    puntos,
    is_closed=True
)

hatch.set_pattern_fill(
    "ar-brstd",   # estilo testeado en LibreCAD
    scale=0.1,
    angle=0
)


#------------------------------------------------------
# configurando

doc.header['$DIMASZ']   = 2.5      # Arrow size
doc.header['$DIMDEC']   = 3        # Decimal precision
doc.header['$DIMDSEP']  = ord(',') # Decimal separator: ',' Nota: ord lo convierte a unicode
doc.header['$DIMLFAC']  = 0.5      # Length factor

#------------------------------------------------------
# elementos dimension

msp.add_leader(
    vertices = [(75, 80), (75, 70), (70, 70)],
    dxfattribs = {"layer":"dimensiones"}
)

msp.add_linear_dim(
    base  = (130,69),
    p1    = (100,69),
    p2    = (150,69),
    text  = "DIMH = <> km",
    dxfattribs = {"layer":"dimensiones"}
)

dim_v = msp.add_linear_dim(
    base  = (40,40),
    p1    = (50,30),
    p2    = (50,50),
    angle = 90,
    text  = "DIMV = <> mm",
    dxfattribs = {"layer":"dimensiones"}
)



#------------------------------------------------------

doc.saveas("test.dxf")
print("Archivo DXF creado correctamente")
