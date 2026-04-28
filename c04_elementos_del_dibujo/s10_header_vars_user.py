#
# Ejemplo  bloque con dos instancias
#
#   https://ezdxf.readthedocs.io/en/stable/tutorials/blocks.html
#

import ezdxf

doc = ezdxf.new()
msp = doc.modelspace()


#========================================================
# CONFIGURACIÓN GENERAL DE UNIDADES (DXF / AutoCAD)
#========================================================

# $INSUNITS → unidades del dibujo (1 unidad del modelo = ?)
# 0  = Sin unidades (NO recomendado)
# 1  = Pulgadas
# 2  = Pies
# 3  = Millas
# 4  = Milímetros
# 5  = Centímetros
# 6  = Metros              <-- recomendado ingeniería / arquitectura
# 7  = Kilómetros
# 8  = Microinches
# 9  = Mils
# 10 = Yardas

doc.header['$INSUNITS'] = 6


#--------------------------------------------------------

# $MEASUREMENT → sistema métrico o imperial
# 0 = Imperial
# 1 = Métrico              <-- recomendado
#
doc.header['$MEASUREMENT'] = 1


#--------------------------------------------------------

# $LUNITS → formato de unidades lineales
# 1 = Científico
# 2 = Decimal              <-- más común
# 3 = Ingeniería
# 4 = Arquitectónico
# 5 = Fraccionario
#
doc.header['$LUNITS'] = 2


#--------------------------------------------------------

# $LUPREC → precisión decimal lineal
# 0 = 10
# 1 = 10.0
# 2 = 10.00
# 3 = 10.000               <-- típico
# 4 = 10.0000
#
doc.header['$LUPREC'] = 3


#--------------------------------------------------------

# $AUNITS → unidades angulares
# 0 = Grados decimales     <-- típico
# 1 = Grados / Min / Seg
# 2 = Gradianes
# 3 = Radianes
# 4 = Topográfico
#
doc.header['$AUNITS'] = 0


#--------------------------------------------------------

# $AUPREC → precisión angular
# 0 = 0
# 1 = 0.0
# 2 = 0.00                <-- típico
# 3 = 0.000
#
doc.header['$AUPREC'] = 2

#------------------------------------------------------

doc.saveas("test.dxf")
print("Archivo DXF creado correctamente")
