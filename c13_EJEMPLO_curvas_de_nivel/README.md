# Mapa de curvas de nivel

Genera un **mapa de curvas de nivel** en DXF a partir de una nube de puntos `(x, y, z)`. Interpola la superficie y exporta cada curva como una polilínea nativa de DXF.

[![Video en YouTube](https://img.youtube.com/vi/I2OK0oglYKg/0.jpg)](https://www.youtube.com/watch?v=I2OK0oglYKg)

## Archivos

| Archivo | Descripcion |
|---|---|
| `Superficie_curvas_nivel.py` | Clase principal: interpolacion, extraccion de curvas, dibujo DXF |
| `EJEMPLO_curvas_nivel.py` | Script con tres ejemplos: colina, valle y terreno con gradiente |

## Pipeline interno

```
Puntos XYZ  →  scipy.griddata  →  Grilla regular  →  matplotlib.contour  →  LWPOLYLINE (ezdxf)
```

## Capas del DXF generado

| Capa | Contenido |
|---|---|
| `CURVAS_NIVEL` | Curvas normales (color segun altura) |
| `CURVAS_MAESTRAS` | Cada N curvas, mas gruesas y con etiqueta |
| `COTAS_CURVAS` | Etiquetas de cota en las curvas |
| `PUNTOS_ORIG` | Puntos originales como circulos |
| `COTAS_PUNTOS` | Cota de cada punto original |
| `LEYENDA` | Informacion del mapa |
| `BORDE` | Rectangulo del area interpolada |

## Uso minimo

```python
from Superficie_curvas_nivel import Superficie_curvas_nivel

pts = [[x1,y1,z1], [x2,y2,z2], ...]   # minimo 4 puntos
obj = Superficie_curvas_nivel()
obj.config(puntos=pts, equidistancia=1.0)
obj.draw(char=3)
obj.get_doc().saveas("mapa.dxf")
```

## Dependencias

```
pip install ezdxf numpy scipy matplotlib
```

## Parametros principales

- `puntos` — lista de `[x, y, z]` o array Nx3
- `equidistancia` — intervalo entre curvas (si es `None`, usa `n_curvas`)
- `n_curvas` — numero de curvas automaticas (default: 10)
- `metodo_interp` — `'cubic'` (suave) o `'linear'` (cambios bruscos)
- `n_maestra` — cada cuantas curvas va una curva maestra mas gruesa
