# Actividad 3A — Dibujar los modelos OLTP y OLAP

> Sin computador. Papel y lápiz.
> Un modelo se piensa antes de programarse.

---

## Punto de partida

El archivo `datos/ventas_limpio.csv`: **una sola tabla** con estas columnas.

```
id_venta · fecha · id_cliente · id_producto · producto · categoria
cantidad · precio_unitario · ciudad_venta
nombre · ciudad_cliente · segmento · total
```

Todo está repetido en cada fila: si un cliente compró 9 veces, su nombre
aparece 9 veces.

---

## Parte 1 — Modelo OLTP

El OLTP es el modelo que usa el sistema de ventas para **operar**.
La regla: **cada dato vive en un solo lugar**.

Dibuja las tablas. Para cada una escribe:
- el nombre,
- sus columnas,
- cuál es la llave primaria (subráyala),
- flechas hacia las tablas con las que se relaciona.

### Responde en el papel

1. ¿Cuántas tablas te salieron?
2. En tu modelo, ¿cuántas veces aparece el nombre de un cliente?
3. Si el cliente se cambia el nombre, ¿cuántas filas hay que actualizar
   en tu modelo? ¿Y en la tabla original de una sola tabla?
4. La columna `total`, ¿la guardas o la calculas cada vez? Argumenta.

### Pista

Mira qué columnas describen al **cliente**, cuáles al **producto** y cuáles a
la **venta**. Ahí están tus tablas.

---

## Parte 2 — Modelo OLAP en estrella

El OLAP es el modelo que usa Power BI para **analizar**.

```
           dim_tiempo
               |
dim_cliente ---+--- hecho_ventas ---+--- dim_producto
```

En el centro va el **hecho** (los números). Alrededor, las **dimensiones**
(los textos con los que se filtra).

Dibújalo. Marca cuál tabla es el hecho y cuáles las dimensiones.

### Responde en el papel

1. ¿Qué representa **una fila** de tu tabla de hechos?
   Escríbelo como una frase que empiece con "una fila es…".
   *(Es la pregunta más importante de toda la actividad.)*
2. ¿Qué columnas quedaron en el hecho y cuáles en las dimensiones?
   ¿Cuál es el criterio?
3. ¿`categoria` es una tabla aparte o una columna de `dim_producto`?
   Justifica.
4. ¿De dónde sale `dim_tiempo`? ¿Está en el CSV?
   ¿Cuántas filas debería tener?

---

## Parte 3 — Comparación

1. Para responder *"venta por categoría y por segmento de cliente"*,
   ¿cuántas uniones necesita cada modelo?
2. ¿En cuál es más fácil registrar una venta nueva?
3. ¿En cuál es más fácil responderle al gerente?
4. Si tuvieras que quedarte con uno solo, ¿cuál?
