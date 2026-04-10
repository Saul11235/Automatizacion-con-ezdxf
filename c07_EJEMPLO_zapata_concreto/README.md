# Zapata aislada de concreto armado

Dibuja la **zapata aislada** de concreto armado en dos vistas dentro de un mismo archivo DXF.

## Archivos

| Archivo | Descripcion |
|---|---|
| `Perfil_zapata.py` | Vista lateral: zapata + columna + acero inferior + estribos |
| `Planta_zapata.py` | Vista desde arriba: contorno, columna centrada, barras en X y en Y |
| `EJEMPLO_zapata.py` | Script que combina ambas vistas y genera tres variantes de tamaño |

## Como usarlo

```python
from Perfil_zapata import Perfil_zapata
from Planta_zapata  import Planta_zapata
import ezdxf

doc = ezdxf.new()
perfil = Perfil_zapata()
planta = Planta_zapata()
perfil.set_doc(doc)
planta.set_doc(doc)

perfil.config(largo_z=120, alto_z=40, largo_col=30)
perfil.draw(char=3)

planta.config(largo_z=120, ancho_z=120, largo_col=30)
planta.move_to(y=250)
planta.draw(char=3)

doc.saveas("zapata.dxf")
```

## Parametros principales

- `largo_z / ancho_z` — dimensiones de la zapata en cm
- `largo_col / ancho_col` — dimensiones de la columna en cm
- `alto_z` — espesor de la zapata en cm
- `recub` — recubrimiento libre en cm
- `n_barras_x / n_barras_y` — numero de barras en cada direccion
- `diam_barra` — diametro de la barra principal (1/2" = 1.27 cm)
