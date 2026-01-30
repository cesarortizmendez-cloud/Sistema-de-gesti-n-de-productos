from typing import List, Dict, Any  # Tipos para documentar

def productos_bajo_stock(productos: List[Dict[str, Any]], umbral: int = 5) -> List[Dict[str, Any]]:  # Filtra productos con stock bajo
    return [p for p in productos if int(p.get("stock", 0)) <= umbral]  # List comprehension con condición

def conteo_por_categoria(productos: List[Dict[str, Any]]) -> Dict[str, int]:  # Cuenta cuántos productos hay por categoría
    conteo = {}  # Diccionario para acumular conteos
    for p in productos:  # Recorremos productos
        cat = p.get("categoria", "Otro")  # Obtenemos categoría, si falta usamos "Otro"
        conteo[cat] = conteo.get(cat, 0) + 1  # Sumamos 1 al contador de esa categoría
    return conteo  # Retornamos el dict con conteos
