# Actividad 1 — Leer los dos archivos y unirlos

## El encargo

Eres el analista de datos de TecnoAndina. Te mandan dos archivos por correo y
te piden un tablero de ventas. No hay documentación ni a quién preguntarle.

- `datos/ventas.xlsx`
- `datos/clientes.csv`

---

## Qué tienes que hacer

Un script que:

1. Lea el Excel en un DataFrame.
2. Lea el CSV en un DataFrame.
3. Una los dos en una sola tabla.
4. Imprima el número de filas de cada uno y del resultado.

---

## Preguntas (respóndelas como comentarios dentro del script)

1. ¿Cuántas filas y columnas tiene cada archivo?
2. ¿Qué pasa si haces `pd.read_csv("datos/clientes.csv")` sin nada más?
   ¿Por qué?
3. ¿Cuál es el separador real del CSV? ¿Cómo te diste cuenta?
4. ¿Por qué columna se unen las dos tablas?
5. ¿Qué tipo de unión usaste (`inner`, `left`, `right`) y por qué?
6. ¿Cuántas filas tenía `ventas` antes de unir y cuántas quedaron después?
7. Si el número cambió, **¿por qué cambió?**

---

## Pistas

<details>
<summary>Pista 1 — el CSV no se lee bien</summary>

Ábrelo con el bloc de notas y mira qué carácter separa los campos.
`pd.read_csv` tiene un parámetro `sep`.
</details>

<details>
<summary>Pista 2 — la unión cambió el número de filas</summary>

Compara en el archivo de clientes:

```python
print(len(clientes))
print(clientes["id_cliente"].nunique())
```

Si esos dos números no son iguales, ya sabes qué pasa.
</details>

---

## Importante

**No arregles nada.** Si ves fechas raras, precios con `$` o ciudades escritas
de cinco formas, déjalas así. Eso es la Capa 2.
