import ezdxf

# ----------------------

doc = ezdxf.readfile('test.dxf')  # documento DXF
msp = doc.modelspace()

# ----------------------
print("ok, archivo leido")
