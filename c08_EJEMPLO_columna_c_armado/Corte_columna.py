# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
import math

class Corte_columna:
    """
    CORTE COLUMNA - desarrollo longitudinal de columna multi-piso
    =============================================================

    Muestra el alzado (corte longitudinal) completo de la columna:

    Desde abajo hacia arriba:
      [ZAPATA]
        - empotramiento de barras con longitud de desarrollo
      [PISO 1 ... PISO N]  (se repite n_pisos veces)
        - zona confinada inferior (Lc): estribos densos
        - zona central             : estribos mas separados
        - zona confinada superior  (Lc): estribos densos
        - NUDO (losa): estribo cerrado en todo el espesor de losa
      [REMATE]
        - prolongacion de barras sobre el ultimo nivel

    Criterios de confinamiento (ACI 318 / NSR-10):
      Lc   = max(h_col, h_piso/6, 50 cm)
      s_conf = min(b_col/4, 8*d_long, 10 cm)  <- zona confinada
      s_cent = min(b_col/2, 16*d_long, 30 cm) <- zona central

    Parametros:
      b_col       = 30    dimension de la columna en cm (cara visible)
      h_col       = 30    dimension perpendicular en cm
      h_piso      = 280   altura libre entre losas en cm
      n_pisos     = 3     numero de pisos
      h_losa      = 20    espesor de la losa en cm
      h_zapata    = 50    alto de la zapata en cm
      ancho_zapata= 120   ancho de la zapata en cm
      recub       = 4     recubrimiento en cm
      d_estribo   = 0.95  diametro estribo cm (3/8"=0.95)
      diam_long   = 1.59  diametro barra longitudinal cm (5/8"=1.59)
      n_barras    = 4     numero de barras longitudinales visibles en el corte
      l_desarrollo= 40    longitud de desarrollo en zapata en cm

    Metodos estandar:
      __init__, config, set_doc, get_doc,
      move, move_to, get_pos, draw
    Tests: _test_1, _test_2, _test_3
    """

    def __init__(self, b_col=30, h_col=30, h_piso=280,
                 n_pisos=3, h_losa=20, h_zapata=50,
                 ancho_zapata=120, recub=4,
                 d_estribo=0.95, diam_long=1.59,
                 n_barras=4, l_desarrollo=40):
        self.config(b_col, h_col, h_piso, n_pisos, h_losa,
                    h_zapata, ancho_zapata, recub,
                    d_estribo, diam_long, n_barras, l_desarrollo)
        self.doc = ezdxf.new()
        self.x = self.y = 0
        print("> objeto creado, Corte_columna")

    def config(self, b_col=30, h_col=30, h_piso=280,
               n_pisos=3, h_losa=20, h_zapata=50,
               ancho_zapata=120, recub=4,
               d_estribo=0.95, diam_long=1.59,
               n_barras=4, l_desarrollo=40):
        self.b_col        = abs(b_col)
        self.h_col        = abs(h_col)
        self.h_piso       = abs(h_piso)
        self.n_pisos      = max(1, int(n_pisos))
        self.h_losa       = abs(h_losa)
        self.h_zapata     = abs(h_zapata)
        self.ancho_zapata = abs(ancho_zapata)
        self.recub        = abs(recub)
        self.d_estribo    = abs(d_estribo)
        self.diam_long    = abs(diam_long)
        self.n_barras     = max(2, int(n_barras))
        self.l_desarrollo = abs(l_desarrollo)
        if self.ancho_zapata < self.b_col * 2:
            self.ancho_zapata = self.b_col * 2
        if self.l_desarrollo > self.h_zapata:
            self.l_desarrollo = self.h_zapata * 0.8
        # longitud de confinamiento segun ACI
        self.Lc = max(self.h_col,
                      self.h_piso / 6,
                      50)
        # separacion estribos zona confinada
        self.s_conf = min(self.b_col / 4,
                          8 * self.diam_long,
                          10)
        # separacion estribos zona central
        self.s_cent = min(self.b_col / 2,
                          16 * self.diam_long,
                          30)
        # altura total del desarrollo
        self.H_total = (self.h_zapata +
                        self.n_pisos * self.h_piso +
                        self.n_pisos * self.h_losa)

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
        # rectangulo de la zapata
        az = self.ancho_zapata
        hz = self.h_zapata
        b  = self.b_col
        xc = x + (az - b) / 2   # x inicio columna centrada en zapata
        return {
            'zapata' : [[x, y], [x+az, y], [x+az, y+hz], [x, y+hz]],
            'x_col'  : xc,
            'y_base' : y + hz,
        }

    def _get_columna_rect(self, x_col=0, y_base=0):
        # rectangulo completo del cuerpo de la columna (todos los pisos)
        b  = self.b_col
        Ht = (self.n_pisos * self.h_piso +
              self.n_pisos * self.h_losa)
        return [[x_col, y_base],
                [x_col + b, y_base],
                [x_col + b, y_base + Ht],
                [x_col,     y_base + Ht]]

    def _get_losas(self, x_col=0, y_base=0):
        """
        rectangulos de las losas en cada nivel.
        la losa se extiende az_losa a cada lado de la columna.
        """
        b     = self.b_col
        hp    = self.h_piso
        hl    = self.h_losa
        az    = self.ancho_zapata
        losas = []
        for i in range(self.n_pisos):
            # y base de la losa = y_base + (i+1)*h_piso + i*h_losa
            y_losa = y_base + (i + 1) * hp + i * hl
            x_losa = x_col - (az - b) / 2
            losas.append([
                    [x_losa,      y_losa     ],
                    [x_losa + az, y_losa     ],
                    [x_losa + az, y_losa + hl],
                    [x_losa,      y_losa + hl],
                    ])
        return losas

    def _get_barras_long(self, x_col=0, y_base=0):
        """
        barras longitudinales:
        - corren desde la zapata hasta el ultimo nivel
        - con prolongacion hacia abajo l_desarrollo dentro de zapata
        - se representan como n_barras lineas verticales
        """
        b    = self.b_col
        r    = self.recub
        de   = self.d_estribo
        d    = self.diam_long
        n    = self.n_barras
        ld   = self.l_desarrollo
        Ht   = (self.n_pisos * self.h_piso +
                self.n_pisos * self.h_losa)
        # rango de x de las barras
        cov  = r + de + d / 2
        x_ini = x_col + cov
        x_fin = x_col + b - cov
        barras = []
        for i in range(n):
            t   = i / (n - 1) if n > 1 else 0.5
            xb  = x_ini + t * (x_fin - x_ini)
            # barra desde el fondo de la zapata hasta el tope
            y_bot = y_base - ld     # dentro de la zapata
            y_top = y_base + Ht     # tope ultimo nivel
            barras.append([[xb, y_bot], [xb, y_top]])
        return barras

    def _get_estribos_piso(self, piso, x_col=0, y_base=0):
        """
        estribos de un piso dado (piso: 0-indexed).
        genera tres grupos:
          - zona_conf_inf : estribos densos en la parte baja del piso
          - zona_cent     : estribos separados en zona central
          - zona_conf_sup : estribos densos en la parte alta del piso
        el nudo (losa) se maneja por separado en _get_estribos_nudo
        """
        b     = self.b_col
        hp    = self.h_piso
        hl    = self.h_losa
        Lc    = self.Lc
        sc    = self.s_conf
        sm    = self.s_cent
        r     = self.recub

        # y base del piso (sobre la losa anterior o sobre zapata)
        if piso == 0:
            y_piso = y_base
        else:
            y_piso = y_base + piso * hp + piso * hl

        x0 = x_col + r
        x1 = x_col + b - r
        estribos = []

        # --- zona confinada inferior ---
        Lc_real = min(Lc, hp / 2)   # no superar la mitad del piso
        y = y_piso + sc
        while y <= y_piso + Lc_real:
            estribos.append({'p1': [x0, y], 'p2': [x1, y], 'tipo': 'conf'})
            y += sc

        # --- zona central ---
        y_cent_ini = y_piso + Lc_real
        y_cent_fin = y_piso + hp - Lc_real
        y = y_cent_ini + sm
        while y <= y_cent_fin:
            estribos.append({'p1': [x0, y], 'p2': [x1, y], 'tipo': 'cent'})
            y += sm

        # --- zona confinada superior ---
        y = y_piso + hp - Lc_real
        while y <= y_piso + hp:
            estribos.append({'p1': [x0, y], 'p2': [x1, y], 'tipo': 'conf'})
            y += sc

        return estribos

    def _get_estribos_nudo(self, piso, x_col=0, y_base=0):
        """
        estribos en el nudo (dentro de la losa) - espaciado denso.
        """
        b   = self.b_col
        hp  = self.h_piso
        hl  = self.h_losa
        sc  = self.s_conf
        r   = self.recub
        # y base del nudo
        y_nudo = y_base + (piso + 1) * hp + piso * hl
        x0 = x_col + r
        x1 = x_col + b - r
        estribos = []
        y = y_nudo + sc
        while y <= y_nudo + hl:
            estribos.append({'p1': [x0, y], 'p2': [x1, y], 'tipo': 'nudo'})
            y += sc
        return estribos

    def _get_dim_points(self, x_col=0, y_base=0):
        b   = self.b_col
        hp  = self.h_piso
        hl  = self.h_losa
        hz  = self.h_zapata
        Lc  = min(self.Lc, hp / 2)
        az  = self.ancho_zapata
        x_losa = x_col - (az - b) / 2
        return [
                # h_piso (primer piso)
                [[x_col + b + 3, y_base      ],
                 [x_col + b + 3, y_base + hp ]],
                # h_losa (primera losa)
                [[x_col + b + 3, y_base + hp ],
                 [x_col + b + 3, y_base + hp + hl]],
                # b_col
                [[x_col,         y_base - 3  ],
                 [x_col + b,     y_base - 3  ]],
                # Lc inferior (primer piso)
                [[x_col - 3,     y_base      ],
                 [x_col - 3,     y_base + Lc ]],
                # ancho zapata
                [[x_losa,        y_base - hz - 3],
                 [x_losa + az,   y_base - hz - 3]],
                ]

    def _get_text(self):
        b   = self.b_col
        h   = self.h_col
        hp  = self.h_piso
        np  = self.n_pisos
        hl  = self.h_losa
        hz  = self.h_zapata
        r   = self.recub
        de  = self.d_estribo
        dl  = self.diam_long
        nb  = self.n_barras
        ld  = self.l_desarrollo
        Lc  = round(self.Lc, 1)
        sc  = round(self.s_conf, 1)
        sm  = round(self.s_cent, 1)
        Ht  = self.H_total
        # area de acero (n_barras es por cara visible, total suele ser 4 o mas)
        as_t = round(nb * math.pi * dl**2 / 4, 2)
        rho  = round(as_t / (b * h) * 100, 2)
        return (f"Columna {b}x{h} cm\n"
                f"N pisos = {np}\n"
                f"h piso  = {hp} cm\n"
                f"h losa  = {hl} cm\n"
                f"h zapata= {hz} cm\n"
                f"H total = {Ht} cm\n\n"
                f"Recub = {r} cm\n"
                f"Estribo d={de} cm\n"
                f"Long: {nb} d={dl} cm\n"
                f"As={as_t} cm2  rho={rho}%\n"
                f"L desarr.={ld} cm\n\n"
                f"Lc = {Lc} cm\n"
                f"s conf = {sc} cm\n"
                f"s cent = {sm} cm")

    def draw(self, x=None, y=None, char=8, border=False):
        """dibuja el desarrollo longitudinal de la columna"""
        self.move_to(x, y)
        x   = self.x
        y   = self.y

        doc = self.doc
        msp = doc.modelspace()

        true_x = x + 18 * char
        true_y = y + 38 * char

        marco_x = self.ancho_zapata + 30  * char
        marco_y = self.H_total      + 60  * char

        centro_x  = x + marco_x / 2
        centro_y  = y + marco_y / 2
        leyenda_x = x + char * 11
        leyenda_y = y + char * 28

        marco = [
                [x           , y           ],
                [x + marco_x , y           ],
                [x + marco_x , y + marco_y ],
                [x           , y + marco_y ],
                ]

        # origen zapata dentro del marco
        ox    = true_x
        oy    = true_y

        zap_data  = self._get_zapata        (ox, oy)
        zap_poly  = zap_data['zapata']
        x_col     = zap_data['x_col']
        y_base    = zap_data['y_base']

        col_rect  = self._get_columna_rect  (x_col, y_base)
        losas     = self._get_losas         (x_col, y_base)
        barras    = self._get_barras_long   (x_col, y_base)
        coord_dim = self._get_dim_points    (x_col, y_base)

        # todos los estribos
        todos_estribos = []
        for piso in range(self.n_pisos):
            todos_estribos += self._get_estribos_piso (piso, x_col, y_base)
            todos_estribos += self._get_estribos_nudo (piso, x_col, y_base)

        if border:
            msp.add_lwpolyline(marco, close=True,  # borde verde
                               dxfattribs={'color': 3})

        # colocando info columna
        msp.add_lwpolyline(zap_poly, close=True, dxfattribs={'lineweight':35})
        msp.add_lwpolyline(col_rect, close=True, dxfattribs={'lineweight':35})
        for losa in losas:
            msp.add_lwpolyline(losa, close=True, dxfattribs={'lineweight':35})

        # barras longitudinales  azul
        for b_long in barras:
            # parte solida (sobre zapata)
            msp.add_line(start=b_long[0], end=b_long[1],
                         dxfattribs={'color': 5, 'lineweight': 50})

        # estribos  rojo
        for est in todos_estribos:
            color = 1 if est['tipo'] in ('conf', 'nudo') else 1
            lw    = 35 if est['tipo'] == 'conf' else \
                    25 if est['tipo'] == 'cent' else 40
            msp.add_line(start=est['p1'], end=est['p2'],
                         dxfattribs={'color': color, 'lineweight': lw})

        # lineas de zona confinada (magenta punteada, referencia)
        b_c = self.b_col
        Lc  = min(self.Lc, self.h_piso / 2)
        for piso in range(self.n_pisos):
            if piso == 0:
                y_piso = y_base
            else:
                y_piso = y_base + piso * self.h_piso + piso * self.h_losa
            # linea inferior de confinamiento
            msp.add_line(
                    start=[x_col,         y_piso + Lc],
                    end  =[x_col + b_c,   y_piso + Lc],
                    dxfattribs={'color': 6, 'lineweight': 13,
                                'linetype': 'DASHED'})
            # linea superior de confinamiento
            msp.add_line(
                    start=[x_col,         y_piso + self.h_piso - Lc],
                    end  =[x_col + b_c,   y_piso + self.h_piso - Lc],
                    dxfattribs={'color': 6, 'lineweight': 13,
                                'linetype': 'DASHED'})

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
        ox, oy = 0, 0
        zd       = self._get_zapata(ox, oy)
        x_col    = zd['x_col']
        y_base   = zd['y_base']
        msp.add_lwpolyline(zd['zapata'], close=True)
        msp.add_lwpolyline(self._get_columna_rect(x_col, y_base), close=True)
        for l in self._get_losas(x_col, y_base):
            msp.add_lwpolyline(l, close=True)
        for b in self._get_barras_long(x_col, y_base):
            msp.add_line(start=b[0], end=b[1])
        for p in range(self.n_pisos):
            for e in self._get_estribos_piso(p, x_col, y_base):
                msp.add_line(start=e['p1'], end=e['p2'])
            for e in self._get_estribos_nudo(p, x_col, y_base):
                msp.add_line(start=e['p1'], end=e['p2'])
        msp.add_mtext("\n" + self._get_text())
        for seg in self._get_dim_points(x_col, y_base):
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
        self.config(b_col=25, n_pisos=2, h_piso=260, h_losa=18, diam_long=1.27)
        self.draw(char=2, border=True)
        self.config(b_col=30, n_pisos=3, h_piso=280, h_losa=20, diam_long=1.59)
        self.draw(char=2, border=True)
        self.config(b_col=40, n_pisos=4, h_piso=300, h_losa=25, diam_long=1.91)
        self.draw(char=2, border=True)
        self.draw(border=True)
        self.get_doc().saveas("test.dxf")
        print("test 3 ok")

if __name__ == '__main__':
    obj = Corte_columna()
    obj._test_1()
    obj._test_2()
    obj._test_3()