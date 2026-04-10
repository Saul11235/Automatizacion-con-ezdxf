# Codigo Demostrativo, no usar en produccion sin revisar

import ezdxf
import math

class Planta_zapata:
    """
    PLANTA ZAPATA - vista en planta de zapata aislada
    =================================================

    esta clase abstraera la vista desde arriba de una zapata
    aislada de concreto armado dibujada con ezdxf.

    La vista en planta muestra:
    - contorno de la zapata
    - contorno de la columna (centrada)
    - barras en direccion X (lineas horizontales)
    - barras en direccion Y (lineas verticales)

    atributos de entrada:

    largo_z      = 120  (default)  largo de la zapata en cm  (direccion X)
    ancho_z      = 120  (default)  ancho de la zapata en cm  (direccion Y)
    largo_col    = 30   (default)  largo de la columna en cm (direccion X)
    ancho_col    = 30   (default)  ancho de la columna en cm (direccion Y)
    recub        = 7.5  (default)  recubrimiento en cm
    n_barras_x   = 6    (default)  numero de barras en direccion X
    n_barras_y   = 6    (default)  numero de barras en direccion Y
    diam_barra   = 1.27 (default)  diametro de barra en cm  (1/2" = 1.27)

    Metodos
      __init__(args)  -> crea obj
      config (args)   -> configura args
      set_doc()       -> configura objeto doc ezdxf
      get_doc()       -> devuelve objeto doc ezdxf
      move(x,y)       -> mueve el pto de referencia (relativo)
      move_to(x,y)    -> cambia el punto de referencia (absoluto)
      get_pos()       -> devuelve posicion actual
      draw(x,y,char)  -> dibuja en el obj doc, en un pto x,y
                         y actualiza el pto de referencia

    Nota: tambien hay metodos internos de prueba
          _test_1, _test_2, _test_3
    """

    def __init__(self, largo_z=120, ancho_z=120,
                 largo_col=30, ancho_col=30,
                 recub=7.5, n_barras_x=6, n_barras_y=6,
                 diam_barra=1.27):
        self.config(largo_z, ancho_z, largo_col, ancho_col,
                    recub, n_barras_x, n_barras_y, diam_barra)
        self.doc = ezdxf.new()
        self.x = self.y = 0
        print("> objeto creado, Planta_zapata")

    def config(self, largo_z=120, ancho_z=120,
               largo_col=30, ancho_col=30,
               recub=7.5, n_barras_x=6, n_barras_y=6,
               diam_barra=1.27):
        self.largo_z    = abs(largo_z)
        self.ancho_z    = abs(ancho_z)
        self.largo_col  = abs(largo_col)
        self.ancho_col  = abs(ancho_col)
        self.recub      = abs(recub)
        self.n_barras_x = max(2, int(n_barras_x))
        self.n_barras_y = max(2, int(n_barras_y))
        self.diam_barra = abs(diam_barra)
        if self.largo_col > self.largo_z * 0.8: self.largo_col = self.largo_z * 0.4
        if self.ancho_col > self.ancho_z * 0.8: self.ancho_col = self.ancho_z * 0.4

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
        # rectangulo exterior de la zapata
        lz = self.largo_z
        az = self.ancho_z
        return [
                [x      , y      ],
                [x + lz , y      ],
                [x + lz , y + az ],
                [x      , y + az ],
                ]

    def _get_contorno_columna(self, x=0, y=0):
        # rectangulo de la columna centrado en la zapata
        lz  = self.largo_z
        az  = self.ancho_z
        lc  = self.largo_col
        ac  = self.ancho_col
        xc  = x + (lz - lc) / 2
        yc  = y + (az - ac) / 2
        return [
                [xc      , yc      ],
                [xc + lc , yc      ],
                [xc + lc , yc + ac ],
                [xc      , yc + ac ],
                ]

    def _get_barras_x(self, x=0, y=0):
        # barras en direccion X (lineas horizontales en planta)
        lz  = self.largo_z
        az  = self.ancho_z
        r   = self.recub
        n   = self.n_barras_x
        d   = self.diam_barra
        # distribucion uniforme en ancho util (Y)
        y_ini = y + r + d / 2
        y_fin = y + az - r - d / 2
        if n == 1:
            ys = [y + az / 2]
        else:
            paso = (y_fin - y_ini) / (n - 1)
            ys   = [y_ini + i * paso for i in range(n)]
        barras = []
        for yb in ys:
            barras.append([[x + r, yb], [x + lz - r, yb]])
        return barras

    def _get_barras_y(self, x=0, y=0):
        # barras en direccion Y (lineas verticales en planta)
        lz  = self.largo_z
        az  = self.ancho_z
        r   = self.recub
        n   = self.n_barras_y
        d   = self.diam_barra
        # distribucion uniforme en largo util (X)
        x_ini = x + r + d / 2
        x_fin = x + lz - r - d / 2
        if n == 1:
            xs = [x + lz / 2]
        else:
            paso = (x_fin - x_ini) / (n - 1)
            xs   = [x_ini + i * paso for i in range(n)]
        barras = []
        for xb in xs:
            barras.append([[xb, y + r], [xb, y + az - r]])
        return barras

    def _get_dim_points(self, x=0, y=0):
        # coordenadas para cotas
        lz  = self.largo_z
        az  = self.ancho_z
        lc  = self.largo_col
        ac  = self.ancho_col
        r   = self.recub
        xc  = x + (lz - lc) / 2
        yc  = y + (az - ac) / 2
        return [
                # largo zapata (X)
                [[x    , y + az ], [x + lz, y + az ]],
                # ancho zapata (Y)
                [[x    , y      ], [x     , y + az ]],
                # largo columna (X)
                [[xc   , y + az + 5], [xc + lc, y + az + 5]],
                # ancho columna (Y)
                [[x - 5, yc    ], [x - 5  , yc + ac]],
                # recubrimiento X
                [[x    , y + az / 2], [x + r, y + az / 2]],
                ]

    def _get_text(self):
        # texto con datos de la planta
        lz      = self.largo_z
        az      = self.ancho_z
        lc      = self.largo_col
        ac      = self.ancho_col
        r       = self.recub
        n_x     = self.n_barras_x
        n_y     = self.n_barras_y
        d       = self.diam_barra
        as_x    = round(n_x * math.pi * d**2 / 4, 2)
        as_y    = round(n_y * math.pi * d**2 / 4, 2)
        sep_x   = round((lz - 2*r) / (n_x - 1), 1) if n_x > 1 else lz
        sep_y   = round((az - 2*r) / (n_y - 1), 1) if n_y > 1 else az
        return (f"Planta = {lz}x{az} cm\n"
                f"Columna = {lc}x{ac} cm\n"
                f"Recub = {r} cm\n\n"
                f"Dir X: {n_x} barras d={d} cm\n"
                f"  sep = {sep_x} cm  As={as_x} cm2\n"
                f"Dir Y: {n_y} barras d={d} cm\n"
                f"  sep = {sep_y} cm  As={as_y} cm2")

    def draw(self, x=None, y=None, char=4, border=False):
        """
        dibuja la planta de la zapata en el modelspace
        """
        self.move_to(x, y)
        x   = self.x
        y   = self.y

        doc = self.doc
        msp = doc.modelspace()

        true_x = x + 8 * char
        true_y = y + 16 * char

        marco_x = self.largo_z + 12 * char
        marco_y = self.ancho_z + 24 * char

        centro_x  = x + marco_x / 2
        centro_y  = y + marco_y / 2
        leyenda_x = x + char * 10
        leyenda_y = y + char * 12

        marco = [
                [x           , y           ],
                [x + marco_x , y           ],
                [x + marco_x , y + marco_y ],
                [x           , y + marco_y ],
                ]

        cnt_zapata = self._get_contorno_zapata  (true_x, true_y)
        cnt_col    = self._get_contorno_columna (true_x, true_y)
        barras_x   = self._get_barras_x         (true_x, true_y)
        barras_y   = self._get_barras_y         (true_x, true_y)
        coord_dim  = self._get_dim_points       (true_x, true_y)

        if border:
            msp.add_lwpolyline(
                    marco,
                    close      = True,
                    dxfattribs = {'color': 3},   # rojo
                    )

        # barras en X (horizontales) - color rojo
        for barra in barras_x:
            msp.add_line(
                    start      = barra[0],
                    end        = barra[1],
                    dxfattribs = {'color': 1, 'lineweight': 40},
                    )

        # barras en Y (verticales) - color azul
        for barra in barras_y:
            msp.add_line(
                    start      = barra[0],
                    end        = barra[1],
                    dxfattribs = {'color': 5, 'lineweight': 40},
                    )

        for segmento in coord_dim:
            msp.add_aligned_dim(
                    p1       = segmento[0],
                    p2       = segmento[1],
                    distance = char*3,
                    text     = "<> cm"
                    )

        # contorno zapata
        msp.add_lwpolyline(
                cnt_zapata,
                close      = True,
                dxfattribs = {'color': 7, 'lineweight': 30},
                )

        # contorno columna
        msp.add_lwpolyline(
                cnt_col,
                close      = True,
                dxfattribs = {'color': 7, 'lineweight': 50},
                )

        msp.add_mtext(
                self._get_text(),
                dxfattribs={
                    "style"              : "iso",
                    "insert"             : (leyenda_x, leyenda_y),
                    "char_height"        : char,
                    "color"              : 8,        # gris
                    "width"              : marco_x,
                    "line_spacing_factor": 0.75,
                    },
                )

        doc.header['$DIMASZ']  = char
        doc.header['$DIMTXT']  = char 
        doc.header['$DIMCLRT'] = 8    # gris
        doc.header['$DIMCLRD'] = 8    # gris
        doc.header['$DIMCLRE'] = 8    # gris

        vports = doc.viewports.get('*ACTIVE')
        if vports: vport = vports[0] if isinstance(vports, list) else vports
        else     : vport = doc.viewports.new('*ACTIVE')
        vport.dxf.center = (centro_x / 2 + 0.5767 * marco_y - 0.06826,
                            centro_y / 2 + 0.25901 * marco_y - 0.021)
        vport.dxf.target = 0, 0, 0
        vport.dxf.height = marco_y * 1.05

        self.move(marco_x, marco_y)
        self.get_pos()

    def _test_1(self):
        # test simple: geometria sin draw()
        doc = ezdxf.new()
        msp = doc.modelspace()
        msp.add_lwpolyline(self._get_contorno_zapata(),  close=True)
        msp.add_lwpolyline(self._get_contorno_columna(), close=True)
        for b in self._get_barras_x():
            msp.add_line(start=b[0], end=b[1])
        for b in self._get_barras_y():
            msp.add_line(start=b[0], end=b[1])
        msp.add_mtext("\n" + self._get_text())
        for seg in self._get_dim_points():
            msp.add_aligned_dim(p1=seg[0], p2=seg[1], distance=3)
        doc.saveas("test.dxf")
        print("test 1 ok")

    def _test_2(self):
        # test de uso del metodo draw
        doc = ezdxf.new()
        self.set_doc(doc)
        self.draw(x=0, y=0, char=3, border=True)
        doc.saveas("test.dxf")
        print("test 2 ok")

    def _test_3(self):
        # test de varias instancias, variando dimensiones y barras
        self.config(largo_z=100, ancho_z=100, largo_col=25, ancho_col=25, n_barras_x=5, n_barras_y=5)
        self.draw(char=2, border=True)
        self.config(largo_z=130, ancho_z=130, largo_col=30, ancho_col=30, n_barras_x=7, n_barras_y=7)
        self.draw(char=2, border=True)
        self.config(largo_z=160, ancho_z=120, largo_col=35, ancho_col=30, n_barras_x=8, n_barras_y=6)
        self.draw(border=True)
        self.draw()  # test off
        self.get_doc().saveas("test.dxf")
        print("test 3 ok")

if __name__ == '__main__':
    obj = Planta_zapata()
    obj._test_1()   # test 1
    obj._test_2()   # test 2
    obj._test_3()   # test 3