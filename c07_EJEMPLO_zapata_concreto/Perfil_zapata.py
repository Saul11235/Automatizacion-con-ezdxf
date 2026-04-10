# Codigo Demostrativo, no usar en produccion sin revisar
import ezdxf, math

class Perfil_zapata:
    """
    Vista lateral (perfil) de una zapata aislada de concreto armado.

    Parametros:
      largo_z      = 120   largo de la zapata en cm
      ancho_z      = 120   ancho de la zapata en cm (solo para leyenda)
      alto_z       = 40    alto de la zapata en cm
      largo_col    = 30    largo de la columna en cm
      ancho_col    = 30    ancho de la columna en cm
      alto_col     = 60    alto de columna visible en cm
      recub        = 7.5   recubrimiento en cm
      n_barras_x   = 6     barras en direccion X
      n_barras_y   = 6     barras en direccion Y
      diam_barra   = 1.27  diametro de barra en cm  (1/2" = 1.27)
      diam_estribo = 0.95  diametro estribo columna  (3/8" = 0.95)
    """

    def __init__(self, largo_z=120, ancho_z=120, alto_z=40,
                 largo_col=30, ancho_col=30, alto_col=60,
                 recub=7.5, n_barras_x=6, n_barras_y=6,
                 diam_barra=1.27, diam_estribo=0.95):
        self.config(largo_z, ancho_z, alto_z, largo_col, ancho_col,
                    alto_col, recub, n_barras_x, n_barras_y,
                    diam_barra, diam_estribo)
        self.doc = ezdxf.new()
        self.x = self.y = 0
        print("> objeto creado, Perfil_zapata")

    def config(self, largo_z=120, ancho_z=120, alto_z=40,
               largo_col=30, ancho_col=30, alto_col=60,
               recub=7.5, n_barras_x=6, n_barras_y=6,
               diam_barra=1.27, diam_estribo=0.95):
        self.largo_z      = abs(largo_z)
        self.ancho_z      = abs(ancho_z)
        self.alto_z       = abs(alto_z)
        self.largo_col    = abs(largo_col)
        self.ancho_col    = abs(ancho_col)
        self.alto_col     = abs(alto_col)
        self.recub        = abs(recub)
        self.n_barras_x   = max(2, int(n_barras_x))
        self.n_barras_y   = max(2, int(n_barras_y))
        self.diam_barra   = abs(diam_barra)
        self.diam_estribo = abs(diam_estribo)
        if self.largo_col > self.largo_z: self.largo_col = self.largo_z * 0.5
        if self.ancho_col > self.ancho_z: self.ancho_col = self.ancho_z * 0.5
        if self.recub > self.alto_z / 2:  self.recub = self.alto_z / 3

    def set_doc(self, doc): self.doc = doc
    def get_doc(self):      return self.doc
    def get_pos(self):      return [self.x, self.y]

    def move(self, x=0, y=0):
        self.x += x
        self.y += y

    def move_to(self, x=None, y=None):
        self.x = x if x is not None else self.x
        self.y = y if y is not None else self.y

    # --- geometria interna ---

    def _get_zapata(self, x=0, y=0):
        lz, az = self.largo_z, self.alto_z
        return [[x, y], [x+lz, y], [x+lz, y+az], [x, y+az]]

    def _get_columna(self, x=0, y=0):
        lz, az = self.largo_z, self.alto_z
        lc, ac = self.largo_col, self.alto_col
        xc = x + (lz - lc) / 2
        yc = y + az
        return [[xc, yc], [xc+lc, yc], [xc+lc, yc+ac], [xc, yc+ac]]

    def _get_barras_inf(self, x=0, y=0):
        r, d, n = self.recub, self.diam_barra, self.n_barras_x
        yc = y + r + d / 2
        return [[[x+r, yc + i*(d+0.3)], [x+self.largo_z-r, yc + i*(d+0.3)]]
                for i in range(n)]

    def _get_estribos_col(self, x=0, y=0):
        lz, az = self.largo_z, self.alto_z
        lc, ac = self.largo_col, self.alto_col
        de     = self.diam_estribo
        xc, yc = x + (lz-lc)/2, y + az
        sep    = lc * 0.4
        estribos, pos = [], xc + de
        while pos < xc + lc - de:
            estribos.append([[pos, yc+de], [pos, yc+ac-de]])
            pos += sep
        return estribos

    def _get_dim_points(self, x=0, y=0):
        lz, az, ac = self.largo_z, self.alto_z, self.alto_col
        lc, r      = self.largo_col, self.recub
        xc         = x + (lz - lc) / 2
        return [
            [[x,  y      ], [x+lz, y           ]],   # largo zapata
            [[x,  y      ], [x,    y+az         ]],   # alto zapata
            [[xc, y+az   ], [xc,   y+az+ac      ]],   # alto columna
            [[xc, y+az+ac+5], [xc+lc, y+az+ac+5]],   # ancho columna
            [[x,  y+r    ], [x+r,  y+r          ]],   # recubrimiento
        ]

    def _get_text(self):
        d  = self.diam_barra
        nx, ny = self.n_barras_x, self.n_barras_y
        as_x   = round(nx * math.pi * d**2 / 4, 2)
        as_y   = round(ny * math.pi * d**2 / 4, 2)
        return (f"Zapata = {self.largo_z}x{self.ancho_z}x{self.alto_z} cm\n"
                f"Columna = {self.largo_col}x{self.ancho_col} cm\n"
                f"Recub = {self.recub} cm\n\n"
                f"Barras X: {nx} d={d} cm  As={as_x} cm2\n"
                f"Barras Y: {ny} d={d} cm  As={as_y} cm2\n\n"
                f"As total = {round(as_x+as_y,2)} cm2\n"
                f"Estribo col d={self.diam_estribo} cm")

    # --- dibujo principal ---

    def draw(self, x=None, y=None, char=6, border=False):
        """Dibuja el perfil de la zapata en el modelspace del doc activo."""
        self.move_to(x, y)
        x, y   = self.x, self.y
        doc    = self.doc
        msp    = doc.modelspace()
        true_x = x + 6 * char
        true_y = y + 22 * char
        marco_x = self.largo_z + 13 * char
        marco_y = self.alto_z + self.alto_col + 30 * char
        centro_x, centro_y = x + marco_x/2, y + marco_y/2
        leyenda_x, leyenda_y = x + char*8, y + char*17

        marco = [[x, y], [x+marco_x, y], [x+marco_x, y+marco_y], [x, y+marco_y]]

        if border:
            msp.add_lwpolyline(marco, close=True, dxfattribs={'color': 3})

        msp.add_lwpolyline(self._get_zapata(true_x, true_y),
                           close=True, dxfattribs={'lineweight': 30})
        msp.add_lwpolyline(self._get_columna(true_x, true_y),
                           close=True, dxfattribs={'lineweight': 30})

        for b in self._get_barras_inf(true_x, true_y):
            msp.add_line(start=b[0], end=b[1], dxfattribs={'color': 1, 'lineweight': 50})

        for e in self._get_estribos_col(true_x, true_y):
            msp.add_line(start=e[0], end=e[1], dxfattribs={'color': 5, 'lineweight': 25})

        msp.add_mtext(self._get_text(), dxfattribs={
            "style": "iso", "insert": (leyenda_x, leyenda_y),
            "char_height": char, "color": 8, "width": marco_x,
            "line_spacing_factor": 0.75})

        for seg in self._get_dim_points(true_x, true_y):
            msp.add_aligned_dim(p1=seg[0], p2=seg[1], distance=char, text="<> cm")

        doc.header['$DIMASZ'] = doc.header['$DIMTXT'] = char
        doc.header['$DIMCLRT'] = doc.header['$DIMCLRD'] = doc.header['$DIMCLRE'] = 8

        vports = doc.viewports.get('*ACTIVE')
        vport  = (vports[0] if isinstance(vports, list) else vports) if vports else doc.viewports.new('*ACTIVE')
        vport.dxf.center = (centro_x/2 + 0.5767*marco_y - 0.068, centro_y/2 + 0.259*marco_y - 0.021)
        vport.dxf.target = (0, 0, 0)
        vport.dxf.height = marco_y * 1.05

        self.move(marco_x, marco_y)


if __name__ == '__main__':
    # prueba rapida: tres zapatas en el mismo DXF
    obj = Perfil_zapata()
    for lado in [100, 130, 160]:
        obj.config(largo_z=lado, ancho_z=lado, alto_z=35, largo_col=25, ancho_col=25)
        obj.draw(char=3, border=True)
    obj.get_doc().saveas("test.dxf")
    print("test ok -> test.dxf")
