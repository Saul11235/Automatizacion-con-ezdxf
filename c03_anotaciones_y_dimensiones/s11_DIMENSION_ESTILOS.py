#  
# Ejemplo elementos de dimension
# 
# https://ezdxf.readthedocs.io/en/stable/tasks/add_dxf_entities.html
#


import ezdxf

doc = ezdxf.new("R2010")
msp = doc.modelspace()


#------------------------------------------------------
#
# NOTA:
#  Dentro de DXF, se suelen guardar algunas variables
#  dentro del HEADER, algunos editores como LibreCAD
#  usan estos como valores predilectos para elementos de DIM
#
#------------------------------------------------------

doc.header['$DIMTXSTY'] = 'romanc'
doc.header['$DIMASZ']   = 2.5      # Arrow size
doc.header['$DIMTXT']   = 1.5      # Text height
doc.header['$DIMCLRT']  = 5        # Text Color: Blue
doc.header['$DIMCLRD']  = 6        # Dimension Line Color: Magenta
doc.header['$DIMCLRE']  = 2        # Extension Line Color: Yellow
doc.header['$DIMDEC']   = 3        # Decimal precision
doc.header['$DIMDSEP']  = ord(',') # Decimal separator: ',' Nota: ord lo convierte a unicode
doc.header['$DIMLFAC']  = 0.5      # Length factor


#------------------------------------------------------

# LEADER (Flecha)
msp.add_leader(
    vertices = [(10, 60), (40, 80), (60, 80)],
)

#------------------------------------------------------

# DIMENSIÓN HORIZONTAL 
msp.add_linear_dim(
    base  = (0, 0),
    p1    = (40, 0),
    p2    = (80, 0),
    text  = "DIMH = <> km",
)

#------------------------------------------------------

# DIMENSIÓN VERTICAL
dim_v = msp.add_linear_dim(
    base  = (0, 0),
    p1    = (0, 0),
    p2    = (0, 50),
    angle = 90,
    text  = "DIMV = <> mm",
)

#------------------------------------------------------

# DIMENSIÓN ALINEADA
msp.add_aligned_dim(
    p1      = (20, 20),
    p2      = (60, 50),
    distance= 8,
    text    = "DIMAL = <> cm",
)

#------------------------------------------------------

msp.add_circle( center  = (120, 70), radius =15 ) # ver secc anterior

# DIMENSIÓN DIÁMETRO
msp.add_diameter_dim(
    center = (120, 70),
    radius = 15,
    angle  = 0,
    text   = "DIAM = <> in",
)

#------------------------------------------------------

msp.add_circle( center  = (160, 70), radius =10 ) # ver secc anterior

# DIMENSIÓN RADIO
msp.add_radius_dim(
    center = (160, 70),
    radius = 10,
    angle  = 30, # ángulo obligatorio
    text   = "RADIO = <> ft",
)

#------------------------------------------------------

msp.add_line( (100, 0), (150,50)) # ver secc anterior
msp.add_line( (100, 0), (180,10)) # ver secc anterior

# DIMENSION ANGULAR
dim2l = msp.add_angular_dim_2l(
    base=(160, 20),               # punto de la línea de dimensión
    line1 = ((100,0), (150,50)),
    line2 = ((100,0), (180,10)),
    text  = "angulo = <>°"
)

#------------------------------------------------------



doc.saveas("test.dxf")
print("Archivo test.dxf generado correctamente.")


