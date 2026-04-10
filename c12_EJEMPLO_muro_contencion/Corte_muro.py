# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
import math

class Corte_muro:
    """
    CORTE MURO - corte transversal de muro de contencion en voladizo
    ================================================================

    Vista mirando el muro de frente (corte transversal).
    Lo que se ve:
      - pantalla como un rectangulo ancho (largo_muro x alto_m)
      - zapata corrida como rectangulo inferior (largo_muro x alto_z)
      - barras verticales distribuidas a lo largo del muro (acero traccion)
      - barras horizontales de temperatura distribuidas en altura
      - barras de zapata (inferiores y superiores) a lo largo del muro
      - indicacion del empuje del suelo en toda la cara posterior

    El suelo empuja TODA la cara posterior de la pantalla uniformemente
    (representado con lineas de empuje en la cara izquierda de la pantalla).

    Parametros:
      largo_muro = 600  longitud del muro en cm
      largo_z    = 150  largo de la zapata en cm (para leyenda)
      alto_z     = 35   alto de la zapata en cm
      alto_m     = 250  alto libre de la pantalla en cm
      e_base     = 30   espesor de la pantalla en cm (para leyenda)
      recub      = 7.5  recubrimiento en cm
      n_vert     = 10   numero de barras verticales visibles
      n_horiz    = 5    numero de barras horizontales de temperatura
      n_zap      = 8    numero de barras en zapata
      sep_vert   = 20   separacion entre barras verticales en cm
      sep_horiz  = 40   separacion entre barras horizontales en cm
      diam_vert  = 1.59 diametro barra vertical  cm
      diam_horiz = 1.27 diametro barra horizontal cm
      diam_zap   = 1.27 diametro barra zapata     cm

    Metodos estandar:
      __init__, config, set_doc, get_doc,
      move, move_to, get_pos, draw
    Tests: _test_1, _test_2, _test_3
    """

    def __init__(self, largo_muro=600, largo_z=150,
                 alto_z=35, alto_m=250, e_base=30,
                 recub=7.5, n_vert=10, n_horiz=5, n_zap=8,
                 sep_vert=20, sep_horiz=40,
                 diam_vert=1.59, diam_horiz=1.27, diam_zap=1.27):
        self.config(largo_muro, largo_z, alto_z, alto_m, e_base,
                    recub, n_vert, n_horiz, n_zap,
                    sep_vert, sep_horiz,
                    diam_vert, diam_horiz, diam_zap)
        self.doc = ezdxf.new()
        self.x = self.y = 0
        print("> objeto creado, Corte_muro")

    def config(self, largo_muro=600, largo_z=150,
               alto_z=35, alto_m=250, e_base=30,
               recub=7.5, n_vert=10, n_horiz=5, n_zap=8,
               sep_vert=20, sep_horiz=40,
               diam_vert=1.59, diam_horiz=1.27, diam_zap=1.27):
        self.largo_muro  = abs(largo_muro)
        self.largo_z     = abs(largo_z)
        self.alto_z      = abs(alto_z)
        self.alto_m      = abs(alto_m)
        self.e_base      = abs(e_base)
        self.recub       = abs(recub)
        self.n_vert      = max(2, int(n_vert))
        self.n_horiz     = max(2, int(n_horiz))
        self.n_zap       = max(2, int(n_zap))
        self.sep_vert    = abs(sep_vert)
        self.sep_horiz   = abs(sep_horiz)
        self.diam_vert   = abs(diam_vert)
        self.diam_horiz  = abs(diam_horiz)
        self.diam_zap    = abs(diam_zap)
        if self.sep_vert  > self.largo_muro: self.sep_vert  = self.largo_muro / 4
        if self.sep_horiz > self.alto_m    : self.sep_horiz = self.alto_m / 3

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

    def _get_pantalla(self, x=0, y=0):
        # pantalla vista de frente: largo_muro x alto_m
        # arranca sobre la zapata
        lm = self.largo_muro
        am = self.alto_m
        hz = self.alto_z
        return [
                [x      , y + hz      ],
                [x + lm , y + hz      ],
                [x + lm , y + hz + am ],
                [x      , y + hz + am ],
                ]

    def _get_zapata(self, x=0, y=0):
        # zapata corrida vista de frente: largo_muro x alto_z
        lm = self.largo_muro
        hz = self.alto_z
        return [
                [x      , y      ],
                [x + lm , y      ],
                [x + lm , y + hz ],
                [x      , y + hz ],
                ]

    def _get_barras_vert(self, x=0, y=0):
        # barras verticales distribuidas a lo largo del muro
        # son las de traccion que trabajan contra el empuje del suelo
        lm  = self.largo_muro
        hz  = self.alto_z
        am  = self.alto_m
        r   = self.recub
        sep = self.sep_vert
        d   = self.diam_vert
        barras = []
        xb = x + r + d / 2
        while xb <= x + lm - r - d / 2:
            barras.append([[xb, y + hz + r],
                           [xb, y + hz + am - r]])
            xb += sep
        return barras

    def _get_barras_horiz(self, x=0, y=0):
        # barras horizontales de temperatura distribuidas en altura
        lm  = self.largo_muro
        hz  = self.alto_z
        am  = self.alto_m
        r   = self.recub
        sep = self.sep_horiz
        d   = self.diam_horiz
        barras = []
        yb = y + hz + r + d / 2
        while yb <= y + hz + am - r - d / 2:
            barras.append([[x + r, yb], [x + lm - r, yb]])
            yb += sep
        return barras

    def _get_barras_zap_inf(self, x=0, y=0):
        # barras inferiores de zapata a lo largo del muro
        lm  = self.largo_muro
        r   = self.recub
        d   = self.diam_zap
        n   = self.n_zap
        yc  = y + r + d / 2
        paso = d + 0.3
        return [[[x + r, yc + i * paso], [x + lm - r, yc + i * paso]]
                for i in range(n)]

    def _get_barras_zap_sup(self, x=0, y=0):
        # barras superiores de zapata a lo largo del muro
        lm  = self.largo_muro
        hz  = self.alto_z
        r   = self.recub
        d   = self.diam_zap
        n   = self.n_zap
        yc  = y + hz - r - d / 2
        paso = d + 0.3
        return [[[x + r, yc - i * paso], [x + lm - r, yc - i * paso]]
                for i in range(n)]

    def _get_lineas_empuje(self, x=0, y=0):
        # lineas que indican el empuje del suelo en la cara posterior
        # se dibujan en el borde izquierdo de la pantalla (cara traccion)
        # como lineas horizontales cortas apuntando hacia la derecha
        hz  = self.alto_z
        am  = self.alto_m
        n   = 8   # cantidad de flechas de empuje ilustrativas
        y_ini = y + hz
        y_fin = y + hz + am
        paso  = am / (n + 1)
        lineas = []
        for i in range(1, n + 1):
            yi = y_ini + i * paso
            # largo de flecha proporcional a la altura (mayor presion abajo)
            factor = i / n
            largo  = 5 + factor * 10
            lineas.append([[x - largo, yi], [x, yi]])
        return lineas

    def _get_dim_points(self, x=0, y=0):
        lm  = self.largo_muro
        hz  = self.alto_z
        am  = self.alto_m
        sep = self.sep_vert
        r   = self.recub
        return [
                # largo del muro
                [[x     , y      ], [x + lm , y      ]],
                # alto zapata
                [[x     , y      ], [x      , y + hz ]],
                # alto pantalla
                [[x     , y + hz ], [x      , y + hz + am]],
                # separacion barras verticales
                [[x + r , y + hz + am + 3], [x + r + sep, y + hz + am + 3]],
                ]

    def _get_text(self):
        lm   = self.largo_muro
        lz   = self.largo_z
        hz   = self.alto_z
        am   = self.alto_m
        eb   = self.e_base
        r    = self.recub
        sv   = self.sep_vert
        sh   = self.sep_horiz
        dv   = self.diam_vert
        dh   = self.diam_horiz
        dz   = self.diam_zap
        nz   = self.n_zap
        # conteo de barras
        n_v  = int((lm - 2*r) / sv) + 1
        n_h  = int((am - 2*r) / sh) + 1
        as_v = round(n_v * math.pi * dv**2 / 4, 2)
        as_h = round(n_h * math.pi * dh**2 / 4, 2)
        as_z = round(nz  * math.pi * dz**2 / 4, 2)
        return (f"Corte muro L={lm} cm\n"
                f"Zapata: {lz}x{hz} cm\n"
                f"Pantalla: {lm}x{am} cm  e={eb} cm\n"
                f"Recub = {r} cm\n\n"
                f"Vert: sep={sv} cm  N~{n_v}  d={dv}\n"
                f"  As~{as_v} cm2/m\n"
                f"Horiz: sep={sh} cm  N~{n_h}  d={dh}\n"
                f"  As~{as_h} cm2\n"
                f"Zapata: {nz} barras d={dz}\n"
                f"  As={as_z} cm2")

    def draw(self, x=None, y=None, char=5, border=False):
        """dibuja el corte transversal del muro en el modelspace"""
        self.move_to(x, y)
        x   = self.x
        y   = self.y

        doc = self.doc
        msp = doc.modelspace()

        true_x = x + 20 * char
        true_y = y + 45 * char

        alto_total = self.alto_z + self.alto_m
        marco_x    = self.largo_muro + 40 * char
        marco_y    = alto_total      + 60 * char

        centro_x  = x + marco_x / 2
        centro_y  = y + marco_y / 2
        leyenda_x = x + char * 22
        leyenda_y = y + char * 35

        marco = [
                [x           , y           ],
                [x + marco_x , y           ],
                [x + marco_x , y + marco_y ],
                [x           , y + marco_y ],
                ]

        pantalla    = self._get_pantalla      (true_x, true_y)
        zapata      = self._get_zapata        (true_x, true_y)
        b_vert      = self._get_barras_vert   (true_x, true_y)
        b_horiz     = self._get_barras_horiz  (true_x, true_y)
        b_zap_inf   = self._get_barras_zap_inf(true_x, true_y)
        b_zap_sup   = self._get_barras_zap_sup(true_x, true_y)
        empuje      = self._get_lineas_empuje (true_x, true_y)
        coord_dim   = self._get_dim_points    (true_x, true_y)

        if border: # verde
            msp.add_lwpolyline(marco, close=True,
                               dxfattribs={'color': 3})

        # contornos
        msp.add_lwpolyline(zapata,   close=True, dxfattribs={'color': 7, 'lineweight': 30})
        msp.add_lwpolyline(pantalla, close=True, dxfattribs={'color': 7, 'lineweight': 30})

        # barras verticales (rojo) - acero principal de traccion
        for b in b_vert:
            msp.add_line(start=b[0], end=b[1],
                         dxfattribs={'color': 1, 'lineweight': 50})

        # barras horizontales (azul) - temperatura
        for b in b_horiz:
            msp.add_line(start=b[0], end=b[1],
                         dxfattribs={'color': 5, 'lineweight': 30})

        # barras zapata inferior (rojo)
        for b in b_zap_inf:
            msp.add_line(start=b[0], end=b[1],
                         dxfattribs={'color': 1, 'lineweight': 50})

        # barras zapata superior (azul)
        for b in b_zap_sup:
            msp.add_line(start=b[0], end=b[1],
                         dxfattribs={'color': 5, 'lineweight': 30})

        msp.add_mtext(self._get_text(),
                      dxfattribs={"style": "iso", "insert": (leyenda_x, leyenda_y),
                                  "char_height": char*2, "color": 8, # gris
                                  "width": marco_x, "line_spacing_factor": 0.75})

        for seg in coord_dim:
            msp.add_aligned_dim(p1=seg[0], p2=seg[1],
                                distance=char, text="<> cm")

        doc.header['$DIMASZ']  = char
        doc.header['$DIMTXT']  = char 
        doc.header['$DIMCLRT'] = 8 # gris
        doc.header['$DIMCLRD'] = 8 # gris
        doc.header['$DIMCLRE'] = 8 # gris

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
        msp.add_lwpolyline(self._get_pantalla(), close=True)
        msp.add_lwpolyline(self._get_zapata(),   close=True)
        for b in self._get_barras_vert():
            msp.add_line(start=b[0], end=b[1])
        for b in self._get_barras_horiz():
            msp.add_line(start=b[0], end=b[1])
        for b in self._get_barras_zap_inf():
            msp.add_line(start=b[0], end=b[1])
        for b in self._get_barras_zap_sup():
            msp.add_line(start=b[0], end=b[1])
        for lin in self._get_lineas_empuje():
            msp.add_line(start=lin[0], end=lin[1])
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
        self.config(largo_muro=500, alto_z=30, alto_m=220, sep_vert=15, sep_horiz=35)
        self.draw(char=2, border=True)
        self.config(largo_muro=600, alto_z=35, alto_m=270, sep_vert=20, sep_horiz=40)
        self.draw(char=2, border=True)
        self.config(largo_muro=700, alto_z=40, alto_m=320, sep_vert=25, sep_horiz=50)
        self.draw(char=2, border=True)
        self.draw(border=True)
        self.draw(border=True)
        self.get_doc().saveas("test.dxf")
        print("test 3 ok")

if __name__ == '__main__':
    obj = Corte_muro()
    obj._test_1()
    obj._test_2()
    obj._test_3()