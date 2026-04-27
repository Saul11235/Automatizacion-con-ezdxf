# En este caso usaremos una funcion para
# analizar diferentes entradas para query

import ezdxf
doc = ezdxf.readfile('test.dxf')  # documento DXF
msp = doc.modelspace()

# -----------------------------------
# funcion que dibuja el titulo en pantalla
def titulo(txt): print(f"\n{40*'-'}\n{txt}\n{40*'-'}")
# -----------------------------------


titulo("Sin filtro mostrar todo el contenido del msp")

# -----------------------------------

for entity in msp:
    print(entity.dxftype())


# -----------------------------------
