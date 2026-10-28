#! Nunca modificamos los archivos originales: creamos uno nuevo.

import pandas as pd

datos = pd.read_csv("datos/ventas_clientes.csv")
print("Filas al empezar:", len(datos))

# -------------------------------------------------------------
# ERROR 1 y 8: filas repetidas
# -------------------------------------------------------------
# ? Se repitieron ventas en el Excel y clientes en el CSV.
# ? Las dos cosas se ven igual: filas identicas.
datos = datos.drop_duplicates()
print("1) Sin filas repetidas ->", len(datos))

# -------------------------------------------------------------
# ERROR 2: la fecha viene en dos formatos
# -------------------------------------------------------------
# ? Probamos un formato y despues el otro.
# ? Lo que no calce con ninguno queda vacio (errors="coerce").
formato_1 = pd.to_datetime(datos["fecha"], format="%Y-%m-%d", errors="coerce")
formato_2 = pd.to_datetime(datos["fecha"], format="%d/%m/%Y", errors="coerce")
datos["fecha"] = formato_1.fillna(formato_2)
print("2) Fechas convertidas. Sin fecha:", datos["fecha"].isna().sum())

# -------------------------------------------------------------
# ERROR 3: hay ventas sin fecha
# -------------------------------------------------------------
# ? Una venta sin fecha no se puede poner en el tablero: se quita.
datos = datos[datos["fecha"].notna()]
print("3) Sin ventas sin fecha ->", len(datos))

# -------------------------------------------------------------
# ERROR 4: el precio viene como texto con "$"
# -------------------------------------------------------------
# ? Quitamos el signo de peso y los puntos, y lo pasamos a numero.
datos["precio_unitario"] = (
    datos["precio_unitario"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.strip()
)
datos["precio_unitario"] = pd.to_numeric(datos["precio_unitario"])
print("4) Precio convertido a numero. Tipo:", datos["precio_unitario"].dtype)

# -------------------------------------------------------------
# ERROR 5: cantidades negativas o en cero
# -------------------------------------------------------------
datos = datos[datos["cantidad"] > 0]
print("5) Solo cantidades positivas ->", len(datos))

# -------------------------------------------------------------
# ERROR 6: la categoria escrita de varias formas
# -------------------------------------------------------------
# ? .strip() quita espacios, .title() deja Primera Letra En Mayuscula
datos["categoria"] = datos["categoria"].str.strip().str.title()
print("6) Categorias:", sorted(datos["categoria"].unique()))

# -------------------------------------------------------------
# ERROR 7: la ciudad de la venta viene vacia
# -------------------------------------------------------------
# ? No inventamos la ciudad: ponemos una etiqueta que deja ver el problema.
datos["ciudad_venta"] = datos["ciudad_venta"].fillna("Sin dato")
print("7) Ciudades de venta:", sorted(datos["ciudad_venta"].unique()))

# -------------------------------------------------------------
# ERROR 9: hay clientes sin segmento
# -------------------------------------------------------------
datos["segmento"] = datos["segmento"].fillna("Sin segmento")
print("9) Segmentos:", sorted(datos["segmento"].unique()))

# -------------------------------------------------------------
# ERROR 10: la ciudad del cliente escrita de varias formas
# -------------------------------------------------------------
datos["ciudad_cliente"] = datos["ciudad_cliente"].str.strip().str.title()
print("10) Ciudades de cliente:", sorted(datos["ciudad_cliente"].unique()))

# -------------------------------------------------------------
# Campo calculado
# -------------------------------------------------------------
# ? El total se calcula UNA vez aqui, para que todos usen el mismo numero.
datos["total"] = datos["cantidad"] * datos["precio_unitario"]

# -------------------------------------------------------------
# Guardar
# -------------------------------------------------------------
datos.to_csv("datos/ventas_limpio.csv", index=False)

print("\n-------------------------------------------")
print("Filas limpias:", len(datos))
print("Venta total  : $", format(datos["total"].sum(), ",.0f"))
print("Guardado en datos/ventas_limpio.csv")
print("\nPrimeras 5 filas:")
print(datos.head())
