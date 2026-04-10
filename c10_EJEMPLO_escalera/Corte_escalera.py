# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
import math

class Corte_escalera:
    """
    CORTE ESCALERA - corte longitudinal de escalera de concreto armado
    ==================================================================

    Muestra la seccion longitudinal de la escalera:
      - losa inclinada (poligono con espesor e_losa)
      - peldanos (huella + contrahuella) como poligonos encima
      - acero longitudinal paralelo al intrados
      - acero de distribucion paralelo al intrados (secundario)
      - apoyos en los extremos (viga o muro)
      - cotas: huella, contrahuella, e_losa, L horiz, H total

    El origen de la escalera es la esquina inferior-izquierda
    (apoyo inferior). La escalera sube hacia la derecha.

    Parametros:
      n_escalones   = 10    numero de escalones
      huella        = 28    ancho de la huella en cm
      contrahuella  = 18    altura de la contrahuella en cm
      ancho_esc     = 120   ancho de la escalera en cm (para leyenda)
      e_losa        = 15    espesor de la losa inclinada en cm
      recub         = 2.5   recubrimiento en cm
      n_barras_long = 5     numero de barras longitudinales
      n_barras_dist = 4     numero de barras de distribucion
      diam_long     = 1.27  diametro barra longitudinal cm (1/2"=1.27)
      diam_dist     = 0.95  diametro barra distribucion  cm (3/8"=0.95)
      ancho_apoyo   = 20    ancho del apoyo (viga/muro) en cm

    Metodos estandar:
      __init__, config, set_doc, get_doc,
      move, move_to, get_pos, draw
    Tests: _test_1, _test_2, _test_3
    """

    def __init__(self, n_escalones=10, huella=28, contrahuella=18,
                 ancho_esc=120, e_losa=15,
                 recub=2.5, n_barras_long=5, n_barras_dist=4,
                 diam_long=1.27, diam_dist=0.95, ancho_apoyo=20):
        self.config(n_escalones, huella, contrahuella, ancho_esc,
                    e_losa, recub, n_barras_long, n_barras_dist,
                    diam_long, diam_dist, ancho_apoyo)
        self.doc = ezdxf.new()
        self.x = self.y = 0
        print("> objeto creado, Corte_escalera")

    def config(self, n_escalones=10, huella=28, contrahuella=18,
               ancho_esc=120, e_losa=15,
               recub=2.5, n_barras_long=5, n_barras_dist=4,
               diam_long=1.27, diam_dist=0.95, ancho_apoyo=20):
        self.n_escalones   = max(2, int(n_escalones))
        self.huella        = abs(huella)
        self.contrahuella  = abs(contrahuella)
        self.ancho_esc     = abs(ancho_esc)
        self.e_losa        = abs(e_losa)
        self.recub         = abs(recub)
        self.n_barras_long = max(2, int(n_barras_long))
        self.n_barras_dist = max(2, int(n_barras_dist))
        self.diam_long     = abs(diam_long)
        self.diam_dist     = abs(diam_dist)
        self.ancho_apoyo   = abs(ancho_apoyo)
        self.L_horiz = self.n_escalones * self.huella
        self.H_total = self.n_escalones * self.contrahuella
        # angulo de inclinacion de la losa
        self.angulo  = math.atan2(self.H_total, self.L_horiz)
        if self.recub > self.e_losa / 2: self.recub = self.e_losa / 3
        if self.e_losa > min(self.huella, self.contrahuella):
            self.e_losa = min(self.huella, self.contrahuella) * 0.8

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

    def _get_losa(self, x=0, y=0):
        """
        poligono de la losa inclinada.
        cara inferior (intrados): linea recta de (x,y) a (x+L,y+H)
        cara superior: desplazada perpendicularmente e_losa hacia arriba
        el poligono tiene 4 vertices
        """
        L  = self.L_horiz
        H  = self.H_total
        e  = self.e_losa
        ag = self.angulo
        # vector perpendicular a la losa (apunta hacia arriba-izquierda)
        # perpendicular unitario: (-sin, cos) del angulo
        dx = -math.sin(ag) * e
        dy =  math.cos(ag) * e
        # 4 puntos:
        # p0 = origen intrados
        # p1 = fin intrados
        # p2 = fin cara superior
        # p3 = inicio cara superior
        p0 = [x,       y      ]
        p1 = [x + L,   y + H  ]
        p2 = [x + L + dx, y + H + dy]
        p3 = [x    + dx, y     + dy]
        return [p0, p1, p2, p3]

    def _get_peldanos(self, x=0, y=0):
        """
        lista de poligonos de cada peldano (huella + contrahuella).
        cada escalon es un rectangulo L-shape simplificado:
        un rectangulo de huella x contrahuella que arranca
        desde el borde frontal del escalon correspondiente.
        """
        h   = self.huella
        ch  = self.contrahuella
        n   = self.n_escalones
        ag  = self.angulo
        e   = self.e_losa
        # vector perpendicular a la losa
        dx = -math.sin(ag) * e
        dy =  math.cos(ag) * e
        peldanos = []
        for i in range(n):
            # esquina inferior-frontal del escalon sobre la cara superior de la losa
            # la cara superior arranca en (x+dx, y+dy) y sube con pendiente
            xi_base = x + dx + i * h
            yi_base = y + dy + i * ch
            # peldano: rectangulo definido por
            # p0 = esquina frontal-inferior (sobre losa)
            # p1 = esquina trasera-inferior (sobre losa, siguiente escalon)
            # p2 = esquina trasera-superior (tope del escalon)
            # p3 = esquina frontal-superior
            # el tope de cada escalon esta ch mas arriba que la base
            p0 = [xi_base        , yi_base     ]
            p1 = [xi_base + h    , yi_base + ch]   # punto sobre la losa en el borde trasero
            p2 = [xi_base + h    , yi_base + ch]   # mismo punto (la huella es horizontal)
            p3 = [xi_base        , yi_base + ch]   # tope frontal

            # el escalon real tiene:
            # - huella horizontal (parte pisable)
            # - contrahuella vertical (parte frontal)
            # construimos el L correcto:
            # base de la huella: desde (xi_base, yi_base) hasta (xi_base+h, yi_base+ch) (sobre losa)
            # la huella va horizontal hacia el frente (en Y global no cambia dentro del escalon)
            # pero como la losa es inclinada, la huella REAL es horizontal aunque la losa no lo sea

            # reconstruccion correcta:
            # punto A: esquina frontal-inferior del escalon (sobre intrados)
            xa = xi_base
            ya = yi_base
            # punto B: esquina trasera del escalon a nivel de la huella (horizontal)
            xb = xi_base + h
            yb = yi_base + ch  # sigue la inclinacion de la losa
            # punto C: tope de la contrahuella trasera
            xc = xb
            yc = yb   # mismo x, y ya esta a nivel del siguiente escalon
            # punto D: tope de la contrahuella frontal (encima de A, ch arriba)
            xd = xa
            yd = ya + ch

            # el peldano como poligono cerrado de 4 puntos
            peldanos.append([[xa, ya], [xb, yb], [xc, yc], [xd, yd]])
        return peldanos

    def _get_escalones_perfil(self, x=0, y=0):
        """
        perfil escalonado real visto de costado.
        genera la linea poligonal del borde superior escalonado
        y los rectangulos de cada escalon como relleno.
        cada escalon es un rectangulo:
          - huella horizontal
          - contrahuella vertical
        sobre la cara superior de la losa inclinada
        """
        h   = self.huella
        ch  = self.contrahuella
        n   = self.n_escalones
        ag  = self.angulo
        e   = self.e_losa
        dx  = -math.sin(ag) * e
        dy  =  math.cos(ag) * e
        escalones = []
        for i in range(n):
            # esquina inferior-izquierda del escalon (en la cara superior de la losa)
            # la cara superior de la losa sube con la misma pendiente
            # en el punto i: x_base = x + dx + i*h, y_base = y + dy + i*ch
            xb = x + dx + i * h
            yb = y + dy + i * ch
            # el escalon se construye asi:
            # (xb, yb) -> (xb+h, yb) huella horizontal
            # (xb+h, yb) -> (xb+h, yb+ch) contrahuella vertical
            # (xb+h, yb+ch) -> (xb, yb+ch) techo huella (hacia atras, pero no existe, es el sig escalon)
            # para el relleno tomamos el triangulo/rectangulo entre
            # la cara de losa y el perfil escalonado

            # poligono del escalon (triangulo + contrahuella)
            # cara frontal del escalon:
            p_frontal_bot = [xb,     yb     ]   # punto sobre losa al inicio del escalon
            p_huella_der  = [xb + h, yb + ch]   # punto sobre losa al final del escalon
            p_tope_der    = [xb + h, yb + ch]   # mismo punto (tope de la huella a la derecha)
            p_tope_izq    = [xb,     yb + ch]   # tope frontal del escalon

            # el escalon como poligono de relleno:
            # el area encima de la cara superior de la losa hasta el perfil escalonado
            escalon_poly = [
                    [xb,     yb     ],   # inicio base del escalon (cara losa)
                    [xb + h, yb + ch],   # fin base del escalon (cara losa)
                    [xb + h, yb + ch],   # tope derecho (== fin base, la huella esta al nivel sig)
                    [xb,     yb + ch],   # tope izquierdo (contrahuella)
                    ]
            # nota: el triangulo de relleno correcto es:
            # de (xb, yb) a (xb+h, yb) [huella horizontal, nivel del tope del escalon]
            # a (xb+h, yb+ch) [borde derecho]
            # a (xb, yb) [cierre]
            # pero la huella debe ser horizontal
            # correccion: la huella va desde el tope frontal al tope trasero a la misma altura
            escalon_correcto = [
                    [xb,     yb     ],       # base frontal (sobre cara losa)
                    [xb + h, yb + ch],       # base trasera (sobre cara losa, siguiente nivel)
                    [xb + h, yb + ch],       # tope trasero (mismo punto, ch vertical ya incluido)
                    [xb,     yb + ch],       # tope frontal
                    ]
            # la forma correcta del peldano en perfil:
            # triangulo: (xb, yb), (xb+h, yb+ch), (xb, yb+ch)
            # es decir: el triangulo entre el punto de la losa, el siguiente punto de la losa,
            # y el tope vertical
            # mas la contrahuella cuadrada
            # simplificado como trapecio:
            trapecio = [
                    [xb,     yb     ],
                    [xb + h, yb + ch],
                    [xb + h, yb + ch + 0],   # el siguiente escalon empieza aqui
                    [xb,     yb + ch],
                    ]
            escalones.append(trapecio)
        return escalones

    def _get_perfil_escalonado(self, x=0, y=0):
        """
        linea poligonal del perfil visible de los escalones
        (el borde superior en el corte longitudinal)
        """
        h   = self.huella
        ch  = self.contrahuella
        n   = self.n_escalones
        ag  = self.angulo
        e   = self.e_losa
        dx  = -math.sin(ag) * e
        dy  =  math.cos(ag) * e
        puntos = []
        # punto inicial: tope del primer escalon (arranca en el apoyo inferior)
        puntos.append([x + dx, y + dy + ch])   # tope primer escalon

        for i in range(n):
            xb   = x + dx + i * h
            yb   = y + dy + i * ch
            # huella horizontal (nivel yb+ch)
            puntos.append([xb,     yb + ch])
            puntos.append([xb + h, yb + ch])
        return puntos

    def _get_acero_long(self, x=0, y=0):
        """
        barras longitudinales paralelas al intrados de la losa.
        se distribuyen perpendicularmente entre intrados y cara superior.
        """
        L   = self.L_horiz
        H   = self.H_total
        e   = self.e_losa
        r   = self.recub
        n   = self.n_barras_long
        d   = self.diam_long
        ag  = self.angulo
        # vector perpendicular unitario (hacia arriba desde intrados)
        udx = -math.sin(ag)
        udy =  math.cos(ag)
        # espesor util entre recubrimientos
        e_util = e - 2 * r
        barras = []
        for i in range(n):
            # posicion perpendicular desde el intrados
            t   = r + d/2 + i * (e_util - d) / (n - 1) if n > 1 else e / 2
            # punto inicio y fin de la barra (paralela a la losa)
            # margen en los extremos: recub
            xi  = x    + udx * t
            yi  = y    + udy * t
            xf  = x + L + udx * t
            yf  = y + H + udy * t
            barras.append([[xi, yi], [xf, yf]])
        return barras

    def _get_acero_dist(self, x=0, y=0):
        """
        barras de distribucion paralelas al intrados (secundarias).
        se representan como lineas punteadas entre las longitudinales.
        """
        L   = self.L_horiz
        H   = self.H_total
        e   = self.e_losa
        r   = self.recub
        n   = self.n_barras_dist
        d   = self.diam_dist
        ag  = self.angulo
        udx = -math.sin(ag)
        udy =  math.cos(ag)
        e_util = e - 2 * r
        barras = []
        for i in range(n):
            t   = r + d/2 + i * (e_util - d) / (n - 1) if n > 1 else e / 2
            xi  = x    + udx * t
            yi  = y    + udy * t
            xf  = x + L + udx * t
            yf  = y + H + udy * t
            barras.append([[xi, yi], [xf, yf]])
        return barras

    def _get_apoyos(self, x=0, y=0):
        """
        rectangulos de apoyo inferior y superior (vigas o muros).
        """
        L   = self.L_horiz
        H   = self.H_total
        a   = self.ancho_apoyo
        e   = self.e_losa
        ag  = self.angulo
        dx  = -math.sin(ag) * e
        dy  =  math.cos(ag) * e
        # apoyo inferior: debajo del inicio de la losa
        ap_inf = [
                [x - a, y - a],
                [x,     y - a],
                [x,     y    ],
                [x - a, y    ],
                ]
        # apoyo superior: al final de la losa
        ap_sup = [
                [x + L,     y + H     ],
                [x + L + a, y + H     ],
                [x + L + a, y + H + a ],
                [x + L,     y + H + a ],
                ]
        return [ap_inf, ap_sup]

    def _get_dim_points(self, x=0, y=0):
        h  = self.huella
        ch = self.contrahuella
        L  = self.L_horiz
        H  = self.H_total
        e  = self.e_losa
        ag = self.angulo
        dx = -math.sin(ag) * e
        dy =  math.cos(ag) * e
        return [
                # largo horizontal total
                [[x    , y      ], [x + L , y      ]],
                # altura total
                [[x + L, y      ], [x + L , y + H  ]],
                # una huella
                [[x    , y - 3  ], [x + h , y - 3  ]],
                # una contrahuella
                [[x + L + 3, y  ], [x + L + 3, y + ch]],
                # espesor losa
                [[x    , y      ], [x + dx, y + dy  ]],
                ]

    def _get_text(self):
        n   = self.n_escalones
        h   = self.huella
        ch  = self.contrahuella
        L   = self.L_horiz
        H   = self.H_total
        e   = self.e_losa
        ae  = self.ancho_esc
        r   = self.recub
        nl  = self.n_barras_long
        nd  = self.n_barras_dist
        dl  = self.diam_long
        dd  = self.diam_dist
        a   = self.ancho_apoyo
        ag  = math.degrees(self.angulo)
        # relacion huella/contrahuella (Blondel: 2ch + h = 60~64 cm)
        blondel = 2 * ch + h
        # areas de acero
        as_long = round(nl * math.pi * dl**2 / 4, 3)
        as_dist = round(nd * math.pi * dd**2 / 4, 3)
        return (f"Escalera de concreto\n"
                f"N escalones = {n}\n"
                f"Huella      = {h} cm\n"
                f"Contrahuella= {ch} cm\n"
                f"Blondel: 2ch+h = {blondel} cm\n\n"
                f"L horiz = {L} cm\n"
                f"H total = {H} cm\n"
                f"Angulo  = {ag:.1f} grados\n"
                f"Ancho   = {ae} cm\n"
                f"e losa  = {e} cm\n"
                f"Apoyo   = {a} cm\n\n"
                f"Long: {nl}d{dl} As={as_long} cm2\n"
                f"Dist: {nd}d{dd} As={as_dist} cm2")

    def draw(self, x=None, y=None, char=5, border=False):
        """dibuja el corte longitudinal de la escalera"""
        self.move_to(x, y)
        x   = self.x
        y   = self.y

        doc = self.doc
        msp = doc.modelspace()

        true_x = x + 8  * char
        true_y = y + 48 * char

        marco_x = self.L_horiz + self.ancho_apoyo * 2 + 20 * char
        marco_y = self.H_total + self.ancho_apoyo     + 70 * char

        centro_x  = x + marco_x / 2
        centro_y  = y + marco_y / 2
        leyenda_x = x + char * 20
        leyenda_y = y + char * 50

        marco = [
                [x           , y           ],
                [x + marco_x , y           ],
                [x + marco_x , y + marco_y ],
                [x           , y + marco_y ],
                ]

        # origen de la escalera dentro del marco
        ox = true_x + self.ancho_apoyo
        oy = true_y + self.ancho_apoyo

        losa       = self._get_losa            (ox, oy)
        escalones  = self._get_escalones_perfil(ox, oy)
        perfil     = self._get_perfil_escalonado(ox, oy)
        ac_long    = self._get_acero_long      (ox, oy)
        ac_dist    = self._get_acero_dist      (ox, oy)
        apoyos     = self._get_apoyos          (ox, oy)
        coord_dim  = self._get_dim_points      (ox, oy)

        if border:  # verde
            msp.add_lwpolyline(marco, close=True, dxfattribs={'color': 3})

        # losa escalera
        msp.add_lwpolyline(losa, close=True,dxfattribs={'lineweight': 30})

        # hatch escalones (gris un poco mas claro)
        for esc in escalones:
            msp.add_lwpolyline(esc, close=True,dxfattribs={ 'lineweight': 20})

        # acero longitudinal (azul)
        for b in ac_long:
            msp.add_line(start=b[0], end=b[1],
                         dxfattribs={'color': 5, 'lineweight': 50})

        # acero de distribucion (rojo, punteado)
        for b in ac_dist:
            msp.add_line(start=b[0], end=b[1],
                         dxfattribs={'color': 1, 'lineweight': 30,
                                     'linetype': 'DASHED'})
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
        ox, oy = self.ancho_apoyo, self.ancho_apoyo
        msp.add_lwpolyline(self._get_losa(ox, oy), close=True)
        for e in self._get_escalones_perfil(ox, oy):
            msp.add_lwpolyline(e, close=True)
        msp.add_lwpolyline(self._get_perfil_escalonado(ox, oy), close=False)
        for b in self._get_acero_long(ox, oy):
            msp.add_line(start=b[0], end=b[1])
        for b in self._get_acero_dist(ox, oy):
            msp.add_line(start=b[0], end=b[1])
        for ap in self._get_apoyos(ox, oy):
            msp.add_lwpolyline(ap, close=True)
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
        self.config(n_escalones=8,  huella=25, contrahuella=19, e_losa=12)
        self.draw(char=2, border=True)
        self.config(n_escalones=10, huella=28, contrahuella=18, e_losa=15)
        self.draw(char=2, border=True)
        self.config(n_escalones=12, huella=30, contrahuella=17, e_losa=18)
        self.draw(char=2, border=True)
        self.get_doc().saveas("test.dxf")
        print("test 3 ok")

if __name__ == '__main__':
    obj = Corte_escalera()
    obj._test_1()
    obj._test_2()
    obj._test_3()