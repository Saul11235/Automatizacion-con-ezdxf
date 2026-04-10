# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
import math

class Corte_losa:
    """
    CORTE LOSA - corte transversal de losa aligerada unidireccional
    ===============================================================

    Vista perpendicular a las viguetas (corte en Y).
    Lo que se ve:
      - capa de compresion superior (ancho_losa x h_losa)
      - secciones de viguetas (b_vig x h_vigueta)
      - bloques entre viguetas (claro_bloque x h_vigueta)
      - acero en pie de cada vigueta (circulos rellenos)
      - acero de temperatura en capa de compresion (linea)
      - cotas de altura, anchos y paso

    Parametros:
      ancho_losa   = 400  ancho total de la losa en cm
      b_vig        = 12   ancho de la vigueta en cm
      claro_bloque = 28   claro libre entre viguetas en cm
      h_total      = 20   altura total (losa + vigueta) en cm
      h_losa       = 5    espesor capa de compresion en cm
      recub        = 2    recubrimiento en cm
      diam_vig     = 0.95 diametro barra de vigueta cm
      n_barras_vig = 2    numero de barras por vigueta
      diam_temp    = 0.64 diametro barra temperatura cm
      sep_temp     = 25   separacion barras de temperatura cm

    Metodos estandar:
      __init__, config, set_doc, get_doc,
      move, move_to, get_pos, draw
    Tests: _test_1, _test_2, _test_3
    """

    def __init__(self, ancho_losa=400, b_vig=12, claro_bloque=28,
                 h_total=20, h_losa=5,
                 recub=2, diam_vig=0.95, n_barras_vig=2,
                 diam_temp=0.64, sep_temp=25):
        self.config(ancho_losa, b_vig, claro_bloque, h_total, h_losa,
                    recub, diam_vig, n_barras_vig, diam_temp, sep_temp)
        self.doc = ezdxf.new()
        self.x = self.y = 0
        print("> objeto creado, Corte_losa")

    def config(self, ancho_losa=400, b_vig=12, claro_bloque=28,
               h_total=20, h_losa=5,
               recub=2, diam_vig=0.95, n_barras_vig=2,
               diam_temp=0.64, sep_temp=25):
        self.ancho_losa   = abs(ancho_losa)
        self.b_vig        = abs(b_vig)
        self.claro_bloque = abs(claro_bloque)
        self.h_total      = abs(h_total)
        self.h_losa       = abs(h_losa)
        self.recub        = abs(recub)
        self.diam_vig     = abs(diam_vig)
        self.n_barras_vig = max(1, int(n_barras_vig))
        self.diam_temp    = abs(diam_temp)
        self.sep_temp     = abs(sep_temp)
        self.h_vig  = self.h_total - self.h_losa
        self.paso   = self.b_vig + self.claro_bloque
        if self.h_losa  >= self.h_total : self.h_losa = self.h_total * 0.25
        if self.paso    >  self.ancho_losa: self.paso  = self.ancho_losa

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

    def _get_capa_compresion(self, x=0, y=0):
        # rectangulo de la capa de compresion superior
        al = self.ancho_losa
        hl = self.h_losa
        hv = self.h_vig
        # la losa se dibuja con Y creciendo hacia arriba
        # capa de compresion esta encima de las viguetas
        return [
                [x      , y + hv      ],
                [x + al , y + hv      ],
                [x + al , y + hv + hl ],
                [x      , y + hv + hl ],
                ]

    def _get_secciones_vigueta(self, x=0, y=0):
        # lista de rectangulos de seccion de cada vigueta
        al   = self.ancho_losa
        bv   = self.b_vig
        hv   = self.h_vig
        paso = self.paso
        secs = []
        xv   = x
        while xv + bv <= x + al + 0.01:
            secs.append([
                    [xv      , y      ],
                    [xv + bv , y      ],
                    [xv + bv , y + hv ],
                    [xv      , y + hv ],
                    ])
            xv += paso
        return secs

    def _get_secciones_bloque(self, x=0, y=0):
        # lista de rectangulos de cada bloque entre viguetas
        al   = self.ancho_losa
        bv   = self.b_vig
        cb   = self.claro_bloque
        hv   = self.h_vig
        paso = self.paso
        blqs = []
        xb   = x + bv   # primer bloque despues de la vigueta de borde
        while xb + cb <= x + al - bv + 0.01:
            blqs.append([
                    [xb      , y      ],
                    [xb + cb , y      ],
                    [xb + cb , y + hv ],
                    [xb      , y + hv ],
                    ])
            xb += paso
        return blqs

    def _get_acero_viguetas(self, x=0, y=0):
        # circulos (o puntos) de acero en pie de cada vigueta
        al   = self.ancho_losa
        bv   = self.b_vig
        hv   = self.h_vig
        paso = self.paso
        r    = self.recub
        d    = self.diam_vig
        n    = self.n_barras_vig
        centros = []
        xv = x
        while xv + bv <= x + al + 0.01:
            # y del centro de la barra (sobre recubrimiento)
            yc = y + r + d / 2
            # distribucion horizontal de barras en la vigueta
            if n == 1:
                centros.append([xv + bv / 2, yc])
            else:
                x_ini = xv + r + d / 2
                x_fin = xv + bv - r - d / 2
                sep   = (x_fin - x_ini) / (n - 1)
                for i in range(n):
                    centros.append([x_ini + i * sep, yc])
            xv += paso
        return centros

    def _get_acero_temp(self, x=0, y=0):
        # barras de temperatura en capa de compresion
        # se distribuyen con sep_temp a lo largo del ancho
        al   = self.ancho_losa
        hv   = self.h_vig
        hl   = self.h_losa
        r    = self.recub
        sep  = self.sep_temp
        d    = self.diam_temp
        # y del eje = en la mitad de la capa de compresion
        yc   = y + hv + r + d / 2
        barras = []
        xb = x + r
        while xb <= x + al - r + 0.01:
            barras.append([xb, yc])   # solo centros, se dibujaran como circulos
            xb += sep
        return barras

    def _get_dim_points(self, x=0, y=0):
        al   = self.ancho_losa
        bv   = self.b_vig
        cb   = self.claro_bloque
        ht   = self.h_total
        hv   = self.h_vig
        hl   = self.h_losa
        paso = self.paso
        return [
                # ancho total losa
                [[x     , y      ], [x + al , y      ]],
                # h total
                [[x     , y      ], [x      , y + ht ]],
                # h capa compresion
                [[x + al + 3, y + hv], [x + al + 3, y + hv + hl]],
                # h vigueta
                [[x + al + 3, y     ], [x + al + 3, y + hv     ]],
                # ancho vigueta
                [[x     , y - 3  ], [x + bv , y - 3 ]],
                # claro bloque
                [[x + bv, y - 3  ], [x + bv + cb, y - 3]],
                ]

    def _get_text(self):
        al   = self.ancho_losa
        bv   = self.b_vig
        cb   = self.claro_bloque
        ht   = self.h_total
        hl   = self.h_losa
        hv   = self.h_vig
        paso = self.paso
        r    = self.recub
        dv   = self.diam_vig
        nv   = self.n_barras_vig
        dt   = self.diam_temp
        st   = self.sep_temp
        # conteos
        n_vigs = int(al / paso) + 1
        n_blqs = max(0, n_vigs - 1)
        n_temp = int((al - 2*r) / st) + 1
        # areas
        as_vig  = round(nv * math.pi * dv**2 / 4, 3)
        as_temp = round(n_temp * math.pi * dt**2 / 4, 3)
        return (f"Losa aligerada  ancho={al} cm\n"
                f"h total = {ht} cm\n"
                f"  capa comp = {hl} cm\n"
                f"  vigueta   = {hv} cm\n"
                f"Recub = {r} cm\n\n"
                f"Vigueta: b={bv} cm\n"
                f"Bloque:  b={cb} cm\n"
                f"Paso = {paso} cm\n"
                f"N viguetas ~ {n_vigs}\n"
                f"N bloques  ~ {n_blqs}\n\n"
                f"As vig: {nv}d{dv} = {as_vig} cm2\n"
                f"Temp: sep={st} N~{n_temp} d={dt}\n"
                f"  As~{as_temp} cm2")

    def draw(self, x=None, y=None, char=5, border=False):
        """dibuja el corte transversal de la losa en el modelspace"""
        self.move_to(x, y)
        x   = self.x
        y   = self.y

        doc = self.doc
        msp = doc.modelspace()

        true_x = x + 15 * char
        true_y = y + 58 * char

        marco_x   = self.ancho_losa + 30 * char
        marco_y   = self.h_total    + 70 * char

        centro_x  = x + marco_x / 2
        centro_y  = y + marco_y / 2
        leyenda_x = x + char * 20
        leyenda_y = y + char * 46

        marco = [
                [x           , y           ],
                [x + marco_x , y           ],
                [x + marco_x , y + marco_y ],
                [x           , y + marco_y ],
                ]

        capa_comp   = self._get_capa_compresion  (true_x, true_y)
        secs_vig    = self._get_secciones_vigueta(true_x, true_y)
        secs_blq    = self._get_secciones_bloque (true_x, true_y)
        centros_vig = self._get_acero_viguetas   (true_x, true_y)
        centros_tmp = self._get_acero_temp       (true_x, true_y)
        coord_dim   = self._get_dim_points       (true_x, true_y)
        r_vig       = self.diam_vig  / 2
        r_tmp       = self.diam_temp / 2

        if border: # verde
            msp.add_lwpolyline(marco, close=True,
                               dxfattribs={'color': 3})

       # contorno capa compresion
        msp.add_lwpolyline(capa_comp, close=True,
                           dxfattribs={'color': 7, 'lineweight': 30})

        # contornos viguetas
        for vig in secs_vig:
            msp.add_lwpolyline(vig, close=True,
                               dxfattribs={'color': 7, 'lineweight': 25})

        # acero en pie de viguetas (circulos rellenos )
        for cx, cy in centros_vig:
            msp.add_circle(center=(cx, cy), radius=r_vig)
            h_b = msp.add_hatch()
            ep  = h_b.paths.add_edge_path()
            ep.add_arc(center=(cx, cy), radius=r_vig,
                       start_angle=0, end_angle=360, ccw=True)
            h_b.set_solid_fill()

        # acero de temperatura en capa de compresion (circulos )
        for cx, cy in centros_tmp:
            msp.add_circle(center=(cx, cy), radius=r_tmp)
            h_t = msp.add_hatch()
            ep  = h_t.paths.add_edge_path()
            ep.add_arc(center=(cx, cy), radius=r_tmp,
                       start_angle=0, end_angle=360, ccw=True)
            h_t.set_solid_fill()

        msp.add_mtext(self._get_text(),
                      dxfattribs={"style": "iso", "insert": (leyenda_x, leyenda_y),
                                  "char_height": char*2, "color": 8,
                                  "width": marco_x, "line_spacing_factor": 0.75})

        for seg in coord_dim:
            msp.add_aligned_dim(p1=seg[0], p2=seg[1],
                                distance=char, text="<> cm")

        doc.header['$DIMASZ']  = char 
        doc.header['$DIMTXT']  = char
        doc.header['$DIMCLRT'] = 8  # gris
        doc.header['$DIMCLRD'] = 8  # gris
        doc.header['$DIMCLRE'] = 8  # gris

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
        msp.add_lwpolyline(self._get_capa_compresion(), close=True)
        for v in self._get_secciones_vigueta():
            msp.add_lwpolyline(v, close=True)
        for b in self._get_secciones_bloque():
            msp.add_lwpolyline(b, close=True)
        for cx, cy in self._get_acero_viguetas():
            msp.add_circle(center=(cx, cy), radius=self.diam_vig/2)
        for cx, cy in self._get_acero_temp():
            msp.add_circle(center=(cx, cy), radius=self.diam_temp/2)
        msp.add_mtext("\n" + self._get_text())
        for seg in self._get_dim_points():
            msp.add_aligned_dim(p1=seg[0], p2=seg[1], distance=1)
        doc.saveas("test.dxf")
        print("test 1 ok")

    def _test_2(self):
        doc = ezdxf.new()
        self.set_doc(doc)
        self.draw(x=0, y=0, char=2, border=True)
        doc.saveas("test.dxf")
        print("test 2 ok")

    def _test_3(self):
        self.config(ancho_losa=300, b_vig=12, claro_bloque=23, h_total=17, h_losa=5)
        self.draw(char=2, border=True)
        self.config(ancho_losa=400, b_vig=12, claro_bloque=28, h_total=20, h_losa=5)
        self.draw(char=2, border=True)
        self.config(ancho_losa=500, b_vig=15, claro_bloque=35, h_total=25, h_losa=5)
        self.draw(char=2, border=True)
        self.get_doc().saveas("test.dxf")
        print("test 3 ok")

if __name__ == '__main__':
    obj = Corte_losa()
    obj._test_1()
    obj._test_2()
    obj._test_3()