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
        "insert": (0, 0),   # posición
        "height": 1.5,      # tamaño del texto
        "color" : 1         # rojo (ACI)
    }
)

#------------------------------------------------------

msp.add_text(
    "HOLA SOY OTRO TEXTO",
    dxfattribs={
        "insert": (0, 3),   # posición
        "height": 0.5,      # tamaño del texto
        "color" : 2         # amarillo(ACI)
    }
)

#------------------------------------------------------

msp.add_text(
    "hola",
    dxfattribs={
        "insert": (5, -4),  # posición
        "height": 3.5,      # tamaño del texto
        "color" : 3         # verde(ACI)
    }
)


#------------------------------------------------------

msp.add_text(
    "mundo",
    dxfattribs={
        "insert": (15, -4), # posición
        "height": -1,       # tamaño del texto
        "color" : 4         # cyan (ACI)
    }
)

# --------------------------------------------------

doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")



