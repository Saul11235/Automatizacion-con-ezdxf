#
# EJEMPLO
# cree un script que analice un documento dxf, que busque todas
# las polilineas y cree una etiqueta en las polilineas buscando area y perimetro
#

import ezdxf

# ----------------------

doc = ezdxf.readfile('test.dxf')  # documento DXF
msp = doc.modelspace()

# ----------------------

def obtiene_datos(puntos):
    # funcion que crea una etiqueta en funcion a un numero de datos
    # calcula area
    n = len(puntos)
    suma = 0
    for i in range(n):
        x1, y1 = puntos[i]
        x2, y2 = puntos[(i + 1) % n]
        suma += (x1 * y2) - (x2 * y1)
    area = abs(suma) / 2
    # calcula perimetro
    n = len(puntos)
    perimetro = 0
    for i in range(n):
        x1, y1 = puntos[i]
        x2, y2 = puntos[(i + 1) % n]
        dx = x2 - x1
        dy = y2 - y1
        distancia = (dx**2 + dy**2) ** 0.5
        perimetro += distancia
    return f"AREA: {area} m2\nPERIMETRO: {perimetro} m"


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


# ----------------------
#
#  Version mas concisa de query
#
for polilinea in msp.query("POLYLINE LWPOLYLINE"):
    # calculando vertices y datos
    vertices = polilinea.get_points()
    puntosXY = []
    for vert in vertices:
        vx   = vert[0]
        vy   = vert[1]
        puntosXY.append([vx,vy])
    #calcula etiqueta y centro de poligono
    centro   = calcular_centro(puntosXY) 
    etiqueta = obtiene_datos(puntosXY)
    # colocando etiqueta al centro
    msp.add_mtext(etiqueta, dxfattribs ={"insert":centro, "color":2, "attachment_point":5} )
    # mensaje
    print("\n Nuevo poligono identificado")
    print(etiqueta)


# ----------------------


doc.saveas('test.dxf')
input("\nok, modificado")
