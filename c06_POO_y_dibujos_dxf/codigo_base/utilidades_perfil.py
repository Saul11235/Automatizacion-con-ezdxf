# Esta clase abstraera un perfil en forma de I
# con ezdxf

import ezdxf

class utilidades_perfil:
    """
    UTILIDADES PERFIL - por Edwin Saul
    ==================================

    esta clase leera un documento en ezdxf y buscara 
    los contenidos de forma especifica

   """ 
    # ------------------------------------------------------

    def __init__(self):
        # constructor del objeto
        self.doc = ezdxf.new()
        print("> objeto creado")

    # ------------------------------------------------------

    def set_doc(self,doc:ezdxf.new) -> None:
        # configurar atributo doc, debe ser 
        self.doc =doc

    def get_doc(self):
        # devuelve atributo doc
        return self.doc

    def load(self,namefile=""):
        # lee un archivo dxf
        self.doc = ezdxf.readfile(namefile)

    # ------------------------------------------------------

    def get_mtxt(self):
        '''
        metodo que devuelve el texto dentro 
        de los objetos mtxt identificados
        '''
        response = []
        msp = self.doc.modelspace()
        for obj in msp.query("MTEXT"):
            response.append(obj.text)
        return response

    # ------------------------------------------------------

    def get_hatch(self):
        '''
        metodo que devuelve todos los objetos hatch
        identificados dentro del archivo dxf
        '''
        response = []
        msp = self.doc.modelspace()
        for obj in msp.query("HATCH"):
            response.append(obj)
        return response

    # ------------------------------------------------------


if __name__ == '__main__':
    obj = utilidades_perfil()
    obj.load("test.dxf")
    print(obj.get_mtxt())
    print(obj.get_hatch())


