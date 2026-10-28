# Actividad 2A — Encontrar los errores

> Aquí **no se corrige nada**. Solo se busca.
> Primero se diagnostica, después se cura.

---

## Punto de partida

El archivo `datos/ventas_clientes.csv` que creó la Capa 1.

---

## Qué tienes que entregar

Una tabla con una fila por error:

| # | Columna | Qué está mal | Cómo lo encontraste | Cuántas filas |
|---|---|---|---|---|

**Hay 10 errores.** Encuentra los que puedas.

---

## Preguntas que ayudan a buscar

1. ¿Hay filas repetidas?
2. ¿Qué columnas tienen vacíos y cuántos?
3. ¿Cuántas categorías de producto debería haber? ¿Cuántas ve pandas?
4. ¿Y ciudades?
5. Mira `datos.dtypes`. ¿Alguna columna que debería ser número es texto?
   ¿Y alguna que debería ser fecha?
6. Imprime unos cuantos valores de `fecha`. ¿Están todos escritos igual?
7. ¿Cuál es la cantidad mínima vendida? ¿Tiene sentido?

---

## Comandos útiles

```python
datos.duplicated().sum()  # filas repetidas
datos.isna().sum()  # vacíos por columna
datos["categoria"].unique()  # valores distintos
datos.dtypes  # tipo de cada columna
datos["cantidad"].min()  # valor mínimo
```
