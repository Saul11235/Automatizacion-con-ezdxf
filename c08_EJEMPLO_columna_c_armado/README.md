# Columna de concreto armado multi-piso

Dibuja una **columna rectangular** de concreto armado en dos representaciones: seccion transversal y desarrollo longitudinal completo (desde zapata hasta el ultimo nivel).

## Archivos

| Archivo | Descripcion |
|---|---|
| `Seccion_columna.py` | Seccion transversal: concreto, estribo, barras longitudinales, ganchos |
| `Corte_columna.py` | Desarrollo longitudinal: zapata, pisos, losas, zonas de confinamiento |
| `EJEMPLO_columna.py` | Script que genera tres variantes de columna en el mismo DXF |

## Concepto clave: zonas de confinamiento

El codigo calcula automaticamente segun **ACI 318 / NSR-10**:

| Parametro | Formula |
|---|---|
| Longitud confinada `Lc` | `max(h_col, h_piso/6, 50 cm)` |
| Separacion zona conf. | `min(b_col/4, 8·d_long, 10 cm)` |
| Separacion zona central | `min(b_col/2, 16·d_long, 30 cm)` |

## Parametros principales

- `b_col / h_col` — dimensiones de la seccion en cm
- `n_pisos` — numero de pisos de la columna
- `h_piso / h_losa` — alturas de piso y losa en cm
- `n_barras_x / n_barras_y` — barras por cara (incluyen esquinas)
- `diam_long` — diametro barra longitudinal (5/8" = 1.59 cm)
