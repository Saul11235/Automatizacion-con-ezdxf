
import ezdxf

doc = ezdxf.new("R2010")
msp = doc.modelspace()

# Línea y punto en 3D
msp.add_line((0, 0, 0), (10, 10, 10))
msp.add_point((5, 5, 5))

# Cubo simple (base + tapa + aristas)
base = [(0,0,0), (10,0,0), (10,10,0), (0,10,0), (0,0,0)]
top  = [(x,y,10) for (x,y,_) in base]

msp.add_polyline3d(base)
msp.add_polyline3d(top)
for p, t in zip(base, top):
    msp.add_line(p, t)

doc.saveas("test.dxf")
print("Archivo generado: test.dxf")
