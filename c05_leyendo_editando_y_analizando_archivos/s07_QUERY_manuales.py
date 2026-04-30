# En este caso usaremos una funcion para
# analizar diferentes entradas para query

import ezdxf
doc = ezdxf.readfile('test.dxf')  # documento DXF
msp = doc.modelspace()

# -----------------------------------
# funcion que dibuja el titulo en pantalla
def titulo(txt): print(f"\n{40*'-'}\n{txt}\n{40*'-'}")
# -----------------------------------
#  Filtrando contenido de modo  manual LINE

titulo("LINE")

for entity in msp:
    if entity.dxftype() == "LINE":
        print(entity.dxf.start, entity.dxf.end)

# -----------------------------------
# Filtrando por nombre de capa

titulo("Elementos en la capa MI_CAPA")

for entity in msp:
    if entity.dxf.layer == "MI_CAPA":
        print(entity.dxftype())

# -----------------------------------
# Circculo con radio  mayor a 4

titulo("CIRCLE con radio mayor a 4")

for entity in msp:
    if entity.dxftype() == "CIRCLE":
        if entity.dxf.radius > 4:
            print("Círculo grande:", entity.dxf.center)

# -----------------------------------
