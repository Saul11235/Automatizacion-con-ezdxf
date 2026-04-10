# Escalera de concreto armado

Dibuja una **escalera de losa inclinada** de concreto armado en dos vistas: planta (vista desde arriba) y corte longitudinal.

## Archivos

| Archivo | Descripcion |
|---|---|
| `Planta_escalera.py` | Vista superior: contorno, lineas de huellas, acero long. y transversal |
| `Corte_escalera.py` | Corte lateral: losa inclinada, peldanos, acero, apoyos |
| `EJEMPLO_escalera.py` | Script que genera tres variantes segun la regla de Blondel |

## Concepto clave: regla de Blondel

La geometria del escalon debe cumplir:

```
60 cm  ≤  2 × contrahuella + huella  ≤  64 cm
```

El ejemplo genera tres combinaciones validas: (h=25, ch=19), (h=28, ch=18), (h=30, ch=17).

## Geometria de la losa inclinada

El angulo de inclinacion se calcula como `atan2(n×ch, n×huella)`. El vector perpendicular a la losa posiciona el acero siempre paralelo al intrados, sin importar el angulo.

## Parametros principales

- `n_escalones` — numero de escalones
- `huella` — ancho del escalon en cm
- `contrahuella` — altura del escalon en cm
- `ancho_esc` — ancho de la escalera en cm
- `e_losa` — espesor de la losa inclinada en cm
