# =============================================================
# CAPA 3 - PASO 6: modelo OLTP (normalizado)
# =============================================================
# ? OLTP = el modelo que usa el sistema de ventas para OPERAR.
# ? Se parte la tabla grande en varias tablas pequenas, sin repetir datos.
#
# Correr desde la carpeta del proyecto:
#   python capa3_datawarehouse/06_modelo_oltp.py

import pandas as pd
import os

datos = pd.read_csv("datos/ventas_limpio.csv")

os.makedirs("datos/oltp", exist_ok=True)

# -------------------------------------------------------------
# Tabla 1: CLIENTES
# -------------------------------------------------------------
# ? Un cliente aparece muchas veces en la tabla grande.
# ? Aqui lo dejamos UNA sola vez.
clientes = datos[["id_cliente", "nombre", "ciudad_cliente", "segmento"]]
clientes = clientes.drop_duplicates()

# -------------------------------------------------------------
# Tabla 2: PRODUCTOS
# -------------------------------------------------------------
productos = datos[["id_producto", "producto", "categoria"]]
productos = productos.drop_duplicates()

# -------------------------------------------------------------
# Tabla 3: VENTAS
# -------------------------------------------------------------
#! La tabla de ventas ya NO guarda el nombre del cliente ni del producto.
#! Solo guarda su codigo. Si el cliente cambia de nombre, se cambia
#! en UN solo lugar.
ventas = datos[
    [
        "id_venta",
        "fecha",
        "id_cliente",
        "id_producto",
        "cantidad",
        "precio_unitario",
        "total",
        "ciudad_venta",
    ]
]

# -------------------------------------------------------------
# Guardar
# -------------------------------------------------------------
clientes.to_csv("datos/oltp/clientes.csv", index=False)
productos.to_csv("datos/oltp/productos.csv", index=False)
ventas.to_csv("datos/oltp/ventas.csv", index=False)

print("Tabla clientes :", len(clientes), "filas")
print("Tabla productos:", len(productos), "filas")
print("Tabla ventas   :", len(ventas), "filas")

print("\nCLIENTES")
print(clientes.head(3))
print("\nPRODUCTOS")
print(productos.head(3))
print("\nVENTAS")
print(ventas.head(3))

# -------------------------------------------------------------
# Para responder una pregunta de negocio hay que volver a unir
# -------------------------------------------------------------
#! Aqui esta la desventaja del OLTP: 2 uniones para UNA pregunta.
respuesta = (
    ventas.merge(clientes, on="id_cliente")
    .merge(productos, on="id_producto")
    .groupby(["categoria", "segmento"])["total"]
    .sum()
)
print("\nVenta por categoria y segmento:")
print(respuesta)
