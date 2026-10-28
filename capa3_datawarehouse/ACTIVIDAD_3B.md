# Actividad 3B — Conectarse a Postgres y cargar los datos

> Esta actividad tiene truco: **no se le va a explicar cómo se hace antes**.
> Tiene que buscar la documentación.

---

## Parte 1 — Investigación

Busca y responde con tus palabras, **citando la página donde lo encontraste**:

1. ¿Qué es `psycopg2` y para qué sirve?
2. ¿Qué es `SQLAlchemy`? ¿Reemplaza a `psycopg2` o trabaja con él?
3. ¿Qué es una **cadena de conexión**? Escribe cómo se arma para Postgres y
   explica cada parte.
4. En pandas, ¿qué hace `DataFrame.to_sql()`? Busca qué significan
   estos parámetros:
   - `if_exists` (y sus tres valores posibles)
   - `index`
5. ¿Qué diferencia hay entre `if_exists="replace"` y `if_exists="append"`?
6. ¿Qué es una **llave foránea** (*foreign key*) en una base de datos?
7. ¿Por qué es mala idea escribir la contraseña de la base dentro del `.py`?

**Fuentes:** documentación oficial de pandas, de SQLAlchemy y de PostgreSQL.

---

## Parte 2 — Hacerlo

Escribe un script que:

1. Se conecte a Postgres.
2. Cree las 4 tablas del modelo OLAP:
   `dim_cliente`, `dim_producto`, `dim_tiempo`, `hecho_ventas`.
3. Cargue los CSV de `datos/olap/`.
4. Imprima cuántas filas quedaron en cada tabla, **consultando la base**
   (no contando el CSV).

### Antes de empezar

Crea la base una sola vez, en pgAdmin o en la terminal:

```sql
CREATE DATABASE tecnoandina;
```

### Reglas

- Las tablas se crean con `CREATE TABLE` escrito por ti, no dejando que
  pandas las invente.
- `hecho_ventas` debe tener **llaves foráneas** hacia las tres dimensiones.
- El script debe poder correrse **dos veces seguidas** sin fallar ni duplicar
  datos.

---

## Parte 3 — Verificación

Escribe estas consultas SQL y anota el resultado:

1. ¿Cuántas filas tiene cada tabla?
2. `SELECT SUM(total) FROM hecho_ventas;` — ¿cuánto da?
3. Venta por categoría, uniendo `hecho_ventas` con `dim_producto`.
4. Venta por mes, uniendo `hecho_ventas` con `dim_tiempo`.

### Prueba de fuego

Intenta insertar a mano una venta de un producto que no existe:

```sql
INSERT INTO hecho_ventas VALUES
  ('V-9999', '2024-05-10', 'C-001', 'P-999', 1, 1000, 1000);
```

- ¿Qué pasó? Copia el mensaje completo.
- ¿Por qué es **bueno** que haya pasado eso?
- ¿Qué habría pasado si los datos estuvieran en un Excel compartido?

