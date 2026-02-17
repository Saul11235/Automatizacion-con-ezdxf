#  
# Ejemplo creando un croquis
# en este ejemplo vamos a definir un croquis 
# que calculara el area y el perimetro de un conjunto de puntos
# en este caso se creara 
#
#------------------------------------------------------

import ezdxf

doc = ezdxf.new() 
msp = doc.modelspace()

#------------------------------------------------------
# en este caso tendremos un conjunto de puntos 

puntos =  [
        [0,100],
        [50,250],
        [150,200],
        [300,200], ##
        [200,250],
        [175,50],
    ]

#------------------------------------------------------
# definiremos funciones para calcular su area, perimetro y centro
def calcular_area(puntos):
    n = len(puntos)
    suma = 0
    for i in range(n):
        x1, y1 = puntos[i]
        x2, y2 = puntos[(i + 1) % n]
        suma += (x1 * y2) - (x2 * y1)
    area = abs(suma) / 2
    return area


def calcular_perimetro(puntos):
    n = len(puntos)
    perimetro = 0
    for i in range(n):
        x1, y1 = puntos[i]
        x2, y2 = puntos[(i + 1) % n]
        dx = x2 - x1
        dy = y2 - y1
        distancia = (dx**2 + dy**2) ** 0.5
        perimetro += distancia
    return perimetro


def calcular_centro(puntos):
    n = len(puntos)
    suma_cross = 0
    suma_x = 0
    suma_y = 0
    for i in range(n):
        x1, y1 = puntos[i]
        x2, y2 = puntos[(i + 1) % n]
        cross = (x1 * y2) - (x2 * y1)
        suma_cross += cross
        suma_x += (x1 + x2) * cross
        suma_y += (y1 + y2) * cross
    area = suma_cross / 2
    xc = suma_x / (6 * area)
    yc = suma_y / (6 * area)
    return (xc, yc)

#------------------------------------------------------
# funcion para ajustar coordenadas de puntos.

def ajustar_coordenads(puntos,offset_x=0,offset_y=0):
    min_x = puntos[0][0]
    min_y = puntos[0][1]
    for pto in puntos: min_x=min(min_x,pto[0]);min_y=min(min_y,pto[1])
    ajustados=[]
    for pto in puntos:
        ajustados.append([pto[0]-min_x+offset_x,pto[1]-min_y+offset_y])
    return ajustados

def dimensiones(puntos):
    puntos = ajustar_coordenads(puntos)
    max_x  = puntos[0][0] 
    max_y  = puntos[0][1] 
    for pto in puntos: max_x = max(max_x,pto[0]);max_y=max(max_y,pto[1])
    return (max_x,max_y)

#------------------------------------------------------
#
#  Creando bloque de croquis
# 

block = doc.blocks.new(name="croquis")
dim=dimensiones(puntos)
dimx = dim[0]
dimy = dim[1]

puntos_ajustados = ajustar_coordenads(puntos,dim[0]*.1,dim[1]*.1) 

block.add_lwpolyline(
        puntos_ajustados,
        close = True,
        )

block.add_lwpolyline(
        [
            [0       ,0       ],
            [dimx*1.2,0       ],
            [dimx*1.2,dimy*1.2],
            [0       ,dimy*1.2]
            ],
        close =  True
        )
hatch = block.add_hatch()

#  agregando contornos al hatch
#------------------------------------------------------
hatch.paths.add_polyline_path( puntos_ajustados,  is_closed= True)

#  configurando el patron
hatch.set_pattern_fill(
    "ansi31",   # estilo testeado en LibreCAD
    scale=5,
    angle=0,
    color=2
)

for index in range(len(puntos)):
    block.add_text(
            puntos[index],
            dxfattribs={
                "height" : dimy/50,
                "insert" : puntos_ajustados[index],
                "color"  : 1
                }
            )

#------------------------------------------------------
# Difiniendo las capas
doc.layers.new( name="croquis area",      dxfattribs={"lineweight":50,"color":2})
doc.layers.new( name="croquis perimetro", dxfattribs={"lineweight":50,"color":3})
doc.layers.new( name="croquis centro",    dxfattribs={"lineweight":50,"color":4})
doc.layers.new( name="tabla puntos",      dxfattribs={"lineweight":50,"color":5})

#------------------------------------------------------
# Nota dim son las dimensiones x,y del poligono
# en este dibujo se coloca a 1.2 veces el ancho (se coloca 0.1) veces la dimension
# para dar aire al dibujo
msp.add_blockref( "croquis", insert=(0,0 )        , dxfattribs={"layer":"croquis area"})
msp.add_blockref( "croquis", insert=(dimx*1.2,0 ) , dxfattribs={"layer":"croquis perimetro"} )
msp.add_blockref( "croquis", insert=(dimx*2.4,0 ) , dxfattribs={"layer":"croquis centro"})

altura_texto = dimy/30
cota_texto   =-dimy/20

msp.add_text(f" Area: {calcular_area(puntos)} m2"         ,dxfattribs={"height":altura_texto, "insert":(0       ,cota_texto),"color":3,"layer":"croquis area"})
msp.add_text(f" Perimetro: {calcular_perimetro(puntos)} m",dxfattribs={"height":altura_texto, "insert":(dimx*1.2,cota_texto),"color":3,"layer":"croquis perimetro"})
msp.add_text(f" Coord centro: {calcular_centro(puntos)}"  ,dxfattribs={"height":altura_texto, "insert":(dimx*2.4,cota_texto),"color":3,"layer":"croquis centro"})


#  Creando etiquetas haciendo tablas de puntos

contador = 0 -3*altura_texto

for pto in puntos:
    contador -= altura_texto*2 
    msp.add_text(
            str(pto),
            dxfattribs={
                "height" : altura_texto,
                "insert" : (0,contador),
                "layer"  : "tabla puntos",
                }
            )

#------------------------------------------------------
# colocando vista viewport al dibujo

vports   = doc.viewports.get('*ACTIVE')
if vports: vport = vports[0] if isinstance(vports, list) else vports
else     : vport = doc.viewports.new('*ACTIVE')
vport.dxf.center =  ((dimx*3)/4+57.25, (dimy*3)/4+25.88)
vport.dxf.target =  0,0,0
vport.dxf.height =  (dimy)*1.5

#------------------------------------------------------

doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")

