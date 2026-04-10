# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
import math

class Planta_escalera:
    """
    PLANTA ESCALERA - vista superior de escalera de concreto armado
    ===============================================================

    Muestra la vista desde arriba de la escalera:
      - contorno de la losa (largo_horiz x ancho_esc)
      - lineas de huellas (divisiones de cada escalon)
      - acero longitudinal (barras paralelas a la direccion de subida)
      - acero de distribucion (barras perpendiculares)
      - flecha indicando la direccion de subida
      - cotas: largo horizontal, ancho, huella

    En planta la escalera se ve como un rectangulo dividido
    en franjas iguales (una por escalon = huella).
    El acero longitudinal corre en la direccion de subida (X).
    El acero de distribucion corre en la direccion del ancho (Y).

    Parametros:
      n_escalones   = 10    numero de escalones
      huella        = 28    ancho de la huella en cm
      contrahuella  = 18    altura de la contrahuella cm (para leyenda)
      ancho_esc     = 120   ancho de la escalera en cm
      e_losa        = 15    espesor de la losa en cm (para leyenda)
      recub         = 2.5   recubrimiento en cm
      n_barras_long = 5     numero de barras longitudinales
      sep_dist      = 20    separacion barras de distribucion en cm
      diam_long     = 1.27  diametro barra longitudinal cm
      diam_dist     = 0.95  diametro barra distribucion  cm

    Metodos estandar:
      __init__, config, set_doc, get_doc,
      move, move_to, get_pos, draw
    Tests: _test_1, _test_2, _test_3
    """

    def __init__(self, n_escalones=10, huella=28, contrahuella=18,
                 ancho_esc=120, e_losa=15,
                 recub=2.5, n_barras_long=5, sep_dist=20,
                 diam_long=1.27, diam_dist=0.95):
        self.config(n_escalones, huella, contrahuella, ancho_esc,
                    e_losa, recub, n_barras_long, sep_dist,
                    diam_long, diam_dist)
        self.doc = ezdxf.new()
        self.x = self.y = 0
        print("> objeto creado, Planta_escalera")

    def config(self, n_escalones=10, huella=28, contrahuella=18,
               ancho_esc=120, e_losa=15,
               recub=2.5, n_barras_long=5, sep_dist=20,
               diam_long=1.27, diam_dist=0.95):
        self.n_escalones   = max(2, int(n_escalones))
        self.huella        = abs(huella)
        self.contrahuella  = abs(contrahuella)
        self.ancho_esc     = abs(ancho_esc)
        self.e_losa        = abs(e_losa)
        self.recub         = abs(recub)
        self.n_barras_long = max(2, int(n_barras_long))
        self.sep_dist      = abs(sep_dist)
        self.diam_long     = abs(diam_long)
        self.diam_dist     = abs(diam_dist)
        self.L_horiz = self.n_escalones * self.huella
        self.H_total = self.n_escalones * self.contrahuella
        if self.sep_dist > self.L_horiz: self.sep_dist = self.L_horiz / 4
        if self.recub > self.ancho_esc / 4: self.recub = self.ancho_esc / 6

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

    def _get_contorno(self, x=0, y=0):
        # rectangulo exterior de la losa en planta
        L  = self.L_horiz
        ae = self.ancho_esc
        return [
                [x      , y      ],
                [x + L  , y      ],
                [x + L  , y + ae ],
                [x      , y + ae ],
                ]

    def _get_lineas_huellas(self, x=0, y=0):
        # lineas verticales que dividen cada escalon (huellas vistas desde arriba)
        ae = self.ancho_esc
        h  = self.huella
        n  = self.n_escalones
        lineas = []
        for i in range(1, n):   # no se dibuja en los bordes
            xi = x + i * h
            lineas.append([[xi, y], [xi, y + ae]])
        return lineas

    def _get_acero_long(self, x=0, y=0):
        # barras longitudinales paralelas a la direccion de subida (en X)
        # se distribuyen en el ancho (Y)
        L   = self.L_horiz
        ae  = self.ancho_esc
        r   = self.recub
        n   = self.n_barras_long
        d   = self.diam_long
        y_ini = y + r + d / 2
        y_fin = y + ae - r - d / 2
        paso  = (y_fin - y_ini) / (n - 1) if n > 1 else 0
        barras = []
        for i in range(n):
            yb = y_ini + i * paso
            barras.append([[x + r, yb], [x + L - r, yb]])
        return barras

    def _get_acero_dist(self, x=0, y=0):
        # barras de distribucion perpendiculares a la subida (en Y)
        # se distribuyen en el largo (X) con separacion sep_dist
        L   = self.L_horiz
        ae  = self.ancho_esc
        r   = self.recub
        sep = self.sep_dist
        d   = self.diam_dist
        barras = []
        xb = x + r
        while xb <= x + L - r + 0.01:
            barras.append([[xb, y + r], [xb, y + ae - r]])
            xb += sep
        return barras

    def _get_flecha_subida(self, x=0, y=0):
        # flecha indicando la direccion de subida (en el centro de la losa)
        L  = self.L_horiz
        ae = self.ancho_esc
        xc = x + L / 2
        yc = y + ae / 2
        largo = min(L * 0.2, ae * 0.4)
        return [[xc - largo/2, yc], [xc + largo/2, yc]]

    def _get_dim_points(self, x=0, y=0):
        L   = self.L_horiz
        ae  = self.ancho_esc
        h   = self.huella
        sep = self.sep_dist
        r   = self.recub
        return [
                # largo total (X)
                [[x     , y      ], [x + L  , y      ]],
                # ancho (Y)
                [[x     , y      ], [x      , y + ae ]],
                # una huella
                [[x     , y - 3  ], [x + h  , y - 3  ]],
                # separacion barras distribucion
                [[x + r , y + ae + 3], [x + r + sep, y + ae + 3]],
                ]

    def _get_text(self):
        n   = self.n_escalones
        h   = self.huella
        ch  = self.contrahuella
        L   = self.L_horiz
        H   = self.H_total
        ae  = self.ancho_esc
        e   = self.e_losa
        r   = self.recub
        nl  = self.n_barras_long
        sep = self.sep_dist
        dl  = self.diam_long
        dd  = self.diam_dist
        ag  = math.degrees(math.atan2(H, L))
        blondel = 2 * ch + h
        # numero de barras de distribucion
        n_dist  = int((L - 2*r) / sep) + 1
        as_long = round(nl    * math.pi * dl**2 / 4, 3)
        as_dist = round(n_dist * math.pi * dd**2 / 4, 3)
        return (f"Planta escalera\n"
                f"N escalones = {n}\n"
                f"Huella      = {h} cm\n"
                f"Contrahuella= {ch} cm\n"
                f"Blondel: 2ch+h = {blondel} cm\n\n"
                f"L horiz = {L} cm\n"
                f"H total = {H} cm\n"
                f"Ancho   = {ae} cm\n"
                f"e losa  = {e} cm\n"
                f"Angulo  = {ag:.1f} grados\n\n"
                f"Long: {nl} barras d={dl} cm\n"
                f"  As={as_long} cm2\n"
                f"Dist: sep={sep} cm  N~{n_dist}\n"
                f"  d={dd} cm  As~{as_dist} cm2")

    def draw(self, x=None, y=None, char=5, border=False):
        """dibuja la planta de la escalera en el modelspace"""
        self.move_to(x, y)
        x   = self.x
        y   = self.y

        doc = self.doc
        msp = doc.modelspace()

        true_x = x + 12 * char
        true_y = y + 52 * char

        marco_x = self.L_horiz   + 24 * char
        marco_y = self.ancho_esc + 60 * char

        centro_x  = x + marco_x / 2
        centro_y  = y + marco_y / 2
        leyenda_x = x + char * 20
        leyenda_y = y + char * 44

        marco = [
                [x           , y           ],
                [x + marco_x , y           ],
                [x + marco_x , y + marco_y ],
                [x           , y + marco_y ],
                ]

        contorno   = self._get_contorno       (true_x, true_y)
        huellas    = self._get_lineas_huellas  (true_x, true_y)
        ac_long    = self._get_acero_long      (true_x, true_y)
        ac_dist    = self._get_acero_dist      (true_x, true_y)
        flecha     = self._get_flecha_subida   (true_x, true_y)
        coord_dim  = self._get_dim_points      (true_x, true_y)

        if border:  # verde
            msp.add_lwpolyline(marco, close=True,
                               dxfattribs={'color': 3})

        # contorno losa
        msp.add_lwpolyline(contorno, close=True,dxfattribs={'lineweight': 40})

        # lineas de huellas
        for lin in huellas:
            msp.add_line(start=lin[0], end=lin[1],
                         dxfattribs={'color': 7, 'lineweight': 15})

        # acero longitudinal (rojo)
        for b in ac_long:
            msp.add_line(start=b[0], end=b[1],
                         dxfattribs={'color': 1, 'lineweight': 40})

        # acero de distribucion (azul, punteado)
        for b in ac_dist:
            msp.add_line(start=b[0], end=b[1],
                         dxfattribs={'color': 5, 'lineweight': 25,
                                     'linetype': 'DASHED'})

        # flecha de subida con texto
        msp.add_line(start=flecha[0], end=flecha[1],
                     dxfattribs={'color': 6, 'lineweight': 20})
        msp.add_mtext("SUBE",
                      dxfattribs={"style": "iso",
                                  "insert": (flecha[1][0] + char, flecha[1][1]),
                                  "char_height": char * 0.8,
                                  "color": 6})

        msp.add_mtext(self._get_text(),
                      dxfattribs={"style": "iso", "insert": (leyenda_x, leyenda_y),
                                  "char_height": char*2, "color": 8,  # gris
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
        ox, oy = 0, 0
        msp.add_lwpolyline(self._get_contorno(ox, oy), close=True)
        for l in self._get_lineas_huellas(ox, oy):
            msp.add_line(start=l[0], end=l[1])
        for b in self._get_acero_long(ox, oy):
            msp.add_line(start=b[0], end=b[1])
        for b in self._get_acero_dist(ox, oy):
            msp.add_line(start=b[0], end=b[1])
        msp.add_mtext("\n" + self._get_text())
        for seg in self._get_dim_points(ox, oy):
            msp.add_aligned_dim(p1=seg[0], p2=seg[1], distance=3)
        doc.saveas("test.dxf")
        print("test 1 ok")

    def _test_2(self):
        doc = ezdxf.new()
        self.set_doc(doc)
        self.draw(x=0, y=0, char=2, border=True)
        doc.saveas("test.dxf")
        print("test 2 ok")

    def _test_3(self):
        self.config(n_escalones=8,  huella=25, contrahuella=19, ancho_esc=100)
        self.draw(char=2, border=True)
        self.config(n_escalones=10, huella=28, contrahuella=18, ancho_esc=120)
        self.draw(char=2, border=True)
        self.config(n_escalones=12, huella=30, contrahuella=17, ancho_esc=140)
        self.draw(char=2, border=True)
        self.get_doc().saveas("test.dxf")
        print("test 3 ok")

if __name__ == '__main__':
    obj = Planta_escalera()
    obj._test_1()
    obj._test_2()
    obj._test_3()