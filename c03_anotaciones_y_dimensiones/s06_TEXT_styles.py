
import ezdxf

doc = ezdxf.new()
msp = doc.modelspace()

# ------------------------------------------------------
#
# DXF no incluye la fuentes en el archivo, debe verificar que su 
# aplicación CAD, tenga acceso a las fuentes indicadas en 
#
# ---------------

msp.add_text(
    "Texto en romanc",
    dxfattribs={
        "style"   : "romanc",  #<--- probado en LibreCAD
        "color"   :  1,
        "insert"  : (0,2)
                }
)

# ---------------

msp.add_text(
    "Texto en gothitt",
    dxfattribs={
        "style"   : "gothitt",  #<--- probado en LibreCAD
        "color"   : 2,
        "insert"  : (0,6),
        }
)

# ---------------

msp.add_text(
    "Texto en simplex",
    dxfattribs={
        "style"   : "simplex",  #<--- probado en LibreCAD
        "color"   : 3,
        "insert"  : (0,10),
        }
)

# ---------------

msp.add_text(
    "Texto en italicc",
    dxfattribs={
        "style"   : "italicc",  #<--- probado en LibreCAD
        "color"   : 4,
        "insert"  : (0,14),
        }
)


# ------------------------------------------------------

doc.saveas("test.dxf")
print("DXF creado")
