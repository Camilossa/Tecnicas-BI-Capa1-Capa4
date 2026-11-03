import pandas as pd

# Lectura de las ventas
df_ventas = pd.read_excel("datos/ventas.xlsx")
# Lectura de los clientes
df_clientes = pd.read_csv("datos/clientes.csv", sep=";")

# Union de ventas y clientes
# ? Las dos tablas tienen "ciudad": los sufijos dicen de donde viene cada una
df_unido = df_ventas.merge(
    df_clientes, how="left", on="id_cliente", suffixes=("_venta", "_cliente")
)

# ? index=False evita la columna "Unnamed: 0", que esconde las filas repetidas
df_unido.to_csv("datos/ventas_clientes.csv", index=False)
