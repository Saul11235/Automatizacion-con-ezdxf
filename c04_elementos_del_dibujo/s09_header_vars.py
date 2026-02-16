
#
# Ejemplo  listar todas las header variables
#
#   https://ezdxf.readthedocs.io/en/stable/tutorials/header.html
#

import ezdxf

doc = ezdxf.new()

#------------------------------------------------------
#
#  las header variables se encuentran en doc.header
#

print("Lista de todas las variables de cabecera del DXF:\n")

for var_name in doc.header.varnames():
    print(var_name, ":",  doc.header[var_name])


#------------------------------------------------------

print("\nTotal de variables de cabecera:", len(doc.header))
