# En este caso usaremos una funcion para
# analizar diferentes entradas para query

import ezdxf
doc = ezdxf.readfile('test.dxf')  # documento DXF
msp = doc.modelspace()

# -----------------------------------
# funcion que dibuja el titulo en pantalla
def titulo(txt): print(f"\n{40*'-'}\n{txt}\n{40*'-'}")
# -----------------------------------

titulo('LINE')

for obj in msp.query('LINE'):              # <- test query
    print(obj)

# -----------------------------------

titulo('LINE CIRCLE TEXT')

for obj in msp.query('LINE CIRCLE TEXT'):  # <- test query
    print(obj)

# -----------------------------------

titulo('*')

for obj in msp.query('*'):                 # <- test query
    print(obj)

# -----------------------------------

titulo('* !LINE !TEXT')

for obj in msp.query('* !LINE !TEXT'):                 # <- test query
    print(obj)

# -----------------------------------



