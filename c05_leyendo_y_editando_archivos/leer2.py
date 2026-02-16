
import ezdxf

# =====================
# 1. Abrir el archivo DXF
# =====================
doc = ezdxf.readfile("input.dxf")
msp = doc.modelspace()

# =====================
# 2. Filtrar líneas que estén en el layer "0"
# =====================
lines_layer_0 = [line for line in msp.query('LINE') if line.dxf.layer == "0"]

# =====================
# 3. Imprimir información de las líneas filtradas
# =====================
print(f"Se encontraron {len(lines_layer_0)} líneas en el layer '0':")
for line in lines_layer_0:
    start = line.dxf.start
    end = line.dxf.end
    print(f"Línea desde {start} hasta {end}")
