# ? Aqui NO corregimos nada. Solo miramos que esta mal.
# ? Primero se diagnostica, despues se cura.

import pandas as pd

datos = pd.read_csv("datos/ventas_clientes.csv")

print("Filas y columnas:", datos.shape)

print("Filas identicas:", datos.duplicated().sum())

print(datos.isna().sum())

print(sorted(datos["categoria"].unique()))

print(sorted(datos["ciudad_cliente"].dropna().unique()))

print(datos.dtypes)

print("\n6) EJEMPLOS DE PRECIO")

print(datos["precio_unitario"].unique()[:8])

print(datos["fecha"].dropna().unique()[:8])

print("Minimo:", datos["cantidad"].min(), " Maximo:", datos["cantidad"].max())
print("Cantidades menores o iguales a cero:", (datos["cantidad"] <= 0).sum())
