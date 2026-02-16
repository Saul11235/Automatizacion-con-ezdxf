#  
# Ejemplo geometrias basicas
#

import ezdxf

doc = ezdxf.new() 
msp = doc.modelspace()

#------------------------------------------------------
# dibujarndo dragon fractal

def dragon_fractal(puntos):
    print(f' {len(puntos)} vertices')
    respuesta = []
    Xanterior = 0
    Yanterior = 0
    Sentido   = -1
    primero   = True
    for p in puntos:
        if primero: primero = False
        else:
            # punto medio entre pto anterior 
            Xmedio   = ( Xanterior+p[0] )/2
            Ymedio   = ( Yanterior+p[1] )/2
            # vector entre pto anterior hacia pto medio
            Xvector  = Xmedio - Xanterior
            Yvector  = Ymedio - Yanterior
            # vector perpendicular
            Xperp    = -Yvector * Sentido
            Yperp    = Xvector * Sentido
            # calculando ertice fractal
            Xfractal = Xmedio + Xperp
            Yfractal = Ymedio + Yperp
            # colocando vertice fractal
            respuesta.append([Xfractal,Yfractal])
        Xanterior  = p[0]; Yanterior = p[1]
        Sentido   *= -1
        respuesta.append(p)
    return respuesta

puntos           =  [[0,0],[2,0]]
nro_iteraciones  =  4

for _ in range(nro_iteraciones): puntos = dragon_fractal(puntos)

msp.add_lwpolyline(puntos,dxfattribs={"color":4})

#------------------------------------------------------

doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")

