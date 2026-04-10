# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
import math

class Seccion_columna:
    """
    SECCION COLUMNA - seccion transversal de columna rectangular
    ============================================================

    Muestra la seccion transversal de la columna:
      - rectangulo de concreto (b_col x h_col)
      - estribo perimetral cerrado
      - barras longitudinales en esquinas y en lados
      - ganchos interiores (estribos de amarre) si hay barras intermedias
      - cotas: b_col, h_col, recubrimiento
      - leyenda con datos de acero

    Las barras se distribuyen:
      - n_barras_x: barras en el lado paralelo a b_col (incluye esquinas)
      - n_barras_y: barras en el lado paralelo a h_col (incluye esquinas)
      - las 4 esquinas siempre tienen barra

    Parametros:
      b_col       = 30    dimension X de la seccion en cm
      h_col       = 30    dimension Y de la seccion en cm
      recub       = 4     recubrimiento libre en cm
      d_estribo   = 0.95  diametro del estribo en cm (3/8"=0.95)
      n_barras_x  = 4     numero de barras en el lado X (incluye esquinas)
      n_barras_y  = 4     numero de barras en el lado Y (incluye esquinas)
      diam_long   = 1.59  diametro barra longitudinal cm (5/8"=1.59)

    Metodos estandar:
      __init__, config, set_doc, get_doc,
      move, move_to, get_pos, draw
    Tests: _test_1, _test_2, _test_3
    """

    def __init__(self, b_col=30, h_col=30, recub=4,
                 d_estribo=0.95, n_barras_x=4, n_barras_y=4,
                 diam_long=1.59):
        self.config(b_col, h_col, recub, d_estribo,
                    n_barras_x, n_barras_y, diam_long)
        self.doc = ezdxf.new()
        self.x = self.y = 0
        print("> objeto creado, Seccion_columna")

    def config(self, b_col=30, h_col=30, recub=4,
               d_estribo=0.95, n_barras_x=4, n_barras_y=4,
               diam_long=1.59):
        self.b_col      = abs(b_col)
        self.h_col      = abs(h_col)
        self.recub      = abs(recub)
        self.d_estribo  = abs(d_estribo)
        self.n_barras_x = max(2, int(n_barras_x))
        self.n_barras_y = max(2, int(n_barras_y))
        self.diam_long  = abs(diam_long)
        if self.recub > min(self.b_col, self.h_col) / 4:
            self.recub = min(self.b_col, self.h_col) / 5
        if self.diam_long > self.recub:
            self.diam_long = self.recub * 0.8
        self.n_total = (2 * self.n_barras_x +
                        2 * self.n_barras_y - 4)

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
        # rectangulo exterior de la columna
        return [
                [x             , y             ],
                [x + self.b_col, y             ],
                [x + self.b_col, y + self.h_col],
                [x             , y + self.h_col],
                ]

    def _get_estribo(self, x=0, y=0):
        # estribo perimetral: rectangulo sobre el recubrimiento
        r  = self.recub
        de = self.d_estribo
        xi = x + r
        yi = y + r
        xf = x + self.b_col - r
        yf = y + self.h_col - r
        return [
                [xi, yi], [xf, yi],
                [xf, yf], [xi, yf],
                ]

    def _get_centros_barras(self, x=0, y=0):
        """
        centros de todas las barras longitudinales.
        distribucion en el perimetro:
          lado inferior: n_barras_x barras
          lado superior: n_barras_x barras
          lado izquierdo (sin esquinas): n_barras_y - 2 barras
          lado derecho   (sin esquinas): n_barras_y - 2 barras
        """
        b   = self.b_col
        h   = self.h_col
        r   = self.recub
        de  = self.d_estribo
        d   = self.diam_long
        nx  = self.n_barras_x
        ny  = self.n_barras_y
        # eje del estribo al centro de la barra
        cov = r + de + d / 2
        # coordenadas utiles
        x0  = x + cov
        x1  = x + b - cov
        y0  = y + cov
        y1  = y + h - cov
        centros = []
        # lado inferior (y=y0): nx barras de x0 a x1
        for i in range(nx):
            t = i / (nx - 1) if nx > 1 else 0.5
            centros.append([x0 + t * (x1 - x0), y0])
        # lado superior (y=y1): nx barras de x0 a x1
        for i in range(nx):
            t = i / (nx - 1) if nx > 1 else 0.5
            centros.append([x0 + t * (x1 - x0), y1])
        # lado izquierdo (x=x0): ny-2 barras internas (sin esquinas)
        for i in range(1, ny - 1):
            t = i / (ny - 1)
            centros.append([x0, y0 + t * (y1 - y0)])
        # lado derecho (x=x1): ny-2 barras internas (sin esquinas)
        for i in range(1, ny - 1):
            t = i / (ny - 1)
            centros.append([x1, y0 + t * (y1 - y0)])
        return centros

    def _get_ganchos(self, x=0, y=0):
        """
        ganchos interiores (estribos de amarre) para barras intermedias.
        se trazan lineas verticales desde el estribo superior al inferior
        en el eje de cada barra intermedia del lado X.
        solo se generan si n_barras_x > 2.
        """
        b   = self.b_col
        h   = self.h_col
        r   = self.recub
        de  = self.d_estribo
        d   = self.diam_long
        nx  = self.n_barras_x
        cov = r + de + d / 2
        x0  = x + cov
        x1  = x + b - cov
        yi  = y + r            # nivel estribo inferior
        ys  = y + h - r        # nivel estribo superior
        ganchos = []
        if nx > 2:
            for i in range(1, nx - 1):
                t  = i / (nx - 1)
                xg = x0 + t * (x1 - x0)
                ganchos.append([[xg, yi], [xg, ys]])
        return ganchos

    def _get_dim_points(self, x=0, y=0):
        b  = self.b_col
        h  = self.h_col
        r  = self.recub
        return [
                # b_col
                [[x    , y      ], [x + b , y      ]],
                # h_col
                [[x    , y      ], [x     , y + h  ]],
                # recubrimiento inferior
                [[x    , y + h/2], [x + r , y + h/2]],
                ]

    def _get_text(self):
        b   = self.b_col
        h   = self.h_col
        r   = self.recub
        de  = self.d_estribo
        nx  = self.n_barras_x
        ny  = self.n_barras_y
        d   = self.diam_long
        nt  = self.n_total
        # area de acero
        as_t  = round(nt * math.pi * d**2 / 4, 2)
        # area bruta
        ag    = b * h
        # cuantia
        rho   = round(as_t / ag * 100, 2)
        # separacion estribos (referencia ACI: min b_col/4, 8d, 10cm)
        s_conf = round(min(b/4, 8*d, 10), 1)
        s_cent = round(min(b/2, 16*d, 30), 1)
        return (f"Seccion columna\n"
                f"b = {b} cm  h = {h} cm\n"
                f"Ag = {ag} cm2\n"
                f"Recub = {r} cm\n"
                f"Estribo d = {de} cm\n\n"
                f"Barras: {nt} d={d} cm\n"
                f"  ({nx} en X, {ny} en Y)\n"
                f"As = {as_t} cm2\n"
                f"Cuantia = {rho} %\n\n"
                f"Sep conf = {s_conf} cm\n"
                f"Sep cent = {s_cent} cm")

    def draw(self, x=None, y=None, char=1, border=False):
        """dibuja la seccion transversal de la columna"""
        self.move_to(x, y)
        x   = self.x
        y   = self.y

        doc = self.doc
        msp = doc.modelspace()

        true_x = x + 6  * char
        true_y = y + 25 * char

        marco_x = self.b_col + 12 * char
        marco_y = self.h_col + 28 * char

        centro_x  = x + marco_x / 2
        centro_y  = y + marco_y / 2
        leyenda_x = x + char * 5
        leyenda_y = y + char * 20

        marco = [
                [x           , y           ],
                [x + marco_x , y           ],
                [x + marco_x , y + marco_y ],
                [x           , y + marco_y ],
                ]

        seccion    = self._get_seccion        (true_x, true_y)
        estribo    = self._get_estribo        (true_x, true_y)
        centros    = self._get_centros_barras (true_x, true_y)
        ganchos    = self._get_ganchos        (true_x, true_y)
        coord_dim  = self._get_dim_points     (true_x, true_y)
        r_long     = self.diam_long / 2

        if border:
            msp.add_lwpolyline(marco, close=True,
                               dxfattribs={'color': 3})  # verde

        # contorno seccion
        msp.add_lwpolyline(seccion, close=True, dxfattribs={'lineweight': 40})

        # estribo perimetral - azul
        msp.add_lwpolyline(estribo, close=True,
                           dxfattribs={'color': 5, 'lineweight': 35})

        # ganchos interiores ( rojo punteado)
        for g in ganchos:
            msp.add_line(start=g[0], end=g[1],
                         dxfattribs={'color': 1, 'lineweight': 20,
                                     'linetype': 'DASHED'})

        # barras longitudinales (circulos rellenos amarillos)
        for cx, cy in centros:
            msp.add_circle(center=(cx, cy), radius=r_long)
            h_b = msp.add_hatch()
            ep  = h_b.paths.add_edge_path()
            ep.add_arc(center=(cx, cy), radius=r_long,
                       start_angle=0, end_angle=360, ccw=True)
            h_b.set_solid_fill()

        msp.add_mtext(self._get_text(),
                      dxfattribs={"style": "iso", "insert": (leyenda_x, leyenda_y),
                                  "char_height": char, "color": 8, # gris
                                  "width": marco_x, "line_spacing_factor": 0.75})

        for seg in coord_dim:
            msp.add_aligned_dim(p1=seg[0], p2=seg[1],
                                distance=char, text="<> cm")

        doc.header['$DIMASZ']  = char 
        doc.header['$DIMTXT']  = char 
        doc.header['$DIMCLRT'] = 8  # gris
        doc.header['$DIMCLRD'] = 8  # gris
        doc.header['$DIMCLRE'] = 8  # gris

        if 'DASHED' not in doc.linetypes:
            doc.linetypes.new('DASHED', dxfattribs={
                'description': 'Dashed',
                'pattern': [0.6, 0.6, -0.2],
                'length': 0.8,
            })

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
        for g in self._get_ganchos():
            msp.add_line(start=g[0], end=g[1])
        for cx, cy in self._get_centros_barras():
            msp.add_circle(center=(cx, cy), radius=self.diam_long/2)
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
        self.config(b_col=25, h_col=25, n_barras_x=3, n_barras_y=3, diam_long=1.27)
        self.draw(char=2, border=True)
        self.config(b_col=30, h_col=30, n_barras_x=4, n_barras_y=4, diam_long=1.59)
        self.draw(char=2, border=True)
        self.config(b_col=40, h_col=40, n_barras_x=5, n_barras_y=5, diam_long=1.91)
        self.draw(char=2, border=True)
        self.get_doc().saveas("test.dxf")
        print("test 3 ok")

if __name__ == '__main__':
    obj = Seccion_columna()
    obj._test_1()
    obj._test_2()
    obj._test_3()