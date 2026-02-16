#  
# Ejemplo true color
# https://ezdxf.readthedocs.io/en/stable/concepts/true_color.html
#
# ---------------------------------------------

import ezdxf

doc = ezdxf.new()       # nuevo documento DXF
msp = doc.modelspace()  # crear modelspace

#------------------------------------------------------
# definir una funcion que dibuja una linea respecto a un indice

def dibuja_linea(R,G,B):
    # define aqui el codigo que calcule las dimensiones x1,x2,y1,y2
    #  y que coloque una linea  para generar un diagrama de vista rgb
    # ------------------------- 
    x1 = R/G+B 
    y1 = G/R+R 
    x2 = x1+1
    y2 = y1+1
    # ------------------------
    # dibujando linea en funcion de rgb
    line = msp.add_line((x1,y1), (x2,y2))
    line.rgb = (R,G,B)

#------------------------------------------------------
#  dibujando varias lineas una por cada color, 

salto = 10 # <- DISTANCIA DE ITERACION

#------------------------------------------------------

for R in range(1,255,salto): 
    for G in range(1,255,salto): 
        for B in range(1,255,salto): 
            dibuja_linea(R,G,B)

#------------------------------------------------------

# Guardar el archivo DXF
doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")

