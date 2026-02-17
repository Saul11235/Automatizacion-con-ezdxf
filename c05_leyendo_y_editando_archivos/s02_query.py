import ezdxf

# ----------------------

doc = ezdxf.readfile('test.dxf')  # documento DXF
msp = doc.modelspace()

# ----------------------
#
# la manera de consultar los objetos en librecad es usando query
#
# ----------------------
# En este ejemplo buscaremos todos los elementos LINE de un 

lineas = msp.query("LINE") # esto devuelve todos los elementos LINE del dibujo

print(f'\n OBJETO LINEAS:  {lineas}\n\n COMO LISTA:    {list(lineas)}\n')

# ----------------------

for elemento in lineas:
    # podremos usar esto para buscar y consultar 
    # la informacion de cada elemento DXF
    #
    #  NOTA: en este caso elemento es
    #        un objeto de la clase line
    #
    inicio = elemento.dxf.start
    fin    = elemento.dxf.end
    # Extraemos x, y
    x1, y1 = inicio.x , inicio.y
    x2, y2 = fin.x    , fin.y
    print(f'  Linea desde ({x1}, {y1})\t hasta ({x2}, {y2})')

# ----------------------

print("\nok, archivo leido")
