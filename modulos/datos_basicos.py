from typing import Optional  # Importamos Optional para indicar que una función puede devolver un valor o None

def normalizar_texto(s: str) -> str:  # Función para limpiar texto (quita espacios y evita None)
    return (s or "").strip()  # Si s es None, usamos "", y además quitamos espacios al inicio y final

def to_int_seguro(s: str) -> Optional[int]:  # Convierte un valor a int, o None si falla
    try:  # Intentamos convertir
        return int(str(s).strip())  # Convertimos a string, quitamos espacios y luego a entero
    except Exception:  # Si algo falla (texto no numérico, etc.)
        return None  # Devolvemos None para que la validación lo detecte

def to_float_seguro(s: str) -> Optional[float]:  # Convierte un valor a float, o None si falla
    try:  # Intentamos convertir
        txt = str(s).strip().replace(",", ".")  # Aceptamos coma decimal y la transformamos a punto
        return float(txt)  # Convertimos a float
    except Exception:  # Si falla la conversión
        return None  # Devolvemos None
