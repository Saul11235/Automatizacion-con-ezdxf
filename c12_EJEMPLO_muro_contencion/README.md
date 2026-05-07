# Muro de contencion 

Dibuja un **muro de contencion** en tres vistas: perfil lateral, planta y corte transversal.

[![Video en YouTube](https://img.youtube.com/vi/eFKOfsQrrSw/0.jpg)](https://www.youtube.com/watch?v=eFKOfsQrrSw)

## Archivos

| Archivo | Descripcion |
|---|---|
| `Perfil_muro.py` | Corte lateral: zapata (puntera+talon), pantalla trapezoidal, acero |
| `Planta_muro.py` | Vista desde arriba: zapata corrida, franja de pantalla, barras |
| `Corte_muro.py` | Vista de frente al muro: pantalla completa, estribos, empuje del suelo |
| `EJEMPLO_muro.py` | Script con tres variantes de altura de muro |

## Concepto clave: el corte transversal

Al ver el muro **de frente**, la pantalla aparece como un rectangulo ancho (`largo_muro × alto_m`). El suelo empuja **toda** esa cara posterior. Las barras verticales son el acero principal que trabaja contra ese empuje.

## Geometria de la zapata

```
largo_z = puntera + e_base (pantalla) + talon
```

La puntera va al frente (lado libre) y el talon al fondo (lado del suelo retenido).

## Parametros principales

- `largo_muro` — longitud total del muro en cm
- `largo_z` — largo de la zapata (puntera + pantalla + talon) en cm
- `puntera` — longitud de la puntera en cm
- `alto_m` — altura libre de la pantalla en cm
- `e_base / e_corona` — espesor de la pantalla en base y corona en cm
