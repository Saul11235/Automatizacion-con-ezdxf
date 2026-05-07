# Losa aligerada

Dibuja una **losa aligerada** en dos vistas: planta (desde arriba) y corte transversal (perpendicular a las viguetas).

[![Video en YouTube](https://img.youtube.com/vi/bon8Zie461k/0.jpg)](https://www.youtube.com/watch?v=bon8Zie461k)

## Archivos

| Archivo | Descripcion |
|---|---|
| `Planta_losa.py` | Vista desde arriba: viguetas, bloques, acero long. y de temperatura |
| `Corte_losa.py` | Corte perpendicular: viguetas, bloques, capa de compresion, acero |
| `EJEMPLO_losa.py` | Script que genera tres variantes de bloque en el mismo DXF |

## Concepto clave: paso de viguetas

```
paso = b_vig + claro_bloque
```

Las viguetas se distribuyen uniformemente en el ancho de la losa. Los bloques (ladrillo hueco) llenan el espacio entre viguetas y se representan con linea punteada.

## Capas del sistema

1. **Capa de compresion** (`h_losa`): losa superior de concreto solido
2. **Viguetas** (`h_vig = h_total - h_losa`): nervios de concreto armado
3. **Bloques**: aligerantes entre viguetas (no estructurales)

## Parametros principales

- `largo_losa / ancho_losa` — dimensiones totales en cm
- `b_vig` — ancho de la vigueta en cm (tipico: 12-15 cm)
- `claro_bloque` — ancho libre entre viguetas en cm (tipico: 23-35 cm)
- `h_total / h_losa` — altura total y de la capa de compresion en cm
