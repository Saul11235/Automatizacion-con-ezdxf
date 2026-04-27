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
    print("\t\t Layer:",obj.dxf.layer)
    print("\t\t Color:",obj.dxf.color)
#
# -----------------------------------

titulo('LINE[layer=="dibujos"]')

for obj in msp.query('LINE[layer=="dibujos"]'):              # <- test query
    print(obj)
    print("\t\t Layer:",obj.dxf.layer)
    print("\t\t Color:",obj.dxf.color)
#
# -----------------------------------

titulo('LINE[layer!="dibujos"]')

for obj in msp.query('LINE[layer!="dibujos"]'):              # <- test query
    print(obj)
    print("\t\t Layer:",obj.dxf.layer)
    print("\t\t Color:",obj.dxf.color)
#
# -----------------------------------

titulo('* !LINE')

for obj in msp.query('* !LINE'):              # <- test query
    print(obj)
    print("\t\t Layer:",obj.dxf.layer)
    print("\t\t Color:",obj.dxf.color)
#
# -----------------------------------

