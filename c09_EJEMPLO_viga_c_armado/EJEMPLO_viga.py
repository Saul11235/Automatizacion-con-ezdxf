# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
from Seccion_viga import *
from Corte_viga   import *

recub     = 4
d_estribo = 0.95
diam_inf  = 1.59
diam_sup  = 1.27
n_inf     = 3
n_sup     = 2

# datos para graficar
sep_y     = 150
sep_x     = 100
char      = 2
border    = False

doc = ezdxf.new()
obj_sec   = Seccion_viga()
obj_corte = Corte_viga()  
obj_sec.set_doc(doc)
obj_corte.set_doc(doc)

variantes = [
    (25, 40, 2, 400, 25),
    (30, 50, 3, 500, 30),
    (35, 60, 4, 600, 35),
]

# nota, para alinear los dibujos en sentido x 
# se ha planteado una variable de ayuda x
ayuda_x = 0

for b_viga, h_viga, n_tramos, L_cc, b_col in variantes:

    # dibujando seccion
    obj_sec.move_to(y=0,x=ayuda_x)
    obj_sec.config(b_viga=b_viga, h_viga=h_viga, recub=recub,
                   d_estribo=d_estribo, n_inf=n_inf, n_sup=n_sup,
                   diam_inf=diam_inf, diam_sup=diam_sup)
    obj_sec.draw(char=char, border=border)
    obj_sec.move(x=sep_x)

    # dibujando corte
    obj_corte.move_to(y=sep_y,x=ayuda_x)
    obj_corte.config(b_viga=b_viga, h_viga=h_viga, n_tramos=n_tramos,
                     L_cc=L_cc, b_col=b_col, 
                     recub=recub, d_estribo=d_estribo,
                     n_inf=n_inf, n_sup=n_sup,
                     diam_inf=diam_inf, diam_sup=diam_sup)
    obj_corte.draw(char=char, border=border)
    obj_corte.move(x=sep_x)

    # ajustando ayuda_x
    ayuda_x= max(obj_sec.x,obj_corte.x)

doc.saveas("test.dxf")
print("dibujo dxf generado")
print()
for b, h, nt, Lcc, bc in variantes:
    Lv = 2 * h
    sc = min(h/4, 8*diam_inf, 24*d_estribo, 30)
    sm = min(h/2, diam_inf, 30)
    print(f"  Viga {b}x{h}  {nt} tramos  L_cc={Lcc}cm  "
          f"Lv={Lv}cm  s_conf={sc:.1f}cm  s_cent={sm:.1f}cm")