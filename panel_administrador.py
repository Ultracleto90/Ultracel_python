import os
import sys
import random
import string
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
import pandas as pd
import requests 
import json


# --- PALETA DE COLORES "ENTERPRISE" ---
COLOR_BARRA_LATERAL = "#001f3f"  # Azul Marino Oscuro
COLOR_CUERPO        = "#f4f7f9"  # Gris muy claro
COLOR_PRIMARIO      = "#005187"  # Azul Corporativo
COLOR_ACCENTO       = "#00a8ff"  # Azul Brillante
COLOR_TEXTO         = "#2c3e50"  # Gris Oscuro
COLOR_BLANCO        = "#ffffff"
COLOR_TEXTO_GRIS    = "#8395A7"  # Texto secundario para el buscador
COLOR_BORDE         = "#DFE6E9"

def obtener_taller_id():
    """Lee el archivo de licencia para saber a qué taller pertenece esta PC"""
    try:
        with open("licencia.json", "r") as f:
            datos = json.load(f)
            return datos.get("taller_id")
    except:
        return None

# Configuración de rutas para recursos (Logo)
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

class PanelAdministrador:
    def __init__(self, id_admin=None):
        self.id_admin_logueado = id_admin if id_admin else 1
        self.ventana = tk.Tk()
        self.ventana.title("Ultracel Enterprise | Panel de Control")
        
        # 1. Configuramos el color de fondo primero
        self.ventana.configure(bg=COLOR_CUERPO)

        # 2. Establecemos un tamaño MÍNIMO para que no se rompa el diseño en pantallas chicas
        self.ventana.minsize(1024, 720)
        
        # 3. LA MAGIA: Intentar abrir maximizado directamente
        # En Windows usa 'zoomed', en Linux/Mac usa los attributes
        try:
            self.ventana.state('zoomed') 
        except:
            try:
                self.ventana.attributes('-zoomed', True)
            except:
                # Si todo falla (como en algunos gestores de ventana), 
                # usamos el tamaño máximo de la pantalla disponible
                width = self.ventana.winfo_screenwidth()
                height = self.ventana.winfo_screenheight()
                self.ventana.geometry(f"{width}x{height}+0+0")

        # Contenedores principales
        self.sidebar = tk.Frame(self.ventana, bg=COLOR_BARRA_LATERAL, width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main_content = tk.Frame(self.ventana, bg=COLOR_CUERPO)
        self.main_content.pack(side="right", fill="both", expand=True)

        self.setup_sidebar()
        self.crear_panel_principal() 

        self.ventana.mainloop()


    def mostrar_corte_caja(self):
        # 1. Limpiamos el panel principal
        for w in self.main_content.winfo_children(): 
            w.destroy()

        # --- Encabezado ---
        header = tk.Frame(self.main_content, bg=COLOR_BLANCO, height=80)
        header.pack(fill="x")
        
        tk.Button(header, text="⬅ REGRESAR", font=("Segoe UI", 10, "bold"), bg="#c0392b", fg="white",
                  relief="flat", command=self.crear_panel_principal, padx=10).pack(side="left", padx=20, pady=20)
                  
        tk.Label(header, text="Historial de Ventas y Corte de Caja", font=("Segoe UI Semilight", 22), 
                 bg=COLOR_BLANCO, fg=COLOR_TEXTO).pack(side="left", pady=20)

        # --- Contenedor Principal (2 Columnas) ---
        main_frame = tk.Frame(self.main_content, bg=COLOR_CUERPO)
        main_frame.pack(fill="both", expand=True, padx=40, pady=20)
        main_frame.grid_columnconfigure(0, weight=3)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_rowconfigure(0, weight=1)

        # --- COLUMNA IZQUIERDA: REGISTRO GENERAL ---
        col_izq = tk.Frame(main_frame, bg=COLOR_BLANCO, highlightthickness=1, highlightbackground="#d1d9e0")
        col_izq.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        # --- BUSCADOR EN VIVO ---
        filtro_frame = tk.Frame(col_izq, bg=COLOR_BLANCO)
        filtro_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(filtro_frame, text="🔍 Buscar (Fecha, Cliente o Vendedor):", font=("Segoe UI", 10, "bold"), bg=COLOR_BLANCO, fg=COLOR_TEXTO_GRIS).pack(side="left")
        busqueda_var = tk.StringVar()
        tk.Entry(filtro_frame, textvariable=busqueda_var, font=("Segoe UI", 10), width=30, bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDE).pack(side="left", padx=10, ipady=3)

        # --- MOTOR DE ORDENAMIENTO AL HACER CLIC EN COLUMNAS ---
        def ordenar_columna(tree, col, reverse):
            lista = [(tree.set(k, col), k) for k in tree.get_children('')]
            
            # Intentamos ordenar como números (para los totales con $)
            try:
                lista.sort(key=lambda t: float(t[0].replace('$', '').replace(',', '')), reverse=reverse)
            except ValueError:
                # Si falla, es porque es texto o fecha, entonces ordenamos alfabéticamente
                lista.sort(reverse=reverse)
                
            for index, (val, k) in enumerate(lista):
                tree.move(k, '', index)
                
            # Cambiamos la función para que el próximo clic ordene al revés
            tree.heading(col, command=lambda: ordenar_columna(tree, col, not reverse))
        tk.Label(col_izq, text="REGISTRO GENERAL DE VENTAS", font=("Segoe UI", 12, "bold"), bg=COLOR_BLANCO, fg=COLOR_PRIMARIO).pack(pady=10)
        
        tree_frame_v = tk.Frame(col_izq, bg=COLOR_BLANCO)
        tree_frame_v.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # OJO: Si tienes el Custom.Treeview importado úsalo, si no, quita el style=...
        style = ttk.Style()
        style.configure("Treeview", rowheight=40)
        
        tree_ventas = ttk.Treeview(tree_frame_v, columns=("ID", "Fecha", "Cliente", "Vendedor", "Total"), show="headings", style="Treeview")
        # Conectamos las columnas al motor de ordenamiento
        tree_ventas.heading("ID", text="ID Venta", command=lambda: ordenar_columna(tree_ventas, "ID", False))
        tree_ventas.column("ID", width=60, anchor="center")
        
        tree_ventas.heading("Fecha", text="Fecha", command=lambda: ordenar_columna(tree_ventas, "Fecha", False))
        tree_ventas.column("Fecha", width=120, anchor="center")
        
        tree_ventas.heading("Cliente", text="Cliente", command=lambda: ordenar_columna(tree_ventas, "Cliente", False))
        tree_ventas.column("Cliente", width=160)
        
        tree_ventas.heading("Vendedor", text="Vendedor", command=lambda: ordenar_columna(tree_ventas, "Vendedor", False))
        tree_ventas.column("Vendedor", width=120)
        
        tree_ventas.heading("Total", text="Total", command=lambda: ordenar_columna(tree_ventas, "Total", False))
        tree_ventas.column("Total", width=90, anchor="e")
        
        scroll_v = ttk.Scrollbar(tree_frame_v, orient="vertical", command=tree_ventas.yview)
        tree_ventas.configure(yscrollcommand=scroll_v.set)
        scroll_v.pack(side="right", fill="y")
        tree_ventas.pack(side="left", fill="both", expand=True)

        # --- COLUMNA DERECHA: DETALLES ---
        col_der = tk.Frame(main_frame, bg=COLOR_BLANCO, highlightthickness=1, highlightbackground="#d1d9e0")
        col_der.grid(row=0, column=1, sticky="nsew")
        
        tk.Label(col_der, text="DETALLES DE LA VENTA", font=("Segoe UI", 12, "bold"), bg=COLOR_BLANCO, fg=COLOR_PRIMARIO).pack(pady=10)
        
        tree_frame_d = tk.Frame(col_der, bg=COLOR_BLANCO)
        tree_frame_d.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        tree_detalles = ttk.Treeview(tree_frame_d, columns=("Cant", "Desc", "P. Unit", "Subtotal"), show="headings")
        tree_detalles.heading("Cant", text="Cant."); tree_detalles.column("Cant", width=40, anchor="center")
        
        # ¡AQUI ESTABA EL ERROR VISUAL! Hicimos la descripcion mucho más ancha
        tree_detalles.heading("Desc", text="Descripción"); tree_detalles.column("Desc", width=200) 
        
        tree_detalles.heading("P. Unit", text="P. Unit."); tree_detalles.column("P. Unit", width=80, anchor="e")
        tree_detalles.heading("Subtotal", text="Subtotal"); tree_detalles.column("Subtotal", width=80, anchor="e")
        
        scroll_d = ttk.Scrollbar(tree_frame_d, orient="vertical", command=tree_detalles.yview)
        tree_detalles.configure(yscrollcommand=scroll_d.set)
        scroll_d.pack(side="right", fill="y")
        tree_detalles.pack(side="left", fill="both", expand=True)

        ventas_originales = []
        # --- LÓGICA DE CARGA Y CÁLCULOS SEGUROS ---
        def cargar_datos():
            ventas_originales.clear()
            mi_taller_id = obtener_taller_id() 
            if not mi_taller_id: return
            
            try:
                res = requests.post("https://www.ultracel.lat/api/pos/historial-ventas", json={"taller_id": mi_taller_id})
                if res.status_code == 200:
                    for v in res.json().get('ventas', []):
                        monto_limpio = float(v['monto_total'])
                        # Guardamos en nuestra lista de respaldo
                        ventas_originales.append((v['id_venta'], v['fecha'], v['cliente'], v['vendedor'], f"${monto_limpio:,.2f}"))
                    
                    actualizar_tabla() # Llenamos la tabla por primera vez
            except Exception as e:
                print(f"Error cargando ventas: {e}")

        def actualizar_tabla(*args):
            for i in tree_ventas.get_children(): tree_ventas.delete(i)
            termino = busqueda_var.get().lower()
            
            for v in ventas_originales:
                # Buscamos coincidencias en cualquier columna (fecha, cliente, vendedor, etc.)
                if termino in str(v[0]).lower() or termino in v[1].lower() or termino in v[2].lower() or termino in v[3].lower():
                    tree_ventas.insert("", "end", values=v)

        # Hacemos que la tabla se actualice cada vez que se escribe en el buscador
        busqueda_var.trace_add("write", actualizar_tabla)

        def mostrar_detalles_venta(event):
            sel = tree_ventas.selection()
            if not sel: return
            id_venta = tree_ventas.item(sel[0], 'values')[0]
            
            for i in tree_detalles.get_children(): tree_detalles.delete(i)
            
            try:
                mi_taller_id = obtener_taller_id() # 🔒 SACAMOS EL PASE VIP
                res = requests.post("https://www.ultracel.lat/api/pos/detalles-venta", json={"id_venta": id_venta, "taller_id": mi_taller_id})
                if res.status_code == 200:
                    for d in res.json().get('detalles', []):
                        # Parche matemático para evitar el crash de strings
                        cantidad = int(d['cantidad'])
                        precio_unit = float(d['precio_unitario'])
                        subtotal = cantidad * precio_unit
                        
                        tree_detalles.insert("", "end", values=(
                            cantidad, d['descripcion_linea'],
                            f"${precio_unit:.2f}", f"${subtotal:.2f}"
                        ))
            except Exception as e:
                print(f"Error cargando detalles: {e}")

        tree_ventas.bind("<<TreeviewSelect>>", mostrar_detalles_venta)
        cargar_datos()

    

    # --- CONFIGURACIÓN DE BARRA LATERAL ---
    def setup_sidebar(self):
        # Logo
        try:
            logo_path = os.path.join(base_path, "assets", "logo_ultracel.png")
            logo_img = Image.open(logo_path).resize((100, 100))
            self.logo_tk = ImageTk.PhotoImage(logo_img)
            tk.Label(self.sidebar, image=self.logo_tk, bg=COLOR_BARRA_LATERAL).pack(pady=30)
        except:
            tk.Label(self.sidebar, text="panel", font=("Arial", 20, "bold"), 
                     bg=COLOR_BARRA_LATERAL, fg="white").pack(pady=30)

        # Estilo de botones del menú
        btn_opts = {
            "font": ("Segoe UI", 11),
            "bg": COLOR_BARRA_LATERAL,
            "fg": "white",
            "activebackground": COLOR_PRIMARIO,
            "activeforeground": "white",
            "relief": "flat",
            "anchor": "w",
            "padx": 25,
            "pady": 15,
            "cursor": "hand2"
        }

        # Botones de navegación
        tk.Button(self.sidebar, text="🏠  Inicio ", command=self.crear_panel_principal, **btn_opts).pack(fill="x")
        tk.Button(self.sidebar, text="👤  Agregar Nuevo Usuario", command=self.agregar_usuarios, **btn_opts).pack(fill="x")
        tk.Button(self.sidebar, text="🔒  Administrar Usuarios", command=self.admin_usuarios, **btn_opts).pack(fill="x")
        tk.Button(self.sidebar, text="📊  Reportes de Material", command=self.ver_reportes_material, **btn_opts).pack(fill="x")

        # Botón Cerrar Sesión
        def confirmar_salida():
            if messagebox.askyesno("Confirmación", "¿Deseas cerrar sesión y volver al inicio?"):
                self.ventana.destroy()
                
                # Lanzamos el Login de nuevo
                import subprocess
                import sys
                subprocess.Popen([sys.executable, "Login.py"])

        tk.Button(self.sidebar, text="⏻  Cerrar Sesión", bg="#c0392b", fg="white", 
                  font=("Segoe UI", 11, "bold"), relief="flat", command=confirmar_salida).pack(side="bottom", fill="x", pady=20)

    # --- 1. VISTA: DASHBOARD PRINCIPAL ---
    def crear_panel_principal(self):
        for w in self.main_content.winfo_children(): w.destroy()
        
        header = tk.Frame(self.main_content, bg=COLOR_BLANCO, height=80)
        header.pack(fill="x")
        tk.Label(header, text="Panel de Control Principal", font=("Segoe UI Semilight", 22), 
                 bg=COLOR_BLANCO, fg=COLOR_TEXTO).pack(side="left", padx=40, pady=20)

        dash_frame = tk.Frame(self.main_content, bg=COLOR_CUERPO)
        dash_frame.pack(fill="both", expand=True, padx=40, pady=40)

        # Tarjeta de Corte de Caja
        card = tk.Frame(dash_frame, bg=COLOR_BLANCO, width=320, height=200, highlightthickness=1, highlightbackground="#d1d9e0")
        card.pack(side="left", padx=10, anchor="n")
        card.pack_propagate(False)

        tk.Label(card, text="Corte de Caja", font=("Segoe UI", 14, "bold"), bg=COLOR_BLANCO, fg=COLOR_PRIMARIO).pack(pady=(30, 10))
        tk.Label(card, text="Generar el reporte de ventas del día.", font=("Segoe UI", 10), bg=COLOR_BLANCO, fg="#7f8c8d").pack(pady=5)
        
        tk.Button(card, text="EJECUTAR CORTE", font=("Segoe UI", 10, "bold"), bg=COLOR_ACCENTO, 
                  fg="white", relief="flat", padx=20, cursor="hand2", 
                  command=self.mostrar_corte_caja).pack(pady=20)

    # --- 2. VISTA: ADMINISTRACIÓN DE USUARIOS (TARJETAS) ---
    def admin_usuarios(self):
        for w in self.main_content.winfo_children(): w.destroy()
        
        header = tk.Frame(self.main_content, bg=COLOR_CUERPO)
        header.pack(fill="x", padx=40, pady=25)
        tk.Label(header, text="Gestión de Usuarios", font=("Segoe UI", 24, "bold"), 
                 bg=COLOR_CUERPO, fg=COLOR_TEXTO).pack(side="left")

        # Contenedor con Scroll
        container = tk.Frame(self.main_content, bg=COLOR_CUERPO)
        container.pack(fill="both", expand=True, padx=40)

        canvas = tk.Canvas(container, bg=COLOR_CUERPO, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_CUERPO)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=850)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def cargar_cards():
            # Limpiamos las tarjetas anteriores
            for w in scrollable_frame.winfo_children(): w.destroy()
            
            # 1. Sacamos el ID del taller de nuestra licencia
            mi_taller_id = obtener_taller_id()
            if not mi_taller_id:
                messagebox.showerror("Error", "No se encontró la licencia. Activa el software primero.")
                return

            try:
                # 2. Le pedimos a Laravel la lista de empleados de este taller
                url_api = "https://www.ultracel.lat/api/empleados"
                respuesta = requests.post(url_api, json={"taller_id": mi_taller_id})
                
                if respuesta.status_code == 200:
                    datos = respuesta.json()
                    empleados = datos.get('empleados', [])
                    
                    # 3. Dibujamos las tarjetas con la información que nos dio Laravel
                    for u in empleados:
                        card = tk.Frame(scrollable_frame, bg=COLOR_BLANCO, pady=15, highlightthickness=1, highlightbackground="#dfe6e9")
                        card.pack(fill="x", pady=8)
                        
                        # NOTA: Ajusté los nombres de las variables (como 'name' y 'email') 
                        # para que coincidan con la estructura estándar de la tabla 'users' de Laravel
                        estado = u.get('permitido', 1) # Si no existe, asume 1 (verde)
                        status_color = "#27ae60" if estado else "#e74c3c"
                        tk.Frame(card, bg=status_color, width=6).pack(side="left", fill="y")

                        info = tk.Frame(card, bg=COLOR_BLANCO, padx=20)
                        info.pack(side="left", fill="both")
                        
                        nombre = u.get('name', 'Usuario sin nombre')
                        correo = u.get('email', 'Sin correo')
                        rol = u.get('rol', 'Sin Rol')
                        id_u = u.get('id')

                        tk.Label(info, text=nombre, font=("Segoe UI", 13, "bold"), bg=COLOR_BLANCO).pack(anchor="w")
                        tk.Label(info, text=f"Rol: {rol}  |  Usuario: @{correo}", font=("Segoe UI", 10), 
                                 bg=COLOR_BLANCO, fg="#7f8c8d").pack(anchor="w")

                        # Botón de gestionar
                        tk.Button(card, text="⚙️ Gestionar", font=("Segoe UI", 10), bg="#f1f2f6", relief="flat", padx=20, 
                                  command=lambda id_seleccionado=id_u: self.editar_usuario_modal(id_seleccionado)).pack(side="right", padx=30)
                else:
                    messagebox.showerror("Error API", "No se pudo cargar la lista de empleados.")
                    
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error de Red", "Asegúrate de que Docker y Laravel estén encendidos.")

        cargar_cards()

    # --- 3. MODAL: EDITAR USUARIO ---
    # --- 3. MODAL: EDITAR USUARIO ---
    # --- 3. MODAL: EDITAR USUARIO ---
    def editar_usuario_modal(self, id_u):
        # 1. Obtenemos los datos del usuario desde Laravel
        mi_taller_id = obtener_taller_id() # 🔒 SACAMOS EL PASE VIP
        try:
            res = requests.post("https://www.ultracel.lat/api/empleado/ver", json={"id": id_u, "taller_id": mi_taller_id})
            if res.status_code != 200:
                return messagebox.showerror("Error", "No se pudo cargar el usuario.")
            u = res.json().get('empleado', {})
        except requests.exceptions.ConnectionError:
            return messagebox.showerror("Error", "Sin conexión al servidor.")

        # --- ADIÓS TOPLEVEL, HOLA PANEL DINÁMICO ---
        # Limpiamos el área de trabajo (Usando la lógica correcta del Administrador)
        for w in self.main_content.winfo_children(): w.destroy()
        
        # Usamos main_content en lugar de panel_dinamico
        contenedor = tk.Frame(self.main_content, bg=COLOR_BLANCO)
        contenedor.pack(fill="both", expand=True) 

        # --- ENCABEZADO Y BOTÓN DE REGRESAR ---
        header = tk.Frame(contenedor, bg=COLOR_BLANCO)
        header.pack(fill="x", padx=40, pady=(30, 10))
        
        tk.Button(header, text="⬅ REGRESAR", font=("Segoe UI", 10, "bold"), bg="#95a5a6", fg="white", 
                  relief="flat", command=self.admin_usuarios, padx=15).pack(side="left")
        
        tk.Label(header, text="EDITAR PERFIL DE USUARIO", font=("Segoe UI", 18, "bold"), 
                 bg=COLOR_BLANCO, fg=COLOR_PRIMARIO).pack(side="left", padx=20)

        # --- CONTENEDOR CENTRAL DEL FORMULARIO ---
        form = tk.Frame(contenedor, bg=COLOR_BLANCO)
        form.pack(fill="x", padx=100, pady=20) 

        entries = {}
        campos = {
            'email': ('Usuario Login (Email):', u.get('email', '')), 
            'name': ('Nombre Completo:', u.get('name', '')), 
            'especialidad': ('Especialidad:', u.get('especialidad', ''))
        }
        
        for key, (lbl, val) in campos.items():
            tk.Label(form, text=lbl, bg=COLOR_BLANCO, font=("Segoe UI", 10, "bold"), fg="#666").pack(anchor="w")
            e = tk.Entry(form, font=("Segoe UI", 12), bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9")
            
            # Parche anti-berrinches
            texto_seguro = val if val is not None else ""
            e.insert(0, texto_seguro)
            
            e.pack(fill="x", pady=(5, 15), ipady=8)
            entries[key] = e

        # --- CAMPO DE CONTRASEÑA NUEVA ---
        tk.Label(form, text="Nueva Contraseña (Dejar en blanco para conservar la actual):", 
                 bg=COLOR_BLANCO, font=("Segoe UI", 10, "bold"), fg="#e74c3c").pack(anchor="w", pady=(10, 0))
        entry_pass = tk.Entry(form, font=("Segoe UI", 12), bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", show="*")
        entry_pass.pack(fill="x", pady=(5, 15), ipady=8)

        # --- ROLES Y PERMISOS ---
        roles_frame = tk.Frame(form, bg=COLOR_BLANCO)
        roles_frame.pack(fill="x", pady=10)

        tk.Label(roles_frame, text="Rol del Sistema:", bg=COLOR_BLANCO, font=("Segoe UI", 10, "bold"), fg="#666").pack(side="left")
        rol_var = tk.StringVar(value=u.get('rol', 'Vendedor'))
        ttk.Combobox(roles_frame, textvariable=rol_var, values=["Admin", "Tecnico", "Vendedor", "Repartidor"], state="readonly", width=15, font=("Segoe UI", 11)).pack(side="left", padx=10)

        perm_var = tk.BooleanVar(value=bool(u.get('permitido', 1)))
        tk.Checkbutton(roles_frame, text="¿Habilitar acceso al sistema?", variable=perm_var, bg=COLOR_BLANCO, font=("Segoe UI", 11, "bold"), fg="#27ae60").pack(side="left", padx=40)

        # --- LÓGICA DE GUARDADO ---
        # --- LÓGICA DE GUARDADO ---
        def salvar():
            payload = {
                "id": id_u,
                "email": entries['email'].get(),
                "name": entries['name'].get(),
                "especialidad": entries['especialidad'].get(),
                "rol": rol_var.get(),
                "permitido": 1 if perm_var.get() else 0,
                "password": entry_pass.get(),
                "taller_id": mi_taller_id # 🔒 CANDADO AÑADIDO AL PAYLOAD
            }
            try:
                res_save = requests.post("https://www.ultracel.lat/api/empleado/actualizar", json=payload)
                if res_save.status_code == 200:
                    messagebox.showinfo("Éxito", "El perfil se actualizó correctamente.")
                    self.admin_usuarios() 
                else:
                    # ¡AQUÍ ESTÁ LA MAGIA CHISMOSA!
                    try:
                        # Intentamos sacar el error exacto que manda Laravel
                        detalle_error = res_save.json().get('message', res_save.text)
                    except:
                        # Si Laravel colapsó feo, mandamos el texto crudo
                        detalle_error = res_save.text
                        
                    messagebox.showerror(f"Error {res_save.status_code}", f"Laravel dice:\n\n{detalle_error}")
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "Error de conexión con el servidor.")

        tk.Button(form, text="GUARDAR CAMBIOS", bg=COLOR_PRIMARIO, fg="white", 
                  font=("Segoe UI", 12, "bold"), relief="flat", command=salvar).pack(pady=30, fill="x")

    # --- 4. MODAL: AGREGAR NUEVO USUARIO ---
    def agregar_usuarios(self):
        # Necesitamos saber a qué taller pertenece este nuevo usuario
        mi_taller_id = obtener_taller_id()
        if not mi_taller_id:
            return messagebox.showerror("Error", "No hay licencia activa.")

        # --- ADIÓS TOPLEVEL, HOLA PANEL DINÁMICO ---
        # Limpiamos el área de trabajo
        for w in self.main_content.winfo_children(): w.destroy()

        contenedor = tk.Frame(self.main_content, bg=COLOR_BLANCO)
        contenedor.pack(fill="both", expand=True)

        # --- ENCABEZADO Y BOTÓN DE REGRESAR ---
        header = tk.Frame(contenedor, bg=COLOR_BLANCO)
        header.pack(fill="x", padx=40, pady=(30, 10))
        
        tk.Button(header, text="⬅ REGRESAR", font=("Segoe UI", 10, "bold"), bg="#95a5a6", fg="white", 
                  relief="flat", command=self.admin_usuarios, padx=15).pack(side="left")
        
        tk.Label(header, text="REGISTRAR NUEVO USUARIO", font=("Segoe UI", 18, "bold"), 
                 bg=COLOR_BLANCO, fg=COLOR_PRIMARIO).pack(side="left", padx=20)

        # --- CONTENEDOR CENTRAL DEL FORMULARIO ---
        form = tk.Frame(contenedor, bg=COLOR_BLANCO)
        form.pack(fill="x", padx=100, pady=20) 

        entries = {}
        campos = {
            'email': 'Usuario Login (Email):', 
            'name': 'Nombre Completo:', 
            'especialidad': 'Especialidad (Opcional):'
        }

        for key, text in campos.items():
            tk.Label(form, text=text, font=("Segoe UI", 10, "bold"), bg=COLOR_BLANCO, fg="#666").pack(anchor="w")
            e = tk.Entry(form, font=("Segoe UI", 12), bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9")
            e.pack(fill="x", pady=(5, 15), ipady=8)
            entries[key] = e

        # --- CAMPO DE CONTRASEÑA ---
        tk.Label(form, text="Contraseña (Dejar en blanco para generar una aleatoria):", 
                 bg=COLOR_BLANCO, font=("Segoe UI", 10, "bold"), fg="#e74c3c").pack(anchor="w", pady=(10, 0))
        entry_pass = tk.Entry(form, font=("Segoe UI", 12), bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9")
        entry_pass.pack(fill="x", pady=(5, 15), ipady=8)

        # --- ROLES ---
        roles_frame = tk.Frame(form, bg=COLOR_BLANCO)
        roles_frame.pack(fill="x", pady=10)

        tk.Label(roles_frame, text="Rol del Sistema:", font=("Segoe UI", 10, "bold"), bg=COLOR_BLANCO, fg="#666").pack(side="left")
        rol_var = tk.StringVar(value="Vendedor")
        ttk.Combobox(roles_frame, textvariable=rol_var, values=["Admin", "Tecnico", "Vendedor", "Repartidor"], state="readonly", width=15, font=("Segoe UI", 11)).pack(side="left", padx=10)

        # --- LÓGICA DE GUARDADO ---
        def guardar():
            # Si el campo está vacío, genera la contraseña aleatoria como lo tenías antes
            passw_ingresada = entry_pass.get()
            passw_final = passw_ingresada if passw_ingresada else ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            if not entries['email'].get() or not entries['name'].get():
                return messagebox.showwarning("Faltan datos", "Complete los campos obligatorios (Email y Nombre).")

            payload = {
                "email": entries['email'].get(),
                "name": entries['name'].get(),
                "especialidad": entries['especialidad'].get(),
                "rol": rol_var.get(),
                "password": passw_final,
                "taller_id": mi_taller_id
            }

            try:
                res = requests.post("https://www.ultracel.lat/api/empleado/crear", json=payload)
                if res.status_code == 200:
                    # Armamos el mensaje de éxito dependiendo de si fue manual o aleatoria
                    msg = f"Usuario creado exitosamente.\n\nUsuario: {entries['email'].get()}\nContraseña: {passw_final}"
                    if not passw_ingresada:
                        msg += "\n\n¡Guarda esta contraseña temporal, se generó automáticamente!"
                    
                    messagebox.showinfo("Registro Exitoso", msg)
                    self.admin_usuarios() # Recargar tabla principal y regresar a la vista anterior
                else:
                    messagebox.showerror("Error", "No se pudo crear. Asegúrate de que el email no esté repetido.")
            except Exception as e: 
                messagebox.showerror("Error", "Problema al conectar con la API.")

        tk.Button(form, text="CREAR USUARIO", bg=COLOR_PRIMARIO, fg="white", 
                  font=("Segoe UI", 12, "bold"), relief="flat", command=guardar).pack(pady=35, fill="x")
    # --- 5. VISTA: REPORTES DE MATERIAL ---
    def ver_reportes_material(self):
        for w in self.main_content.winfo_children(): w.destroy()
        
        header = tk.Frame(self.main_content, bg=COLOR_CUERPO)
        header.pack(fill="x", padx=40, pady=25)
        tk.Label(header, text="Solicitudes de Material", font=("Segoe UI", 24, "bold"), 
                 bg=COLOR_CUERPO, fg=COLOR_TEXTO).pack(side="left")

        # Estilo de Tabla
        frame_tabla = tk.Frame(self.main_content, bg=COLOR_BLANCO, bd=1, relief="solid")
        frame_tabla.pack(fill="both", expand=True, padx=40, pady=10)

        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

        columnas = ("ID", "Fecha", "Técnico", "Producto", "Cantidad", "Estado")
        tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="browse")
        
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=130)

        tree.pack(side="left", fill="both", expand=True)
        
        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

        def cargar_datos():
            for i in tree.get_children(): tree.delete(i)
            
            mi_taller_id = obtener_taller_id()
            if not mi_taller_id: return
            
            try:
                res = requests.post("https://www.ultracel.lat/api/material/admin-listar", json={"taller_id": mi_taller_id})
                if res.status_code == 200:
                    for r in res.json().get('solicitudes', []):
                        tree.insert("", "end", values=(
                            r['id_solicitud'], 
                            r['fecha'], 
                            r['nombre_completo'], 
                            r['nombre_producto'], 
                            r['cantidad_solicitada'], 
                            r['estado_solicitud']
                        ))
            except requests.exceptions.ConnectionError:
                pass # Evitamos spam visual

        def actualizar_estado(nuevo):
            sel = tree.selection()
            if not sel: 
                return messagebox.showwarning("Selección", "Elige una solicitud.")
            
            # Extraemos el ID de la solicitud seleccionada
            id_s = tree.item(sel[0])['values'][0]
            
            try:
                mi_taller_id = obtener_taller_id() # 🔒 SACAMOS EL PASE VIP
                payload = {
                    "id_solicitud": id_s,
                    "estado": nuevo,
                    "taller_id": mi_taller_id # 🔒 CANDADO AÑADIDO
                }
                res = requests.post("https://www.ultracel.lat/api/material/actualizar-estado", json=payload)
                
                if res.status_code == 200:
                    messagebox.showinfo("Éxito", f"La solicitud ha sido marcada como '{nuevo}'.")
                    cargar_datos() # Recargamos la tabla automáticamente
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el estado de la solicitud.")
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "Fallo de conexión al servidor.")

        # Botones inferioresz
        btn_f = tk.Frame(self.main_content, bg=COLOR_CUERPO)
        btn_f.pack(fill="x", padx=40, pady=25)

        tk.Button(btn_f, text="✅ APROBAR", bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=20, command=lambda: actualizar_estado("Aprobada")).pack(side="left", padx=5)
        tk.Button(btn_f, text="❌ RECHAZAR", bg="#e74c3c", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=20, command=lambda: actualizar_estado("Rechazada")).pack(side="left", padx=5)
        
        tk.Button(btn_f, text="📥 EXCEL", bg="#006400", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=20, command=lambda: self.exportar_excel(tree)).pack(side="right", padx=5)
        tk.Button(btn_f, text="🔄 RECARGAR", bg=COLOR_PRIMARIO, fg="white", font=("Segoe UI", 10), relief="flat", padx=20, command=cargar_datos).pack(side="right", padx=5)

        cargar_datos()

    def exportar_excel(self, tree):
        data = [tree.item(c)["values"] for c in tree.get_children()]
        if not data: return messagebox.showwarning("Vacío", "No hay datos para exportar.")
        
        df = pd.DataFrame(data, columns=["ID", "Fecha", "Técnico", "Producto", "Cantidad", "Estado"])
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if path:
            df.to_excel(path, index=False)
            messagebox.showinfo("Guardado", "El reporte se ha exportado con éxito.")

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que deseas salir y volver al Login?"):
            
            self.root.destroy() 
            
            
            import subprocess
            import sys
            subprocess.Popen([sys.executable, "Login.py"])

if __name__ == "__main__":
    id_logueado = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    app = PanelAdministrador(id_admin=id_logueado)