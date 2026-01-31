Instrucciones de instalación:
## Instalación en Windows (usuario final)

Este programa NO requiere instalar Python. Es un ejecutable listo para usar.

### Requisitos
- Windows 10/11

### Pasos
1. Copia `SGP.exe` a una carpeta del equipo (ejemplo: `C:\SGP\` o Escritorio).
2. Haz doble clic en `SGP.exe` para abrir el programa. (está en la carpeta dist/SGP.exe)
3. Si Windows SmartScreen bloquea la ejecución:
   - Click en “Más información”
   - Luego “Ejecutar de todas formas”

### Dónde se guardan los datos
El sistema guarda los productos automáticamente en el perfil del usuario, para evitar problemas de permisos:

`C:\Users\<TuUsuario>\AppData\Roaming\SGP\data\productos.json`

### Respaldo / Migración de datos
Para respaldar o mover tus datos a otro PC:
1. Cierra el programa.
2. Copia el archivo `productos.json` desde la ruta anterior.
3. En el nuevo PC, ejecútalo una vez para que cree la carpeta y luego reemplaza ese `productos.json`.

### Exportación de reportes
- Excel y PDF se guardan donde el usuario seleccione al exportar (recomendado: Documentos).



Descripción de la aplicación:


# Sistema de Gestión de Productos (SGP)

Aplicación en Python con:
- Interfaz gráfica Tkinter
- Persistencia en archivo JSON (data/productos.json)
- Exportación de reportes a Excel y PDF
- Importación de Excel (.xlsx)
- Estructuras de datos: list, dict, set, tuple
- Función recursiva: cálculo de valor de inventario

## Estructura
- main.py
- modulos/
- data/
- exports/
- docs/

## Instalación (para el programador)
1) Crear y activar .venv  empleando en cmd el comando .venv\Sripts\activate
2) Instalar dependencias:
   pip install -r requirements.txt
  
 Los datos siempre se guardaran en: 
   C:\Users\<Usuario>\AppData\Roaming\SGP\data\productos.json
   
## Ejecutar
python main.py
el comando para generar el .exe con PyInstaller (con icono y sin consola)

## Importar Excel
El Excel debe tener encabezados (en la primera fila) como:
sku, nombre, categoria, precio, stock, activo

Categorias válidas:
Aseo, Alimentos, Ferretería, Otro

----------------------------------------------------------------------------------------------------
Desarrollo del proyecto:
----------------------------------------------------------------------------------------------------
Este proyecto corresponde a un Sistema de Gestión de Productos (SGP) desarrollado como aplicación ejecutable en Windows, cumpliendo los requerimientos del trabajo al implementar una solución completa con interfaz gráfica, persistencia liviana, operaciones CRUD, validaciones, estructuras de datos obligatorias, recursividad, y generación/importación de reportes. La aplicación fue construida en Python utilizando la librería Tkinter (ttk) para la interfaz, permitiendo a cualquier usuario operar el sistema mediante formularios, botones y una tabla de visualización (Treeview) sin necesidad de conocimientos técnicos. El sistema incorpora un formulario ordenado para el ingreso y edición de productos (SKU, nombre, categoría, precio, stock y estado activo), y una tabla con scroll para listar los registros, seleccionar un elemento y ejecutar acciones de agregar, actualizar y eliminar, cumpliendo el núcleo funcional del CRUD y asegurando una experiencia de uso consistente.

En relación con el almacenamiento, el proyecto utiliza una base de datos liviana basada en un archivo JSON (texto liviano), evitando motores pesados y cumpliendo con el requisito de persistencia local. Para garantizar que el programa funcione en cualquier equipo sin problemas de permisos, la persistencia se implementó guardando automáticamente el archivo productos.json dentro del perfil del usuario en Windows (ruta típica: AppData\Roaming\SGP\data\productos.json). De esta forma, el ejecutable puede distribuirse como un único archivo y los datos quedan protegidos y disponibles entre ejecuciones, sin depender de la carpeta donde se copie el .exe. Además, la escritura se realizó de manera segura mediante un archivo temporal y reemplazo controlado, reduciendo el riesgo de corrupción de datos ante cierres inesperados.

En cuanto a la calidad de datos, el sistema incorpora un módulo explícito de validaciones, donde se controlan reglas esenciales: 
- obligatoriedad de campos, 
- formato del SKU (alfanumérico y símbolos permitidos), 
- unicidad del SKU, 
- pertenencia de la categoría a un conjunto permitido,
- validación numérica de precio y stock (no negativos).
 
  Estas validaciones se aplican tanto al ingreso manual como a la importación desde Excel, lo cual asegura coherencia y evita que registros inválidos ingresen al sistema. Adicionalmente, el proyecto cumple con la exigencia de uso de estructuras de datos al emplear: listas para almacenar la colección principal de productos, diccionarios para representar cada producto como entidad con atributos, sets para gestionar y verificar rápidamente la unicidad de SKUs, y tuplas para definir catálogos inmutables como el listado de categorías. Asimismo, se incorporó una función recursiva para calcular el valor total del inventario (suma de precio * stock por producto).

  Respecto de los reportes, el proyecto integra exportación a Excel utilizando openpyxl y exportación a PDF mediante reportlab, ambas bibliotecas livianas y ampliamente utilizadas. La exportación genera archivos estructurados con encabezados y datos consistentes, y el usuario puede seleccionar la ubicación de guardado, apoyando la generación de evidencias y documentación del sistema. En complemento, se añadió una funcionalidad relevante adicional: importación desde Excel (.xlsx) como entrada de datos, leyendo encabezados por nombre y aplicando el mismo motor de validación que en el formulario. Durante la importación, el sistema gestiona conflictos de SKU preguntando una única vez si se desea sobrescribir registros existentes, y al finalizar entrega un resumen de resultados (nuevos, actualizados y rechazados con motivos), lo cual mejora la trazabilidad y la transparencia del proceso. Esta integración permite operar el sistema tanto de manera interactiva como a través de carga masiva de datos, fortaleciendo el cumplimiento del objetivo de gestión y reportabilidad.

  Se entrega un proyecto ejecutable  empaquetado con PyInstaller, generando un archivo .exe en modo --onefile y --windowed para que se ejecute como aplicación de escritorio sin consola. Esta decisión facilita la distribución y uso por terceros, ya que el programa puede ejecutarse en un equipo Windows sin instalar Python ni dependencias adicionales. En conjunto, el proyecto implementa una solución modular (separación por archivos de persistencia, validación, gestión de datos, utilidades, exportaciones e interfaz), funcional y orientada al aprendizaje, donde cada componente se encuentra documentado mediante comentarios para facilitar la comprensión del código y la trazabilidad de los requerimientos implementados.


# Descripción de Módulos y Funciones (Lógica de Operación)

A continuación se describe, cada módulo del proyecto, identificando sus funciones y explicando cómo opera la lógica interna de cada una. La explicación se enfoca en el rol de cada archivo dentro de la arquitectura modular y en el flujo de datos desde la interfaz hasta la persistencia en JSON y la generación/importación de reportes.

---

## `modulos/persistencia_json.py` — Persistencia (base de datos liviana JSON)

Este módulo define la ubicación segura donde se guardarán los datos y gestiona la lectura/escritura del archivo JSON que actúa como base de datos liviana.

- **`_directorio_base_app(nombre_app="SGP")`**: determina una carpeta base confiable para almacenar datos del programa. En Windows utiliza `APPDATA` para construir una ruta del tipo `AppData\Roaming\SGP`. Si `APPDATA` no existiera, utiliza la carpeta del usuario como respaldo. Además, crea la carpeta si no existe, asegurando disponibilidad del directorio.

- **`obtener_ruta_datos()`**: construye la ruta final al archivo `productos.json`. Parte desde la carpeta base, crea la subcarpeta `data` y retorna la ruta final `...\SGP\data\productos.json`. Centraliza la decisión de ubicación del almacenamiento.

- **`cargar_productos(ruta=RUTA_DATOS)`**: carga el contenido del JSON y lo transforma a estructuras Python. Si el archivo no existe, lo crea como `[]` y retorna lista vacía. Si el JSON está corrupto, retorna lista vacía para evitar fallas del sistema. Si el JSON es una lista, la retorna directamente; si es un diccionario con clave `"productos"`, retorna esa lista interna.

- **`guardar_productos(productos, ruta=RUTA_DATOS)`**: guarda la lista de productos en JSON. Implementa escritura segura usando un archivo temporal (`.tmp`) y luego reemplazo, reduciendo riesgos de corrupción ante cierres inesperados.

---

## `modulos/datos_basicos.py` — Normalización y conversiones seguras

Este módulo agrupa funciones auxiliares para limpiar texto y convertir valores sin generar errores.

- **`normalizar_texto(s)`**: convierte `None` a texto vacío y aplica `strip()` para eliminar espacios, evitando fallas al validar o comparar campos.

- **`to_int_seguro(s)`**: intenta convertir una entrada a entero. Si falla, retorna `None`, permitiendo que la validación emita un mensaje apropiado.

- **`to_float_seguro(s)`**: convierte a `float` admitiendo coma o punto decimal. Si falla, retorna `None`. Se utiliza para validar el precio.

---

## `modulos/validaciones.py` — Reglas de negocio y construcción del producto

Este módulo concentra reglas que aseguran que los datos sean correctos antes de ingresar a la lista y al JSON.

- **`CATEGORIAS` (tupla)**: catálogo inmutable de categorías válidas, cumpliendo además el requisito de uso de `tuple` para definir conjuntos fijos.

- **`validar_producto(...)`**: valida campos y construye el diccionario final del producto.  
  La lógica opera en etapas:  
  1) Normaliza entradas (`strip`).  
  2) Valida SKU (obligatorio, patrón permitido, largo).  
  3) Valida nombre (obligatorio, largo mínimo).  
  4) Verifica categoría perteneciente a `CATEGORIAS`.  
  5) Convierte y valida precio/stock (numéricos y no negativos).  
  6) Verifica unicidad de SKU usando un `set`:  
     - En modo `crear`, el SKU no puede existir.  
     - En modo `editar`, se permite mantener el SKU original; si cambia, el nuevo no puede estar ocupado.  
  7) Construye el producto como `dict` con tipos correctos y agrega `creado_en`.  
  8) Retorna `(ok, producto, errores)`.

---

## `modulos/gestion_datos.py` — CRUD en memoria (lista de productos)

Este módulo implementa operaciones CRUD sobre la estructura principal: una lista de diccionarios producto.

- **`index_por_sku(productos, sku)`**: recorre la lista y retorna el índice del producto cuyo SKU coincide. Retorna `-1` si no existe.

- **`construir_set_skus(productos)`**: construye un `set` con SKUs existentes, permitiendo validación de unicidad rápida.

- **`agregar_producto(productos, producto)`**: agrega el producto a la lista (CRUD: Create).

- **`actualizar_producto(productos, sku_original, producto_nuevo)`**: reemplaza el producto encontrado por `sku_original` con el nuevo diccionario, conservando `creado_en`. Retorna `True/False` según éxito (CRUD: Update).

- **`eliminar_producto(productos, sku)`**: elimina el producto por SKU usando `pop` y retorna `True/False` (CRUD: Delete).

- **`buscar(productos, texto)`**: filtra productos por coincidencia parcial en SKU, nombre o categoría, usando comparación normalizada (`casefold`). Retorna lista filtrada.

---

## `modulos/funciones_utiles.py` — Recursión aplicada (requisito)

Este módulo contiene una función recursiva usada para calcular el valor total del inventario.

- **`valor_inventario_recursivo(productos, i=0)`**: suma recursivamente `precio * stock` de cada producto.  
  Caso base: cuando `i` alcanza el final de la lista retorna `0.0`.  
  Caso recursivo: suma el subtotal del producto `i` con el resultado de la llamada recursiva `i+1`.

---

## `modulos/reportes.py` — Cálculos de reporte (filtros y agregaciones)

Este módulo define cálculos útiles para reportes lógicos o indicadores.

- **`productos_bajo_stock(productos, umbral=5)`**: retorna productos cuyo stock es menor o igual al umbral.

- **`conteo_por_categoria(productos)`**: genera un `dict` con conteo de productos por categoría, incrementando contadores por cada producto.

---

## `modulos/exportaciones.py` — Exportación e importación (Excel/PDF)

Este módulo transforma datos en archivos externos y permite cargar datos desde Excel.

- **`CAMPOS`**: define el orden estándar de columnas para exportación, garantizando consistencia.

- **`exportar_excel(registros, ruta)`**: crea un archivo `.xlsx` con encabezados y filas. Ajusta ancho de columnas para legibilidad y guarda en la ruta elegida.

- **`exportar_pdf(registros, ruta, titulo="Reporte de Productos")`**: genera un PDF con título y tabla. Aplica estilos básicos (rejilla, encabezado, fuente) y construye el documento final.

- **`importar_excel(ruta)`**: lee un `.xlsx` como entrada. Toma encabezados, recorre filas desde la segunda, construye un `dict` por fila (encabezado → valor), ignora filas vacías y retorna una lista de diccionarios lista para validar e integrar con el JSON.

---

## `modulos/ui_tkinter.py` — Interfaz gráfica y orquestación del sistema

Este módulo contiene la interfaz Tkinter y coordina el flujo completo: usuario → validación → CRUD → guardado JSON → refresco de tabla → reportes.

- **Clase `App(tk.Tk)`**: representa la aplicación completa. Mantiene `self.productos` en memoria (lista) y sincroniza con JSON mediante el módulo de persistencia.

Funciones principales de la clase:

- **`__init__()`**: inicializa la ventana, carga JSON, construye el set de SKUs, define modo del formulario y carga tabla + resumen.

- **`_ui()`**: construye la interfaz: barra de búsqueda, formulario alineado (grid), botones de acciones y tabla (Treeview) con scroll.

- **`_fila_entry(...)` / `_fila_combo(...)`**: helpers para crear filas alineadas (label + input), garantizando que cada widget se cree con el “padre” correcto y evitando desorden visual.

- **`on_buscar()`**: filtra usando `buscar(...)`, refresca tabla y actualiza el resumen según resultados.

- **`on_ver_todo()`**: limpia búsqueda y vuelve a mostrar todos los registros.

- **`on_guardar()`**: agrega o actualiza. Valida con `validar_producto(...)`, ejecuta `agregar_producto(...)` o `actualizar_producto(...)`, actualiza `self.skus`, guarda JSON y refresca.

- **`on_eliminar()`**: elimina el producto seleccionado tras confirmación, guarda JSON y refresca tabla.

- **`on_limpiar()`**: restablece el formulario a estado inicial y vuelve a modo crear.

- **`on_seleccionar()`**: al seleccionar una fila, carga sus datos al formulario y cambia a modo editar.

- **`on_exportar_excel()` / `on_exportar_pdf()`**: exportan los registros visibles en la tabla usando `exportar_excel(...)` o `exportar_pdf(...)`.

- **`on_importar_excel()`**: importa carga masiva. Lee con `importar_excel(...)`, pregunta política de sobrescritura, valida cada fila con `validar_producto(...)` y agrega/actualiza según corresponda. Muestra resumen final de importación (nuevos/actualizados/rechazados).

- **`_refrescar_tabla(registros)`**: repinta el Treeview eliminando filas antiguas e insertando filas nuevas.

- **`_registros_visibles()`**: transforma lo visible en la tabla a una lista de `dict`, permitiendo exportación consistente de lo filtrado.

- **`_actualizar_resumen(registros=None)`**: calcula cantidad de productos y valor del inventario usando `valor_inventario_recursivo(...)` y lo muestra en la barra inferior.

---

## `main.py` — Punto de entrada

- **`main()`**: crea la aplicación `App` y ejecuta `mainloop()` para mantener la ventana funcionando.
- El bloque `if __name__ == "__main__":` asegura que el programa se ejecute solo al correr `main.py` directamente.
