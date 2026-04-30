# ----------------------
import ezdxf

doc = ezdxf.readfile('test.dxf')  # documento DXF
msp = doc.modelspace()

# ----------------------
# En este ejemplo buscaremos todos los elementos LINE de un 

lineas = msp.query("LINE") 

# esto devuelve todos los elementos LINE del dibujo

for elemento in lineas:
    print(elemento)

# ----------------------

print("\nok, archivo leido")
