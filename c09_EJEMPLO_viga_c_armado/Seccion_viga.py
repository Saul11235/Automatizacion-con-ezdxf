# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
import math

class Seccion_viga:
    """
    SECCION VIGA - seccion transversal de viga de concreto armado
    =============================================================

    Muestra la seccion transversal de la viga con:
      - rectangulo de concreto (b_viga x h_viga)
      - estribo perimetral cerrado
      - barras inferiores (traccion en centro de tramo)
      - barras superiores (traccion en apoyos / corridas)
      - cotas: b_viga, h_viga, recubrimiento
      - leyenda con cuantia y separacion de estribos calculada

    Separaciones de estribos
      s_conf = min(h/4, 8d_long, 24d_est, 30 cm)
      s_cent = min(h/2, d_long, 30 cm)
      Lv     = 2 * h_viga  (longitud zona confinada desde cara columna)

    Parametros por defecto:
      b_viga      = 30    ancho de la viga en cm
      h_viga      = 50    altura de la viga en cm
      recub       = 4     recubrimiento libre en cm
      d_estribo   = 0.95  diametro del estribo cm (3/8"=0.95)
      n_inf       = 3     numero de barras inferiores
      n_sup       = 2     numero de barras superiores (corridas)
      diam_inf    = 1.59  diametro barra inferior cm  (5/8"=1.59)
      diam_sup    = 1.27  diametro barra superior cm  (1/2"=1.27)

    Metodos estandar:
      __init__, config, set_doc, get_doc,
      move, move_to, get_pos, draw
    Tests: _test_1, _test_2, _test_3
    """

    def __init__(self, b_viga=30, h_viga=50, recub=4,
                 d_estribo=0.95, n_inf=3, n_sup=2,
                 diam_inf=1.59, diam_sup=1.27):
        self.config(b_viga, h_viga, recub, d_estribo,
                    n_inf, n_sup, diam_inf, diam_sup)
        self.doc = ezdxf.new()
        self.x = self.y = 0
        print("> objeto creado, Seccion_viga")

    def config(self, b_viga=30, h_viga=50, recub=4,
               d_estribo=0.95, n_inf=3, n_sup=2,
               diam_inf=1.59, diam_sup=1.27):
        self.b_viga     = abs(b_viga)
        self.h_viga     = abs(h_viga)
        self.recub      = abs(recub)
        self.d_estribo  = abs(d_estribo)
        self.n_inf      = max(1, int(n_inf))
        self.n_sup      = max(1, int(n_sup))
        self.diam_inf   = abs(diam_inf)
        self.diam_sup   = abs(diam_sup)
        if self.recub > self.b_viga / 4: self.recub = self.b_viga / 5
        # separaciones ACI 318 / NSR-10
        self.s_conf = round(min(self.h_viga / 4,
                                8  * self.diam_inf,
                                24 * self.d_estribo,
                                30), 1)
        self.s_cent = round(min(self.h_viga / 2,
                                self.diam_inf,
                                30), 1)
        self.Lv = round(2 * self.h_viga, 1)

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

    def _get_seccion(self, x=0, y=0):
        b = self.b_viga
        h = self.h_viga
        return [[x, y], [x+b, y], [x+b, y+h], [x, y+h]]

    def _get_estribo(self, x=0, y=0):
        b  = self.b_viga
        h  = self.h_viga
        r  = self.recub
        xi = x + r
        yi = y + r
        xf = x + b - r
        yf = y + h - r
        return [[xi, yi], [xf, yi], [xf, yf], [xi, yf]]

    def _get_barras_inf(self, x=0, y=0):
        b   = self.b_viga
        r   = self.recub
        de  = self.d_estribo
        d   = self.diam_inf
        n   = self.n_inf
        cov = r + de + d / 2
        yc  = y + cov
        x0  = x + cov
        x1  = x + b - cov
        if n == 1: return [[x + b/2, yc]]
        paso = (x1 - x0) / (n - 1)
        return [[x0 + i*paso, yc] for i in range(n)]

    def _get_barras_sup(self, x=0, y=0):
        b   = self.b_viga
        h   = self.h_viga
        r   = self.recub
        de  = self.d_estribo
        d   = self.diam_sup
        n   = self.n_sup
        cov = r + de + d / 2
        yc  = y + h - cov
        x0  = x + cov
        x1  = x + b - cov
        if n == 1: return [[x + b/2, yc]]
        paso = (x1 - x0) / (n - 1)
        return [[x0 + i*paso, yc] for i in range(n)]

    def _get_dim_points(self, x=0, y=0):
        b = self.b_viga
        h = self.h_viga
        r = self.recub
        return [
                [[x,   y+h   ], [x+b, y+h   ]],
                [[x,   y     ], [x,   y+h   ]],
                [[x,   y+h/2 ], [x+r, y+h/2 ]],
                ]

    def _get_text(self):
        b   = self.b_viga
        h   = self.h_viga
        r   = self.recub
        de  = self.d_estribo
        ni  = self.n_inf
        ns  = self.n_sup
        di  = self.diam_inf
        ds  = self.diam_sup
        sc  = self.s_conf
        sm  = self.s_cent
        lv  = self.Lv
        as_inf = round(ni * math.pi * di**2 / 4, 2)
        as_sup = round(ns * math.pi * ds**2 / 4, 2)
        rho_inf = round(as_inf / (b * h) * 100, 3)
        return (f"Seccion viga {b}x{h} cm\n"
                f"Recub = {r} cm\n"
                f"Estribo d = {de} cm\n\n"
                f"Inf: {ni}d{di}  As={as_inf} cm2\n"
                f"Sup: {ns}d{ds}  As={as_sup} cm2\n"
                f"rho inf = {rho_inf} %\n\n"
                f"Lv = 2h = {lv} cm\n"
                f"s conf = {sc} cm\n"
                f"s cent = {sm} cm")

    def draw(self, x=None, y=None, char=1, border=False):
        """dibuja la seccion transversal de la viga"""
        self.move_to(x, y)
        x = self.x
        y = self.y

        doc = self.doc
        msp = doc.modelspace()

        true_x = x + 5  * char
        true_y = y + 21 * char
        marco_x = self.b_viga + 10 * char
        marco_y = self.h_viga + 26 * char
        centro_x  = x + marco_x / 2
        centro_y  = y + marco_y / 2
        leyenda_x = x + char * 4
        leyenda_y = y + char * 17

        marco = [[x, y], [x+marco_x, y],
                 [x+marco_x, y+marco_y], [x, y+marco_y]]

        sec   = self._get_seccion    (true_x, true_y)
        est   = self._get_estribo    (true_x, true_y)
        b_inf = self._get_barras_inf (true_x, true_y)
        b_sup = self._get_barras_sup (true_x, true_y)
        dims  = self._get_dim_points (true_x, true_y)
        r_inf = self.diam_inf / 2
        r_sup = self.diam_sup / 2

        if border: # verde
            msp.add_lwpolyline(marco, close=True, dxfattribs={'color': 3})

        # seccion de viga
        msp.add_lwpolyline(sec, close=True, dxfattribs={'lineweight': 40})

        # seccion de estribo
        msp.add_lwpolyline(est, close=True, dxfattribs={'color': 5, 'lineweight': 35})

        # barras inferiores
        for cx, cy in b_inf:
            hb = msp.add_hatch()
            ep = hb.paths.add_edge_path()
            ep.add_arc(center=(cx, cy), radius=r_inf,
                       start_angle=0, end_angle=360, ccw=True)
            hb.set_solid_fill()

        # barras superiores
        for cx, cy in b_sup:
            hb = msp.add_hatch()
            ep = hb.paths.add_edge_path()
            ep.add_arc(center=(cx, cy), radius=r_sup,
                       start_angle=0, end_angle=360, ccw=True)
            hb.set_solid_fill()

        msp.add_mtext(self._get_text(),
                      dxfattribs={"style": "iso", "insert": (leyenda_x, leyenda_y),
                                  "char_height": char, "color": 8,  # gris
                                  "width": marco_x, "line_spacing_factor": 0.75})

        for seg in dims:
            msp.add_aligned_dim(p1=seg[0], p2=seg[1], distance=char, text="<> cm")

        doc.header['$DIMASZ']  = char
        doc.header['$DIMTXT']  = char 
        doc.header['$DIMCLRT'] = 8  # gris 
        doc.header['$DIMCLRD'] = 8  # gris
        doc.header['$DIMCLRE'] = 8  # gris

        vports = doc.viewports.get('*ACTIVE')
        if vports: vport = vports[0] if isinstance(vports, list) else vports
        else     : vport = doc.viewports.new('*ACTIVE')
        vport.dxf.center = (centro_x/2 + 0.5767*marco_y - 0.06826,
                            centro_y/2 + 0.25901*marco_y - 0.021)
        vport.dxf.target = 0, 0, 0
        vport.dxf.height = marco_y * 1.05

        self.move(marco_x, marco_y)
        self.get_pos()

    def _test_1(self):
        doc = ezdxf.new()
        msp = doc.modelspace()
        msp.add_lwpolyline(self._get_seccion(), close=True)
        msp.add_lwpolyline(self._get_estribo(), close=True)
        for cx, cy in self._get_barras_inf():
            msp.add_circle(center=(cx, cy), radius=self.diam_inf/2)
        for cx, cy in self._get_barras_sup():
            msp.add_circle(center=(cx, cy), radius=self.diam_sup/2)
        msp.add_mtext("\n" + self._get_text())
        for seg in self._get_dim_points():
            msp.add_aligned_dim(p1=seg[0], p2=seg[1], distance=2)
        doc.saveas("test.dxf")
        print("test 1 ok")

    def _test_2(self):
        doc = ezdxf.new()
        self.set_doc(doc)
        self.draw(x=0, y=0, char=2, border=True)
        doc.saveas("test.dxf")
        print("test 2 ok")

    def _test_3(self):
        self.config(b_viga=25, h_viga=40, n_inf=2, n_sup=2, diam_inf=1.27)
        self.draw(char=2, border=True)
        self.config(b_viga=30, h_viga=50, n_inf=3, n_sup=2, diam_inf=1.59)
        self.draw(char=2, border=True)
        self.config(b_viga=35, h_viga=60, n_inf=4, n_sup=3, diam_inf=1.91)
        self.draw(char=2, border=True)
        self.get_doc().saveas("test.dxf")
        print("test 3 ok")

if __name__ == '__main__':
    obj = Seccion_viga()
    obj._test_1()
    obj._test_2()
    obj._test_3()