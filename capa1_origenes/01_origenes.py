import pandas as pd

# Lectura de las ventas
df_ventas = pd.read_excel("datos/ventas.xlsx")
# Lectura de los clientes
df_clientes = pd.read_csv("datos/clientes.csv", sep=";")

# Union de ventas y clientes
df_unido = df_ventas.merge(df_clientes, how="left", on="id_cliente")
