import os  # Para trabajar con rutas y carpetas del sistema operativo
import tkinter as tk  # Librería base de interfaz gráfica
from tkinter import ttk, messagebox, filedialog  # Componentes modernos (ttk) + mensajes + diálogos de archivo
from datetime import datetime  # Para generar nombres de archivos con fecha/hora

from .persistencia_json import cargar_productos, guardar_productos  # Funciones para cargar/guardar JSON
from .gestion_datos import construir_set_skus, agregar_producto, actualizar_producto, eliminar_producto, buscar  # CRUD y búsqueda
from .validaciones import validar_producto, CATEGORIAS  # Validación de datos + categorías permitidas
from .funciones_utiles import valor_inventario_recursivo  # Función recursiva (requisito)
from .exportaciones import exportar_excel, exportar_pdf, importar_excel  # Exportación e importación


class App(tk.Tk):  # Clase principal de la aplicación (hereda de Tk)
    def __init__(self):  # Constructor
        super().__init__()  # Inicializa la ventana base
        self.title("Sistema de Gestión de Productos (Tkinter + JSON + Excel/PDF)")  # Título de la ventana
        self.geometry("1050x600")  # Tamaño inicial sugerido (más ancho para que se vea ordenado)

        self.ruta_datos = os.path.join("data", "productos.json")  # Ruta del archivo JSON
        self.productos = cargar_productos(self.ruta_datos)  # Carga lista de productos desde JSON
        self.skus = construir_set_skus(self.productos)  # Construye set de SKUs para validar unicidad

        self.modo = "crear"  # Estado del formulario: crear o editar
        self.sku_original = None  # Guarda SKU original cuando editamos

        self._ui()  # Construye la interfaz gráfica
        self._refrescar_tabla(self.productos)  # Muestra todos los productos en la tabla
        self._actualizar_resumen()  # Muestra resumen inferior (cantidad y valor inventario)

    # ------------------------- CONSTRUCCIÓN UI -------------------------

    def _ui(self):  # Crea toda la interfaz
        # --- Contenedor superior (búsqueda) ---
        top = ttk.Frame(self, padding=10)  # Frame superior con padding
        top.pack(fill="x")  # Se ajusta al ancho

        ttk.Label(top, text="Buscar:").pack(side="left")  # Etiqueta “Buscar”
        self.var_buscar = tk.StringVar()  # Variable de texto para búsqueda
        ent_buscar = ttk.Entry(top, textvariable=self.var_buscar, width=40)  # Campo búsqueda
        ent_buscar.pack(side="left", padx=6)  # Posiciona campo

        ttk.Button(top, text="Aplicar", command=self.on_buscar).pack(side="left")  # Botón aplicar búsqueda
        ttk.Button(top, text="Ver todo", command=self.on_ver_todo).pack(side="left", padx=6)  # Botón ver todo

        # --- Contenedor principal: izquierda (form) / derecha (tabla) ---
        main = ttk.Frame(self, padding=10)  # Frame principal
        main.pack(fill="both", expand=True)  # Ocupa el área disponible

        # ----------- PANEL IZQUIERDO (FORMULARIO) -----------
        form = ttk.LabelFrame(main, text="Producto", padding=12)  # Caja del formulario
        form.pack(side="left", fill="y", padx=(0, 12))  # A la izquierda, con separación

        # Variables del formulario
        self.var_sku = tk.StringVar()  # SKU
        self.var_nombre = tk.StringVar()  # Nombre
        self.var_categoria = tk.StringVar(value=CATEGORIAS[0])  # Categoría (valor inicial)
        self.var_precio = tk.StringVar()  # Precio
        self.var_stock = tk.StringVar()  # Stock
        self.var_activo = tk.BooleanVar(value=True)  # Activo

        # Sub-frame para campos (usaremos grid para alinearlos)
        fields = ttk.Frame(form)  # Contenedor de campos
        fields.pack(fill="x")  # Se ajusta a lo ancho del form

        # Configuramos columnas para que la segunda crezca al redimensionar
        fields.columnconfigure(0, weight=0)  # Columna 0 (labels) no crece
        fields.columnconfigure(1, weight=1)  # Columna 1 (inputs) sí crece

        # Creamos filas con helpers que construyen widgets con el padre correcto
        self.ent_sku = self._fila_entry(fields, 0, "SKU", self.var_sku)  # Entrada SKU
        self.ent_nombre = self._fila_entry(fields, 1, "Nombre", self.var_nombre)  # Entrada Nombre
        self.cb_categoria = self._fila_combo(fields, 2, "Categoría", self.var_categoria, CATEGORIAS)  # Combo Categoría
        self.ent_precio = self._fila_entry(fields, 3, "Precio", self.var_precio)  # Entrada Precio
        self.ent_stock = self._fila_entry(fields, 4, "Stock", self.var_stock)  # Entrada Stock

        # Fila “Activo” (checkbox alineado)
        lbl_activo = ttk.Label(fields, text="Activo")  # Label Activo
        lbl_activo.grid(row=5, column=0, sticky="w", pady=6, padx=(0, 8))  # Lo ubicamos en grid
        chk_activo = ttk.Checkbutton(fields, variable=self.var_activo)  # Checkbox activo
        chk_activo.grid(row=5, column=1, sticky="w", pady=6)  # Lo ubicamos al lado del label

        # Separador
        ttk.Separator(form).pack(fill="x", pady=10)  # Línea separadora

        # Sub-frame para botones de acciones
        actions = ttk.Frame(form)  # Frame para botones CRUD
        actions.pack(fill="x")  # Ocupa ancho

        self.btn_guardar = ttk.Button(actions, text="Agregar", command=self.on_guardar)  # Botón guardar
        self.btn_guardar.pack(fill="x", pady=4)  # Ocupa ancho

        ttk.Button(actions, text="Eliminar (selección)", command=self.on_eliminar).pack(fill="x", pady=4)  # Botón eliminar
        ttk.Button(actions, text="Limpiar", command=self.on_limpiar).pack(fill="x", pady=4)  # Botón limpiar

        # Separador
        ttk.Separator(form).pack(fill="x", pady=10)  # Línea separadora

        # Sub-frame para botones de reportes
        reports = ttk.Frame(form)  # Frame para exportar/importar
        reports.pack(fill="x")  # Ocupa ancho

        ttk.Button(reports, text="Exportar Excel", command=self.on_exportar_excel).pack(fill="x", pady=4)  # Exportar Excel
        ttk.Button(reports, text="Exportar PDF", command=self.on_exportar_pdf).pack(fill="x", pady=4)  # Exportar PDF
        ttk.Button(reports, text="Importar Excel", command=self.on_importar_excel).pack(fill="x", pady=4)  # Importar Excel

        # ----------- PANEL DERECHO (TABLA) -----------
        table_box = ttk.Frame(main)  # Frame para tabla
        table_box.pack(side="left", fill="both", expand=True)  # Ocupa el resto del espacio

        cols = ("sku", "nombre", "categoria", "precio", "stock", "activo", "creado_en")  # Columnas
        self.tree = ttk.Treeview(table_box, columns=cols, show="headings")  # Treeview (tabla)

        # Encabezados y tamaños de columna
        self.tree.heading("sku", text="SKU")  # Encabezado SKU
        self.tree.heading("nombre", text="NOMBRE")  # Encabezado Nombre
        self.tree.heading("categoria", text="CATEGORÍA")  # Encabezado Categoría
        self.tree.heading("precio", text="PRECIO")  # Encabezado Precio
        self.tree.heading("stock", text="STOCK")  # Encabezado Stock
        self.tree.heading("activo", text="ACTIVO")  # Encabezado Activo
        self.tree.heading("creado_en", text="CREADO EN")  # Encabezado creado_en

        # Config de columnas (ancho y alineación)
        self.tree.column("sku", width=90, anchor="w")  # Columna SKU
        self.tree.column("nombre", width=240, anchor="w")  # Columna Nombre
        self.tree.column("categoria", width=120, anchor="w")  # Columna Categoría
        self.tree.column("precio", width=90, anchor="e")  # Precio alineado a la derecha
        self.tree.column("stock", width=70, anchor="e")  # Stock a la derecha
        self.tree.column("activo", width=70, anchor="center")  # Activo centrado
        self.tree.column("creado_en", width=150, anchor="w")  # Fecha

        # Scroll vertical para tabla
        yscroll = ttk.Scrollbar(table_box, orient="vertical", command=self.tree.yview)  # Scroll
        self.tree.configure(yscrollcommand=yscroll.set)  # Vinculamos scroll

        self.tree.pack(side="left", fill="both", expand=True)  # Tabla ocupa espacio
        yscroll.pack(side="right", fill="y")  # Scroll al lado

        self.tree.bind("<<TreeviewSelect>>", self.on_seleccionar)  # Evento al seleccionar fila

        # --- Barra inferior (resumen) ---
        bottom = ttk.Frame(self, padding=10)  # Frame inferior
        bottom.pack(fill="x")  # Ocupa ancho
        self.lbl_resumen = ttk.Label(bottom, text="Resumen: ...")  # Label resumen
        self.lbl_resumen.pack(side="left")  # A la izquierda

    # ------------------------- HELPERS DE CAMPOS (GRID) -------------------------

    def _fila_entry(self, parent, row, label, variable):  # Crea una fila label + entry usando grid
        lbl = ttk.Label(parent, text=label)  # Creamos label con padre correcto
        lbl.grid(row=row, column=0, sticky="w", pady=6, padx=(0, 8))  # Ubicamos label

        ent = ttk.Entry(parent, textvariable=variable)  # Creamos entry con padre correcto (IMPORTANTÍSIMO)
        ent.grid(row=row, column=1, sticky="ew", pady=6)  # Ubicamos entry y permitimos que crezca horizontalmente
        return ent  # Retornamos el entry por si lo necesitamos

    def _fila_combo(self, parent, row, label, variable, values):  # Crea una fila label + combobox usando grid
        lbl = ttk.Label(parent, text=label)  # Creamos label
        lbl.grid(row=row, column=0, sticky="w", pady=6, padx=(0, 8))  # Ubicamos label

        cb = ttk.Combobox(parent, textvariable=variable, values=values, state="readonly")  # Creamos combobox
        cb.grid(row=row, column=1, sticky="ew", pady=6)  # Ubicamos combobox
        return cb  # Retornamos el combobox

    # ------------------------- ACCIONES -------------------------

    def on_buscar(self):  # Acción buscar
        filtrados = buscar(self.productos, self.var_buscar.get())  # Filtramos lista
        self._refrescar_tabla(filtrados)  # Actualizamos tabla
        self._actualizar_resumen(filtrados)  # Actualizamos resumen

    def on_ver_todo(self):  # Acción ver todo
        self.var_buscar.set("")  # Limpia caja de búsqueda
        self._refrescar_tabla(self.productos)  # Muestra todo
        self._actualizar_resumen()  # Resumen global

    def on_guardar(self):  # Agregar o actualizar
        ok, producto, errores = validar_producto(  # Validamos lo ingresado
            sku=self.var_sku.get(),  # SKU
            nombre=self.var_nombre.get(),  # Nombre
            categoria=self.var_categoria.get(),  # Categoría
            precio=self.var_precio.get(),  # Precio
            stock=self.var_stock.get(),  # Stock
            activo=self.var_activo.get(),  # Activo
            skus_existentes=self.skus,  # Set SKUs
            modo=self.modo,  # Modo
            sku_original=self.sku_original  # SKU original en edición
        )

        if not ok:  # Si falló validación
            messagebox.showerror("Validación", "\n".join(errores))  # Muestra errores
            return  # Sale

        if self.modo == "crear":  # Si estamos creando
            agregar_producto(self.productos, producto)  # Agrega
        else:  # Si estamos editando
            if not actualizar_producto(self.productos, self.sku_original, producto):  # Intenta actualizar
                messagebox.showerror("Error", "No se pudo actualizar (SKU original no encontrado).")  # Error
                return  # Sale

        self.skus = construir_set_skus(self.productos)  # Reconstruye set de SKUs
        guardar_productos(self.productos, self.ruta_datos)  # Guarda JSON

        self.on_ver_todo()  # Refresca
        self.on_limpiar()  # Limpia formulario
        messagebox.showinfo("OK", "Guardado correctamente.")  # Mensaje éxito

    def on_eliminar(self):  # Eliminar selección
        sel = self.tree.selection()  # Obtiene selección
        if not sel:  # Si no hay
            messagebox.showwarning("Atención", "Selecciona un producto en la tabla.")  # Aviso
            return  # Sale

        sku = self.tree.item(sel[0], "values")[0]  # Lee SKU de la fila
        if not messagebox.askyesno("Confirmar", f"¿Eliminar SKU {sku}?"):  # Confirma
            return  # Sale si no confirma

        if eliminar_producto(self.productos, sku):  # Elimina del arreglo
            self.skus = construir_set_skus(self.productos)  # Actualiza set
            guardar_productos(self.productos, self.ruta_datos)  # Guarda
            self.on_ver_todo()  # Refresca
            self.on_limpiar()  # Limpia
            messagebox.showinfo("OK", "Eliminado.")  # Aviso
        else:  # Si no encontró
            messagebox.showerror("Error", "No se encontró el producto.")  # Error

    def on_limpiar(self):  # Limpia formulario
        self.modo = "crear"  # Cambia a crear
        self.sku_original = None  # Resetea SKU original
        self.btn_guardar.config(text="Agregar")  # Botón dice Agregar

        self.var_sku.set("")  # Limpia SKU
        self.var_nombre.set("")  # Limpia nombre
        self.var_categoria.set(CATEGORIAS[0])  # Categoría por defecto
        self.var_precio.set("")  # Limpia precio
        self.var_stock.set("")  # Limpia stock
        self.var_activo.set(True)  # Activo por defecto

    def on_seleccionar(self, _evt):  # Cuando se selecciona una fila
        sel = self.tree.selection()  # Selección
        if not sel:  # Si no hay
            return  # Sale

        values = self.tree.item(sel[0], "values")  # Obtiene valores de la fila

        self.modo = "editar"  # Cambia a editar
        self.sku_original = values[0]  # Guarda SKU original
        self.btn_guardar.config(text="Actualizar")  # Botón dice Actualizar

        self.var_sku.set(values[0])  # Carga SKU
        self.var_nombre.set(values[1])  # Carga nombre
        self.var_categoria.set(values[2])  # Carga categoría
        self.var_precio.set(values[3])  # Carga precio
        self.var_stock.set(values[4])  # Carga stock

        self.var_activo.set(str(values[5]).lower() in ("true", "1", "si", "sí", "yes"))  # Interpreta activo

    def on_exportar_excel(self):  # Exportar lo visible
        registros = self._registros_visibles()  # Registros visibles
        if not registros:  # Si no hay
            messagebox.showwarning("Atención", "No hay registros para exportar.")  # Aviso
            return  # Sale

        ruta = filedialog.asksaveasfilename(  # Pide ruta
            defaultextension=".xlsx",  # Extensión
            filetypes=[("Excel", "*.xlsx")],  # Tipo
            initialdir=os.path.join(os.getcwd(), "exports"),  # Carpeta sugerida
            initialfile=f"productos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"  # Nombre sugerido
        )
        if not ruta:  # Si canceló
            return  # Sale

        os.makedirs(os.path.dirname(ruta), exist_ok=True)  # Crea carpeta si falta
        exportar_excel(registros, ruta)  # Exporta
        messagebox.showinfo("OK", f"Exportado a Excel:\n{ruta}")  # Aviso

    def on_exportar_pdf(self):  # Exportar PDF
        registros = self._registros_visibles()  # Registros visibles
        if not registros:  # Si no hay
            messagebox.showwarning("Atención", "No hay registros para exportar.")  # Aviso
            return  # Sale

        ruta = filedialog.asksaveasfilename(  # Pide ruta
            defaultextension=".pdf",  # Extensión
            filetypes=[("PDF", "*.pdf")],  # Tipo
            initialdir=os.path.join(os.getcwd(), "exports"),  # Carpeta sugerida
            initialfile=f"productos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"  # Nombre sugerido
        )
        if not ruta:  # Si canceló
            return  # Sale

        os.makedirs(os.path.dirname(ruta), exist_ok=True)  # Crea carpeta
        exportar_pdf(registros, ruta)  # Exporta
        messagebox.showinfo("OK", f"Exportado a PDF:\n{ruta}")  # Aviso

    def on_importar_excel(self):  # Importar Excel
        ruta = filedialog.askopenfilename(  # Selecciona archivo
            filetypes=[("Excel", "*.xlsx")],  # Solo xlsx
            initialdir=os.getcwd()  # Carpeta inicial
        )
        if not ruta:  # Si canceló
            return  # Sale

        try:  # Intentamos leer
            registros = importar_excel(ruta)  # Lee excel a lista de dicts
        except Exception as e:  # Si falla
            messagebox.showerror("Error", f"No se pudo leer el Excel.\n{e}")  # Muestra error
            return  # Sale

        if not registros:  # Si no hay registros
            messagebox.showwarning("Atención", "El Excel no contiene registros.")  # Aviso
            return  # Sale

        sobrescribir = messagebox.askyesno(  # Pregunta política
            "Importación",
            "¿Deseas SOBRESCRIBIR productos cuando el SKU ya exista?\n"
            "Sí = actualiza existentes | No = solo agrega nuevos"
        )

        importados = 0  # Contador nuevos
        actualizados = 0  # Contador actualizados
        rechazados = 0  # Contador rechazados
        razones = []  # Motivos de rechazo

        self.skus = construir_set_skus(self.productos)  # Reconstruye set

        for fila_excel, r in enumerate(registros, start=2):  # Recorre filas (start=2 porque fila 1 es encabezado)
            sku = str(r.get("sku", "")).strip()  # Lee SKU
            nombre = str(r.get("nombre", "")).strip()  # Lee nombre
            categoria = str(r.get("categoria", "")).strip()  # Lee categoría
            precio = str(r.get("precio", "")).strip()  # Lee precio
            stock = str(r.get("stock", "")).strip()  # Lee stock

            activo_raw = r.get("activo", True)  # Lee activo
            if isinstance(activo_raw, str):  # Si viene como texto
                activo = activo_raw.strip().lower() in ("1", "true", "si", "sí", "yes")  # Convierte a bool
            else:  # Si viene como número/bool
                activo = bool(activo_raw)  # Convierte a bool

            sku_original = sku if sku in self.skus else None  # Define sku_original si ya existe
            modo = "editar" if sku_original else "crear"  # Define modo

            ok, producto, errores = validar_producto(  # Reusa validación
                sku=sku, nombre=nombre, categoria=categoria,
                precio=precio, stock=stock, activo=activo,
                skus_existentes=self.skus, modo=modo, sku_original=sku_original
            )

            if not ok:  # Si inválido
                rechazados += 1  # Suma rechazados
                razones.append(f"Fila {fila_excel}: " + "; ".join(errores))  # Guarda motivo
                continue  # Sigue

            if sku in self.skus and not sobrescribir:  # Si existe y no se sobrescribe
                rechazados += 1  # Rechaza
                razones.append(f"Fila {fila_excel}: SKU {sku} ya existe (no se sobrescribe).")  # Motivo
                continue  # Sigue

            if sku in self.skus:  # Si existe y se sobrescribe
                if actualizar_producto(self.productos, sku, producto):  # Actualiza
                    actualizados += 1  # Suma actualizados
                else:  # Si falla
                    rechazados += 1  # Rechaza
                    razones.append(f"Fila {fila_excel}: no se pudo actualizar SKU {sku}.")  # Motivo
            else:  # Si no existe
                agregar_producto(self.productos, producto)  # Agrega nuevo
                importados += 1  # Suma importados
                self.skus.add(sku)  # Agrega al set

        guardar_productos(self.productos, self.ruta_datos)  # Guarda JSON
        self.on_ver_todo()  # Refresca tabla completa
        self._actualizar_resumen()  # Refresca resumen

        resumen = (  # Mensaje final
            f"Importación finalizada:\n"
            f"- Nuevos: {importados}\n"
            f"- Actualizados: {actualizados}\n"
            f"- Rechazados: {rechazados}"
        )

        if razones:  # Si hay razones
            resumen += "\n\nEjemplos de errores:\n" + "\n".join(razones[:10])  # Muestra máx 10

        messagebox.showinfo("Resultado", resumen)  # Muestra resultado

    # ------------------------- TABLA Y RESUMEN -------------------------

    def _refrescar_tabla(self, registros):  # Actualiza la tabla con registros
        for item in self.tree.get_children():  # Recorre filas actuales
            self.tree.delete(item)  # Borra filas

        for p in registros:  # Inserta registros nuevos
            self.tree.insert("", "end", values=(  # Inserta una fila
                p.get("sku", ""),  # SKU
                p.get("nombre", ""),  # Nombre
                p.get("categoria", ""),  # Categoría
                p.get("precio", ""),  # Precio
                p.get("stock", ""),  # Stock
                p.get("activo", ""),  # Activo
                p.get("creado_en", ""),  # Creado en
            ))

    def _registros_visibles(self):  # Obtiene registros visibles en la tabla
        registros = []  # Lista de dicts
        for iid in self.tree.get_children():  # Recorre filas
            v = self.tree.item(iid, "values")  # Obtiene values
            registros.append({  # Construye dict
                "sku": v[0],  # SKU
                "nombre": v[1],  # Nombre
                "categoria": v[2],  # Categoría
                "precio": v[3],  # Precio
                "stock": v[4],  # Stock
                "activo": v[5],  # Activo
                "creado_en": v[6],  # Creado en
            })
        return registros  # Retorna lista

    def _actualizar_resumen(self, registros=None):  # Actualiza resumen inferior
        regs = registros if registros is not None else self.productos  # Usa filtrados o todos
        total = len(regs)  # Número de productos
        valor = valor_inventario_recursivo(regs)  # Valor inventario con recursión
        self.lbl_resumen.config(text=f"Resumen: {total} productos | Valor inventario: {valor:,.0f}")  # Muestra resumen
