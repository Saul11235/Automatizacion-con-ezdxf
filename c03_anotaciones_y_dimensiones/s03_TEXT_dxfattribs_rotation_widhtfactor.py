#  
# Ejemplo  texto
#

import ezdxf

doc = ezdxf.new() 
msp = doc.modelspace()

#------------------------------------------------------

msp.add_text(
    "HOLA SOY UN TEXTO",
    dxfattribs={
        "insert"  : (0, 0),   # posición
        "color"   : 1 ,       # rojo (ACI)
        "rotation": 45,       # rotacion del texto
        "width"   : 0.75,     # escala de ancho del texto       
    }
)

#------------------------------------------------------

msp.add_text(
    "HOLA SOY OTRO TEXTO",
    dxfattribs={
        "insert"  : (0, 3),   # posición
        "color"   : 2,        # amarillo(ACI)
        "rotation": -30,      # rotacion del texto
        "width"   : 1.5,     # escala de ancho del texto       
    }
)

#------------------------------------------------------

msp.add_text(
    "hola",
    dxfattribs={
        "insert": (5, -4),  # posición
        "color" : 3,        # verde(ACI)
        "rotation": -180,      # rotacion del texto
        "width"   : -1,     # escala de ancho del texto       
    }
)


#------------------------------------------------------

msp.add_text(
    "mundo",
    dxfattribs={
        "insert": (15, -4), # posición
        "color" : 4,        # cyan (ACI)
        "rotation": -90,      # rotacion del texto
        "width"   : -2,     # escala de ancho del texto       
    }
)

# --------------------------------------------------

doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")



