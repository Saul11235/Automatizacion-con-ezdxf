import ezdxf

# ----------------------

doc = ezdxf.readfile('test.dxf')  # documento DXF
msp = doc.modelspace()

# ----------------------
#
#  Version mas concisa de query
#
for linea in msp.query("LINE"):
    x1, y1 = linea.dxf.start.x , linea.dxf.start.y
    x2, y2 = linea.dxf.end.x   , linea.dxf.end.y
    print(f'desde ({x1}, {y1})\t hasta ({x2}, {y2})')

# ----------------------

print("\nok, archivo leido")
