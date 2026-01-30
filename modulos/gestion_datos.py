from typing import List, Dict, Any  # Tipos para documentar estructuras de datos

def index_por_sku(productos: List[Dict[str, Any]], sku: str) -> int:  # Busca el índice de un producto por SKU
    for i, p in enumerate(productos):  # Recorremos la lista con índice
        if p.get("sku") == sku:  # Si el SKU coincide
            return i  # Retornamos el índice encontrado
    return -1  # Si no se encontró, retornamos -1

def construir_set_skus(productos: List[Dict[str, Any]]) -> set:  # Construye un set con todos los SKUs (evita duplicados)
    return set(p.get("sku") for p in productos if p.get("sku"))  # Set comprehension (rápido) filtrando SKUs no vacíos

def agregar_producto(productos: List[Dict[str, Any]], producto: Dict[str, Any]) -> None:  # Agrega un producto a la lista
    productos.append(producto)  # Append agrega al final de la lista (CRUD: Create)

def actualizar_producto(productos: List[Dict[str, Any]], sku_original: str, producto_nuevo: Dict[str, Any]) -> bool:  # Actualiza producto existente
    idx = index_por_sku(productos, sku_original)  # Buscamos el índice del producto a actualizar
    if idx == -1:  # Si no existe
        return False  # No se pudo actualizar

    creado = productos[idx].get("creado_en")  # Rescatamos fecha/hora original
    if creado:  # Si existe
        producto_nuevo["creado_en"] = creado  # Conservamos el creado_en original

    productos[idx] = producto_nuevo  # Reemplazamos el dict en esa posición (CRUD: Update)
    return True  # Indicamos éxito

def eliminar_producto(productos: List[Dict[str, Any]], sku: str) -> bool:  # Elimina producto por SKU
    idx = index_por_sku(productos, sku)  # Buscamos el índice
    if idx == -1:  # Si no existe
        return False  # No se pudo eliminar
    productos.pop(idx)  # Quitamos el elemento en ese índice (CRUD: Delete)
    return True  # Éxito

def buscar(productos: List[Dict[str, Any]], texto: str) -> List[Dict[str, Any]]:  # Busca por SKU/nombre/categoría
    q = (texto or "").strip().casefold()  # Normalizamos a minúsculas para comparación robusta
    if not q:  # Si no hay texto de búsqueda
        return list(productos)  # Devolvemos copia de toda la lista

    filtrados = []  # Lista de resultados
    for p in productos:  # Recorremos productos (bucle)
        sku = str(p.get("sku", "")).casefold()  # SKU en minúscula
        nombre = str(p.get("nombre", "")).casefold()  # Nombre en minúscula
        categoria = str(p.get("categoria", "")).casefold()  # Categoría en minúscula

        if q in sku or q in nombre or q in categoria:  # Condición: si el texto aparece en alguno
            filtrados.append(p)  # Agregamos al resultado

    return filtrados  # Devolvemos lista filtrada
