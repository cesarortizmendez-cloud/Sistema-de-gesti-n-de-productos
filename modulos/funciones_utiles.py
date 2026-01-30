from typing import List, Dict, Any  # Importamos tipos para claridad

def valor_inventario_recursivo(productos: List[Dict[str, Any]], i: int = 0) -> float:  # Función recursiva (requisito)
    if i >= len(productos):  # Caso base: si el índice llegó al final
        return 0.0  # Retornamos 0 para terminar la suma

    p = productos[i]  # Tomamos el producto actual
    subtotal = float(p.get("precio", 0.0)) * int(p.get("stock", 0))  # Calculamos precio * stock
    return subtotal + valor_inventario_recursivo(productos, i + 1)  # Llamada recursiva al siguiente índice
