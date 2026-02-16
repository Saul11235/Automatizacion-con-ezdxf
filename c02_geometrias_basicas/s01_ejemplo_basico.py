import ezdxf

doc = ezdxf.new('R2010')  # documento DXF
msp = doc.modelspace()    # Espacio modelo

msp.add_line((0, 0), (100, 100))     
msp.add_circle((50, 50), 25)       

doc.saveas("test.dxf") 

# ----------------------
print("ok")
