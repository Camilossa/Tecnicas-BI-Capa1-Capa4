# =============================================================
# CAPA 3 - PASO 8: guardar el modelo OLAP en Postgres
# =============================================================
#! ANTES de correr esto, crea la base una sola vez.
#! En pgAdmin o en la terminal:   CREATE DATABASE tecnoandina;


import pandas as pd
from sqlalchemy import create_engine, text

# -------------------------------------------------------------
# 1) Datos de conexion
# -------------------------------------------------------------
#! Cambia USUARIO y CLAVE por los tuyos.
USUARIO = "postgres"
CLAVE = "postgres"
HOST = "localhost"
PUERTO = "5432"
BASE = "tecnoandina"

# ? Asi se arma la direccion de la base de datos:
# ? postgresql://usuario:clave@servidor:puerto/base
conexion = create_engine(
    f"postgresql+psycopg2://{USUARIO}:{CLAVE}@{HOST}:{PUERTO}/{BASE}"
)

# -------------------------------------------------------------
# 2) Crear las tablas
# -------------------------------------------------------------
# ? DROP TABLE IF EXISTS borra la tabla si ya existia.
# ? Asi se puede correr este script las veces que se quiera.
#! Las dimensiones se crean primero porque el hecho apunta hacia ellas.
crear_tablas = """
DROP TABLE IF EXISTS hecho_ventas;
DROP TABLE IF EXISTS dim_cliente;
DROP TABLE IF EXISTS dim_producto;
DROP TABLE IF EXISTS dim_tiempo;

CREATE TABLE dim_cliente (
    id_cliente     VARCHAR(10) PRIMARY KEY,
    nombre         VARCHAR(100),
    ciudad_cliente VARCHAR(50),
    segmento       VARCHAR(30)
);

CREATE TABLE dim_producto (
    id_producto VARCHAR(10) PRIMARY KEY,
    producto    VARCHAR(100),
    categoria   VARCHAR(30)
);

CREATE TABLE dim_tiempo (
    fecha      DATE PRIMARY KEY,
    anio       INT,
    mes        INT,
    nombre_mes VARCHAR(15),
    dia        INT
);

CREATE TABLE hecho_ventas (
    id_venta        VARCHAR(10) PRIMARY KEY,
    fecha           DATE        REFERENCES dim_tiempo(fecha),
    id_cliente      VARCHAR(10) REFERENCES dim_cliente(id_cliente),
    id_producto     VARCHAR(10) REFERENCES dim_producto(id_producto),
    cantidad        INT,
    precio_unitario BIGINT,
    total           BIGINT
);
"""

with conexion.begin() as con:
    con.execute(text(crear_tablas))
print("Tablas creadas.")

# -------------------------------------------------------------
# 3) Cargar los datos
# -------------------------------------------------------------
#! El orden importa: primero las dimensiones, al final el hecho.
#! Si se carga el hecho primero, Postgres lo rechaza porque apunta
#! a clientes y productos que todavia no existen.
tablas = ["dim_cliente", "dim_producto", "dim_tiempo", "hecho_ventas"]

for tabla in tablas:
    df = pd.read_csv("datos/olap/" + tabla + ".csv")
    # ? if_exists="append" agrega los datos a la tabla que ya creamos arriba.
    df.to_sql(tabla, conexion, if_exists="append", index=False)
    print("Cargada", tabla, "->", len(df), "filas")

# -------------------------------------------------------------
# 4) Revisar que si quedo guardado
# -------------------------------------------------------------
print("\nLeyendo desde Postgres:")
for tabla in tablas:
    cuantas = pd.read_sql("SELECT COUNT(*) AS n FROM " + tabla, conexion)
    print(" ", tabla, "->", cuantas["n"][0], "filas")

total = pd.read_sql("SELECT SUM(total) AS venta FROM hecho_ventas", conexion)
print("\nVenta total en la base: $", format(total["venta"][0], ",.0f"))
