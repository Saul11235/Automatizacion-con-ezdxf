# Esta clase abstraera un perfil en forma de I
# con ezdxf

import ezdxf

class perfil_I:
    """
    PERFIL I - por Edwin Saul
    =========================

    esta clase abstraera un perfil dibujado con ezdxf
    el constructor tendra los siguientes atributos de entrada

    ancho = 20   (default)
    alto  = 30   (default)
    ala   = 5    (default)
    alma  = 8    (default)

    internamente se define un punto de referencia para
    insertar el dibujo en un objeto doc, de ezdxf.

    Metodos
      __init__(args)  -> crea obj,
      config (args)   -> configura arg
      set_doc()       -> configura objeto doc ezdxf
      get_doc()       -> devuelve objeto doc ezdxf
      move(x,y)       -> mueve el pto de referencia
      move_to(x,y)    -> cambia el punto de referencia 
      draw(x,y,char)  -> dibuja en el obj doc, en un pto x 
                         y actualiza el pto de referencia
                         pass

    Nota: tambien hay metodos internos de prueba
          _test_1 _test_2, _test_3
    """ 
    # ------------------------------------------------------

    def __init__(self,ancho=20,alto=30,ala=5,alma=8):
        # constructor del objeto
        self.config(ancho,alto,ala,alma)
        # objeto doc ezdxf
        self.doc = ezdxf.new()
        # punteros del archivo
        self.x   = 0
        self.y   = 0
        print("> objeto creado, perfil I")

    # ------------------------------------------------------

    def config(self,ancho=20,alto=30,ala=5,alma=8):
        # configura valores de 
        self.ancho = abs(ancho)
        self.alto  = abs(alto)
        self.ala   = abs(ala)
        self.alma  = abs(alma)
        if self.ala  > self.alto/2: self.ala  = self.alto/2
        if self.alma > self.ancho : self.alma = self.ancho

    # ------------------------------------------------------

    def set_doc(self,doc:ezdxf.new) -> None:
        # configurar atributo doc, debe ser 
        self.doc =doc

    def get_doc(self):
        # devuelve atributo doc
        return self.doc

    # ------------------------------------------------------

    def move(self,x=0,y=0):
        # mueve el punto de referencia
        self.x += x
        self.y += y

    def move_to(self, x= None, y= None):
        # mueve el punto de referencia a una pos especifica
        self.x = x if x is not None else self.x
        self.y = y if y is not None else self.y

    def get_pos(self):
        # devuelve posicion
        return [self.x,self.y]

    # ------------------------------------------------------

    def _get_poligono(self,x=0,y=0):
        # funcion interna que devuelve las coordenadas del poligono del perfil 
        ancho = self.ancho
        alto  = self.alto
        ala   = self.ala
        alma  = self.alma
        return [
                # Coord X               Coord Y
                [x                      , y          ],
                [x+ancho                , y          ],
                [x+ancho                , y+ala      ],
                [x+ancho-(ancho-alma)/2 , y+ala      ],
                [x+ancho-(ancho-alma)/2 , y+alto-ala ],
                [x+ancho                , y+alto-ala ],
                [x+ancho                , y+alto     ],
                [x                      , y+alto     ],
                [x                      , y+alto-ala ],
                [x+(ancho-alma)/2       , y+alto-ala ],
                [x+(ancho-alma)/2       , y+ala      ],
                [x                      , y+ala      ],
                ]

    # ------------------------------------------------------

    def _get_dim_points(self,x=0,y=0):
        # funcion que devuelve las coordenadas de los elementos de dimension
        ancho = self.ancho
        alto  = self.alto
        ala   = self.ala
        alma  = self.alma
        return [
                #   X1             Y1              X2               Y2
                [[x               ,y         ],[x               ,y+ala     ]],
                [[x               ,y+ala     ],[x               ,y+alto-ala]],
                [[x               ,y+alto-ala],[x               ,y+alto    ]],
                [[x               ,y+alto    ],[x+(ancho-alma)/2,y+alto    ]],
                [[x+(ancho-alma)/2,y+alto    ],[x+(ancho+alma)/2,y+alto    ]],
                [[x+(ancho+alma)/2,y+alto    ],[x+ancho         ,y+alto    ]],
                [[x+ancho         ,y+alto    ],[x+ancho         ,y         ]],
                [[x+ancho         ,y         ],[x               ,y         ]],
                ]
 
    # ------------------------------------------------------

    def _get_text(self):
        # funcion interna que devuelve texto con datos de poligono
        ancho     = self.ancho
        alto      = self.alto
        ala       = self.ala
        alma      = self.alma
        #------------------------
        Area      = ancho*ala*2+alma*(alto-2*ala)  
        Perimetro = 2*(ancho+alto) + 2*(ancho-alma)
        #------------------------
        return f"Area = {Area}\nPerim = {Perimetro}\n\nAncho = {ancho}\nAla = {ala}\nAlto = {alto}\nAlma = {alma}"

    # ------------------------------------------------------

    def draw(self,x=None,y=None,char=1,border=False):
        """
        funcion que dibuja el objeto en un modelspace
        """
        # moviendo pto ref
        self.move_to(x,y)
        x         = self.x
        y         = self.y

        # creando variable
        doc       = self.doc
        msp       = doc.modelspace()

        # verdaderos x y para figura 
        true_x    = x+3*char
        true_y    = y+11*char

        # dimension de marco de figura 
        marco_x   = self.ancho+6*char
        marco_y   = self.alto+13*char

        # punto central marco 
        centro_x  = x+marco_x/2
        centro_y  = y+marco_y/2

        # punto leyenda 
        leyenda_x = x+char*1
        leyenda_y = y+char*9

        # puntos de marco
        marco= [ 
                [x         ,y         ],
                [x+marco_x ,y         ],
                [x+marco_x ,y+marco_y ],
                [x         ,y+marco_y,  ],
                ]

        # datos
        poligono  = self._get_poligono  (true_x,true_y)
        coord_dim = self._get_dim_points(true_x,true_y)

        # Dibujando marco
        if border:
            msp.add_lwpolyline(
                 marco,
                 close      = True,
                 dxfattribs = {'color':1},
                            )

        # Dibujando poligono
        hatch = msp.add_hatch()
        hatch.paths.add_polyline_path(
                poligono,
                is_closed = True
                )
        hatch.set_solid_fill()
        hatch.dxf.color =4    # color cyan

        # colocando leyenda
        msp.add_mtext(
                self._get_text(),
                dxfattribs={
                    "style"              : "iso",
                    "insert"             : (leyenda_x,leyenda_y),
                    "char_height"        : char,
                    "color"              : 2,     # amarillo
                    "width"              : marco_y-char,
                    "line_spacing_factor": 0.75,        # interlineado
                    },
                )

        # colocando elementos dim
        for segmento in coord_dim:
            msp.add_aligned_dim(
                    p1       = segmento[0],
                    p2       = segmento[1],
                    distance = char,
                    text     = "<> mm"
                    )

        # estilos dimension
        doc.header['$DIMASZ']   = char/4
        doc.header['$DIMTXT']   = char/4
        doc.header['$DIMCLRT']  = 3   # verde
        doc.header['$DIMCLRD']  = 6   # magenta
        doc.header['$DIMCLRE']  = 2   # amarillo

        # ajustar vista
        vports   = doc.viewports.get('*ACTIVE')
        if vports: vport = vports[0] if isinstance(vports, list) else vports
        else     : vport = doc.viewports.new('*ACTIVE')
        vport.dxf.center =  ( centro_x/2 +0.5767*marco_y-0.06826, centro_y/2 +0.25901*marco_y-0.021 )
        vport.dxf.target =  0,0,0
        vport.dxf.height =  marco_y*1.05

        # moviendo pto referencia
        self.move(marco_x,marco_y)

        # devuelve coord del final 
        self.get_pos()


    # ------------------------------------------------------

    def _test_1(self):
        # test simple de uso de metodos
        doc = ezdxf.new()
        msp = doc.modelspace()
        #-----------
        msp.add_lwpolyline(self._get_poligono(), close=True)
        msp.add_mtext("\n"+self._get_text())
        for segmento in self._get_dim_points():
            msp.add_aligned_dim(p1 = segmento[0], p2 = segmento[1], distance=1)
        #-----------
        doc.saveas("test.dxf")
        print("test 1 ok")

    # ------------------------------------------------------
        
    def _test_2(self):
        # test de uso demetodo draw
        doc = ezdxf.new()
        self.set_doc(doc)
        self.draw(x=100,y=200,char=4,border=True)
        doc.saveas("test.dxf")
        print("test 2 ok")

    # ------------------------------------------------------

    def _test_3(self):
        # test de varias instancias de draw
        self.config(alto=30,ancho=30)
        self.draw(char=1, border= True)
        self.config(alto=30,ancho=40,ala=3)
        self.draw(char=3)
        self.config(alto=20,ancho=50,alma=2)
        self.draw(char=4, border=True)
        self.get_doc().saveas("test.dxf")
        print("test 3 ok")

    # ------------------------------------------------------


if __name__ == '__main__':
    obj = perfil_I()
#    obj._test_1()   # test 1
#    obj._test_2()   # test 2
    obj._test_3()   # test 3


