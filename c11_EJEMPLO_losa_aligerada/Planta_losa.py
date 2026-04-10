# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
import math

class Planta_losa:
    """
    PLANTA LOSA - vista en planta de losa aligerada unidireccional
    ==============================================================

    Muestra la vista desde arriba de la losa aligerada:
      - contorno de la losa (largo_losa x ancho_losa)
      - franjas de viguetas (en la direccion principal Lx)
      - espacios de bloques entre viguetas
      - acero de vigueta en eje de cada vigueta (linea punteada)
      - acero de temperatura perpendicular a las viguetas
      - vigas de apoyo en los bordes (si se indica)

    Las viguetas corren en la direccion X (largo_losa).
    Los bloques se ubican entre viguetas en la direccion Y.
    El paso entre ejes de vigueta = b_vig + claro_bloque.

    Parametros:
      largo_losa   = 500  longitud de la losa en direccion de viguetas (cm)
      ancho_losa   = 400  ancho de la losa perpendicular a viguetas (cm)
      b_vig        = 12   ancho de la vigueta en cm
      claro_bloque = 28   claro libre entre viguetas (ancho del bloque) en cm
      h_total      = 20   altura total de losa en cm (para leyenda)
      h_losa       = 5    espesor capa de compresion en cm (para leyenda)
      recub        = 2    recubrimiento en cm
      diam_vig     = 0.95 diametro barra de vigueta cm  (3/8" = 0.95)
      n_barras_vig = 2    numero de barras por vigueta
      sep_temp     = 25   separacion barras de temperatura en cm
      diam_temp    = 0.64 diametro barra temperatura cm (1/4" = 0.64)

    Metodos estandar:
      __init__, config, set_doc, get_doc,
      move, move_to, get_pos, draw
    Tests: _test_1, _test_2, _test_3
    """

    def __init__(self, largo_losa=500, ancho_losa=400,
                 b_vig=12, claro_bloque=28,
                 h_total=20, h_losa=5,
                 recub=2, diam_vig=0.95, n_barras_vig=2,
                 sep_temp=25, diam_temp=0.64):
        self.config(largo_losa, ancho_losa, b_vig, claro_bloque,
                    h_total, h_losa, recub, diam_vig, n_barras_vig,
                    sep_temp, diam_temp)
        self.doc = ezdxf.new()
        self.x = self.y = 0
        print("> objeto creado, Planta_losa")

    def config(self, largo_losa=500, ancho_losa=400,
               b_vig=12, claro_bloque=28,
               h_total=20, h_losa=5,
               recub=2, diam_vig=0.95, n_barras_vig=2,
               sep_temp=25, diam_temp=0.64):
        self.largo_losa   = abs(largo_losa)
        self.ancho_losa   = abs(ancho_losa)
        self.b_vig        = abs(b_vig)
        self.claro_bloque = abs(claro_bloque)
        self.h_total      = abs(h_total)
        self.h_losa       = abs(h_losa)
        self.recub        = abs(recub)
        self.diam_vig     = abs(diam_vig)
        self.n_barras_vig = max(1, int(n_barras_vig))
        self.sep_temp     = abs(sep_temp)
        self.diam_temp    = abs(diam_temp)
        self.paso = self.b_vig + self.claro_bloque
        if self.paso > self.ancho_losa: self.paso = self.ancho_losa
        if self.sep_temp > self.largo_losa: self.sep_temp = self.largo_losa / 4

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
        # rectangulo exterior de la losa
        ll = self.largo_losa
        al = self.ancho_losa
        return [
                [x      , y      ],
                [x + ll , y      ],
                [x + ll , y + al ],
                [x      , y + al ],
                ]

    def _get_viguetas(self, x=0, y=0):
        # lista de rectangulos de cada vigueta en planta
        # las viguetas corren en X (largo_losa)
        # se distribuyen en Y comenzando desde el borde
        ll   = self.largo_losa
        al   = self.ancho_losa
        bv   = self.b_vig
        paso = self.paso
        vigs = []
        yv   = y   # primer borde es vigueta de borde
        while yv + bv <= y + al + 0.01:
            vigs.append([
                    [x      , yv      ],
                    [x + ll , yv      ],
                    [x + ll , yv + bv ],
                    [x      , yv + bv ],
                    ])
            yv += paso
        return vigs

    def _get_bloques(self, x=0, y=0):
        # lista de rectangulos de cada bloque en planta
        ll   = self.largo_losa
        al   = self.ancho_losa
        bv   = self.b_vig
        cb   = self.claro_bloque
        paso = self.paso
        bloques = []
        yb   = y + bv   # bloques empiezan despues de la primera vigueta
        while yb + cb <= y + al - bv + 0.01:
            bloques.append([
                    [x      , yb      ],
                    [x + ll , yb      ],
                    [x + ll , yb + cb ],
                    [x      , yb + cb ],
                    ])
            yb += paso
        return bloques

    def _get_acero_viguetas(self, x=0, y=0):
        # lineas en el eje de cada vigueta (acero longitudinal)
        ll   = self.largo_losa
        al   = self.ancho_losa
        bv   = self.b_vig
        paso = self.paso
        n    = self.n_barras_vig
        d    = self.diam_vig
        lineas = []
        yv = y
        while yv + bv <= y + al + 0.01:
            yc = yv + bv / 2   # eje de vigueta
            # si hay varias barras, las distribuye en el ancho util
            if n == 1:
                lineas.append([[x + self.recub, yc],
                               [x + ll - self.recub, yc]])
            else:
                sep = (bv - 2*self.recub) / (n - 1)
                for i in range(n):
                    yi = yv + self.recub + i * sep
                    lineas.append([[x + self.recub, yi],
                                   [x + ll - self.recub, yi]])
            yv += paso
        return lineas

    def _get_acero_temp(self, x=0, y=0):
        # barras de temperatura perpendiculares a las viguetas (en Y)
        # se distribuyen a lo largo de Lx con separacion sep_temp
        ll   = self.largo_losa
        al   = self.ancho_losa
        sep  = self.sep_temp
        r    = self.recub
        barras = []
        xb = x + r
        while xb <= x + ll - r + 0.01:
            barras.append([[xb, y + r], [xb, y + al - r]])
            xb += sep
        return barras

    def _get_dim_points(self, x=0, y=0):
        ll   = self.largo_losa
        al   = self.ancho_losa
        bv   = self.b_vig
        cb   = self.claro_bloque
        paso = self.paso
        sep  = self.sep_temp
        r    = self.recub
        return [
                # largo losa (X)
                [[x     , y      ], [x + ll , y      ]],
                # ancho losa (Y)
                [[x     , y      ], [x      , y + al ]],
                # ancho vigueta
                [[x - 3 , y      ], [x - 3  , y + bv ]],
                # claro bloque
                [[x - 3 , y + bv ], [x - 3  , y + bv + cb]],
                # separacion temperatura
                [[x + r , y + al + 3], [x + r + sep, y + al + 3]],
                ]

    def _get_text(self):
        ll   = self.largo_losa
        al   = self.ancho_losa
        bv   = self.b_vig
        cb   = self.claro_bloque
        ht   = self.h_total
        hl   = self.h_losa
        paso = self.paso
        r    = self.recub
        dv   = self.diam_vig
        nv   = self.n_barras_vig
        st   = self.sep_temp
        dt   = self.diam_temp
        # numero de viguetas
        n_vigs = int(al / paso) + 1
        # numero de bloques
        n_blqs = max(0, n_vigs - 1)
        # numero de barras temperatura
        n_temp = int((ll - 2*r) / st) + 1
        # areas de acero
        as_vig  = round(nv * math.pi * dv**2 / 4, 3)
        as_temp = round(n_temp * math.pi * dt**2 / 4, 3)
        hv      = ht - hl
        return (f"Losa aligerada = {ll}x{al} cm\n"
                f"h total = {ht} cm\n"
                f"  losa sup = {hl} cm\n"
                f"  vigueta  = {hv} cm\n"
                f"Recub = {r} cm\n\n"
                f"Vigueta: b={bv} cm\n"
                f"Bloque:  b={cb} cm\n"
                f"Paso (eje-eje) = {paso} cm\n"
                f"N viguetas ~ {n_vigs}\n"
                f"N bloques  ~ {n_blqs}\n\n"
                f"As vig: {nv}d{dv} = {as_vig} cm2\n"
                f"As temp: sep={st} cm  d={dt}\n"
                f"  N~{n_temp}  As~{as_temp} cm2")

    def draw(self, x=None, y=None, char=1, border=False):
        """dibuja la planta de la losa aligerada en el modelspace"""
        self.move_to(x, y)
        x   = self.x
        y   = self.y

        doc = self.doc
        msp = doc.modelspace()

        true_x = x + 30 * char
        true_y = y + 70 * char

        marco_x   = self.largo_losa + 50  * char
        marco_y   = self.ancho_losa + 100 * char

        centro_x  = x + marco_x / 2
        centro_y  = y + marco_y / 2
        leyenda_x = x + char * 30
        leyenda_y = y + char * 59

        marco = [
                [x           , y           ],
                [x + marco_x , y           ],
                [x + marco_x , y + marco_y ],
                [x           , y + marco_y ],
                ]

        contorno    = self._get_contorno       (true_x, true_y)
        viguetas    = self._get_viguetas       (true_x, true_y)
        bloques     = self._get_bloques        (true_x, true_y)
        ac_vigs     = self._get_acero_viguetas (true_x, true_y)
        ac_temp     = self._get_acero_temp     (true_x, true_y)
        coord_dim   = self._get_dim_points     (true_x, true_y)

        if border:  # verde
            msp.add_lwpolyline(marco, close=True,
                               dxfattribs={'color': 3})
        # contorno exterior
        msp.add_lwpolyline(contorno, close=True,
                           dxfattribs={'color': 7, 'lineweight': 50})

        # contornos viguetas
        for vig in viguetas:
            msp.add_lwpolyline(vig, close=True,
                               dxfattribs={'color': 7, 'lineweight': 20})

        # acero de vigueta (rojo)
        for b in ac_vigs:
            msp.add_line(start=b[0], end=b[1],
                         dxfattribs={'color': 1, 'lineweight': 40,
                                     'linetype': 'DASHED'})

        # acero de temperatura (azul)
        for b in ac_temp:
            msp.add_line(start=b[0], end=b[1],
                         dxfattribs={'color': 5, 'lineweight': 25})

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
        msp.add_lwpolyline(self._get_contorno(), close=True)
        for v in self._get_viguetas():
            msp.add_lwpolyline(v, close=True)
        for b in self._get_bloques():
            msp.add_lwpolyline(b, close=True)
        for b in self._get_acero_viguetas():
            msp.add_line(start=b[0], end=b[1])
        for b in self._get_acero_temp():
            msp.add_line(start=b[0], end=b[1])
        msp.add_mtext("\n" + self._get_text())
        for seg in self._get_dim_points():
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
        # variando dimensiones de losa y paso de viguetas
        self.config(largo_losa=400, ancho_losa=300, b_vig=12, claro_bloque=23)
        self.draw(char=2, border=True)
        self.config(largo_losa=500, ancho_losa=400, b_vig=12, claro_bloque=28)
        self.draw(char=2, border=True)
        self.config(largo_losa=600, ancho_losa=500, b_vig=15, claro_bloque=35)
        self.draw(char=2, border=True)
        self.get_doc().saveas("test.dxf")
        print("test 3 ok")

if __name__ == '__main__':
    obj = Planta_losa()
    obj._test_1()
    obj._test_2()
    obj._test_3()