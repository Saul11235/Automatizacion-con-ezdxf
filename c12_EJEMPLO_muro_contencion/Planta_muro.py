# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
import math

class Planta_muro:
    """
    PLANTA MURO - vista en planta de muro de contencion en voladizo
    ===============================================================

    Muestra la vista desde arriba:
      - contorno de la zapata corrida (largo_muro x largo_z)
      - franja de la pantalla (largo_muro x e_base)
      - barras longitudinales (a lo largo del muro, en pantalla)
      - barras transversales (a lo ancho, en zapata y pantalla)
      - cotas principales

    Parametros:
      largo_muro = 600  longitud del muro en cm
      largo_z    = 150  largo de la zapata (puntera + pantalla + talon) en cm
      puntera    = 40   puntera en cm
      e_base     = 30   espesor de la pantalla en la base en cm
      alto_z     = 35   alto de la zapata en cm (para leyenda)
      alto_m     = 250  alto de la pantalla en cm (para leyenda)
      recub      = 7.5  recubrimiento en cm
      n_long     = 10   numero de barras longitudinales visibles en planta
      sep_trans  = 20   separacion entre barras transversales en cm
      diam_long  = 1.59 diametro barra longitudinal cm
      diam_trans = 1.27 diametro barra transversal  cm

    Metodos estandar:
      __init__, config, set_doc, get_doc,
      move, move_to, get_pos, draw
    Tests: _test_1, _test_2, _test_3
    """

    def __init__(self, largo_muro=600, largo_z=150, puntera=40,
                 e_base=30, alto_z=35, alto_m=250,
                 recub=7.5, n_long=10, sep_trans=20,
                 diam_long=1.59, diam_trans=1.27):
        self.config(largo_muro, largo_z, puntera, e_base,
                    alto_z, alto_m, recub, n_long, sep_trans,
                    diam_long, diam_trans)
        self.doc = ezdxf.new()
        self.x = self.y = 0
        print("> objeto creado, Planta_muro")

    def config(self, largo_muro=600, largo_z=150, puntera=40,
               e_base=30, alto_z=35, alto_m=250,
               recub=7.5, n_long=10, sep_trans=20,
               diam_long=1.59, diam_trans=1.27):
        self.largo_muro  = abs(largo_muro)
        self.largo_z     = abs(largo_z)
        self.puntera     = abs(puntera)
        self.e_base      = abs(e_base)
        self.alto_z      = abs(alto_z)
        self.alto_m      = abs(alto_m)
        self.recub       = abs(recub)
        self.n_long      = max(2, int(n_long))
        self.sep_trans   = abs(sep_trans)
        self.diam_long   = abs(diam_long)
        self.diam_trans  = abs(diam_trans)
        if self.puntera  > self.largo_z * 0.6 : self.puntera = self.largo_z * 0.3
        if self.e_base   > self.largo_z        : self.e_base  = self.largo_z * 0.2
        if self.sep_trans > self.largo_muro    : self.sep_trans = self.largo_muro / 4

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

    def _get_contorno_zapata(self, x=0, y=0):
        # rectangulo largo_muro x largo_z
        lm = self.largo_muro
        lz = self.largo_z
        return [
                [x      , y      ],
                [x + lm , y      ],
                [x + lm , y + lz ],
                [x      , y + lz ],
                ]

    def _get_franja_pantalla(self, x=0, y=0):
        # franja que representa la pantalla en planta
        # ubicada desde la puntera hasta puntera+e_base
        lm = self.largo_muro
        p  = self.puntera
        eb = self.e_base
        return [
                [x      , y + p      ],
                [x + lm , y + p      ],
                [x + lm , y + p + eb ],
                [x      , y + p + eb ],
                ]

    def _get_barras_long(self, x=0, y=0):
        # barras longitudinales (paralelas al eje del muro)
        # se ubican en la franja de la pantalla, distribuidas en e_base
        lm  = self.largo_muro
        p   = self.puntera
        eb  = self.e_base
        r   = self.recub
        n   = self.n_long
        d   = self.diam_long
        # distribucion en el espesor (Y en planta = largo_z direction)
        y_ini = y + p + r + d / 2
        y_fin = y + p + eb - r - d / 2
        paso  = (y_fin - y_ini) / (n - 1) if n > 1 else 0
        barras = []
        for i in range(n):
            yb = y_ini + i * paso
            barras.append([[x + r, yb], [x + lm - r, yb]])
        return barras

    def _get_barras_trans(self, x=0, y=0):
        # barras transversales (perpendiculares al eje del muro)
        # recorren todo el largo_z (puntera + pantalla + talon)
        lz  = self.largo_z
        lm  = self.largo_muro
        r   = self.recub
        sep = self.sep_trans
        d   = self.diam_trans
        barras = []
        xb = x + r
        while xb <= x + lm - r:
            barras.append([[xb, y + r], [xb, y + lz - r]])
            xb += sep
        return barras

    def _get_dim_points(self, x=0, y=0):
        lm  = self.largo_muro
        lz  = self.largo_z
        p   = self.puntera
        eb  = self.e_base
        sep = self.sep_trans
        r   = self.recub
        return [
                # largo del muro
                [[x     , y      ], [x + lm , y      ]],
                # largo de la zapata
                [[x     , y      ], [x      , y + lz ]],
                # puntera
                [[x - 3 , y      ], [x - 3  , y + p  ]],
                # espesor pantalla
                [[x - 3 , y + p  ], [x - 3  , y + p + eb]],
                # separacion barras transversales
                [[x + r , y + lz + 3], [x + r + sep, y + lz + 3]],
                ]

    def _get_text(self):
        lm   = self.largo_muro
        lz   = self.largo_z
        p    = self.puntera
        eb   = self.e_base
        hz   = self.alto_z
        am   = self.alto_m
        r    = self.recub
        nl   = self.n_long
        sep  = self.sep_trans
        dl   = self.diam_long
        dt   = self.diam_trans
        n_t  = int((lm - 2*r) / sep) + 1
        as_l = round(nl  * math.pi * dl**2 / 4, 2)
        as_t = round(n_t * math.pi * dt**2 / 4, 2)
        talon = lz - p - eb
        return (f"Planta muro = {lm} cm\n"
                f"Zapata: {lz} cm  hz={hz} cm\n"
                f"  Puntera={p} cm  Talon={talon:.0f} cm\n"
                f"Pantalla: h={am} cm  e={eb} cm\n"
                f"Recub = {r} cm\n\n"
                f"Long: {nl} barras d={dl} cm  As={as_l} cm2\n"
                f"Trans: sep={sep} cm d={dt} cm\n"
                f"  N~{n_t} und  As~{as_t} cm2")

    def draw(self, x=None, y=None, char=5, border=False):
        """dibuja la planta del muro en el modelspace"""
        self.move_to(x, y)
        x   = self.x
        y   = self.y

        doc = self.doc
        msp = doc.modelspace()

        true_x = x + 10 * char
        true_y = y + 23 * char

        marco_x   = self.largo_muro + 20 * char
        marco_y   = self.largo_z    + 30 * char

        centro_x  = x + marco_x / 2
        centro_y  = y + marco_y / 2
        leyenda_x = x + char * 5
        leyenda_y = y + char * 18

        marco = [
                [x           , y           ],
                [x + marco_x , y           ],
                [x + marco_x , y + marco_y ],
                [x           , y + marco_y ],
                ]

        cnt_zap   = self._get_contorno_zapata  (true_x, true_y)
        franja    = self._get_franja_pantalla  (true_x, true_y)
        b_long    = self._get_barras_long      (true_x, true_y)
        b_trans   = self._get_barras_trans     (true_x, true_y)
        coord_dim = self._get_dim_points       (true_x, true_y)

        if border:  # verde
            msp.add_lwpolyline(marco, close=True,
                               dxfattribs={'color': 3})

        # contornos
        msp.add_lwpolyline(cnt_zap, close=True,dxfattribs={'lineweight': 30})
        msp.add_lwpolyline(franja,  close=True,dxfattribs={'lineweight': 50})
                           
        # barras longitudinales (rojo)
        for b in b_long:
            msp.add_line(start=b[0], end=b[1],
                         dxfattribs={'color': 1, 'lineweight': 40})

        # barras transversales (azul)
        for b in b_trans:
            msp.add_line(start=b[0], end=b[1],
                         dxfattribs={'color': 5, 'lineweight': 30})

        msp.add_mtext(self._get_text(),
                      dxfattribs={"style": "iso", "insert": (leyenda_x, leyenda_y),
                                  "char_height": char*2, "color": 8,  # gris
                                  "width": marco_x, "line_spacing_factor": 0.75})

        for seg in coord_dim:
            msp.add_aligned_dim(p1=seg[0], p2=seg[1],
                                distance=char, text="<> cm")

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

        self.move(marco_x, marco_y)
        self.get_pos()

    def _test_1(self):
        doc = ezdxf.new()
        msp = doc.modelspace()
        msp.add_lwpolyline(self._get_contorno_zapata(),  close=True)
        msp.add_lwpolyline(self._get_franja_pantalla(),  close=True)
        for b in self._get_barras_long():
            msp.add_line(start=b[0], end=b[1])
        for b in self._get_barras_trans():
            msp.add_line(start=b[0], end=b[1])
        msp.add_mtext("\n" + self._get_text())
        for seg in self._get_dim_points():
            msp.add_aligned_dim(p1=seg[0], p2=seg[1], distance=4)
        doc.saveas("test.dxf")
        print("test 1 ok")

    def _test_2(self):
        doc = ezdxf.new()
        self.set_doc(doc)
        self.draw(x=0, y=0, char=3, border=True)
        doc.saveas("test.dxf")
        print("test 2 ok")

    def _test_3(self):
        self.config(largo_muro=500, largo_z=140, puntera=35, e_base=28, n_long=8,  sep_trans=15)
        self.draw(char=2, border=True)
        self.config(largo_muro=600, largo_z=160, puntera=45, e_base=32, n_long=10, sep_trans=20)
        self.draw(char=2, border=True)
        self.config(largo_muro=700, largo_z=180, puntera=50, e_base=36, n_long=12, sep_trans=25)
        self.draw(char=2, border=True)
        self.draw(border=True)
        self.get_doc().saveas("test.dxf")
        print("test 3 ok")

if __name__ == '__main__':
    obj = Planta_muro()
    obj._test_1()
    obj._test_2()
    obj._test_3()