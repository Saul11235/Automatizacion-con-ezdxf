# variables de usuario solo disponibles a partir de DXF v 2004

#
# Ejemplo  header variables personalizadas
#
#   Creando variables de usuario y texto en un DXF R2018
#

import ezdxf

doc = ezdxf.new('R2018')

#------------------------------------------------------
#  Variables estandar
doc.header['$USERI1'] = 1234      # Entero
doc.header['$USERR1'] = 99.99     # Float: Precio o medida

#------------------------------------------------------
#  Variables personalizadas
doc.header.custom_vars.append("MiEtiqueta", "Este es mi texto personalizado")

#------------------------------------------------------

doc.saveas("test.dxf")
print("Archivo 'test.dxf' creado con exito")
