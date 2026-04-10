#
# Ejemplo  capas (layers)
#
#   Definicion de capas y propiedades
#

import ezdxf

doc = ezdxf.new()
msp = doc.modelspace()

#------------------------------------------------------
#  creando capas

doc.layers.new(   # capa 1: visible, roja, imprimible
    name      ="capa1",
    dxfattribs={
        "color"     : 1,    # rojo
        "lineweight": 25,   # grosor de linea
        "plot"      : 1,    # imprimible
    }
)

doc.layers.new(   # capa 2: visible, verde, NO imprimible
    name      = "capa2",  
    dxfattribs= {
        "color"     : 3,    # verde
        "lineweight": 50,   # linea mas gruesa
        "plot"      : 0,    # no imprimible
    }
)

doc.layers.new(   # capa 3: azul, oculta, imprimible
    name      ="capa3",
    dxfattribs={
        "color"     : 5,    # azul
        "lineweight": 15,   # linea fina
        "plot"      : 1,    # imprimible
    }
)

#------------------------------------------------------
#  controlando visibilidad de capas
objCapa3 = doc.layers.get("capa3")
objCapa3.freeze()  

#------------------------------------------------------
#  dibujando lineas de ejemplo en cada capa

msp.add_line( [10,10], [60,10],  dxfattribs={"layer":"capa1"} )
msp.add_line( [10,20], [60,20],  dxfattribs={"layer":"capa2"} )
msp.add_line( [10,30], [60,30],  dxfattribs={"layer":"capa3"} )

#------------------------------------------------------

doc.saveas("test.dxf")
print("Archivo DXF creado correctamente")
