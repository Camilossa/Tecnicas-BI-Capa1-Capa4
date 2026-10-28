# =============================================================
# CAPA 3 - PASO 7: modelo OLAP (estrella)
# =============================================================
# ? OLAP = el modelo que usa Power BI para ANALIZAR.
# ?
# ?            dim_tiempo
# ?                |
# ?  dim_cliente --+-- hecho_ventas --+-- dim_producto
# ?
# ? En el centro va el HECHO (los numeros) y alrededor las
# ? DIMENSIONES (los textos con los que se filtra).
#
# Correr desde la carpeta del proyecto:
#   python capa3_datawarehouse/07_modelo_olap.py

import pandas as pd
import os

datos = pd.read_csv("datos/ventas_limpio.csv")
datos["fecha"] = pd.to_datetime(datos["fecha"])

os.makedirs("datos/olap", exist_ok=True)

# -------------------------------------------------------------
# DIMENSION CLIENTE
# -------------------------------------------------------------
dim_cliente = datos[["id_cliente", "nombre", "ciudad_cliente", "segmento"]]
dim_cliente = dim_cliente.drop_duplicates()

# -------------------------------------------------------------
# DIMENSION PRODUCTO
# -------------------------------------------------------------
#! La categoria va DENTRO de dim_producto, no en una tabla aparte.
#! Eso es lo que hace que el modelo sea una estrella.
dim_producto = datos[["id_producto", "producto", "categoria"]]
dim_producto = dim_producto.drop_duplicates()

# -------------------------------------------------------------
# DIMENSION TIEMPO
# -------------------------------------------------------------
# ? Esta tabla no viene de los datos: se construye.
# ? Lleva TODOS los dias del ano, incluso los que no tuvieron ventas,
# ? porque Power BI los necesita para comparar meses.
meses = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]

dim_tiempo = pd.DataFrame()
dim_tiempo["fecha"] = pd.date_range("2024-01-01", "2024-12-31")
dim_tiempo["anio"] = dim_tiempo["fecha"].dt.year
dim_tiempo["mes"] = dim_tiempo["fecha"].dt.month
dim_tiempo["nombre_mes"] = dim_tiempo["mes"].apply(lambda m: meses[m - 1])
dim_tiempo["dia"] = dim_tiempo["fecha"].dt.day

# -------------------------------------------------------------
# TABLA DE HECHOS
# -------------------------------------------------------------
#! El hecho solo guarda codigos y numeros. Nada de texto.
hecho_ventas = datos[
    [
        "id_venta",
        "fecha",
        "id_cliente",
        "id_producto",
        "cantidad",
        "precio_unitario",
        "total",
    ]
]

# -------------------------------------------------------------
# Guardar
# -------------------------------------------------------------
dim_cliente.to_csv("datos/olap/dim_cliente.csv", index=False)
dim_producto.to_csv("datos/olap/dim_producto.csv", index=False)
dim_tiempo.to_csv("datos/olap/dim_tiempo.csv", index=False)
hecho_ventas.to_csv("datos/olap/hecho_ventas.csv", index=False)

print("dim_cliente  :", len(dim_cliente), "filas")
print("dim_producto :", len(dim_producto), "filas")
print("dim_tiempo   :", len(dim_tiempo), "filas")
print("hecho_ventas :", len(hecho_ventas), "filas")

print("\nHECHO_VENTAS (solo codigos y numeros)")
print(hecho_ventas.head(3))
print("\nDIM_TIEMPO")
print(dim_tiempo.head(3))

# -------------------------------------------------------------
# La misma pregunta del paso 6
# -------------------------------------------------------------
# ? Aqui son 2 uniones, siempre desde el hecho hacia afuera.
# ? Y en Power BI no se escribe ninguna: se arrastran los campos.
respuesta = (
    hecho_ventas.merge(dim_producto, on="id_producto")
    .merge(dim_cliente, on="id_cliente")
    .groupby(["categoria", "segmento"])["total"]
    .sum()
)
print("\nVenta por categoria y segmento:")
print(respuesta)
