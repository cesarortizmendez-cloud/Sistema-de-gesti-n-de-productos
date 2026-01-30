import re  # Importamos re para validar patrones (por ejemplo SKU)
from datetime import datetime  # Importamos datetime para guardar fecha/hora de creación
from typing import Dict, Any, Tuple, List, Optional  # Tipos para documentar entradas y salidas

from .datos_basicos import normalizar_texto, to_int_seguro, to_float_seguro  # Importamos helpers de limpieza y conversión

CATEGORIAS = ("Aseo", "Alimentos", "Ferretería", "Otro")  # Tupla inmutable (cumple requisito de estructura de datos)

def validar_producto(  # Función que valida campos y arma el diccionario del producto
    sku: str,  # SKU ingresado
    nombre: str,  # Nombre ingresado
    categoria: str,  # Categoría ingresada
    precio: str,  # Precio ingresado (texto o número)
    stock: str,  # Stock ingresado (texto o número)
    activo: bool,  # Estado activo/inactivo
    skus_existentes: set,  # Conjunto (set) de SKUs existentes para asegurar unicidad
    modo: str = "crear",  # Modo: "crear" o "editar"
    sku_original: Optional[str] = None  # SKU original (solo en edición)
) -> Tuple[bool, Dict[str, Any], List[str]]:  # Retorna: OK?, producto dict, lista de errores
    errores: List[str] = []  # Lista donde acumulamos mensajes de error

    sku_n = normalizar_texto(sku)  # Limpiamos SKU (sin espacios)
    nombre_n = normalizar_texto(nombre)  # Limpiamos nombre
    categoria_n = normalizar_texto(categoria)  # Limpiamos categoría

    if not sku_n:  # Si SKU está vacío
        errores.append("SKU es obligatorio.")  # Agregamos error
    elif not re.fullmatch(r"[A-Za-z0-9_-]{2,30}", sku_n):  # Si SKU no cumple formato
        errores.append("SKU inválido (usa letras/números/_/- y largo 2 a 30).")  # Agregamos error

    if not nombre_n:  # Si nombre está vacío
        errores.append("Nombre es obligatorio.")  # Agregamos error
    elif len(nombre_n) < 2:  # Si nombre es demasiado corto
        errores.append("Nombre debe tener al menos 2 caracteres.")  # Agregamos error

    if categoria_n not in CATEGORIAS:  # Si la categoría no está en la tupla permitida
        errores.append(f"Categoría inválida. Usa: {', '.join(CATEGORIAS)}")  # Agregamos error

    precio_f = to_float_seguro(precio)  # Intentamos convertir precio a float
    if precio_f is None:  # Si no se pudo convertir
        errores.append("Precio debe ser numérico.")  # Agregamos error
    elif precio_f < 0:  # Si es negativo
        errores.append("Precio no puede ser negativo.")  # Agregamos error

    stock_i = to_int_seguro(stock)  # Intentamos convertir stock a entero
    if stock_i is None:  # Si no se pudo convertir
        errores.append("Stock debe ser numérico (entero).")  # Agregamos error
    elif stock_i < 0:  # Si es negativo
        errores.append("Stock no puede ser negativo.")  # Agregamos error

    if modo == "crear":  # Si estamos creando un producto nuevo
        if sku_n in skus_existentes:  # Si el SKU ya existe
            errores.append("SKU ya existe, debe ser único.")  # Agregamos error
    elif modo == "editar":  # Si estamos editando
        if sku_original is None:  # Si no tenemos SKU original
            errores.append("Error interno: falta sku_original.")  # Error interno
        else:  # Si sí tenemos SKU original
            if sku_n != sku_original and sku_n in skus_existentes:  # Si cambiaron SKU y el nuevo ya existe
                errores.append("SKU nuevo ya existe, debe ser único.")  # Agregamos error

    producto = {  # Construimos el diccionario del producto (estructura dict)
        "sku": sku_n,  # Guardamos SKU limpio
        "nombre": nombre_n,  # Guardamos nombre limpio
        "categoria": categoria_n,  # Guardamos categoría
        "precio": float(precio_f) if precio_f is not None else 0.0,  # Guardamos precio como float
        "stock": int(stock_i) if stock_i is not None else 0,  # Guardamos stock como int
        "activo": bool(activo),  # Guardamos activo como booleano
        "creado_en": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Guardamos fecha/hora actual
    }  # Fin del dict producto

    return (len(errores) == 0), producto, errores  # Retornamos OK si no hay errores, y además el dict y lista de errores
