# =============================================================
# PROGRAMAR: corre main.py todos los dias a las 8:00 am
# =============================================================
# ? Funciona igual en Mac, Windows y Linux.
# ? Se corre UNA vez con:   uv run programar.py
# ? y se deja la terminal abierta. Para detenerlo: Ctrl + C
#! Si se cierra la terminal o se apaga el computador, deja de programar.

# ? subprocess sirve para ejecutar otros programas desde Python
# ? (aqui lo usamos para ejecutar main.py).
import subprocess

# ? sys.executable nos da la ruta del Python que esta corriendo (el del .venv).
import sys

# ? time trae funciones de tiempo; usaremos time.sleep para "esperar".
import time

# ? datetime sirve para obtener la fecha y hora actual.
from datetime import datetime

# ? Path sirve para manejar rutas de carpetas, igual en Mac y Windows.
from pathlib import Path

# ? schedule es la libreria que programa tareas a una hora.
# ? Se instalo con:  uv add schedule
import schedule

# ? Carpeta del proyecto (donde esta este archivo).
# ? __file__ = ruta de programar.py, .resolve() = ruta completa, .parent = su carpeta.
RAIZ = Path(__file__).resolve().parent

# ? Hora a la que se ejecuta, en formato 24 horas "HH:MM".
HORA = "14:49"


# ? Funcion con lo que se hace cada dia a la hora programada.
def correr_todo():
    # ? Muestra la fecha y hora en que empezo.
    # ? strftime("%Y-%m-%d %H:%M") la deja como 2026-11-04 08:00
    print("\n[", datetime.now().strftime("%Y-%m-%d %H:%M"), "] Corriendo main.py ...")

    # ? Ejecuta main.py con el mismo Python, parado en la carpeta del proyecto.
    # ? Es como escribir en la terminal:  python main.py
    # ? Se corre aparte para que, si falla, el programador siga vivo
    # ? y lo intente de nuevo manana.
    resultado = subprocess.run([sys.executable, "main.py"], cwd=RAIZ)

    # ? returncode 0 = main.py termino bien.
    if resultado.returncode == 0:
        # ? schedule.next_run() dice la fecha y hora de la proxima ejecucion.
        print("Listo. Proxima ejecucion:", schedule.next_run())
    # ? Cualquier otro numero = algun paso fallo.
    else:
        print("Fallo. Se intentara de nuevo manana a las", HORA)


# ? Aqui se programa la tarea. Se lee casi como en ingles:
# ? schedule.every()   -> "cada"
# ? .day               -> "dia"
# ? .at(HORA)          -> "a las 08:00"
# ? .do(correr_todo)   -> "haz correr_todo"
#! Ojo: se pasa correr_todo SIN parentesis. Asi le damos la funcion
#! para que la llame despues, en vez de ejecutarla ahora mismo.
schedule.every().day.at(HORA).do(correr_todo)

# ? Mensajes para saber que quedo programado.
print("Programado todos los dias a las", HORA)
print("Proxima ejecucion:", schedule.next_run())
print("(Deja esta ventana abierta. Ctrl + C para salir)")

# ? while True es un ciclo infinito: se repite para siempre (hasta Ctrl + C).
# ? schedule NO se ejecuta solo; alguien tiene que preguntarle "¿ya es hora?".
while True:
    # ? run_pending() revisa si ya llego la hora de alguna tarea y, si si, la ejecuta.
    schedule.run_pending()
    # ? Espera 30 segundos antes de volver a revisar,
    # ? para no gastar procesador preguntando a cada instante.
    time.sleep(30)
