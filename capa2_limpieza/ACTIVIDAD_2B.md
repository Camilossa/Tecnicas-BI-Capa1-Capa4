# Actividad 2B — Corregir los errores

---

## Qué tienes que hacer

Un script que lea `datos/ventas_clientes.csv`, corrija los 10 errores y
guarde `ventas_limpio_<tus_apellidos>.csv`.

**No modifiques los archivos originales.**

---

## Los 10 errores a corregir

- [ ] 1. Filas repetidas
- [ ] 2. La fecha viene en dos formatos distintos
- [ ] 3. Hay ventas sin fecha
- [ ] 4. El precio viene como texto con `$` (ej: `$ 1.900.000`)
- [ ] 5. Hay cantidades negativas o en cero
- [ ] 6. La categoría está escrita de varias formas
- [ ] 7. Hay ventas sin ciudad
- [ ] 8. Hay clientes repetidos
- [ ] 9. Hay clientes sin segmento
- [ ] 10. La ciudad del cliente está escrita de varias formas

Al final, agrega una columna:

```python
datos["total"] = datos["cantidad"] * datos["precio_unitario"]
```

---

## Por cada corrección, un comentario así

```python
# ERROR: la categoría aparece como "Computo", "COMPUTO", "computo", " Computo "
# DECISIÓN: quitar espacios y dejar todo en formato Título
# FILAS AFECTADAS: 420
datos["categoria"] = datos["categoria"].str.strip().str.title()
```

Las tres líneas. La de **decisión** es la que se evalúa.

---

## Las decisiones que hay que pensar

Estas no tienen una sola respuesta. Argumenta la tuya en el comentario.

**1. Ventas sin fecha.** ¿Se borran o se dejan? ¿Qué pasa con ellas en un
gráfico de ventas por mes?

**2. Cantidad negativa.** ¿Es basura o es una **devolución** mal registrada?
¿Cambiaría tu decisión si el negocio te dice que sí manejan devoluciones?

**3. Ciudad vacía.** ¿Se borra la venta, se pone `"Sin dato"` o se pone la
ciudad más común? ¿Cuál de las tres **esconde** el problema?

**4. Segmento vacío.** Mismo dilema. ¿Rellenar con `"Sin segmento"` o con el
segmento más frecuente?

---

## Al final, el script debe imprimir

```
Filas al empezar: 453
1) Sin filas repetidas -> 400
2) ...
Filas limpias: ...
Venta total: $ ...
```

Así, cuando alguien pregunte *"¿por qué el tablero muestra menos ventas que
mi Excel?"*, tienes la respuesta.

---

## Ayudas de pandas

```python
datos.drop_duplicates()                       # quitar repetidas
datos[datos["cantidad"] > 0]                  # filtrar filas
datos["col"].fillna("Sin dato")               # rellenar vacíos
datos["col"].str.strip().str.title()          # limpiar texto
datos["col"].str.replace("$", "", regex=False)# quitar un carácter
pd.to_numeric(datos["col"])                   # texto -> número
pd.to_datetime(datos["col"], format="%Y-%m-%d", errors="coerce")
```
