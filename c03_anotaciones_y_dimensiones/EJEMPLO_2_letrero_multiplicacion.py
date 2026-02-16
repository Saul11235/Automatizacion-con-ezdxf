#  
# Ejemplo letrero multiplicacion
#

import ezdxf

doc = ezdxf.new() 
msp = doc.modelspace()

#------------------------------------------------------
# configurando Header vars para dar estilo al DXF

doc.header['$DIMTXSTY'] = 'romanc'
doc.header['$DIMASZ']   = 0.5      # Arrow size
doc.header['$DIMTXT']   = 0.75     # Text height
doc.header['$DIMCLRT']  = 5        # Text Color: Blue
doc.header['$DIMCLRD']  = 6        # Dimension Line Color: Magenta
doc.header['$DIMCLRE']  = 2        # Extension Line Color: Yellow
doc.header['$DIMDEC']   = 3        # Decimal precision
doc.header['$DIMDSEP']  = ord('.') # Decimal separator: '.' Nota: ord lo convierte a unicode
doc.header['$DIMLFAC']  = 0.5      # Length factor

#------------------------------------------------------

def linea_txt(contenido="hola mundo", color=4, xpos=0, ypos=0):
    # dibuja linea de texto
    text = msp.add_text(
            " "+contenido,
            dxfattribs ={
                "height" : 0.75,
                "style"  : "romanc",
                "color"  : color
                })
    text.dxf.insert = (xpos, ypos)


def dibujar_dimension(x1,y1,x2,y2,distance=0.5):
    # dibuja elemento de dimension lineal
    msp.add_aligned_dim(
            p1         = (x1,y1),
            p2         = (x2,y2),
            text       = "<> cm", 
            distance   = distance, 
            dxfattribs = {
                "layer" : "dim",
                "layer" : "dimension"
                        } ) 


def dibujar_tabla(x=0,y=0, base=12, orden=5, color=2, ancho=12):
    # funcion que dibuja una tabla de multiplicar
    print(f" Nueva tabla del {base}, en {x},{y}")
    # creando contador para crear ineas
    contadorY=y
    contador =0
    linea_txt(f"TABLA DEL {base}",color,x,contadorY)
    for i in range(orden):
        contadorY -= 1
        texto      =  f"{base} x {i+1} = {base*(i+1)}"
        linea_txt(texto,color,x,contadorY)
    # calculando vertices cuadro
    x1 = x
    y1 = y +1
    x2 = x+ancho
    y2 = y +1
    x3 = x+ancho
    y3 = contadorY-0.2
    x4 = x
    y4 = contadorY-0.2
    # dibujando cuadro
    puntos = [ (x1,y1),(x2,y2),(x3,y3),(x4,y4) ]
    msp.add_lwpolyline(puntos, dxfattribs={"closed": True,"color":color})
    # dibujando elementos de dimension
    dibujar_dimension( x1,y1, x2,y2             )
    dibujar_dimension( x2,y2, x3,y3, distance=2 )
    dibujar_dimension( x3,y3, x4,y4, distance=2 )
    dibujar_dimension( x1,y1, x4,y4, distance=-2)

# este es un ejemplo que ha va a aumentar 

def dibujar_varias_tablas(desde=4, hasta=15, orden=9, step=20):
    distX = 0
    for base in range(desde,hasta):
        distX  += step
        dibujar_tabla(distX,0,base, orden, base)

#------------------------------------------------------
# escribiendo lineas

dibujar_varias_tablas()

#------------------------------------------------------

doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")
