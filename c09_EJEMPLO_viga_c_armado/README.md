# Viga de concreto armado

Dibuja una **viga continua** de concreto armado apoyada en multiples columnas, en dos representaciones: seccion transversal y desarrollo longitudinal con zonas de confinamiento.

[![Video en YouTube](https://img.youtube.com/vi/1oN2CoAcDDs/0.jpg)](https://www.youtube.com/watch?v=1oN2CoAcDDs)

## Archivos

| Archivo | Descripcion |
|---|---|
| `Seccion_viga.py` | Seccion transversal: concreto, estribo, barras inf. y sup. |
| `Corte_viga.py` | Desarrollo longitudinal: columnas, tramos, zonas conf., acero |
| `EJEMPLO_viga.py` | Script que genera tres variantes de viga en el mismo DXF |

## Concepto clave: zonas de confinamiento

Segun **ACI 318 / NSR-10**:

| Parametro | Formula |
|---|---|
| Longitud confinada `Lv` | `2 × h_viga` (desde cara de columna) |
| Separacion zona conf. | `min(h/4, 8d_long, 24d_est, 30 cm)` |
| Separacion zona central | `min(h/2, d_long, 30 cm)` |

El acero **superior** es corrido (traccion en nudos). El acero **inferior** es por tramo con anclaje (traccion en vano).

## Parametros principales

- `b_viga / h_viga` — dimensiones de la seccion en cm
- `n_tramos` — numero de tramos de la viga
- `L_cc` — luz centro a centro entre columnas en cm
- `b_col` — ancho de la columna en cm
- `n_inf / n_sup` — barras inferiores y superiores
