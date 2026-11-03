# =============================================================
# MAIN: corre todo el proceso de punta a punta
# =============================================================
# ? Ejecuta los pasos de cada capa en orden.
# ? Si un paso falla, se detiene y no sigue con los demas.
# ? Cada ejecucion queda guardada en la carpeta logs/
# ? Ej: logs/2026-11-04_08-00-00.log        -> salio todo bien
# ?     logs/2026-11-04_08-00-00_ERROR.log  -> algo fallo (adentro dice que)

# ? os sirve para manejar variables del sistema (la usamos para el idioma del texto).
import os

# ? subprocess sirve para ejecutar otros programas desde Python
# ? (como si los escribieramos en la terminal).
import subprocess

# ? sys da acceso a cosas del Python que esta corriendo:
# ? su ubicacion (sys.executable) y la forma de terminar el programa (sys.exit).
import sys

# ? datetime sirve para obtener la fecha y hora actual.
from datetime import datetime

# ? Path sirve para manejar rutas de carpetas y archivos
# ? sin preocuparse si es Mac ("/") o Windows ("\").
from pathlib import Path

# ? __file__ es la ruta de este archivo (main.py).
# ? .resolve() la convierte en ruta completa (absoluta).
# ? .parent se queda con la carpeta que lo contiene = la raiz del proyecto.
#! Los scripts usan rutas como "datos/ventas.xlsx", por eso
#! hay que correrlos parados en esta carpeta.
RAIZ = Path(__file__).resolve().parent

# ? Carpeta donde se guardan los logs (registros de cada ejecucion).
CARPETA_LOGS = RAIZ / "logs"
# ? mkdir la crea si no existe. exist_ok=True evita error si ya existe.
CARPETA_LOGS.mkdir(exist_ok=True)

# ? Nombre del log de ESTA ejecucion, con la fecha y hora en que empezo.
#! Se usa "-" y no ":" en la hora porque Windows no permite ":" en nombres de archivo.
LOG = CARPETA_LOGS / (datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log")

# ? Lista con los scripts a ejecutar, EN ORDEN.
#! El orden importa: cada paso usa los archivos que genero el anterior.
PASOS = [
    "capa1_origenes/01_origenes.py",  # ? une ventas + clientes -> ventas_clientes.csv
    "capa2_limpieza/04_ver_errores.py",  # ? muestra duplicados, vacios y tipos
    "capa2_limpieza/05_limpiar.py",  # ? limpia los datos -> ventas_limpio.csv
    "capa3_datawarehouse/06_modelo_oltp.py",  # ? arma las tablas OLTP -> datos/oltp/
    "capa3_datawarehouse/07_modelo_olap.py",  # ? arma el modelo estrella -> datos/olap/
    "capa3_datawarehouse/08_cargar_postgres.py",  # ? sube el modelo OLAP a Postgres
]


# ? Funcion para mostrar un texto en pantalla Y guardarlo en el log al mismo tiempo.
def escribir(texto):
    # ? Lo muestra en la terminal, como un print normal.
    print(texto, flush=True)
    # ? open(..., "a") abre el archivo para AGREGAR al final (append), sin borrar lo anterior.
    # ? encoding="utf-8" para que las tildes y la ñ se guarden bien.
    # ? with ... cierra el archivo solo al terminar el bloque.
    with open(LOG, "a", encoding="utf-8") as archivo:
        archivo.write(texto + "\n")


# ? def crea una funcion: un bloque de codigo con nombre que se puede llamar.
def main():
    # ? "=" * 60 repite el signo igual 60 veces, para hacer una linea separadora.
    escribir("=" * 60)
    # ? datetime.now() = fecha y hora de este momento.
    # ? strftime(...) le da formato: año-mes-dia hora:minuto:segundo.
    escribir("Inicio: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    escribir("=" * 60)

    # ? Copia de las variables del sistema, con PYTHONIOENCODING en utf-8.
    # ? Asi los scripts hijos mandan su texto en utf-8 (importante en Windows).
    entorno = {**os.environ, "PYTHONIOENCODING": "utf-8"}

    # ? for recorre la lista PASOS, uno por uno.
    # ? En cada vuelta, la variable "paso" tiene el nombre de un script.
    for paso in PASOS:
        # ? f"..." permite meter variables dentro del texto con {}.
        # ? \n hace un salto de linea antes del mensaje.
        escribir(f"\n>>> Corriendo {paso}")

        # ? subprocess.run ejecuta el script y espera a que termine.
        # ? sys.executable = el mismo Python del .venv que corre este main.
        # ? Es como escribir en la terminal:  python capa1_origenes/01_origenes.py
        # ? cwd=RAIZ hace que se ejecute parado en la carpeta del proyecto.
        # ? capture_output=True "atrapa" todo lo que el script imprime,
        # ? para poder guardarlo en el log (si no, solo saldria en pantalla).
        # ? text=True y encoding="utf-8" lo entregan como texto normal.
        resultado = subprocess.run(
            [sys.executable, paso],
            cwd=RAIZ,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=entorno,
        )

        # ? stdout = lo que el script imprimio normalmente (sus print).
        # ? .rstrip() quita los saltos de linea sobrantes del final.
        if resultado.stdout:
            escribir(resultado.stdout.rstrip())
        # ? stderr = los errores y advertencias (aqui sale el "Traceback" si algo falla).
        if resultado.stderr:
            escribir("--- Errores / advertencias ---")
            escribir(resultado.stderr.rstrip())

        # ? returncode es el "codigo de salida" del script:
        # ? 0 = termino bien, cualquier otro numero = hubo un error.
        if resultado.returncode != 0:
            # ? Avisamos cual paso fallo y con que codigo.
            escribir(f"\n!!! Fallo {paso} (codigo {resultado.returncode}). Se detiene.")
            # ? Le cambiamos el nombre al log para que termine en _ERROR.log
            # ? y se vea de una en la carpeta cuales ejecuciones fallaron.
            # ? .stem = nombre sin la extension (ej: "2026-11-04_08-00-00").
            LOG.rename(LOG.with_name(LOG.stem + "_ERROR.log"))
            # ? sys.exit termina el programa aqui mismo, sin correr los pasos que faltan.
            # ? Le pasamos el mismo codigo de error para que quien llamo a main.py sepa que fallo.
            sys.exit(resultado.returncode)

    # ? Si llegamos aqui, todos los pasos terminaron bien.
    escribir("\nFin OK: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    escribir("Log guardado en: " + str(LOG))


# ? Esta condicion es verdadera solo cuando corremos este archivo directamente
# ? (uv run main.py). Si otro archivo lo importa, NO se ejecuta main() solo.
if __name__ == "__main__":
    # ? Llama a la funcion main() que definimos arriba.
    main()
