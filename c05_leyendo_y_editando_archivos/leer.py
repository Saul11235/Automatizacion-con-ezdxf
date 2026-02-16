
import ezdxf

# =====================
# 1. Cargar el archivo DXF existente
# =====================
doc = ezdxf.readfile("input.dxf")

# Obtener el modelspace
msp = doc.modelspace()

# =====================
# 2. Recorrer y listar todas las entidades
# =====================
print("=== Contenido del DXF ===")
for e in msp:
    print(f"Tipo: {e.dxftype()}, Datos: {e.dxfattribs()}")

# =====================
# 3. Leer solo líneas
# =====================
print("\n=== Líneas en el DXF ===")
for line in msp.query('LINE'):
    start = line.dxf.start
    end = line.dxf.end
    print(f"Línea desde {start} hasta {end}")

# =====================
# 4. Leer círculos
# =====================
print("\n=== Círculos en el DXF ===")
for circle in msp.query('CIRCLE'):
    center = circle.dxf.center
    radius = circle.dxf.radius
    print(f"Círculo en {center} con radio {radius}")

# =====================
# 5. Leer bloques insertados
# =====================
print("\n=== Bloques insertados (BLOCKREF) ===")
for blockref in msp.query('INSERT'):
    name = blockref.dxf.name
    insert_point = blockref.dxf.insert
    print(f"Bloque '{name}' insertado en {insert_point}")
