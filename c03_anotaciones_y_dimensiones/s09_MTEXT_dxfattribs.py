#  
# Ejemplo  mtext 
#

import ezdxf

doc = ezdxf.new() 
msp = doc.modelspace()

#------------------------------------------------------

# probando hacer un texto de varias lineas 

texto_var = 'Hola mundo\nsoy un texto\nde varias\nlineas'

msp.add_mtext(
    texto_var,
    dxfattribs={
        "style"              : "romanc",
        "insert"             : (10,20),  # pto insercion
        "char_height"        : 2.5,      # altura del texto
        "width"              : 20,       # ancho del párrafo
        "color"              : 2,        # color (amarillo ACI)
        "rotation"           : 45,       # rotación (grados)
        "attachment_point"   : 5,        # alineación (centro)
        "line_spacing_factor": 1.2,      # interlineado
        "bg_fill"            : 1         # fondo activado
                }
)

#------------------------------------------------------

doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")

