# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
import math

class Perfil_muro:
    """
    PERFIL MURO - corte longitudinal de muro de contencion en voladizo
    ==================================================================

    Muestra la seccion transversal del muro (vista lateral):
      - zapata corrida (puntera al frente, talon al fondo)
      - pantalla vertical (trapecio: mas gruesa en base, corona mas delgada)
      - acero vertical de traccion en cara del talon (cara del suelo)
      - acero horizontal de temperatura en pantalla
      - acero inferior de zapata
      - acero superior de zapata (contra-traccion)

    Parametros:
      largo_z    = 150  largo total de la zapata en cm
      puntera    = 40   longitud de la puntera en cm
      alto_z     = 35   alto de la zapata en cm
      alto_m     = 250  alto libre de la pantalla en cm
      e_base     = 30   espesor de la pantalla en la base en cm
      e_corona   = 20   espesor en la corona del muro en cm
      recub      = 7.5  recubrimiento en cm
      n_vert     = 8    numero de barras verticales visibles en perfil
      n_horiz    = 5    numero de barras horizontales de temperatura
      n_zap_inf  = 5    numero de barras inferiores de zapata
      n_zap_sup  = 4    numero de barras superiores de zapata
      diam_vert  = 1.59 diametro barra vertical  cm  (5/8" = 1.59)
      diam_horiz = 1.27 diametro barra horizontal cm (1/2" = 1.27)
      diam_zap   = 1.27 diametro barra zapata     cm

    Metodos estandar:
      __init__, config, set_doc, get_doc,
      move, move_to, get_pos, draw
    Tests: _test_1, _test_2, _test_3
    """

    def __init__(self, largo_z=150, puntera=40, alto_z=35,
                 alto_m=250, e_base=30, e_corona=20,
                 recub=7.5, n_vert=8, n_horiz=5,
                 n_zap_inf=5, n_zap_sup=4,
                 diam_vert=1.59, diam_horiz=1.27, diam_zap=1.27):
        self.config(largo_z, puntera, alto_z, alto_m, e_base, e_corona,
                    recub, n_vert, n_horiz, n_zap_inf, n_zap_sup,
                    diam_vert, diam_horiz, diam_zap)
        self.doc = ezdxf.new()
        self.x = self.y = 0
        print("> objeto creado, Perfil_muro")

    def config(self, largo_z=150, puntera=40, alto_z=35,
               alto_m=250, e_base=30, e_corona=20,
               recub=7.5, n_vert=8, n_horiz=5,
               n_zap_inf=5, n_zap_sup=4,
               diam_vert=1.59, diam_horiz=1.27, diam_zap=1.27):
        self.largo_z    = abs(largo_z)
        self.puntera    = abs(puntera)
        self.alto_z     = abs(alto_z)
        self.alto_m     = abs(alto_m)
        self.e_base     = abs(e_base)
        self.e_corona   = abs(e_corona)
        self.recub      = abs(recub)
        self.n_vert     = max(2, int(n_vert))
        self.n_horiz    = max(2, int(n_horiz))
        self.n_zap_inf  = max(2, int(n_zap_inf))
        self.n_zap_sup  = max(2, int(n_zap_sup))
        self.diam_vert  = abs(diam_vert)
        self.diam_horiz = abs(diam_horiz)
        self.diam_zap   = abs(diam_zap)
        if self.puntera  > self.largo_z * 0.6: self.puntera  = self.largo_z * 0.3
        if self.e_corona > self.e_base        : self.e_corona = self.e_base
        if self.recub    > self.e_base  / 2   : self.recub    = self.e_base  / 3
        if self.e_base   > self.largo_z       : self.e_base   = self.largo_z * 0.2

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

    def _get_zapata(self, x=0, y=0):
        # rectangulo de la zapata corrida
        lz = self.largo_z
        hz = self.alto_z
        return [
                [x      , y      ],
                [x + lz , y      ],
                [x + lz , y + hz ],
                [x      , y + hz ],
                ]

    def _get_pantalla(self, x=0, y=0):
        # trapecio de la pantalla:
        # cara de la puntera (izquierda) es vertical
        # cara del talon (derecha) tiene talud hacia adentro en la corona
        # la pantalla arranca desde la parte superior de la zapata
        p      = self.puntera
        hz     = self.alto_z
        am     = self.alto_m
        e_base = self.e_base
        e_cor  = self.e_corona
        # x inicio pantalla = puntera
        xp     = x + p
        # y base pantalla = tope de zapata
        yp     = y + hz
        # diferencia de espesores = talud en cara del talon
        talud  = e_base - e_cor
        return [
                [xp          , yp      ],           # base izq (cara puntera)
                [xp + e_base , yp      ],           # base der (cara talon)
                [xp + e_cor  , yp + am ],           # corona der
                [xp          , yp + am ],           # corona izq
                ]

    def _get_barras_vert(self, x=0, y=0):
        # barras verticales de traccion en cara del talon
        p      = self.puntera
        hz     = self.alto_z
        am     = self.alto_m
        e_base = self.e_base
        e_cor  = self.e_corona
        r      = self.recub
        d      = self.diam_vert
        n      = self.n_vert
        # x cara talon en base = x_pantalla + e_base - recub
        x_barra_ini = x + p + e_base - r - d / 2
        x_barra_fin = x_barra_ini - (e_base-e_cor)
        # distribucion vertical
        y_ini   = y + hz + r + d / 2
        y_fin   = y + hz + am - r - d / 2
        paso    = (y_fin - y_ini) / (n - 1)
        barras  = []
        for i in range(n):
            yi = y_ini + i * paso
            barras.append([[x_barra_ini, yi - 1], [x_barra_fin, yi + 1]])
        # en perfil las barras verticales se ven como puntos/cortes cortos
        # mejor: una linea continua que representa el acero longitudinal
        return [[[x_barra_ini, y + hz + r], [x_barra_fin, y + hz + am - r]]]

    def _get_barras_horiz(self, x=0, y=0):
        # barras horizontales de temperatura en la pantalla
        # en perfil se ven como lineas horizontales
        p      = self.puntera
        hz     = self.alto_z
        am     = self.alto_m
        e_base = self.e_base
        e_cor  = self.e_corona
        r      = self.recub
        d      = self.diam_horiz
        n      = self.n_horiz
        xp     = x + p
        y_ini  = y + hz + r + d / 2
        y_fin  = y + hz + am - r - d / 2
        paso   = (y_fin - y_ini) / (n - 1)
        barras = []
        for i in range(n):
            yi     = y_ini + i * paso
            # interpolacion del espesor en esa altura
            t      = i / (n - 1)
            e_loc  = e_base + t * (e_cor - e_base)
            x_ini  = xp + r
            x_fin  = xp + e_loc - r
            barras.append([[x_ini, yi], [x_fin, yi]])
        return barras

    def _get_barras_zap_inf(self, x=0, y=0):
        # barras inferiores de la zapata
        lz    = self.largo_z
        r     = self.recub
        d     = self.diam_zap
        n     = self.n_zap_inf
        yc    = y + r + d / 2
        paso  = d + 0.3
        return [[[x + r, yc + i * paso], [x + lz - r, yc + i * paso]]
                for i in range(n)]

    def _get_barras_zap_sup(self, x=0, y=0):
        # barras superiores de la zapata (contra-traccion)
        lz    = self.largo_z
        hz    = self.alto_z
        r     = self.recub
        d     = self.diam_zap
        n     = self.n_zap_sup
        yc    = y + hz - r - d / 2
        paso  = d + 0.3
        return [[[x + r, yc - i * paso], [x + lz - r, yc - i * paso]]
                for i in range(n)]

    def _get_dim_points(self, x=0, y=0):
        lz    = self.largo_z
        hz    = self.alto_z
        am    = self.alto_m
        p     = self.puntera
        e_b   = self.e_base
        return [
                # largo zapata
                [[x     , y      ], [x + lz , y      ]],
                # alto zapata
                [[x     , y      ], [x      , y + hz ]],
                # alto pantalla
                [[x + p , y + hz ], [x + p  , y + hz + am]],
                # puntera
                [[x     , y - 3  ], [x + p  , y - 3  ]],
                # espesor base pantalla
                [[x + p , y + hz - 3], [x + p + e_b, y + hz - 3]],
                ]

    def _get_text(self):
        lz   = self.largo_z
        p    = self.puntera
        hz   = self.alto_z
        am   = self.alto_m
        e_b  = self.e_base
        e_c  = self.e_corona
        r    = self.recub
        nv   = self.n_vert
        nh   = self.n_horiz
        dv   = self.diam_vert
        dh   = self.diam_horiz
        dz   = self.diam_zap
        nzi  = self.n_zap_inf
        nzs  = self.n_zap_sup
        as_v = round(nv  * math.pi * dv**2 / 4, 2)
        as_h = round(nh  * math.pi * dh**2 / 4, 2)
        as_z = round((nzi + nzs) * math.pi * dz**2 / 4, 2)
        return (f"Zapata: {lz} cm  hz={hz} cm\n"
                f"Puntera={p} cm  Talon={lz-p-e_b:.0f} cm\n"
                f"Pantalla: h={am} cm\n"
                f"  base={e_b} cm  corona={e_c} cm\n"
                f"Recub = {r} cm\n\n"
                f"Vert: {nv} d={dv} cm  As={as_v} cm2\n"
                f"Horiz:{nh} d={dh} cm  As={as_h} cm2\n"
                f"Zapata:{nzi}+{nzs} d={dz} cm  As={as_z} cm2")

    def draw(self, x=None, y=None, char=5, border=False):
        """dibuja el perfil del muro en el modelspace"""
        self.move_to(x, y)
        x   = self.x
        y   = self.y

        doc = self.doc
        msp = doc.modelspace()

        true_x = x + 3  * char
        true_y = y + 20 * char

        alto_total = self.alto_z + self.alto_m
        marco_x    = self.largo_z   + 10 * char
        marco_y    = alto_total     + 25 * char
        centro_x  = x + marco_x / 2
        centro_y  = y + marco_y / 2
        leyenda_x = x + char * 4
        leyenda_y = y + char * 15

        marco = [
                [x           , y           ],
                [x + marco_x , y           ],
                [x + marco_x , y + marco_y ],
                [x           , y + marco_y ],
                ]

        zapata      = self._get_zapata        (true_x, true_y)
        pantalla    = self._get_pantalla      (true_x, true_y)
        b_vert      = self._get_barras_vert   (true_x, true_y)
        b_horiz     = self._get_barras_horiz  (true_x, true_y)
        b_zap_inf   = self._get_barras_zap_inf(true_x, true_y)
        b_zap_sup   = self._get_barras_zap_sup(true_x, true_y)
        coord_dim   = self._get_dim_points    (true_x, true_y)

        if border:  # verde
            msp.add_lwpolyline(marco, close=True,
                               dxfattribs={'color': 3})
        # contornos
        msp.add_lwpolyline(zapata,   close=True, dxfattribs={'color': 7, 'lineweight': 30})
        msp.add_lwpolyline(pantalla, close=True, dxfattribs={'color': 7, 'lineweight': 30})

        # acero vertical pantalla (rojo)
        for b in b_vert:
            msp.add_line(start=b[0], end=b[1],
                         dxfattribs={'color': 1, 'lineweight': 50})

        # acero horizontal temperatura (azul)
        for b in b_horiz:
            msp.add_line(start=b[0], end=b[1],
                         dxfattribs={'color': 5, 'lineweight': 30})

        # acero zapata inferior (rojo)
        for b in b_zap_inf:
            msp.add_line(start=b[0], end=b[1],
                         dxfattribs={'color': 1, 'lineweight': 50})

        # acero zapata superior (azul)
        for b in b_zap_sup:
            msp.add_line(start=b[0], end=b[1],
                         dxfattribs={'color': 5, 'lineweight': 30})

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

        # vista
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
        msp.add_lwpolyline(self._get_zapata(),   close=True)
        msp.add_lwpolyline(self._get_pantalla(), close=True)
        for b in self._get_barras_vert():
            msp.add_line(start=b[0], end=b[1])
        for b in self._get_barras_horiz():
            msp.add_line(start=b[0], end=b[1])
        for b in self._get_barras_zap_inf():
            msp.add_line(start=b[0], end=b[1])
        for b in self._get_barras_zap_sup():
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
        self.config(largo_z=140, puntera=35, alto_m=220, e_base=28)
        self.draw(char=2, border=True)
        self.config(largo_z=160, puntera=45, alto_m=270, e_base=32)
        self.draw(char=2, border=True)
        self.config(largo_z=180, puntera=50, alto_m=320, e_base=36)
        self.draw(char=2, border=True)
        self.draw(border=True)
        self.get_doc().saveas("test.dxf")
        print("test 3 ok")

if __name__ == '__main__':
    obj = Perfil_muro()
    obj._test_1()
    obj._test_2()
    obj._test_3()