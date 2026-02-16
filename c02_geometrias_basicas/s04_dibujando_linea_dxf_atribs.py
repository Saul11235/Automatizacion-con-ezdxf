#  
# Ejemplo dxfattribs
#
# https://ezdxf.readthedocs.io/en/stable/concepts/linetypes.html
# https://ezdxf.readthedocs.io/en/stable/concepts/lineweights.html

import ezdxf

doc = ezdxf.new() 
msp = doc.modelspace()

# ------------------------------------
# 
# Nota: dxfatribs es un atributo de un diccionario
#       indicando con los atributos de un objeto
#
#  de los datos:
#
#      color 3         = verde
#      lineweight 40   = 0.40mm 
#      linetype DASHED = linea punteada
#
# ------------------------------------


# dibujarndo lineas  -------------
msp.add_line( [1,1] , [5,5] , 
             dxfattribs = {
                 "color":3,
                 "lineweight":40,
                 "linetype":"DASHED"
                 } 
             )
#----------------------------------

# Guardar el archivo DXF
doc.saveas("test.dxf")

print("Archivo DXF creado correctamente")

