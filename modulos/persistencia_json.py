import json  # Permite leer y escribir JSON
import os  # Permite trabajar con rutas y crear carpetas
import sys  # Permite detectar si el programa corre como .exe (PyInstaller)
from typing import List, Dict, Any  # Tipos para claridad y aprendizaje


def _directorio_base_app(nombre_app: str = "SGP") -> str:  # Devuelve la carpeta base segura para guardar datos
    # En Windows, APPDATA apunta a: C:\Users\<Usuario>\AppData\Roaming  # Comentario
    appdata = os.environ.get("APPDATA")  # Obtenemos APPDATA desde variables de entorno

    if appdata:  # Si existe APPDATA (lo normal en Windows)
        base = os.path.join(appdata, nombre_app)  # Creamos ruta: ...\AppData\Roaming\SGP
    else:  # Si por alguna razón APPDATA no existe
        base = os.path.join(os.path.expanduser("~"), f".{nombre_app.lower()}")  # Usamos carpeta del usuario como respaldo

    os.makedirs(base, exist_ok=True)  # Creamos la carpeta base si no existe
    return base  # Retornamos la ruta base


def obtener_ruta_datos() -> str:  # Construye y devuelve la ruta final del archivo JSON
    base = _directorio_base_app("SGP")  # Obtenemos carpeta base de la app (segura)
    carpeta_data = os.path.join(base, "data")  # Creamos subcarpeta "data"
    os.makedirs(carpeta_data, exist_ok=True)  # Aseguramos que exista
    return os.path.join(carpeta_data, "productos.json")  # Ruta final al JSON


RUTA_DATOS = obtener_ruta_datos()  # Ruta por defecto del “archivo base de datos”


def cargar_productos(ruta: str = RUTA_DATOS) -> List[Dict[str, Any]]:  # Carga productos desde JSON
    os.makedirs(os.path.dirname(ruta), exist_ok=True)  # Asegura que exista la carpeta donde vive el archivo

    if not os.path.exists(ruta):  # Si el archivo no existe aún
        with open(ruta, "w", encoding="utf-8") as f:  # Lo creamos en escritura
            f.write("[]")  # Lo iniciamos como lista vacía
        return []  # Retornamos lista vacía

    with open(ruta, "r", encoding="utf-8") as f:  # Abrimos el archivo en lectura
        try:  # Intentamos leer JSON válido
            data = json.load(f)  # Convertimos JSON a estructura Python
        except json.JSONDecodeError:  # Si el archivo estuviera corrupto o mal escrito
            return []  # Retornamos vacío para no romper la app

    if isinstance(data, list):  # Si el JSON es una lista (formato esperado)
        return data  # Retornamos esa lista

    if isinstance(data, dict) and isinstance(data.get("productos"), list):  # Si alguien guardó un dict con "productos"
        return data["productos"]  # Retornamos la lista dentro del dict

    return []  # Cualquier otro formato lo tratamos como vacío


def guardar_productos(productos: List[Dict[str, Any]], ruta: str = RUTA_DATOS) -> None:  # Guarda productos en JSON
    os.makedirs(os.path.dirname(ruta), exist_ok=True)  # Asegura que exista la carpeta

    tmp = ruta + ".tmp"  # Archivo temporal para escritura segura
    with open(tmp, "w", encoding="utf-8") as f:  # Abrimos el temporal para escribir
        json.dump(productos, f, ensure_ascii=False, indent=2)  # Guardamos el JSON “bonito” (indentado)

    os.replace(tmp, ruta)  # Reemplazamos el archivo real por el temporal (reduce riesgo de corrupción)
