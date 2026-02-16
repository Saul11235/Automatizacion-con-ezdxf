import ezdxf

doc = ezdxf.new('R2010')  # documento DXF
msp = doc.modelspace()    # Espacio modelo

# definiendo elementos en capas

# capa:  "lineas"
msp.add_line((0, 0),    (100, 100), dxfattribs={"layer":"lineas"})     
msp.add_line((130, 40), (10, 20)  , dxfattribs={"layer":"lineas"})     
msp.add_line((10, 140), (130, 10) , dxfattribs={"layer":"lineas"})     

# capa:  "circulos"
msp.add_circle((250, 50), 25, dxfattribs={"layer":"circulos"})       
msp.add_circle((220, 80), 35, dxfattribs={"layer":"circulos"})       
msp.add_circle((200, 10), 45, dxfattribs={"layer":"circulos"})       

doc.saveas("test.dxf") 
print("creado ok")
