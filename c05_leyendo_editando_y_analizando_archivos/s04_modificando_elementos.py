import ezdxf

# ----------------------

doc = ezdxf.readfile('test.dxf')  # documento DXF
msp = doc.modelspace()

# ----------------------
#
#  Version mas concisa de query
#
for linea in msp.query("LINE"):
    linea.update_dxf_attribs({
            'color': 4,          # Cian
            'linetype': 'HIDDEN' # Opcional: cambiar estilo de línea
        })
    print(f'  linea modificada')

# ----------------------
# debemos guardar al final

doc.saveas('test.dxf')

print("\nok, archivo modificado")
