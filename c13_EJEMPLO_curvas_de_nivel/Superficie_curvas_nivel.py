# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
import numpy  as np
from   scipy.interpolate import griddata
import matplotlib
matplotlib.use('Agg')          # backend sin pantalla
import matplotlib.pyplot as plt
import matplotlib.contour as mcontour
import math

class Superficie_curvas_nivel:
    """
    SUPERFICIE CURVAS DE NIVEL
    ==========================

    Recibe una nube de puntos (x, y, z) y genera un dibujo DXF con:
      - curvas de nivel interpoladas (LWPOLYLINE por nivel)
      - etiquetas de cota en cada curva
      - puntos originales como circulos con su cota
      - curvas de nivel maestras (cada n curvas) mas gruesas
      - leyenda con rango Z, equidistancia y metodo de interpolacion
      - cotas minima y maxima marcadas

    La interpolacion usa scipy.griddata con metodo configurable
    (cubic recomendado para superficies suaves, linear para datos
    con cambios bruscos).

    Parametros:
      puntos       = []       lista de [x, y, z] o array Nx3
      equidistancia= None     intervalo entre curvas (auto si None)
      n_curvas     = 10       numero de curvas (usado si equidistancia=None)
      metodo_interp= 'cubic'  metodo scipy: 'cubic', 'linear', 'nearest'
      resolucion   = 200      puntos de la grilla de interpolacion (NxN)
      n_maestra    = 5        cada cuantas curvas va una curva maestra
      escala       = 1.0      factor de escala para coordenadas XY
      mostrar_puntos= True    dibujar los puntos originales
      dec_cotas    = 2        decimales en las etiquetas de cota

    Metodos estandar:
      __init__(args)  -> crea obj
      config (args)   -> configura args
      set_doc()       -> configura objeto doc ezdxf
      get_doc()       -> devuelve objeto doc ezdxf
      move(x,y)       -> mueve el pto de referencia (relativo)
      move_to(x,y)    -> cambia el punto de referencia (absoluto)
      get_pos()       -> devuelve posicion actual
      draw(x,y)       -> procesa e interpola, dibuja en doc

    Tests: _test_1, _test_2, _test_3
    """

    def __init__(self, puntos=None,
                 equidistancia=None, n_curvas=10,
                 metodo_interp='cubic', resolucion=200,
                 n_maestra=5, escala=1.0,
                 mostrar_puntos=True, dec_cotas=2):
        self.config(puntos, equidistancia, n_curvas,
                    metodo_interp, resolucion,
                    n_maestra, escala, mostrar_puntos, dec_cotas)
        self.doc = ezdxf.new()
        self.x = self.y = 0
        print("> objeto creado, Superficie_curvas_nivel")

    def config(self, puntos=None,
               equidistancia=None, n_curvas=10,
               metodo_interp='cubic', resolucion=200,
               n_maestra=5, escala=1.0,
               mostrar_puntos=True, dec_cotas=2):
        # puntos: lista de [x,y,z] o array Nx3
        if puntos is not None and len(puntos) > 0:
            pts = np.array(puntos, dtype=float)
            if pts.ndim == 1:
                pts = pts.reshape(1, 3)
            self.pts = pts
        else:
            self.pts = None
        self.equidistancia  = equidistancia
        self.n_curvas       = max(2, int(n_curvas))
        self.metodo_interp  = metodo_interp
        self.resolucion     = max(50, int(resolucion))
        self.n_maestra      = max(1, int(n_maestra))
        self.escala         = abs(escala) if escala != 0 else 1.0
        self.mostrar_puntos = bool(mostrar_puntos)
        self.dec_cotas      = max(0, int(dec_cotas))

    def set_puntos(self, puntos):
        """permite cargar los puntos despues de crear el objeto"""
        pts = np.array(puntos, dtype=float)
        if pts.ndim == 1:
            pts = pts.reshape(1, 3)
        self.pts = pts

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

    def _validar_puntos(self):
        if self.pts is None or len(self.pts) < 4:
            raise ValueError("Se necesitan al menos 4 puntos para interpolar.")
        if self.pts.shape[1] != 3:
            raise ValueError("Cada punto debe tener exactamente 3 coordenadas [x, y, z].")

    def _interpolar(self):
        """
        Interpola la nube de puntos en una grilla regular.
        Devuelve: xi, yi (grilla), zi (valores interpolados)
        """
        pts  = self.pts
        xs   = pts[:, 0] * self.escala
        ys   = pts[:, 1] * self.escala
        zs   = pts[:, 2]

        x_min, x_max = xs.min(), xs.max()
        y_min, y_max = ys.min(), ys.max()

        # pequeno margen para evitar bordes vacios
        mx = (x_max - x_min) * 0.05
        my = (y_max - y_min) * 0.05

        xi = np.linspace(x_min - mx, x_max + mx, self.resolucion)
        yi = np.linspace(y_min - my, y_max + my, self.resolucion)
        XI, YI = np.meshgrid(xi, yi)

        # interpolacion
        zi = griddata((xs, ys), zs, (XI, YI), method=self.metodo_interp)

        # rellenar NaN en bordes con metodo nearest
        mascara_nan = np.isnan(zi)
        if mascara_nan.any():
            zi_near = griddata((xs, ys), zs, (XI, YI), method='nearest')
            zi[mascara_nan] = zi_near[mascara_nan]

        return xi, yi, zi

    def _calcular_niveles(self, zi):
        """
        Calcula los niveles de las curvas de nivel.
        Si se define equidistancia, la usa. Si no, genera n_curvas niveles.
        """
        z_min = float(np.nanmin(zi))
        z_max = float(np.nanmax(zi))

        if self.equidistancia is not None:
            eq = abs(self.equidistancia)
            nivel_ini = math.ceil (z_min / eq) * eq
            nivel_fin = math.floor(z_max / eq) * eq
            niveles   = np.arange(nivel_ini, nivel_fin + eq * 0.001, eq)
            niveles   = niveles[(niveles >= z_min) & (niveles <= z_max)]
        else:
            niveles = np.linspace(z_min, z_max, self.n_curvas + 2)[1:-1]

        return niveles, z_min, z_max

    def _extraer_curvas(self, xi, yi, zi, niveles):
        """
        Usa matplotlib.contour para extraer las polylineas de cada nivel.
        Usa cs.allsegs: lista de listas de arrays, una entrada por nivel.
        Devuelve lista de dicts: {z, segmentos: [[(x,y),...], ...]}
        """
        fig, ax = plt.subplots()
        cs = ax.contour(xi, yi, zi, levels=niveles)
        plt.close(fig)

        curvas = []
        for nivel, segs_nivel in zip(cs.levels, cs.allsegs):
            segs = []
            for seg in segs_nivel:
                arr = np.array(seg)
                if arr.ndim == 2 and len(arr) >= 2:
                    segs.append(arr.tolist())
            curvas.append({'z': float(nivel), 'segmentos': segs})

        return curvas

    def _crear_capas(self, doc):
        """
        Crea las capas en el documento DXF.
        """
        capas = {
            'CURVAS_NIVEL'    : {'color': 3},    # verde
            'CURVAS_MAESTRAS' : {'color': 2},    # amarillo, mas gruesas
            'COTAS_CURVAS'    : {'color': 3},    # verde
            'PUNTOS_ORIG'     : {'color': 1},    # rojo
            'COTAS_PUNTOS'    : {'color': 1},    # rojo
            'LEYENDA'         : {'color': 7},    # blanco/negro
            'BORDE'           : {'color': 8},    # gris
        }
        for nombre, props in capas.items():
            if nombre not in doc.layers:
                doc.layers.new(nombre, dxfattribs={'color': props['color']})

    def _dibujar_curvas(self, msp, curvas, niveles, ox, oy, char, z_min, z_max):
        """
        Dibuja las curvas de nivel en el modelspace.
        Cada nivel es una o mas LWPOLYLINE.
        Cada N curvas se dibuja como curva maestra (mas gruesa).
        Se coloca una etiqueta de cota en un punto representativo.
        """
        fmt    = f"{{:.{self.dec_cotas}f}}"
        n_m    = self.n_maestra
        eq_z   = (z_max - z_min)

        for idx, curva in enumerate(curvas):
            z        = curva['z']
            segs     = curva['segmentos']
            maestra  = (idx % n_m == 0)
            capa     = 'CURVAS_MAESTRAS' if maestra else 'CURVAS_NIVEL'
            lw       = 40 if maestra else 18

            # color degradado por altura: azul (bajo) -> verde -> rojo (alto)
            # en DXF usamos colores del indice: 5=azul, 3=verde, 1=rojo
            if eq_z > 0:
                t = (z - z_min) / eq_z
            else:
                t = 0.5
            if   t < 0.33: color = 5    # azul
            elif t < 0.66: color = 3    # verde
            else         : color = 1    # rojo

            etiqueta_puesta = False

            for seg in segs:
                if len(seg) < 2:
                    continue

                # trasladar al origen del dibujo
                pts_dxf = [(ox + p[0], oy + p[1]) for p in seg]

                msp.add_lwpolyline(
                    pts_dxf,
                    close      = False,
                    dxfattribs = {
                        'layer'     : capa,
                        'color'     : color,
                        'lineweight': lw,
                    }
                )

                # colocar etiqueta una vez por nivel, en el segmento mas largo
                if not etiqueta_puesta and maestra:
                    # punto medio del segmento mas largo
                    mejor_seg  = max(segs, key=lambda s: len(s))
                    mid        = len(mejor_seg) // 2
                    px         = ox + mejor_seg[mid][0]
                    py         = oy + mejor_seg[mid][1]
                    texto      = fmt.format(z)
                    msp.add_mtext(
                        texto,
                        dxfattribs={
                            'layer'      : 'COTAS_CURVAS',
                            'insert'     : (px, py),
                            'char_height': char * 0.8,
                            'color'      : color,
                            'width'      : char * 6,
                            'style'      : 'iso',
                        }
                    )
                    etiqueta_puesta = True

            # para curvas no maestras, etiquetar cada 2 niveles en segmento largo
            if not maestra and idx % 2 == 0 and segs:
                mejor_seg = max(segs, key=lambda s: len(s))
                if len(mejor_seg) >= 2:
                    mid  = len(mejor_seg) // 3
                    px   = ox + mejor_seg[mid][0]
                    py   = oy + mejor_seg[mid][1]
                    msp.add_mtext(
                        fmt.format(z),
                        dxfattribs={
                            'layer'      : 'COTAS_CURVAS',
                            'insert'     : (px, py),
                            'char_height': char * 0.5,
                            'color'      : color,
                            'width'      : char * 4,
                            'style'      : 'iso',
                        }
                    )

    def _dibujar_puntos(self, msp, ox, oy, char, z_min, z_max):
        """
        Dibuja los puntos originales como circulos con su cota.
        """
        fmt  = f"{{:.{self.dec_cotas}f}}"
        eq_z = z_max - z_min if z_max != z_min else 1
        r    = char * 0.4

        for pt in self.pts:
            px = ox + pt[0] * self.escala
            py = oy + pt[1] * self.escala
            pz = pt[2]

            # color segun altura
            t = (pz - z_min) / eq_z
            if   t < 0.33: color = 5
            elif t < 0.66: color = 3
            else         : color = 1

            # circulo
            msp.add_circle(
                center=(px, py),
                radius=r,
                dxfattribs={'layer': 'PUNTOS_ORIG', 'color': color}
            )

            # cota del punto
            msp.add_mtext(
                fmt.format(pz),
                dxfattribs={
                    'layer'      : 'COTAS_PUNTOS',
                    'insert'     : (px + r * 1.5, py + r * 0.5),
                    'char_height': char * 0.6,
                    'color'      : color,
                    'width'      : char * 5,
                    'style'      : 'iso',
                }
            )

    def _dibujar_borde(self, msp, xi, yi, ox, oy):
        """Borde del area de la grilla interpolada"""
        x0 = ox + xi.min()
        x1 = ox + xi.max()
        y0 = oy + yi.min()
        y1 = oy + yi.max()
        msp.add_lwpolyline(
            [(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
            close      = True,
            dxfattribs = {'layer': 'BORDE', 'color': 8, 'lineweight': 25}
        )

    def _dibujar_leyenda(self, msp, ox, oy, xi, yi,
                         niveles, z_min, z_max, char):
        """
        Leyenda con informacion del mapa de curvas de nivel.
        Se coloca a la derecha del borde.
        """
        fmt  = f"{{:.{self.dec_cotas}f}}"
        xL   = ox + xi.max() + char * 2
        yL   = oy + yi.max()

        if self.equidistancia is not None:
            eq_txt = f"{self.equidistancia}"
        else:
            if len(niveles) > 1:
                eq_txt = f"~{round(niveles[1]-niveles[0], self.dec_cotas)}"
            else:
                eq_txt = "N/A"

        n_pts = len(self.pts)
        texto = (f"CURVAS DE NIVEL\n"
                 f"---------------\n"
                 f"Z max = {fmt.format(z_max)}\n"
                 f"Z min = {fmt.format(z_min)}\n"
                 f"Rango = {fmt.format(z_max - z_min)}\n"
                 f"Equidist = {eq_txt}\n"
                 f"N curvas  = {len(niveles)}\n"
                 f"Maestras c/{self.n_maestra}\n"
                 f"Metodo = {self.metodo_interp}\n"
                 f"N puntos = {n_pts}\n"
                 f"Resol = {self.resolucion}x{self.resolucion}")

        msp.add_mtext(
            texto,
            dxfattribs={
                'layer'              : 'LEYENDA',
                'insert'             : (xL, yL-char*10),
                'char_height'        : char * 0.9,
                'color'              : 7,
                'width'              : char * 12,
                'line_spacing_factor': 0.8,
                'style'              : 'iso',
            }
        )

        # escala de colores: azul -> verde -> rojo
        dy = char * 1.5
        for i, (label, color) in enumerate([
                ('Zona alta (Z max)', 1),
                ('Zona media'       , 3),
                ('Zona baja (Z min)', 5),
        ]):
            y_item = yL - char * 2 - i * dy
            msp.add_line(
                start=[xL,          y_item],
                end  =[xL + char*2, y_item],
                dxfattribs={'layer': 'LEYENDA', 'color': color, 'lineweight': 40}
            )
            msp.add_mtext(
                label,
                dxfattribs={
                    'layer'      : 'LEYENDA',
                    'insert'     : (xL + char*2.5, y_item - char*0.3),
                    'char_height': char * 0.7,
                    'color'      : color,
                    'width'      : char * 10,
                    'style'      : 'iso',
                }
            )

    def _marcar_extremos(self, msp, ox, oy, char, z_min, z_max):
        """Marca el punto de Z minima y Z maxima en el mapa"""
        fmt = f"{{:.{self.dec_cotas}f}}"
        for extremo, color, label in [
                (z_min, 5, 'MIN'),
                (z_max, 1, 'MAX'),
        ]:
            idx = np.argmin(np.abs(self.pts[:, 2] - extremo))
            px  = ox + self.pts[idx, 0] * self.escala
            py  = oy + self.pts[idx, 1] * self.escala
            r   = char * 0.8
            # circulo grande
            msp.add_circle(
                center=(px, py), radius=r,
                dxfattribs={'layer': 'PUNTOS_ORIG', 'color': color, 'lineweight': 50}
            )
            # texto
            msp.add_mtext(
                f"{label}={fmt.format(extremo)}",
                dxfattribs={
                    'layer'      : 'COTAS_PUNTOS',
                    'insert'     : (px + r * 1.5, py + r),
                    'char_height': char,
                    'color'      : color,
                    'width'      : char * 8,
                    'style'      : 'iso',
                }
            )

    def _ajustar_vista(self, doc, ox, oy, xi, yi):
        """Centra la vista en el area del mapa"""
        cx = ox + (xi.min() + xi.max()) / 2
        cy = oy + (yi.min() + yi.max()) / 2
        alto = yi.max() - yi.min()
        vports = doc.viewports.get('*ACTIVE')
        if vports: vport = vports[0] if isinstance(vports, list) else vports
        else     : vport = doc.viewports.new('*ACTIVE')
        vport.dxf.center = (cx, cy)
        vport.dxf.target = (0, 0, 0)
        vport.dxf.height = alto * 1.2

    def draw(self, x=None, y=None, char=1):
        """
        Procesa la nube de puntos, interpola y dibuja el mapa
        de curvas de nivel en el documento ezdxf.

        x, y: punto de insercion del mapa
        char: tamano de referencia para textos y simbolos
        """
        self._validar_puntos()
        self.move_to(x, y)
        ox = self.x
        oy = self.y

        doc = self.doc
        msp = doc.modelspace()

        self._crear_capas(doc)

        print("> interpolando superficie...")
        xi, yi, zi = self._interpolar()

        print("> calculando niveles...")
        niveles, z_min, z_max = self._calcular_niveles(zi)
        print(f"  Z min={z_min:.3f}  Z max={z_max:.3f}  N niveles={len(niveles)}")

        print("> extrayendo curvas de nivel...")
        curvas = self._extraer_curvas(xi, yi, zi, niveles)

        print("> dibujando en DXF...")
        self._dibujar_borde  (msp, xi, yi, ox, oy)
        self._dibujar_curvas (msp, curvas, niveles, ox, oy, char, z_min, z_max)
        self._marcar_extremos(msp, ox, oy, char, z_min, z_max)

        if self.mostrar_puntos:
            self._dibujar_puntos(msp, ox, oy, char, z_min, z_max)

        self._dibujar_leyenda(msp, ox, oy, xi, yi,
                              niveles, z_min, z_max, char)
        self._ajustar_vista  (doc, ox, oy, xi, yi)

        # avanzar el punto de referencia
        ancho = xi.max() - xi.min()
        alto  = yi.max() - yi.min()
        self.move(ancho + char * 15, alto)
        self.get_pos()
        print("> dibujo completado")

    # DATOS DE PRUEBA

    @staticmethod
    def _generar_puntos_colina(n=40, seed=42):
        """Genera una colina gaussiana con ruido para pruebas"""
        rng = np.random.default_rng(seed)
        x   = rng.uniform(0, 100, n)
        y   = rng.uniform(0, 100, n)
        z   = (50 * np.exp(-((x-50)**2 + (y-50)**2) / 800)
               + rng.normal(0, 1, n))
        return np.column_stack([x, y, z]).tolist()

    @staticmethod
    def _generar_puntos_valle(n=50, seed=7):
        """Genera un valle entre dos lomas para pruebas"""
        rng = np.random.default_rng(seed)
        x   = rng.uniform(0, 200, n)
        y   = rng.uniform(0, 150, n)
        z   = (30 * np.exp(-((x-50)**2)  / 600) +
               25 * np.exp(-((x-150)**2) / 600) -
               10 * np.exp(-((y-75)**2)  / 1000) +
               rng.normal(0, 0.5, n))
        return np.column_stack([x, y, z]).tolist()

    @staticmethod
    def _generar_puntos_terreno(n=60, seed=13):
        """Genera terreno irregular con gradiente para pruebas"""
        rng = np.random.default_rng(seed)
        x   = rng.uniform(0, 300, n)
        y   = rng.uniform(0, 200, n)
        z   = (x * 0.1 + y * 0.05
               + 20 * np.sin(x / 40) * np.cos(y / 30)
               + rng.normal(0, 1.5, n))
        return np.column_stack([x, y, z]).tolist()

    # TESTS

    def _test_1(self):
        """test basico: colina gaussiana, equidistancia automatica"""
        pts = self._generar_puntos_colina(n=40)
        self.config(puntos=pts, n_curvas=10, metodo_interp='cubic',
                    mostrar_puntos=True, dec_cotas=2)
        self.draw(x=0, y=0, char=3)
        self.get_doc().saveas("test.dxf")
        print("test 1 ok -> test_curvas_1_colina.dxf")

    def _test_2(self):
        """test valle: equidistancia fija de 2 unidades"""
        pts = self._generar_puntos_valle(n=50)
        self.config(puntos=pts, equidistancia=2.0,
                    metodo_interp='cubic', n_maestra=5,
                    mostrar_puntos=True, dec_cotas=1)
        self.draw(x=0, y=0, char=3)
        self.get_doc().saveas("test.dxf")
        print("test 2 ok -> test_curvas_2_valle.dxf")

    def _test_3(self):
        """test terreno con gradiente, metodo linear"""
        pts = self._generar_puntos_terreno(n=60)
        self.config(puntos=pts, equidistancia=5.0,
                    metodo_interp='linear', n_maestra=4,
                    resolucion=150, mostrar_puntos=True, dec_cotas=1)
        self.draw(x=0, y=0, char=4)
        self.get_doc().saveas("test.dxf")
        print("test 3 ok -> test_curvas_3_terreno.dxf")

if __name__ == '__main__':
    obj = Superficie_curvas_nivel()
    obj._test_1()

    obj2 = Superficie_curvas_nivel()
    obj2._test_2()

    obj3 = Superficie_curvas_nivel()
    obj3._test_3()