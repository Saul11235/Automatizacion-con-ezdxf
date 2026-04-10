# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
import math

class Corte_viga:
    """
    CORTE VIGA - desarrollo longitudinal de viga continua multi-apoyo
    =================================================================

    Muestra el alzado (corte longitudinal) de la viga continua.
    De izquierda a derecha: COL - tramo - COL - tramo - ... - COL

    Cada tramo tiene tres zonas:
      - zona confinada izq (Lv = 2h desde cara de columna)
      - zona central
      - zona confinada der (Lv = 2h desde cara de columna)

    Las columnas (nudos) tienen estribos densos en toda su altura.

    Acero longitudinal:
      - SUPERIOR corrido: de extremo a extremo (traccion en nudos)
      - INFERIOR por tramo: con anclaje en nudo (traccion en vano)

    Criterios:
      Lv     = 2 * h_viga
      s_conf = min(h/4, 8d_long, 24d_est, 30 cm)
      s_cent = min(h/2, d_long, 30 cm)

    Parametros:
      b_viga      = 30    ancho de la viga en cm
      h_viga      = 50    altura de la viga en cm
      n_tramos    = 3     numero de tramos (n_cols = n_tramos + 1)
      L_cc        = 500   luz centro a centro entre columnas en cm
      b_col       = 30    ancho de la columna en cm
      h_col       = 150   altura de columna visible arriba y abajo en cm
      recub       = 4     recubrimiento en cm
      d_estribo   = 0.95  diametro estribo cm
      n_inf       = 3     barras inferiores por tramo
      n_sup       = 2     barras superiores corridas
      diam_inf    = 1.59  diametro barra inferior cm
      diam_sup    = 1.27  diametro barra superior cm

    Metodos estandar:
      __init__, config, set_doc, get_doc,
      move, move_to, get_pos, draw
    Tests: _test_1, _test_2, _test_3
    """

    def __init__(self,          b_viga=30,      h_viga=50,
                 n_tramos=3,    L_cc=500,       b_col=30,
                 h_col=30,      recub=4,        d_estribo=0.95,
                 n_inf=3,       n_sup=2,        diam_inf=1.59,
                 diam_sup=1.27):
        self.config(b_viga, h_viga, n_tramos, L_cc, b_col, h_col, recub, d_estribo, n_inf, n_sup, diam_inf, diam_sup)                
        self.doc = ezdxf.new()
        self.x = self.y = 0
        print("> objeto creado, Corte_viga")

    def config  (self,          b_viga=30,      h_viga=50,
                 n_tramos=3,    L_cc=500,       b_col=30,
                 h_col=30,      recub=4,        d_estribo=0.95,
                 n_inf=3,       n_sup=2,        diam_inf=1.59,
                 diam_sup=1.27):
        self.b_viga    = abs(b_viga)
        self.h_viga    = abs(h_viga)
        self.n_tramos  = max(1, int(n_tramos))
        self.L_cc      = abs(L_cc)
        self.b_col     = abs(b_col)
        self.h_col     = abs(h_col)
        self.recub     = abs(recub)
        self.d_estribo = abs(d_estribo)
        self.n_inf     = max(1, int(n_inf))
        self.n_sup     = max(1, int(n_sup))
        self.diam_inf  = abs(diam_inf)
        self.diam_sup  = abs(diam_sup)
        if self.b_col > self.L_cc * 0.3: self.b_col = self.L_cc * 0.15
        # valores aproximados, NO USAR SIN REVISAR OJO
        self.Lv     = round(2 * self.h_viga, 1)
        self.s_conf = round(min(self.h_viga / 4, 8  * self.diam_inf,24 * self.d_estribo,30), 1)
        self.s_cent = self.s_conf*2
        n_cols       = self.n_tramos + 1
        self.L_total = n_cols * self.b_col + self.n_tramos * self.L_cc

    def set_doc(self, doc: ezdxf.new) -> None:
        self.doc = doc

    def get_doc(self):
        return self.doc

    def move(self, x=0, y=0):
        self.x += x
        self.y += y

    def move_to(self, x=None, y=None):
        self.x = x if x is not None else self.x
        self.y = y if y is not None else self.y

    def get_pos(self):
        return [self.x, self.y]

    def _x_col(self, i):
        """x del borde izquierdo de la columna i (0-indexed)"""
        return i * (self.b_col + self.L_cc)

    def _get_columnas(self, x=0, y=0):
        """columnas arriba y abajo de la viga"""
        cols = []
        hc   = self.h_col
        hv   = self.h_viga
        bc   = self.b_col
        for i in range(self.n_tramos + 1):
            xc = x + self._x_col(i)
            # columna inferior
            cols.append([[xc,    y - hc],
                         [xc+bc, y - hc],
                         [xc+bc, y     ],
                         [xc,    y     ]])
            # columna superior
            cols.append([[xc,    y + hv     ],
                         [xc+bc, y + hv     ],
                         [xc+bc, y + hv + hc],
                         [xc,    y + hv + hc]])
        return cols

    def _get_viga(self, x=0, y=0):
        """rectangulo de la viga de extremo a extremo"""
        return [[x,             y          ],
                [x+self.L_total,y          ],
                [x+self.L_total,y+self.h_viga],
                [x,             y+self.h_viga]]

    def _get_zonas_conf(self, x=0, y=0):
        """rectangulos de las zonas confinadas en cada tramo"""
        hv   = self.h_viga
        bc   = self.b_col
        Lv   = self.Lv
        zonas = []
        for t in range(self.n_tramos):
            xi  = x + self._x_col(t) + bc
            xf  = x + self._x_col(t + 1)
            Lv_r = min(Lv, (xf - xi) / 2)
            # zona conf izq
            zonas.append([[xi,       y],
                          [xi+Lv_r,  y],
                          [xi+Lv_r,  y+hv],
                          [xi,       y+hv]])
            # zona conf der
            zonas.append([[xf-Lv_r,  y],
                          [xf,       y],
                          [xf,       y+hv],
                          [xf-Lv_r,  y+hv]])
        return zonas

    def _get_estribos(self, x=0, y=0):
        """todos los estribos de la viga"""
        hv  = self.h_viga  # altura viga
        r   = self.recub   # recubrimientos
        sc  = self.s_conf  # valores normativa
        sm  = self.s_cent
        Lv  = self.Lv
        bc  = self.b_col
        y0  = y + r
        y1  = y + hv - r
        ests = []

        for t in range(self.n_tramos):
            xi   = x + self._x_col(t) + bc
            xf   = x + self._x_col(t + 1)
            Lv_r = min(Lv, (xf - xi) / 2)

            # zona conf izq
            xe = xi + sc
            while xe <= xi + Lv_r:
                ests.append({'p1': [xe, y0], 'p2': [xe, y1], 'tipo': 'conf'})
                xe += sc

            # zona central
            xe = xi + Lv_r + sm
            while xe < xf - Lv_r:
                ests.append({'p1': [xe, y0], 'p2': [xe, y1], 'tipo': 'cent'})
                xe += sm

            # zona conf der
            xe = xf - Lv_r
            while xe < xf - sc / 2:
                ests.append({'p1': [xe, y0], 'p2': [xe, y1], 'tipo': 'conf'})
                xe += sc

        # nudos (estribos dentro de cada columna, por toda la altura de viga)
        for i in range(self.n_tramos + 1):
            xc = x + self._x_col(i)
            xe = xc + sc
            while xe < xc + bc:
                ests.append({'p1': [xe, y0], 'p2': [xe, y1], 'tipo': 'nudo'})
                xe += sc

        return ests

    def _get_barras_sup(self, x=0, y=0):
        """barras superiores corridas (traccion en nudos)"""
        hv  = self.h_viga
        r   = self.recub
        de  = self.d_estribo
        d   = self.diam_sup
        n   = self.n_sup
        cov = r + de + d / 2
        x0  = x
        x1  = x + self.L_total
        barras = []
        for i in range(n):
            yb = y + hv - cov - i * (d + 0.5)
            barras.append([[x0, yb], [x1, yb]])
        return barras

    def _get_barras_inf(self, x=0, y=0):
        """barras inferiores por tramo con anclaje en nudo"""
        r   = self.recub
        de  = self.d_estribo
        d   = self.diam_inf
        n   = self.n_inf
        bc  = self.b_col
        cov = r + de + d / 2
        anc = min(bc * 0.8, 15 * d)
        barras = []
        for t in range(self.n_tramos):
            xi = x + self._x_col(t) + bc - anc
            xf = x + self._x_col(t + 1) + anc
            for i in range(n):
                yb = y + cov + i * (d + 0.5)
                barras.append([[xi, yb], [xf, yb]])
        return barras

    def _get_lineas_Lv(self, x=0, y=0):
        """lineas punteadas que marcan el limite de la zona confinada"""
        hv  = self.h_viga
        bc  = self.b_col
        Lv  = self.Lv
        lins = []
        for t in range(self.n_tramos):
            xi   = x + self._x_col(t) + bc
            xf   = x + self._x_col(t + 1)
            Lv_r = min(Lv, (xf - xi) / 2)
            lins.append([[xi + Lv_r, y], [xi + Lv_r, y + hv]])
            lins.append([[xf - Lv_r, y], [xf - Lv_r, y + hv]])
        return lins

    def _get_dim_points(self, x=0, y=0):
        hv  = self.h_viga
        bc  = self.b_col
        Lv  = self.Lv
        xc0 = x + self._x_col(0) + bc / 2
        xc1 = x + self._x_col(1) + bc / 2
        xl0 = x + self._x_col(0) + bc
        xl1 = x + self._x_col(1)
        Lv_r = min(Lv, (xl1 - xl0) / 2)
        return [
                # L centro-centro
                [[xc0, y - self.h_col], [xc1, y - self.h_col]],
                # L libre
                [[xl0, y - 12], [xl1, y - 12]],
                # h_viga
                [[x + self.L_total + 5, y],
                 [x + self.L_total + 5, y + hv]],
                # b_col
                [[x, y + hv + 6],
                 [x + bc, y + hv + 6]],
                # Lv
                [[xl0, y + hv + 6],
                 [xl0 + Lv_r, y + hv + 6]],
                ]

    def _get_text(self):
        b   = self.b_viga
        h   = self.h_viga
        nt  = self.n_tramos
        Lcc = self.L_cc
        bc  = self.b_col
        r   = self.recub
        de  = self.d_estribo
        ni  = self.n_inf
        ns  = self.n_sup
        di  = self.diam_inf
        ds  = self.diam_sup
        sc  = self.s_conf
        sm  = self.s_cent
        Lv  = self.Lv
        Llib = Lcc - bc
        as_inf = round(ni * math.pi * di**2 / 4, 2)
        as_sup = round(ns * math.pi * ds**2 / 4, 2)
        return (f"Viga continua {b}x{h} cm\n"
                f"N tramos = {nt}\n"
                f"L cc   = {Lcc} cm\n"
                f"L libre= {Llib} cm\n"
                f"b col  = {bc} cm\n"
                f"Recub  = {r} cm\n\n"
                f"Inf: {ni}d{di}  As={as_inf} cm2\n"
                f"Sup: {ns}d{ds}  As={as_sup} cm2\n\n"
                f"Lv = 2h = {Lv} cm\n"
                f"s conf = {sc} cm\n"
                f"s cent = {sm} cm")

    def draw(self, x=None, y=None, char=5, border=False):
        """dibuja el desarrollo longitudinal de la viga continua"""
        self.move_to(x, y)

        # declarando variables en el metodo
        x         = self.x
        y         = self.y

        doc       = self.doc
        msp       = doc.modelspace()

        true_x    = x + 8  * char 
        true_y    = y + 30 * char + self.h_col

        marco_x   = self.L_total + 20 * char
        marco_y   = self.h_viga + 2 * self.h_col + 40 * char

        centro_x  = x + marco_x / 2
        centro_y  = y + marco_y / 2
        
        leyenda_x = x + char * 10
        leyenda_y = y + char * 22

        marco = [[x,         y         ],
                 [x+marco_x, y         ],
                 [x+marco_x, y+marco_y ],
                 [x,         y+marco_y ]]

        ox = true_x
        oy = true_y

        cols       = self._get_columnas  (ox, oy)
        viga       = self._get_viga      (ox, oy)
        zonas      = self._get_zonas_conf(ox, oy)
        estribos   = self._get_estribos  (ox, oy)
        b_sup      = self._get_barras_sup(ox, oy)
        b_inf      = self._get_barras_inf(ox, oy)
        lins_Lv    = self._get_lineas_Lv (ox, oy)
        coord_dim  = self._get_dim_points(ox, oy)

        if border:  # verde
            msp.add_lwpolyline(marco, close=True, dxfattribs={'color': 3})

        # dibujo columas
        for col in cols:
            msp.add_lwpolyline(col, close=True,dxfattribs={'lineweight':25})

        # dibujo vigas
        msp.add_lwpolyline(viga, close=True, dxfattribs={'lineweight': 40})

        # lineas Lv  rojo
        for lin in lins_Lv:
            msp.add_line(start=lin[0], end=lin[1],dxfattribs={'color': 1, 'lineweight': 13,'linetype': 'DASHED'})                        

        # estribos azul
        for est in estribos:
            lw = 35 if est['tipo'] in ('conf', 'nudo') else 18
            msp.add_line(start=est['p1'], end=est['p2'],dxfattribs={'color': 5, 'lineweight': lw})     

        # barras superiores corridas (rojo)
        for b in b_sup:
            msp.add_line(start=b[0], end=b[1],dxfattribs={'color': 1, 'lineweight': 40})

        # barras inferiores por tramo rojo
        for b in b_inf:
            msp.add_line(start=b[0], end=b[1],dxfattribs={'color': 1, 'lineweight': 50})
                         
        # leyenda gris
        msp.add_mtext(self._get_text(),dxfattribs={"style": "iso", "insert": (leyenda_x, leyenda_y),"char_height": char, "color": 8,"width": marco_x, "line_spacing_factor": 0.75})               

        # cpolocando elementos de dim
        for seg in coord_dim:
            msp.add_aligned_dim(p1=seg[0], p2=seg[1], distance=char, text="<> cm")

        # estilos dim 
        doc.header['$DIMASZ']  = char
        doc.header['$DIMTXT']  = char
        doc.header['$DIMCLRT'] = 8 # gris
        doc.header['$DIMCLRD'] = 8 # gris
        doc.header['$DIMCLRE'] = 8 # gris

        # ajustando viewport
        vports = doc.viewports.get('*ACTIVE')
        if vports: vport = vports[0] if isinstance(vports, list) else vports
        else     : vport = doc.viewports.new('*ACTIVE')
        vport.dxf.center = (centro_x/2 + 0.5767*marco_y - 0.06826,
                            centro_y/2 + 0.25901*marco_y - 0.021)
        vport.dxf.target = 0, 0, 0
        vport.dxf.height = marco_y * 1.05
        
        # moviendo puntuero
        self.move(marco_x, marco_y)
        self.get_pos()

    def _test_1(self):
        doc = ezdxf.new()
        msp = doc.modelspace()
        ox, oy = 0, self.h_col
        for col in self._get_columnas(ox, oy):
            msp.add_lwpolyline(col, close=True)
        msp.add_lwpolyline(self._get_viga(ox, oy), close=True)
        for est in self._get_estribos(ox, oy):
            msp.add_line(start=est['p1'], end=est['p2'])
        for b in self._get_barras_sup(ox, oy):
            msp.add_line(start=b[0], end=b[1])
        for b in self._get_barras_inf(ox, oy):
            msp.add_line(start=b[0], end=b[1])
        for lin in self._get_lineas_Lv(ox, oy):
            msp.add_line(start=lin[0], end=lin[1])
        msp.add_mtext("\n" + self._get_text())
        for seg in self._get_dim_points(ox, oy):
            msp.add_aligned_dim(p1=seg[0], p2=seg[1], distance=4)
        doc.saveas("test.dxf")
        print("test 1 ok")

    def _test_2(self):
        doc = ezdxf.new()
        self.set_doc(doc)
        self.draw(x=0, y=0, char=2, border=True)
        doc.saveas("test.dxf")
        print("test 2 ok")

    def _test_3(self):
        self.config(b_viga=25, h_viga=40, n_tramos=2, L_cc=400, b_col=25)
        self.draw(char=2, border=True)
        self.config(b_viga=30, h_viga=50, n_tramos=3, L_cc=500, b_col=30)
        self.draw(char=2, border=True)
        self.config(b_viga=35, h_viga=60, n_tramos=4, L_cc=600, b_col=35)
        self.draw(char=2, border=True)
        self.draw(border=True)
        self.get_doc().saveas("test.dxf")
        print("test 3 ok")

if __name__ == '__main__':
    obj = Corte_viga()
    obj._test_1()
    obj._test_2()
    obj._test_3()
