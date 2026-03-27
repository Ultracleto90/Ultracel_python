from PIL import Image, ImageTk, ImageFilter
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import sys
import requests
import json
# --- PALETA DE COLORES PROFESIONAL ---
COLOR_PRIMARIO       = "#1B2A4A"   # Azul marino oscuro (header, acentos fuertes)
COLOR_SECUNDARIO     = "#2E86DE"   # Azul vibrante (botones principales)
COLOR_ACENTO         = "#54A0FF"   # Azul claro (hover, acentos suaves)
COLOR_EXITO          = "#10AC84"   # Verde elegante (guardar, confirmar)
COLOR_PELIGRO        = "#EE5A24"   # Naranja-rojo (eliminar, cerrar sesion)
COLOR_ADVERTENCIA    = "#F6B93B"   # Amarillo dorado (advertencias)
COLOR_TEXTO_OSCURO   = "#2C3A4B"   # Texto principal
COLOR_TEXTO_GRIS     = "#8395A7"   # Texto secundario / subtitulos
COLOR_TEXTO_BLANCO   = "#FFFFFF"   # Texto sobre fondos oscuros
COLOR_FONDO_APP      = "#F1F2F6"   # Fondo general de la app
COLOR_FONDO_PANEL    = "#FFFFFF"   # Fondo del panel flotante
COLOR_FONDO_SECCION  = "#F8F9FA"   # Fondo sutil para secciones internas
COLOR_BORDE          = "#DFE6E9"   # Bordes sutiles
COLOR_MENU_BG        = "#1B2A4A"   # Fondo del menu lateral
COLOR_MENU_HOVER     = "#2E4066"   # Hover en el menu lateral
COLOR_FILA_PAR       = "#FFFFFF"   # Filas pares en tablas
COLOR_FILA_IMPAR     = "#F0F6FF"   # Filas impares en tablas (azul muy tenue)
COLOR_SELECCION      = "#D6EAF8"   # Color de seleccion en tablas
COLOR_NOTA_VENTA_BG  = "#EAF2F8"   # Fondo nota de venta
# --- FUENTES ---
FUENTE_TITULO        = ("Segoe UI", 16, "bold")
FUENTE_SUBTITULO     = ("Segoe UI", 12, "bold")
FUENTE_CUERPO        = ("Segoe UI", 10)
FUENTE_CUERPO_BOLD   = ("Segoe UI", 10, "bold")
FUENTE_BOTON         = ("Segoe UI", 11, "bold")
FUENTE_MENU          = ("Segoe UI", 11)
FUENTE_MENU_TITULO   = ("Segoe UI", 15, "bold")
FUENTE_ETIQUETA      = ("Segoe UI", 9)
FUENTE_TABLA         = ("Segoe UI", 9)
FUENTE_TABLA_HEAD    = ("Segoe UI", 10, "bold")
FUENTE_TOTAL         = ("Segoe UI", 18, "bold")

def obtener_taller_id():
    """Lee el archivo de licencia para saber a qué taller pertenece esta PC"""
    try:
        with open("licencia.json", "r") as f:
            datos = json.load(f)
            return datos.get("taller_id")
    except:
        return None
def configurar_estilos_ttk():
    """Configura los estilos ttk para Treeview, Combobox, Scrollbar, etc."""
    style = ttk.Style()
    style.theme_use("clam")
    # --- Treeview ---
    style.configure("Custom.Treeview",
                    background=COLOR_FILA_PAR,
                    foreground=COLOR_TEXTO_OSCURO,
                    fieldbackground=COLOR_FILA_PAR,
                    rowheight=30,
                    font=FUENTE_TABLA,
                    borderwidth=0)
    style.configure("Custom.Treeview.Heading",
                    background=COLOR_PRIMARIO,
                    foreground=COLOR_TEXTO_BLANCO,
                    font=FUENTE_TABLA_HEAD,
                    relief="flat",
                    padding=(8, 6))
    style.map("Custom.Treeview.Heading",
              background=[("active", COLOR_SECUNDARIO)])
    style.map("Custom.Treeview",
              background=[("selected", COLOR_SELECCION)],
              foreground=[("selected", COLOR_TEXTO_OSCURO)])
    # --- Combobox ---
    style.configure("Custom.TCombobox",
                    fieldbackground=COLOR_TEXTO_BLANCO,
                    background=COLOR_SECUNDARIO,
                    foreground=COLOR_TEXTO_OSCURO,
                    arrowcolor=COLOR_SECUNDARIO,
                    padding=6)
    style.map("Custom.TCombobox",
              fieldbackground=[("readonly", COLOR_TEXTO_BLANCO)],
              selectbackground=[("readonly", COLOR_SELECCION)])
    # --- Scrollbar ---
    style.configure("Custom.Vertical.TScrollbar",
                    gripcount=0,
                    background=COLOR_BORDE,
                    troughcolor=COLOR_FONDO_APP,
                    borderwidth=0,
                    arrowsize=14)
    style.map("Custom.Vertical.TScrollbar",
              background=[("active", COLOR_ACENTO), ("!active", "#C8D6E5")])
def crear_boton(parent, texto, comando, color_bg, color_fg=None,
                fuente=None, height=1, ancho=None, padx_btn=12, pady_btn=6):
    """Crea un boton estilizado con efecto hover."""
    if color_fg is None:
        color_fg = COLOR_TEXTO_BLANCO
    if fuente is None:
        fuente = FUENTE_BOTON
    btn = tk.Button(parent, text=texto, font=fuente, bg=color_bg, fg=color_fg,
                    activebackground=color_bg, activeforeground=color_fg,
                    relief="flat", cursor="hand2", bd=0,
                    height=height, command=comando)
    if ancho:
        btn.configure(width=ancho)
    btn.configure(padx=padx_btn, pady=pady_btn)
    def on_enter(e):
        btn.configure(bg=_aclarar_color(color_bg, 25))
    def on_leave(e):
        btn.configure(bg=color_bg)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn
def crear_entry_estilizado(parent, font=None, width=None, textvariable=None):
    """Crea un Entry con borde sutil y padding."""
    if font is None:
        font = FUENTE_CUERPO
    frame = tk.Frame(parent, bg=COLOR_BORDE, bd=0, highlightthickness=0)
    kwargs = dict(font=font, bd=0, bg=COLOR_TEXTO_BLANCO,
                  fg=COLOR_TEXTO_OSCURO, insertbackground=COLOR_SECUNDARIO,
                  highlightthickness=0)
    if width:
        kwargs['width'] = width
    if textvariable:
        kwargs['textvariable'] = textvariable
    entry = tk.Entry(frame, **kwargs)
    entry.pack(fill="x", padx=1, pady=1, ipady=6)
    return frame, entry
def crear_text_estilizado(parent, height=3, font=None):
    """Crea un Text widget con borde sutil."""
    if font is None:
        font = FUENTE_CUERPO
    frame = tk.Frame(parent, bg=COLOR_BORDE, bd=0, highlightthickness=0)
    text_widget = tk.Text(frame, height=height, font=font, bd=0,
                          bg=COLOR_TEXTO_BLANCO, fg=COLOR_TEXTO_OSCURO,
                          insertbackground=COLOR_SECUNDARIO,
                          highlightthickness=0, padx=8, pady=6)
    text_widget.pack(fill="x", padx=1, pady=1)
    return frame, text_widget
def _aclarar_color(hex_color, cantidad=30):
    """Aclara un color hexadecimal."""
    hex_color = hex_color.lstrip('#')
    r = min(255, int(hex_color[0:2], 16) + cantidad)
    g = min(255, int(hex_color[2:4], 16) + cantidad)
    b = min(255, int(hex_color[4:6], 16) + cantidad)
    return f"#{r:02x}{g:02x}{b:02x}"
class PanelVendedor:
    
    def __init__(self, id_vendedor=None):
        self.id_vendedor_logueado = id_vendedor if id_vendedor else 1
        self.ventana = tk.Tk()
        self.ventana.title("Panel Vendedor - ULTRA-CEL")
        self.ventana.geometry("1100x700")
        self.ventana.minsize(900, 600)
        self.ventana.resizable(True, True)
        self.ventana.configure(bg=COLOR_FONDO_APP)
        self.ventana.geometry("1000x600") # Tamaño base
        self.ventana.minsize(900, 600)
        
        # --- ABRIR MAXIMIZADO SIEMPRE ---
        try:
            self.ventana.state('zoomed')
        except:
            self.ventana.attributes('-zoomed', True)
        configurar_estilos_ttk()
        
        self.tree_reparaciones = None
        self.tree_clientes = None
        self.tree_inventario = None
        self.total_var = tk.StringVar(value="$0.00")
        
        # --- Creacion de la Interfaz Base ---
        try:
            if getattr(sys, 'frozen', False): base_path = sys._MEIPASS
            else: base_path = os.path.dirname(__file__)
            image_path = os.path.join(base_path, "assets", "fondo.png")
            fondo = Image.open(image_path).resize((1100, 700))
            fondo_blur = fondo.filter(ImageFilter.GaussianBlur(10))
            self.fondo_img = ImageTk.PhotoImage(fondo_blur)
            self.canvas_fondo = tk.Canvas(self.ventana, width=1100, height=700, highlightthickness=0)
            self.canvas_fondo.pack(fill="both", expand=True)
            self.canvas_fondo.create_image(0, 0, anchor="nw", image=self.fondo_img)
            self._overlay_id = self.canvas_fondo.create_rectangle(0, 0, 1100, 700, fill=COLOR_FONDO_APP, stipple="gray25", outline="")
        except Exception as e:
            print(f"Error cargando fondo: {e}")
            self.ventana.configure(bg=COLOR_FONDO_APP)
            self.canvas_fondo = tk.Canvas(self.ventana, width=1100, height=700,
                                          highlightthickness=0, bg=COLOR_FONDO_APP)
            self.canvas_fondo.pack(fill="both", expand=True)
            self._overlay_id = None
        # --- Panel flotante con sombra sutil ---
        self._shadow_id = self.canvas_fondo.create_rectangle(28, 28, 1078, 678,
                                           fill="#C8D6E5", outline="", stipple="gray12")
        self.panel_flotante = tk.Frame(self.canvas_fondo, bg=COLOR_FONDO_PANEL,
                                       highlightbackground=COLOR_BORDE,
                                       highlightthickness=1)
        self._panel_win_id = self.canvas_fondo.create_window(550, 350, window=self.panel_flotante,
                                        anchor="center", width=1050, height=650)
        
        self.menu_visible = False
        # --- Boton Hamburguesa estilizado ---
        self.boton_menu = tk.Button(self.panel_flotante, text="  \u2630  Menu  ",
                                    font=FUENTE_MENU, bg=COLOR_PRIMARIO,
                                    fg=COLOR_TEXTO_BLANCO, relief="flat",
                                    cursor="hand2", bd=0, padx=10, pady=4,
                                    activebackground=COLOR_MENU_HOVER,
                                    activeforeground=COLOR_TEXTO_BLANCO,
                                    command=self.toggle_menu)
        self.boton_menu.place(x=10, y=10)
        
        # --- Menu lateral ---
        self.menu_lateral = tk.Frame(self.canvas_fondo, bg=COLOR_MENU_BG, width=0)
        self.menu_lateral.place(x=0, y=0, relheight=1)
        self.menu_lateral.pack_propagate(False)
        self.crear_menu_lateral()
        
        # --- Panel dinamico (contenido principal) ---
        self.panel_dinamico = tk.Frame(self.panel_flotante, bg=COLOR_FONDO_PANEL)
        self.panel_dinamico.place(x=0, y=60, relwidth=1.0, relheight=1.0, height=-60)
        self.panel_dinamico.grid_rowconfigure(0, weight=1)
        self.panel_dinamico.grid_columnconfigure(0, weight=1)
        # --- Responsividad ---
        self.canvas_fondo.bind("<Configure>", self._on_resize)
        
        self.mostrar_venta_rapida()
        self.ventana.mainloop()
    def _on_resize(self, event):
        """Actualiza los elementos del canvas al redimensionar la ventana."""
        w = event.width
        h = event.height
        # Overlay de fondo
        if hasattr(self, '_overlay_id') and self._overlay_id:
            self.canvas_fondo.coords(self._overlay_id, 0, 0, w, h)
        # Sombra del panel
        margen = 25
        self.canvas_fondo.coords(self._shadow_id, margen + 3, margen + 3, w - margen + 3, h - margen + 3)
        # Panel flotante centrado
        self.canvas_fondo.coords(self._panel_win_id, w / 2, h / 2)
        self.canvas_fondo.itemconfigure(self._panel_win_id, width=w - margen * 2, height=h - margen * 2)
    def toggle_menu(self):
        target_width = 200 if not self.menu_visible else 0
        step = 15
        current_width = self.menu_lateral.winfo_width()
        def animate():
            nonlocal current_width
            if self.menu_visible and current_width > target_width: current_width -= step
            elif not self.menu_visible and current_width < target_width: current_width += step
            else: current_width = target_width
            self.menu_lateral.place_configure(width=current_width)
            if current_width != target_width: self.ventana.after(10, animate)
            else: self.menu_visible = not self.menu_visible
        animate()

    def crear_menu_lateral(self):
        self.menu_lateral.configure(bg=COLOR_MENU_BG)
        # --- Encabezado del menu ---
        header_frame = tk.Frame(self.menu_lateral, bg=COLOR_MENU_BG)
        header_frame.pack(fill="x", pady=(25, 5))
        tk.Label(header_frame, text="ULTRA-CEL", font=FUENTE_MENU_TITULO,
                 bg=COLOR_MENU_BG, fg=COLOR_TEXTO_BLANCO).pack()
        tk.Label(header_frame, text="Panel Vendedor", font=FUENTE_ETIQUETA,
                 bg=COLOR_MENU_BG, fg=COLOR_ACENTO).pack()
        # Separador
        sep_frame = tk.Frame(self.menu_lateral, bg=COLOR_MENU_HOVER, height=1)
        sep_frame.pack(fill="x", padx=20, pady=(15, 10))
        # --- Opciones del menu ---
        opciones = [
            ("\u2B05  Regresar",             self.toggle_menu),
            ("\U0001F6D2  Realizar Venta",    self.mostrar_venta_rapida),
            ("\U0001F4DC  Historial Ventas",  self.mostrar_historial),
            ("\U0001F4E6  Inventario",        self.mostrar_inventario),
            ("\U0001F465  Admin Clientes",    self.mostrar_admin_clientes),
            ("\U0001F4F1  Nuevo dispositivo", self.agregar_celular_nuevo)
        ]
        for texto, comando in opciones:
            btn_frame = tk.Frame(self.menu_lateral, bg=COLOR_MENU_BG)
            btn_frame.pack(fill="x")
            def combinado(c=comando, t=texto):
                c()
                if t != "\u2B05  Regresar":
                    self.toggle_menu()
            btn = tk.Button(btn_frame, text=texto, anchor="w",
                            bg=COLOR_MENU_BG, fg=COLOR_TEXTO_BLANCO, relief="flat",
                            font=FUENTE_MENU, padx=25, pady=12, bd=0,
                            activebackground=COLOR_MENU_HOVER,
                            activeforeground=COLOR_TEXTO_BLANCO, cursor="hand2",
                            command=combinado)
            btn.pack(fill="x")
            # Hover effect
            def on_enter(e, b=btn, f=btn_frame):
                b.configure(bg=COLOR_MENU_HOVER)
                f.configure(bg=COLOR_MENU_HOVER)
            def on_leave(e, b=btn, f=btn_frame):
                b.configure(bg=COLOR_MENU_BG)
                f.configure(bg=COLOR_MENU_BG)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        # --- Boton Salir (fijado al fondo) ---
        def salir_a_login():
            if messagebox.askyesno("Confirmar salida", "¿Esta seguro que desea salir y regresar al Login?"):
                self.ventana.destroy()
                from Login import iniciar_sesion
                iniciar_sesion()
        btn_salir = tk.Button(self.menu_lateral, text="\u23FB  Cerrar Sesion", anchor="center",
                              bg=COLOR_PELIGRO, fg=COLOR_TEXTO_BLANCO, relief="flat",
                              font=FUENTE_BOTON, pady=12, bd=0, cursor="hand2",
                              activebackground=_aclarar_color(COLOR_PELIGRO, 20),
                              activeforeground=COLOR_TEXTO_BLANCO,
                              command=salir_a_login)
        btn_salir.place(relx=0, rely=0.92, relwidth=1)
        
        
    def limpiar_panel(self):
        for widget in self.panel_dinamico.winfo_children():
            widget.destroy()
    def mostrar_venta_rapida(self):
        self.limpiar_panel()
        # Cada vista ahora crea su propio contenedor y lo pone en la celda (0,0) del panel_dinamico
        contenedor = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        contenedor.grid(row=0, column=0, sticky="nsew")
        # --- Encabezado ---
        header = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL)
        header.pack(fill="x", padx=20, pady=(10, 5))
        tk.Label(header, text="\U0001F6D2 Punto de Venta (Nota de Venta)", font=FUENTE_TITULO,
                 bg=COLOR_FONDO_PANEL, fg=COLOR_PRIMARIO).pack(anchor="w")
        tk.Label(header, text="Busca productos, agrega reparaciones y finaliza la venta",
                 font=FUENTE_ETIQUETA, bg=COLOR_FONDO_PANEL,
                 fg=COLOR_TEXTO_GRIS).pack(anchor="w")
        # Separador
        tk.Frame(contenedor, height=2, bg=COLOR_BORDE).pack(fill="x", padx=20, pady=(5, 10))
        # Contenedor principal con 2 columnas
        main_frame = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL)
        main_frame.pack(fill="both", expand=True, padx=20, pady=5)
        main_frame.grid_columnconfigure(0, minsize=320)
        main_frame.grid_columnconfigure(1, minsize=420, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        # Columna izquierda: busqueda y acciones
        col_izquierda = tk.Frame(main_frame, bg=COLOR_FONDO_PANEL, width=320)
        col_izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        col_izquierda.grid_propagate(False)
        # Contenedor para el cliente
        cliente_frame = tk.Frame(col_izquierda, bg=COLOR_FONDO_PANEL)
        cliente_frame.pack(fill="x", pady=(0, 10))
        tk.Label(cliente_frame, text="Cliente:", font=FUENTE_CUERPO_BOLD,
                 bg=COLOR_FONDO_PANEL, fg=COLOR_TEXTO_OSCURO).pack(anchor="w")
        cliente_var = tk.StringVar()
        combo_clientes = ttk.Combobox(cliente_frame, textvariable=cliente_var,
                                       state="readonly", font=FUENTE_CUERPO,
                                       style="Custom.TCombobox")
        combo_clientes.pack(fill="x", ipady=4)

        # --- NUEVA LÓGICA DE API PARA CLIENTES ---
        clientes_map = {}
        mi_taller_id = obtener_taller_id()
        
        if mi_taller_id:
            try:
                url_api = "https://www.ultracel.lat/api/pos/clientes"
                res = requests.post(url_api, json={"taller_id": mi_taller_id})
                if res.status_code == 200:
                    clientes = res.json().get('clientes', [])
                    clientes_map = {f"{c.get('id_cliente')} - {c.get('nombre_completo')}": c.get('id_cliente') for c in clientes}
            except requests.exceptions.ConnectionError:
                pass # Evitamos spam visual, el combobox quedará solo con "Venta de Mostrador"

        combo_clientes['values'] = ["0 - Venta de Mostrador"] + list(clientes_map.keys())
        combo_clientes.set("0 - Venta de Mostrador")
        # Frame y tabla de reparaciones listas para entregar
        reparaciones_frame = tk.Frame(col_izquierda, bg=COLOR_FONDO_PANEL)
        reparaciones_frame.pack(fill="x", pady=5)
        tk.Label(reparaciones_frame, text="Reparaciones Listas para Entregar:",
                 font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_PANEL,
                 fg=COLOR_TEXTO_OSCURO).pack(anchor="w")
        self.tree_reparaciones = ttk.Treeview(reparaciones_frame,
                                               columns=("ID", "Equipo", "Monto"),
                                               show="headings", height=4,
                                               style="Custom.Treeview")
        self.tree_reparaciones.heading("ID", text="ID")
        self.tree_reparaciones.heading("Equipo", text="Equipo")
        self.tree_reparaciones.heading("Monto", text="Monto a Pagar")
        self.tree_reparaciones.column("ID", width=40)
        self.tree_reparaciones.column("Equipo", width=180)
        self.tree_reparaciones.column("Monto", width=90, anchor="e")
        self.tree_reparaciones.pack(fill="x", pady=5)
        # Contenedor para la busqueda de productos
        productos_frame = tk.Frame(col_izquierda, bg=COLOR_FONDO_PANEL)
        productos_frame.pack(fill="both", expand=True, pady=5)
        tk.Label(productos_frame, text="Buscar Producto:", font=FUENTE_CUERPO_BOLD,
                 bg=COLOR_FONDO_PANEL, fg=COLOR_TEXTO_OSCURO).pack(anchor="w", pady=(10, 0))
        search_var = tk.StringVar()
        search_frame, search_entry = crear_entry_estilizado(productos_frame, textvariable=search_var)
        search_frame.pack(fill="x", pady=(0, 5))
        tree_productos = ttk.Treeview(productos_frame,
                                       columns=("ID", "Producto", "Precio"),
                                       show="headings", height=5,
                                       style="Custom.Treeview")
        tree_productos.heading("ID", text="ID")
        tree_productos.heading("Producto", text="Producto")
        tree_productos.heading("Precio", text="Precio")
        tree_productos.column("ID", width=40)
        tree_productos.column("Producto", width=180)
        tree_productos.column("Precio", width=70, anchor="e")
        tree_productos.pack(fill="both", expand=True, pady=5)
        # Columna derecha: nota de venta (carrito)
        col_derecha = tk.Frame(main_frame, bg=COLOR_NOTA_VENTA_BG,
                               highlightbackground=COLOR_BORDE, highlightthickness=1)
        col_derecha.grid(row=0, column=1, sticky="nsew")
        col_derecha.grid_rowconfigure(0, weight=0)
        col_derecha.grid_rowconfigure(1, weight=1)
        col_derecha.grid_rowconfigure(2, weight=0)
        col_derecha.grid_rowconfigure(3, weight=0)
        col_derecha.grid_columnconfigure(0, weight=1)
        tk.Label(col_derecha, text="Nota de Venta", font=FUENTE_SUBTITULO,
                 bg=COLOR_NOTA_VENTA_BG, fg=COLOR_PRIMARIO).grid(row=0, column=0,
                 sticky="ew", padx=10, pady=10)
        self.tree_carrito = ttk.Treeview(col_derecha,
                                          columns=("Cant", "Desc", "Precio", "Subtotal"),
                                          show="headings", style="Custom.Treeview")
        self.tree_carrito.heading("Cant", text="Cant.")
        self.tree_carrito.heading("Desc", text="Descripcion")
        self.tree_carrito.heading("Precio", text="P. Unit.")
        self.tree_carrito.heading("Subtotal", text="Subtotal")
        self.tree_carrito.column("Cant", width=40, anchor="center")
        self.tree_carrito.column("Desc", width=200)
        self.tree_carrito.column("Precio", width=80, anchor="e")
        self.tree_carrito.column("Subtotal", width=90, anchor="e")
        self.tree_carrito.grid(row=1, column=0, sticky="nsew", padx=10)
        total_frame = tk.Frame(col_derecha, bg=COLOR_NOTA_VENTA_BG)
        total_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        tk.Label(total_frame, text="TOTAL:", font=FUENTE_TOTAL,
                 bg=COLOR_NOTA_VENTA_BG, fg=COLOR_PRIMARIO).pack(side="left")
        tk.Label(total_frame, textvariable=self.total_var, font=FUENTE_TOTAL,
                 bg=COLOR_NOTA_VENTA_BG, fg=COLOR_PRIMARIO).pack(side="right")
        
        def agregar_seleccion_unica():
            # Revisamos si hay algo seleccionado en la tabla de productos
            sel_prod = tree_productos.selection()
            
            # Revisamos si hay algo seleccionado en la tabla de reparaciones
            # (Usamos try/except por si la tabla de reparaciones está oculta)
            try:
                sel_rep = self.tree_reparaciones.selection()
            except AttributeError:
                sel_rep = ()

            if sel_prod:
                self.agregar_item_carrito(tree_productos, "producto")
                tree_productos.selection_remove(sel_prod) # Quitamos la selección para no confundir
            elif sel_rep:
                self.agregar_item_carrito(self.tree_reparaciones, "reparacion")
                self.tree_reparaciones.selection_remove(sel_rep)
            else:
                messagebox.showwarning("Selección Vacía", "Por favor, selecciona un producto o una reparación de las listas.")

        # --- UX EXTRA: Que al hacer clic en una tabla, se deseleccione la otra ---
        def limpiar_seleccion_rep(event):
            try:
                for item in self.tree_reparaciones.selection():
                    self.tree_reparaciones.selection_remove(item)
            except: pass

        def limpiar_seleccion_prod(event):
            for item in tree_productos.selection():
                tree_productos.selection_remove(item)

        tree_productos.bind("<Button-1>", limpiar_seleccion_rep)
        # Asegúrate de aplicar el bind a tree_reparaciones justo después de crearlo en tu código:
        # self.tree_reparaciones.bind("<Button-1>", limpiar_seleccion_prod)

        def procesar_venta_actual():
            items_carrito = self.tree_carrito.get_children()
            
            if not items_carrito:
                return messagebox.showwarning("Carrito Vacío", "No hay artículos ni reparaciones en la nota de venta.")

            # 1. Obtenemos IDs básicos
            taller_id = obtener_taller_id()
            id_cliente = clientes_map.get(cliente_var.get(), 0) # Si es Mostrador, mandará 0
            
            # ⚠️ OJO AQUÍ: Necesitamos el ID del cajero/vendedor que inició sesión. 
            # Si tienes una función como obtener_id_usuario(), úsala. 
            # Por ahora le pondré 1 para que no falle.
            try:
                from Login import obtener_id_usuario # Ajusta esto a como importas tus variables globales
                id_vendedor = obtener_id_usuario()
            except ImportError:
                id_vendedor = 1 

            total_venta = 0.0
            payload_items = []

            # 2. Extraemos la información de la tabla del carrito
            for iid in items_carrito:
                valores = self.tree_carrito.item(iid, 'values')
                # valores = (cantidad, descripcion, precio_unitario, subtotal)
                cantidad = int(valores[0])
                descripcion = valores[1]
                precio_unit = float(valores[2].replace('$', '').replace(',', ''))
                
                # Extraemos el Tipo y el ID real del IID mágico que armamos (ej: "P5_0" o "R12")
                tipo = "P" if str(iid).startswith("P") else "R"
                
                # Le quitamos la letra inicial. Si es "P5_0", lo partimos y nos quedamos con el "5"
                id_raw = str(iid).split('_')[0]
                id_item = int(id_raw[1:]) 

                payload_items.append({
                    "tipo": tipo,
                    "id_item": id_item,
                    "cantidad": cantidad,
                    "precio_unitario": precio_unit,
                    "descripcion": descripcion
                })
                
                total_venta += (cantidad * precio_unit)

            # 3. Armamos el JSON final
            payload = {
                "taller_id": taller_id,
                "id_cliente": id_cliente,
                "id_vendedor": id_vendedor,
                "total": total_venta,
                "items": payload_items
            }

            # 4. Confirmamos y enviamos a Laravel
            if messagebox.askyesno("Confirmar Cobro", f"¿Deseas procesar esta venta por un TOTAL de ${total_venta:.2f}?"):
                try:
                    res = requests.post("https://www.ultracel.lat/api/pos/procesar-venta", json=payload)
                    
                    if res.status_code == 200:
                        messagebox.showinfo("¡Venta Exitosa!", "La venta se ha registrado. El stock y las reparaciones han sido actualizadas.")
                        
                        # Limpiamos todo el panel para el siguiente cliente
                        for i in self.tree_carrito.get_children(): self.tree_carrito.delete(i)
                        self.actualizar_total_carrito()
                        
                        cliente_var.set("Cliente de Mostrador")
                        on_cliente_seleccionado() # Ocultará las reparaciones
                        buscar_productos()        # Recargará el stock actualizado
                        
                    else:
                        print(f"🚨 ERROR EN VENTA: {res.text}")
                        messagebox.showerror("Error", "Ocurrió un problema al guardar la venta. Revisa la terminal.")
                except requests.exceptions.ConnectionError:
                    messagebox.showerror("Error", "Sin conexión al servidor.")

        
        # ==========================================
        # BOTÓN ÚNICO EN LA COLUMNA IZQUIERDA
        # ==========================================
        botones_accion_frame = tk.Frame(col_izquierda, bg=COLOR_FONDO_PANEL)
        botones_accion_frame.pack(fill="x", pady=(15, 0))
        
        btn_add_unico = crear_boton(botones_accion_frame, "Añadir a la Nota ➡",
                    agregar_seleccion_unica, # ¡Llama a tu nueva función inteligente!
                    COLOR_SECUNDARIO, fuente=FUENTE_CUERPO_BOLD, height=2)
        btn_add_unico.pack(fill="x", expand=True)


        # ==========================================
        # BOTONES DEL CARRITO EN LA COLUMNA DERECHA
        # ==========================================
        # Nota: Asumo que COLOR_NOTA_VENTA_BG es una variable tuya, si marca error cámbiala por COLOR_FONDO_PANEL
        botones_carrito_frame = tk.Frame(col_derecha, bg=COLOR_FONDO_PANEL) 
        botones_carrito_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        crear_boton(botones_carrito_frame, "❌ Quitar Item", self.quitar_item_carrito,
                    COLOR_PELIGRO, fuente=FUENTE_CUERPO_BOLD).pack(side="left")
        
        btn_cobrar_final = crear_boton(botones_carrito_frame, "💰 Finalizar y Cobrar", 
                    procesar_venta_actual, # ¡Llama a tu nueva función gigante que arma el JSON!
                    COLOR_EXITO, fuente=FUENTE_CUERPO_BOLD)
        btn_cobrar_final.pack(side="right", fill="x", expand=True, ipady=5, padx=(10, 0))
        def buscar_productos(*args):
            termino = search_var.get()
            mi_taller_id = obtener_taller_id()
            if not mi_taller_id: return

            for i in tree_productos.get_children(): tree_productos.delete(i)
            try:
                res = requests.post("https://www.ultracel.lat/api/pos/buscar-productos", json={"taller_id": mi_taller_id, "termino": termino})
                if res.status_code == 200:
                    for p in res.json().get('productos', []):
                        tree_productos.insert("", "end", values=(p['id_producto'], p['nombre_producto'], f"${float(p['precio_venta']):.2f}"))
            except requests.exceptions.ConnectionError:
                pass

        search_var.trace_add("write", buscar_productos)
        buscar_productos()

        def on_cliente_seleccionado(*args):
            for i in self.tree_reparaciones.get_children(): self.tree_reparaciones.delete(i)
            #btn_add_reparacion_izq.config(state="disabled")
            
            id_cliente = clientes_map.get(cliente_var.get())
            if not id_cliente:
                reparaciones_frame.pack_forget()
                return
            
            reparaciones_frame.pack(fill="x", pady=5)
            
            # Recuperamos el taller_id
            mi_taller_id = obtener_taller_id()
            
            try:
                # AQUÍ agregamos el taller_id al JSON
                res = requests.post("https://www.ultracel.lat/api/pos/reparaciones-cliente", json={"id_cliente": id_cliente, "taller_id": mi_taller_id})
                
                if res.status_code == 200:
                    reparaciones = res.json().get('reparaciones', [])
                    for r in reparaciones:
                        # LA MAGIA: float() envuelve a r['presupuesto'] para que Python no colapse
                        presupuesto = f"${float(r['presupuesto']):.2f}" if r.get('presupuesto') else "Sin Presupuesto"
                        
                        self.tree_reparaciones.insert("", "end", values=(r['id_reparacion'], r['equipo'], presupuesto))
                    
                    if reparaciones:
                        #btn_add_reparacion_izq.config(state="normal")
                        pass
                else:
                    print(f"🚨 ERROR: {res.status_code} - {res.text}")
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "No se pudo conectar al servidor.")

        combo_clientes.bind("<<ComboboxSelected>>", on_cliente_seleccionado)

    def agregar_item_carrito(self, treeview, tipo_item):
        item_seleccionado = treeview.selection()
        if not item_seleccionado: return
        
        valores = treeview.item(item_seleccionado[0], 'values')
        
        if tipo_item == "producto":
            id_item, desc, precio_str = valores
            precio = float(precio_str.replace('$', '').replace(',', ''))
            # Guardamos el ID del producto y el tipo en el iid del treeview
            self.tree_carrito.insert("", "end", iid=f"P{id_item}_{len(self.tree_carrito.get_children())}", values=(1, desc, f"${precio:.2f}", f"${precio:.2f}"))
        
        elif tipo_item == "reparacion":
            id_item, desc, precio_str = valores
            
            # --- PROTECCIÓN ANTI-CRASH ---
            if "Sin Presupuesto" in precio_str:
                return messagebox.showwarning("Atención", "No puedes cobrar un equipo que no tiene presupuesto definido.")
                
            precio = float(precio_str.replace('$', '').replace(',', ''))
            
            # Verificamos que no agregue la misma reparación dos veces al carrito
            for item_id in self.tree_carrito.get_children():
                if item_id.startswith(f"R{id_item}"):
                    return messagebox.showwarning("Duplicado", "Esta reparación ya está en la nota de venta.")

            self.tree_carrito.insert("", "end", iid=f"R{id_item}", values=(1, f"Servicio: {desc}", f"${precio:.2f}", f"${precio:.2f}"))
            
        self.actualizar_total_carrito()
    def quitar_item_carrito(self):
        item_seleccionado = self.tree_carrito.selection()
        if not item_seleccionado: return
        self.tree_carrito.delete(item_seleccionado[0])
        self.actualizar_total_carrito()
    def actualizar_total_carrito(self):
        total = 0.0
        for item_id in self.tree_carrito.get_children():
            valores = self.tree_carrito.item(item_id, 'values')
            subtotal_str = valores[3]
            total += float(subtotal_str.replace('$', ''))
        self.total_var.set(f"${total:.2f}")
    def finalizar_venta(self, id_cliente, id_vendedor):
        items_en_carrito = self.tree_carrito.get_children()
        if not items_en_carrito:
            return messagebox.showwarning("Carrito Vacio", "No hay items en la nota de venta.")
        
        total = float(self.total_var.get().replace('$', ''))
        if not messagebox.askyesno("Confirmar Venta", f"El total de la venta es ${total:.2f}.\n¿Desea continuar y finalizar la venta?"):
            return

        mi_taller_id = obtener_taller_id()
        if not mi_taller_id: return messagebox.showerror("Error", "Licencia inválida.")

        # Empaquetamos el carrito para Laravel
        payload_items = []
        for iid in items_en_carrito:
            valores = self.tree_carrito.item(iid, 'values')
            cantidad, desc, p_unit_str, _ = valores
            payload_items.append({
                "tipo": iid[0], # 'P' o 'R'
                "id_item": int(iid[1:]),
                "cantidad": int(cantidad),
                "precio_unitario": float(p_unit_str.replace('$', '')),
                "descripcion": desc
            })

        try:
            payload = {
                "taller_id": mi_taller_id,
                "id_cliente": id_cliente if id_cliente else 0,
                "id_vendedor": self.id_vendedor_logueado, # Ojo aquí, asegúrate de que exista esta variable en el init del vendedor
                "total": total,
                "items": payload_items
            }
            res = requests.post("https://www.ultracel.lat/api/pos/procesar-venta", json=payload)
            
            if res.status_code == 200:
                messagebox.showinfo("Venta Finalizada", "La venta se ha registrado exitosamente.")
                self.mostrar_venta_rapida() # Recarga la vista
            else:
                messagebox.showerror("Error", "No se pudo completar la venta en el servidor.")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "Fallo de conexión al procesar la venta.")
    def mostrar_admin_clientes(self):
        self.limpiar_panel()
        contenedor = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        contenedor.pack(fill="both", expand=True)
        # --- Encabezado ---
        header = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL)
        header.pack(fill="x", padx=20, pady=(10, 5))
        tk.Label(header, text="\U0001F465 Administracion de Clientes", font=FUENTE_TITULO,
                 bg=COLOR_FONDO_PANEL, fg=COLOR_PRIMARIO).pack(anchor="w")
        tk.Label(header, text="Doble clic en un cliente para ver su historial de reparaciones",
                 font=FUENTE_ETIQUETA, bg=COLOR_FONDO_PANEL,
                 fg=COLOR_TEXTO_GRIS).pack(anchor="w")
        # Separador
        tk.Frame(contenedor, height=2, bg=COLOR_BORDE).pack(fill="x", padx=20, pady=(5, 10))
        
        # --- Frame principal para la tabla ---
        main_frame = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL)
        main_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # --- Creacion y posicionamiento de la tabla Treeview ---
        self.tree_clientes = ttk.Treeview(main_frame, columns=("ID", "Nombre", "Telefono"),
                                           show="headings", style="Custom.Treeview")
        
        self.tree_clientes.heading("ID", text="ID Cliente")
        self.tree_clientes.heading("Nombre", text="Nombre Completo")
        self.tree_clientes.heading("Telefono", text="Telefono")
        
        self.tree_clientes.column("ID", width=80, anchor="center")
        self.tree_clientes.column("Nombre", width=350)
        self.tree_clientes.column("Telefono", width=150)
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical",
                                  command=self.tree_clientes.yview,
                                  style="Custom.Vertical.TScrollbar")
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree_clientes.pack(side="left", fill="both", expand=True)
        # --- Logica para llenar la tabla con datos de la BD ---
        mi_taller_id = obtener_taller_id()
        if mi_taller_id:
            try:
                res = requests.post("https://www.ultracel.lat/api/pos/clientes", json={"taller_id": mi_taller_id})
                if res.status_code == 200:
                    for i, cliente in enumerate(res.json().get('clientes', [])):
                        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                        self.tree_clientes.insert("", "end", values=(
                            cliente['id_cliente'],
                            cliente['nombre_completo'],
                            cliente.get('telefono', 'N/A') # Asegúrate de que tu endpoint de clientes mande el teléfono
                        ), tags=(tag,))
            except: pass
        
        self.tree_clientes.tag_configure('oddrow', background=COLOR_FILA_IMPAR)
        self.tree_clientes.tag_configure('evenrow', background=COLOR_FILA_PAR)
        # --- Asignar evento de doble clic ---
        self.tree_clientes.bind("<Double-1>", self.mostrar_historial_cliente)
        # --- Botones de Accion ---
        botones_frame = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL)
        botones_frame.pack(pady=10, padx=20, fill="x", side="bottom")
        crear_boton(botones_frame, "\U0001F464 Nuevo Cliente", self.abrir_formulario_cliente,
                    COLOR_EXITO, fuente=FUENTE_CUERPO_BOLD).pack(side="left")
        def editar_seleccion_cli():
            item_sel = self.tree_clientes.selection()
            if not item_sel:
                messagebox.showwarning("Ninguna Seleccion", "Por favor, selecciona un cliente para editar.")
                return
            id_cliente = self.tree_clientes.item(item_sel[0], 'values')[0]
            self.abrir_formulario_cliente(id_cliente)
        crear_boton(botones_frame, "\u270F Editar Seleccionado", editar_seleccion_cli,
                    COLOR_ADVERTENCIA, fuente=FUENTE_CUERPO_BOLD).pack(side="left", padx=10)
        crear_boton(botones_frame, "\u274C Eliminar Seleccionado", self.eliminar_cliente_seleccionado,
                    COLOR_PELIGRO, fuente=FUENTE_CUERPO_BOLD).pack(side="left")
    def mostrar_salida_dispositivos(self):
        self.limpiar_panel()
        contenedor = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        contenedor.grid(row=0, column=0, sticky="nsew")
        # --- Encabezado ---
        header = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL)
        header.pack(fill="x", padx=20, pady=(10, 5))
        tk.Label(header, text="Salida de Dispositivos", font=FUENTE_TITULO,
                 bg=COLOR_FONDO_PANEL, fg=COLOR_PRIMARIO).pack(anchor="w")
        # Separador
        tk.Frame(contenedor, height=2, bg=COLOR_BORDE).pack(fill="x", padx=20, pady=(5, 10))
        form_frame = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL, padx=20)
        form_frame.pack(fill="x")
        entradas = ["Producto", "Salida", "Fecha", "Lugar", "Estado"]
        self.salida_vars = {}
        for e in entradas:
            tk.Label(form_frame, text=e + ":", font=FUENTE_CUERPO_BOLD,
                     bg=COLOR_FONDO_PANEL, fg=COLOR_TEXTO_OSCURO).pack(anchor="w", pady=(8, 0))
            var = tk.StringVar()
            self.salida_vars[e] = var
            entry_frame, entry_widget = crear_entry_estilizado(form_frame, textvariable=var)
            entry_frame.pack(fill="x", pady=(0, 5))
        def registrar_salida():
            datos = {k: v.get() for k, v in self.salida_vars.items()}
            messagebox.showinfo("Salida registrada", f"Datos:\n" + "\n".join(f"{k}: {v}" for k, v in datos.items()))
        crear_boton(contenedor, "Registrar Salida", registrar_salida,
                    COLOR_SECUNDARIO).pack(padx=20, pady=15, anchor="w")
    def abrir_formulario_producto(self, sku_editar=None):
        self.limpiar_panel()

        contenedor = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        contenedor.pack(fill="both", expand=True)

        # --- Barra Superior ---
        top_bar = tk.Frame(contenedor, bg=COLOR_PRIMARIO, height=50)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        tk.Button(top_bar, text="⬅ REGRESAR", font=("Segoe UI", 10, "bold"), bg="#c0392b", fg="white",
                  relief="flat", command=self.mostrar_inventario, padx=10).pack(side="left", padx=10, pady=10)

        titulo = "✏️ Editar Producto" if sku_editar else "➕ Registrar Nuevo Producto"
        tk.Label(top_bar, text=titulo, font=FUENTE_SUBTITULO, 
                 bg=COLOR_PRIMARIO, fg=COLOR_TEXTO_BLANCO).pack(side="left", padx=15, pady=10)

        # --- Contenedor del Formulario ---
        form_frame = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL, padx=100, pady=30)
        form_frame.pack(fill="both", expand=True)

        # Diccionario para guardar las variables
        vars_prod = {
            "sku": tk.StringVar(),
            "nombre_producto": tk.StringVar(),
            "marca_compatible": tk.StringVar(),
            "stock": tk.StringVar(value="0"),
            "precio_venta": tk.StringVar(value="0.00"),
            "tipo_producto": tk.StringVar(value="Venta Directa") # Valor por defecto
        }

        # --- Diseño de los campos en Grid ---
        # Fila 0: SKU y Nombre
        tk.Label(form_frame, text="SKU/Código:", font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_PANEL).grid(row=0, column=0, sticky="w", pady=10)
        tk.Entry(form_frame, textvariable=vars_prod["sku"], font=FUENTE_CUERPO, bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDE).grid(row=0, column=1, sticky="ew", padx=(0, 30), ipady=5)

        tk.Label(form_frame, text="Nombre del Producto:", font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_PANEL).grid(row=0, column=2, sticky="w", pady=10)
        tk.Entry(form_frame, textvariable=vars_prod["nombre_producto"], font=FUENTE_CUERPO, bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDE).grid(row=0, column=3, sticky="ew", ipady=5)

        # Fila 1: Tipo y Marca
        tk.Label(form_frame, text="Tipo de Producto:", font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_PANEL).grid(row=1, column=0, sticky="w", pady=10)
        ttk.Combobox(form_frame, textvariable=vars_prod["tipo_producto"], values=["Refacción", "Venta Directa"], state="readonly", font=FUENTE_CUERPO).grid(row=1, column=1, sticky="ew", padx=(0, 30), ipady=5)

        tk.Label(form_frame, text="Marca Compatible (Opcional):", font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_PANEL).grid(row=1, column=2, sticky="w", pady=10)
        tk.Entry(form_frame, textvariable=vars_prod["marca_compatible"], font=FUENTE_CUERPO, bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDE).grid(row=1, column=3, sticky="ew", ipady=5)

        # Fila 2: Stock y Precio
        tk.Label(form_frame, text="Stock Inicial:", font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_PANEL).grid(row=2, column=0, sticky="w", pady=10)
        tk.Entry(form_frame, textvariable=vars_prod["stock"], font=FUENTE_CUERPO, bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDE).grid(row=2, column=1, sticky="ew", padx=(0, 30), ipady=5)

        tk.Label(form_frame, text="Precio de Venta ($):", font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_PANEL).grid(row=2, column=2, sticky="w", pady=10)
        tk.Entry(form_frame, textvariable=vars_prod["precio_venta"], font=FUENTE_CUERPO, bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDE).grid(row=2, column=3, sticky="ew", ipady=5)

        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        # Si estamos editando, cargamos los datos (Asumiendo que tienes una ruta para ver por SKU)
        if sku_editar:
            try:
                res = requests.post("https://www.ultracel.lat/api/inventario/obtener-por-sku", json={"sku": sku_editar, "taller_id": obtener_taller_id()})
                if res.status_code == 200:
                    prod_data = res.json().get('producto', {})
                    if prod_data:
                        vars_prod["sku"].set(prod_data.get('sku', ''))
                        vars_prod["nombre_producto"].set(prod_data.get('nombre_producto', ''))
                        vars_prod["tipo_producto"].set(prod_data.get('tipo_producto', 'Venta Directa'))
                        vars_prod["marca_compatible"].set(prod_data.get('marca_compatible', ''))
                        vars_prod["stock"].set(prod_data.get('stock', '0'))
                        vars_prod["precio_venta"].set(prod_data.get('precio_venta', '0.00'))
                        
                        # Si es editar, bloqueamos el SKU para que no lo rompan
                        vars_prod["sku"].set(prod_data.get('sku'))
            except: pass

        def guardar_producto():
            payload = {k: v.get() for k, v in vars_prod.items()}
            payload["taller_id"] = obtener_taller_id()
            
            if not payload["sku"] or not payload["nombre_producto"]:
                return messagebox.showwarning("Datos Incompletos", "SKU y Nombre son obligatorios.")

            # Ruta ficticia, asegúrate de tenerla en Laravel
            ruta_api = "https://www.ultracel.lat/api/inventario/actualizar" if sku_editar else "https://www.ultracel.lat/api/inventario/crear"
            
            try:
                res_save = requests.post(ruta_api, json=payload)
                if res_save.status_code == 200:
                    messagebox.showinfo("Éxito", "Producto guardado correctamente.")
                    self.mostrar_inventario() # Regresamos a la tabla
                else:
                    messagebox.showerror("Error", f"No se pudo guardar: {res_save.text}")
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "Fallo de conexión al servidor.")

        # Botón Guardar
        btn_frame = tk.Frame(form_frame, bg=COLOR_FONDO_PANEL)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=40)
        
        crear_boton(btn_frame, "💾 GUARDAR PRODUCTO", guardar_producto, COLOR_EXITO, height=2).pack(side="left", padx=10)
        # Forzar actualizacion del scrollregion al inicio
        
    def eliminar_producto_seleccionado(self):
        item_sel = self.tree_inventario.selection()
        if not item_sel: return messagebox.showwarning("Ninguna Seleccion", "Por favor, selecciona un producto.")
        
        sku_a_eliminar = self.tree_inventario.item(item_sel[0], 'values')[0]
        nombre_a_eliminar = self.tree_inventario.item(item_sel[0], 'values')[1]
        
        if messagebox.askyesno("Confirmar Eliminacion", f"¿Estas seguro de eliminar permanentemente el producto:\n\n{nombre_a_eliminar} (SKU: {sku_a_eliminar})?"):
            mi_taller_id = obtener_taller_id()
            if not mi_taller_id: return
            try:
                res = requests.post("https://www.ultracel.lat/api/inventario/eliminar", json={"sku": sku_a_eliminar, "taller_id": mi_taller_id})
                if res.status_code == 200:
                    messagebox.showinfo("Eliminado", "Producto eliminado.")
                    self.mostrar_inventario()
                else: messagebox.showerror("Error", "No se pudo eliminar el producto.")
            except: messagebox.showerror("Error", "Fallo de conexion.")
    def mostrar_gestion_compras(self):
        self.limpiar_panel()
        contenedor = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        contenedor.grid(row=0, column=0, sticky="nsew")
        # --- Encabezado ---
        header = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL)
        header.pack(fill="x", padx=20, pady=(10, 5))
        tk.Label(header, text="Gestionar Compras", font=FUENTE_TITULO,
                 bg=COLOR_FONDO_PANEL, fg=COLOR_PRIMARIO).pack(anchor="w")
        # Separador
        tk.Frame(contenedor, height=2, bg=COLOR_BORDE).pack(fill="x", padx=20, pady=(5, 10))
        form_frame = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL, padx=20)
        form_frame.pack(fill="x")
        campos = ["Producto", "Cantidad", "Precio", "Fecha"]
        self.compra_vars = {}
        for campo in campos:
            tk.Label(form_frame, text=campo + ":", font=FUENTE_CUERPO_BOLD,
                     bg=COLOR_FONDO_PANEL, fg=COLOR_TEXTO_OSCURO).pack(anchor="w", pady=(8, 0))
            var = tk.StringVar()
            self.compra_vars[campo] = var
            entry_frame, entry_widget = crear_entry_estilizado(form_frame, textvariable=var)
            entry_frame.pack(fill="x", pady=(0, 5))
        def registrar_compra():
            datos = {k: v.get() for k, v in self.compra_vars.items()}
            messagebox.showinfo("Compra registrada", f"Datos:\n" + "\n".join(f"{k}: {v}" for k, v in datos.items()))
        crear_boton(contenedor, "Registrar Compra", registrar_compra,
                    COLOR_SECUNDARIO).pack(padx=20, pady=15, anchor="w")
        
    def mostrar_historial_cliente(self, event=None):
        item_sel = self.tree_clientes.selection()
        if not item_sel: return
        
        id_cliente = self.tree_clientes.item(item_sel[0], 'values')[0]
        nombre_cliente = self.tree_clientes.item(item_sel[0], 'values')[1]

        # 1. Limpiamos el panel para meter la nueva vista
        self.limpiar_panel()

        contenedor = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_APP)
        contenedor.pack(fill="both", expand=True)

        # --- BARRA DE TÍTULO (Navegación) ---
        barra_titulo = tk.Frame(contenedor, bg=COLOR_PRIMARIO, height=50)
        barra_titulo.pack(fill="x")
        barra_titulo.pack_propagate(False)

        tk.Button(barra_titulo, text="⬅ REGRESAR", font=("Segoe UI", 10, "bold"), bg="#c0392b", fg="white",
                  relief="flat", command=self.mostrar_admin_clientes, padx=10).pack(side="left", padx=10, pady=10)

        tk.Label(barra_titulo, text=f"Historial de Reparaciones: {nombre_cliente}", font=FUENTE_SUBTITULO, 
                 bg=COLOR_PRIMARIO, fg=COLOR_TEXTO_BLANCO).pack(side="left", padx=15, pady=10)

        # --- INTERFAZ DE LA TABLA ---
        tree_frame = tk.Frame(contenedor, bg=COLOR_FONDO_APP)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tree_historial = ttk.Treeview(tree_frame, columns=("ID", "Fecha", "Dispositivo", "Estado", "Presupuesto"),
                                      show="headings", style="Custom.Treeview")
        
        tree_historial.heading("ID", text="ID Orden")
        tree_historial.heading("Fecha", text="Fecha")
        tree_historial.heading("Dispositivo", text="Dispositivo")
        tree_historial.heading("Estado", text="Estado")
        tree_historial.heading("Presupuesto", text="Presupuesto")
        
        tree_historial.column("ID", width=60, anchor="center")
        tree_historial.column("Fecha", width=100, anchor="center")
        tree_historial.column("Dispositivo", width=250)
        tree_historial.column("Estado", width=120, anchor="center")
        tree_historial.column("Presupuesto", width=100, anchor="e")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_historial.yview, style="Custom.Vertical.TScrollbar")
        tree_historial.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree_historial.pack(side="left", fill="both", expand=True)

        # --- COLORES DE ESTADO (Igual que en el panel del Técnico) ---
        tree_historial.tag_configure('oddrow', background=COLOR_FILA_IMPAR)
        tree_historial.tag_configure('evenrow', background=COLOR_FILA_PAR)
        tree_historial.tag_configure('Recibido', background='#ffeaa7')             # Amarillo
        tree_historial.tag_configure('En Reparación', background='#74b9ff')        # Azul
        tree_historial.tag_configure('Esperando Aprobación', background='#fab1a0') # Naranja
        tree_historial.tag_configure('Reparado', background='#55efc4')             # Verde Claro
        tree_historial.tag_configure('Entregado', background='#dfe6e9')            # Gris (Ya se fue)

        # --- LÓGICA DE DATOS CONEXIÓN A LARAVEL ---
        try:
            mi_taller_id = obtener_taller_id() # 🔒 PASE VIP
            res = requests.post("https://www.ultracel.lat/api/clientes/historial", json={"id_cliente": id_cliente, "taller_id": mi_taller_id})
            if res.status_code == 200:
                historial = res.json().get('historial', [])
                if not historial:
                    tree_historial.insert("", "end", values=("", "", "Este cliente no tiene reparaciones registradas.", "", ""))
                else:
                    for i, rep in enumerate(historial):
                        # Parche matemático de prevención
                        try:
                            presupuesto_formato = f"${float(rep['presupuesto']):.2f}" if rep.get('presupuesto') else "Sin Presupuesto"
                        except:
                            presupuesto_formato = "Sin Presupuesto"
                        
                        # Decidimos el color: si es un estado conocido usamos ese color, si no, lo hacemos cebra
                        estado = rep.get('estado', '')
                        tag = estado if estado in ['Recibido', 'En Reparación', 'Esperando Aprobación', 'Reparado', 'Entregado'] else ('evenrow' if i % 2 == 0 else 'oddrow')
                        
                        tree_historial.insert("", "end", values=(
                            rep['id_reparacion'], rep['fecha'], rep['dispositivo'], estado, presupuesto_formato
                        ), tags=(tag,))
            else:
                print(f"🚨 Error en Historial: {res.text}")
        except Exception as e:
            print(f"🚨 Error Python: {e}")
            messagebox.showerror("Error", "No se pudo conectar con el servidor.")
    
    def agregar(self, nombre, precio):
        self.carrito.append((nombre, precio))
        texto = "\n".join([f"{i+1}. {n} - ${p}" for i, (n, p) in enumerate(self.carrito)])
        self.carrito_label.config(text=texto)
        self.total_var.set(f"${sum(p for _, p in self.carrito):.2f}")
    def mostrar_historial(self):
        self.limpiar_panel()
        contenedor = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        contenedor.pack(fill="both", expand=True)
        # --- Encabezado ---
        header = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL)
        header.pack(fill="x", padx=20, pady=(10, 5))
        tk.Label(header, text="\U0001F4DC Historial de Ventas", font=FUENTE_TITULO,
                 bg=COLOR_FONDO_PANEL, fg=COLOR_PRIMARIO).pack(anchor="w")
        tk.Label(header, text="Selecciona una venta para ver sus detalles",
                 font=FUENTE_ETIQUETA, bg=COLOR_FONDO_PANEL,
                 fg=COLOR_TEXTO_GRIS).pack(anchor="w")
        # Separador
        tk.Frame(contenedor, height=2, bg=COLOR_BORDE).pack(fill="x", padx=20, pady=(5, 10))
        # --- Contenedor Principal con 2 columnas ---
        main_frame = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL)
        main_frame.pack(fill="both", expand=True, padx=20, pady=5)
        main_frame.grid_columnconfigure(0, weight=2) # Columna de la lista de ventas
        main_frame.grid_columnconfigure(1, weight=1) # Columna de detalles
        main_frame.grid_rowconfigure(0, weight=1)
        # --- COLUMNA IZQUIERDA: LISTA MAESTRA DE VENTAS ---
        col_izquierda = tk.Frame(main_frame, bg=COLOR_FONDO_PANEL)
        col_izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        tk.Label(col_izquierda, text="Todas las Ventas Registradas", font=FUENTE_SUBTITULO,
                 bg=COLOR_FONDO_PANEL, fg=COLOR_PRIMARIO).pack(anchor="w")
        
        tree_frame_v = tk.Frame(col_izquierda, bg=COLOR_FONDO_PANEL)
        tree_frame_v.pack(fill="both", expand=True, pady=(5, 0))
        tree_ventas = ttk.Treeview(tree_frame_v,
                                    columns=("ID", "Fecha", "Cliente", "Vendedor", "Total"),
                                    show="headings", height=15, style="Custom.Treeview")
        tree_ventas.heading("ID", text="ID Venta"); tree_ventas.heading("Fecha", text="Fecha");
        tree_ventas.heading("Cliente", text="Cliente"); tree_ventas.heading("Vendedor", text="Vendedor");
        tree_ventas.heading("Total", text="Monto Total");
        
        tree_ventas.column("ID", width=60, anchor="center"); tree_ventas.column("Fecha", width=120);
        tree_ventas.column("Cliente", width=150); tree_ventas.column("Vendedor", width=150);
        tree_ventas.column("Total", width=100, anchor="e");
        scrollbar_v = ttk.Scrollbar(tree_frame_v, orient="vertical",
                                     command=tree_ventas.yview,
                                     style="Custom.Vertical.TScrollbar")
        tree_ventas.configure(yscrollcommand=scrollbar_v.set)
        scrollbar_v.pack(side="right", fill="y")
        tree_ventas.pack(side="left", fill="both", expand=True)
        # --- COLUMNA DERECHA: DETALLES DE LA VENTA SELECCIONADA ---
        col_derecha = tk.Frame(main_frame, bg=COLOR_FONDO_SECCION,
                               highlightbackground=COLOR_BORDE, highlightthickness=1)
        col_derecha.grid(row=0, column=1, sticky="nsew")
        tk.Label(col_derecha, text="Detalles de la Venta", font=FUENTE_SUBTITULO,
                 bg=COLOR_FONDO_SECCION, fg=COLOR_PRIMARIO).pack(pady=10)
        
        tree_detalles = ttk.Treeview(col_derecha,
                                      columns=("Cant", "Desc", "P. Unit", "Subtotal"),
                                      show="headings", height=15, style="Custom.Treeview")
        tree_detalles.heading("Cant", text="Cant."); tree_detalles.heading("Desc", text="Descripcion");
        tree_detalles.heading("P. Unit", text="P. Unit."); tree_detalles.heading("Subtotal", text="Subtotal");
        
        tree_detalles.column("Cant", width=40, anchor="center"); tree_detalles.column("Desc", width=150);
        tree_detalles.column("P. Unit", width=80, anchor="e"); tree_detalles.column("Subtotal", width=80, anchor="e");
        tree_detalles.pack(fill="both", expand=True, padx=10, pady=(0,10))
        # --- LOGICA DE LA BASE DE DATOS ---
        def cargar_lista_ventas():
            mi_taller_id = obtener_taller_id()
            if not mi_taller_id: return
            for i in tree_ventas.get_children(): tree_ventas.delete(i)
            
            try:
                res = requests.post("https://www.ultracel.lat/api/pos/historial-ventas", json={"taller_id": mi_taller_id})
                if res.status_code == 200:
                    for idx, v in enumerate(res.json().get('ventas', [])):
                        tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                        
                        # ¡LA MAGIA! Convertimos el texto a número real
                        monto_limpio = float(v['monto_total'])
                        
                        tree_ventas.insert("", "end", values=(
                            v['id_venta'], v['fecha'], v['cliente'],
                            v['vendedor'], f"${monto_limpio:.2f}"
                        ), tags=(tag,))
                        
                    tree_ventas.tag_configure('oddrow', background=COLOR_FILA_IMPAR)
                    tree_ventas.tag_configure('evenrow', background=COLOR_FILA_PAR)
                else:
                    print(f"🚨 Error en Laravel (Ventas): {res.text}")
            except Exception as e: 
                print(f"🚨 Error en Python (Cargar Ventas): {e}")

        def mostrar_detalles_venta(event):
            item_seleccionado = tree_ventas.selection()
            if not item_seleccionado: return
            id_venta = tree_ventas.item(item_seleccionado[0], 'values')[0]
            
            for i in tree_detalles.get_children(): tree_detalles.delete(i)
            try:
                mi_taller_id = obtener_taller_id() # 🔒 CANDADO AÑADIDO
                res = requests.post("https://www.ultracel.lat/api/pos/detalles-venta", json={"id_venta": id_venta, "taller_id": mi_taller_id})
                if res.status_code == 200:
                    for d in res.json().get('detalles', []):
                        
                        # ¡LA MAGIA x2! Aseguramos que todo sea numérico antes de multiplicar
                        cantidad = int(d['cantidad'])
                        precio_unitario = float(d['precio_unitario'])
                        subtotal = cantidad * precio_unitario
                        
                        tree_detalles.insert("", "end", values=(
                            cantidad, d['descripcion_linea'],
                            f"${precio_unitario:.2f}", f"${subtotal:.2f}"
                        ))
                else:
                    print(f"🚨 Error en Laravel (Detalles): {res.text}")
            except Exception as e: 
                print(f"🚨 Error en Python (Mostrar Detalles): {e}")
                
        # --- CONEXION DE EVENTOS ---
        tree_ventas.bind("<<TreeviewSelect>>", mostrar_detalles_venta)
        cargar_lista_ventas()
    import tkinter as tk
    from tkinter import ttk, messagebox, simpledialog
    def mostrar_inventario(self):
        self.limpiar_panel()
        contenedor = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        contenedor.pack(fill="both", expand=True)

        # --- Encabezado ---
        header = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL)
        header.pack(fill="x", padx=20, pady=(20, 5))
        tk.Label(header, text="\U0001F4E6 Gestión de Inventario para Venta", font=FUENTE_TITULO,
                 bg=COLOR_FONDO_PANEL, fg=COLOR_PRIMARIO).pack(anchor="w")
        tk.Label(header, text="Busca, agrega, edita o elimina productos del inventario",
                 font=FUENTE_ETIQUETA, bg=COLOR_FONDO_PANEL, fg=COLOR_TEXTO_GRIS).pack(anchor="w")
        
        tk.Frame(contenedor, height=2, bg=COLOR_BORDE).pack(fill="x", padx=20, pady=(5, 10))

        # --- Frame para Controles ---
        controles_frame = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL)
        controles_frame.pack(fill="x", pady=10, padx=20)
        
        # Botones de Acción
        crear_boton(controles_frame, "➕ Nuevo Producto", lambda: self.abrir_formulario_producto(),
                    COLOR_EXITO, fuente=FUENTE_CUERPO_BOLD).pack(side="left", padx=(0,10))

        def editar_seleccion_inv():
            item_sel = self.tree_inventario.selection()
            if not item_sel: return messagebox.showwarning("Selección", "Selecciona un producto de la tabla.")
            
            # Asumimos que el SKU está en la primera columna [0]
            sku_sel = self.tree_inventario.item(item_sel[0], 'values')[0]
            self.abrir_formulario_producto(sku_sel) 

        crear_boton(controles_frame, "✏️ Editar Seleccionado", editar_seleccion_inv,
                    COLOR_ADVERTENCIA, fuente=FUENTE_CUERPO_BOLD).pack(side="left", padx=(0,10))
        # Si tienes la funcion eliminar_producto_seleccionado, se queda igual
        crear_boton(controles_frame, "❌ Eliminar", self.eliminar_producto_seleccionado, COLOR_PELIGRO, fuente=FUENTE_CUERPO_BOLD).pack(side="left")
        
        # Barra de Búsqueda
        search_var = tk.StringVar()
        search_frame_outer = tk.Frame(controles_frame, bg=COLOR_FONDO_PANEL)
        search_frame_outer.pack(side="right", fill="x")
        tk.Label(search_frame_outer, text="\U0001F50D Buscar:", font=FUENTE_CUERPO,
                 bg=COLOR_FONDO_PANEL, fg=COLOR_TEXTO_OSCURO).pack(side="left", padx=(10, 5))
        search_entry_frame, search_entry = crear_entry_estilizado(search_frame_outer, textvariable=search_var)
        search_entry_frame.pack(side="left")

        # --- Treeview ---
        tree_frame = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tree_inventario = ttk.Treeview(tree_frame,
                                             columns=("SKU", "Producto", "Tipo", "Stock", "Precio"),
                                             show="headings", style="Custom.Treeview")
        
        cols = {"SKU": 100, "Producto": 250, "Tipo": 120, "Stock": 80, "Precio": 100}
        for col, width in cols.items():
            self.tree_inventario.heading(col, text=col)
            self.tree_inventario.column(col, width=width, anchor="center" if col in ["Stock", "Precio"] else "w")
            
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_inventario.yview, style="Custom.Vertical.TScrollbar")
        self.tree_inventario.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree_inventario.pack(side="left", fill="both", expand=True)
        
        self.tree_inventario.tag_configure('oddrow', background=COLOR_FILA_IMPAR)
        self.tree_inventario.tag_configure('evenrow', background=COLOR_FILA_PAR)

        def actualizar_lista_inventario(*args):
            for i in self.tree_inventario.get_children():
                self.tree_inventario.delete(i)
            
            mi_taller_id = obtener_taller_id()
            if not mi_taller_id: return
            
            try:
                # Usamos la ruta general para ver TODO (Refacciones y Venta Directa)
                res = requests.post("https://www.ultracel.lat/api/inventario/buscar", json={"taller_id": mi_taller_id, "termino": search_var.get()})
                if res.status_code == 200:
                    for i, prod in enumerate(res.json().get('productos', [])):
                        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                        precio = float(prod.get('precio_venta', 0))
                        
                        self.tree_inventario.insert("", "end", values=(
                            prod.get('sku', 'N/A'), 
                            prod.get('nombre_producto', ''), 
                            prod.get('tipo_producto', ''),
                            prod.get('stock', 0), 
                            f"${precio:.2f}"
                        ), tags=(tag,))
                else:
                    print(f"Error API: {res.status_code} - {res.text}")
            except requests.exceptions.ConnectionError:
                pass

        search_var.trace_add("write", actualizar_lista_inventario)
        actualizar_lista_inventario()
    def abrir_formulario_cliente(self, id_cliente=None):
        self.limpiar_panel()

        contenedor = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        contenedor.pack(fill="both", expand=True)

        # --- Barra Superior (Navegación) ---
        top_bar = tk.Frame(contenedor, bg=COLOR_PRIMARIO, height=50)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        tk.Button(top_bar, text="⬅ REGRESAR", font=("Segoe UI", 10, "bold"), bg="#c0392b", fg="white",
                  relief="flat", command=self.mostrar_admin_clientes, padx=10).pack(side="left", padx=10, pady=10)

        titulo = "✏️ Editar Cliente" if id_cliente else "➕ Registrar Nuevo Cliente"
        tk.Label(top_bar, text=titulo, font=FUENTE_SUBTITULO, 
                 bg=COLOR_PRIMARIO, fg=COLOR_TEXTO_BLANCO).pack(side="left", padx=15, pady=10)

        # --- Contenedor del Formulario ---
        form_frame = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL, padx=100, pady=40)
        form_frame.pack(fill="both", expand=True)

        # Variables reactivas para los campos
        vars_cli = {
            "nombre": tk.StringVar(),
            "apellidos": tk.StringVar(),
            "telefono": tk.StringVar(),
            "email": tk.StringVar()
        }

        # --- Diseño de los campos en Grid ---
        # Fila 0: Nombre y Apellidos
        tk.Label(form_frame, text="Nombre(s):", font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_PANEL).grid(row=0, column=0, sticky="w", pady=10)
        tk.Entry(form_frame, textvariable=vars_cli["nombre"], font=FUENTE_CUERPO, bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDE).grid(row=0, column=1, sticky="ew", padx=(0, 30), ipady=5)

        tk.Label(form_frame, text="Apellidos:", font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_PANEL).grid(row=0, column=2, sticky="w", pady=10)
        tk.Entry(form_frame, textvariable=vars_cli["apellidos"], font=FUENTE_CUERPO, bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDE).grid(row=0, column=3, sticky="ew", ipady=5)

        # Fila 1: Teléfono y Email
        tk.Label(form_frame, text="Teléfono:", font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_PANEL).grid(row=1, column=0, sticky="w", pady=10)
        tk.Entry(form_frame, textvariable=vars_cli["telefono"], font=FUENTE_CUERPO, bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDE).grid(row=1, column=1, sticky="ew", padx=(0, 30), ipady=5)

        tk.Label(form_frame, text="Correo Electrónico (Opcional):", font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_PANEL).grid(row=1, column=2, sticky="w", pady=10)
        tk.Entry(form_frame, textvariable=vars_cli["email"], font=FUENTE_CUERPO, bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDE).grid(row=1, column=3, sticky="ew", ipady=5)

        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        # --- Lógica de Edición (Cargar datos de Laravel) ---
        if id_cliente:
            try:
                mi_taller_id = obtener_taller_id() # 🔒 CANDADO AÑADIDO
                res = requests.post("https://www.ultracel.lat/api/clientes/obtener", json={"id_cliente": id_cliente, "taller_id": mi_taller_id})
                if res.status_code == 200:
                    cli_data = res.json().get('cliente', {})
                    if cli_data:
                        vars_cli["nombre"].set(cli_data.get('nombre', ''))
                        vars_cli["apellidos"].set(cli_data.get('apellidos', ''))
                        vars_cli["telefono"].set(cli_data.get('telefono', ''))
                        vars_cli["email"].set(cli_data.get('email', '') if cli_data.get('email') else '')
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "No se pudo conectar al servidor para obtener los datos del cliente.")

        # --- Lógica de Guardado ---
        def guardar_cliente():
            payload = {
                "taller_id": obtener_taller_id(),
                "nombre": vars_cli["nombre"].get(),
                "apellidos": vars_cli["apellidos"].get(),
                "telefono": vars_cli["telefono"].get(),
                "email": vars_cli["email"].get()
            }

            if not payload["nombre"] or not payload["apellidos"]:
                return messagebox.showwarning("Datos Incompletos", "El nombre y los apellidos son obligatorios.")

            # Si estamos editando, le adjuntamos el ID al paquete
            if id_cliente:
                payload["id_cliente"] = id_cliente 

            try:
                res_save = requests.post("https://www.ultracel.lat/api/clientes/guardar", json=payload)
                if res_save.status_code == 200:
                    messagebox.showinfo("Éxito", res_save.json().get('message', 'Cliente guardado correctamente.'))
                    self.mostrar_admin_clientes() # Magia: regresa a la tabla y la actualiza
                else:
                    print(f"🚨 ERROR AL GUARDAR CLIENTE: {res_save.text}")
                    messagebox.showerror("Error", "No se pudo guardar la información. Revisa la terminal.")
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "Fallo de conexión al servidor.")

        # Botón Guardar
        btn_frame = tk.Frame(form_frame, bg=COLOR_FONDO_PANEL)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=40)
        
        crear_boton(btn_frame, "💾 GUARDAR CLIENTE", guardar_cliente, COLOR_EXITO, height=2).pack(side="left", padx=10)
        
    # Agregala como un nuevo metodo de la clase PanelVendedor
    def agregar_celular_nuevo(self):
        self.limpiar_panel()

        contenedor = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_APP)
        contenedor.pack(fill="both", expand=True)

        barra_titulo = tk.Frame(contenedor, bg=COLOR_PRIMARIO, height=50)
        barra_titulo.pack(fill="x")
        barra_titulo.pack_propagate(False)

        tk.Button(barra_titulo, text="⬅ REGRESAR", font=("Segoe UI", 10, "bold"), bg="#c0392b", fg="white",
                  relief="flat", command=self.mostrar_admin_clientes, padx=10).pack(side="left", padx=10, pady=10)

        tk.Label(barra_titulo, text="\U0001F4F1 Registrar Nuevo Celular", font=FUENTE_SUBTITULO,
                 bg=COLOR_PRIMARIO, fg=COLOR_TEXTO_BLANCO).pack(side="left", padx=15, pady=10)

        canvas = tk.Canvas(contenedor, bg=COLOR_FONDO_APP, highlightthickness=0)
        scrollbar = ttk.Scrollbar(contenedor, orient="vertical", command=canvas.yview, style="Custom.Vertical.TScrollbar")
        scroll_frame = tk.Frame(canvas, bg=COLOR_FONDO_APP)

        scroll_frame_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(scroll_frame_id, width=canvas.winfo_width())

        scroll_frame.bind("<Configure>", on_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            if event.delta:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            else:
                if event.num == 4: canvas.yview_scroll(-1, "units")
                elif event.num == 5: canvas.yview_scroll(1, "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)

        form_content = tk.Frame(scroll_frame, bg=COLOR_FONDO_APP, padx=100)
        form_content.pack(fill="both", expand=True, pady=20)

        tk.Label(form_content, text="Datos del Cliente", font=FUENTE_SUBTITULO, bg=COLOR_FONDO_APP, fg=COLOR_PRIMARIO).pack(pady=(15, 5))
        tk.Frame(form_content, height=2, bg=COLOR_BORDE).pack(fill="x", pady=(0, 15))

        frame_cliente = tk.Frame(form_content, bg=COLOR_FONDO_APP)
        frame_cliente.pack(fill="x")

        # --- MAGIA: Selector de Clientes Existentes ---
        tk.Label(frame_cliente, text="¿Es un cliente frecuente?:", font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_APP, fg=COLOR_TEXTO_OSCURO).pack(fill="x", pady=(0, 5))
        
        clientes_map = {"➕ Registrar Nuevo Cliente": None}
        lista_nombres = ["➕ Registrar Nuevo Cliente"]
        mi_taller_id = obtener_taller_id()

        try:
            # Aprovechamos la ruta del POS que ya nos trae los clientes
            res_cli = requests.post("https://www.ultracel.lat/api/pos/clientes", json={"taller_id": mi_taller_id})
            if res_cli.status_code == 200:
                for c in res_cli.json().get('clientes', []):
                    nombre_completo = c['nombre_completo']
                    clientes_map[nombre_completo] = c['id_cliente']
                    lista_nombres.append(nombre_completo)
        except: pass

        combo_cliente_var = tk.StringVar(value="➕ Registrar Nuevo Cliente")
        combo_clientes = ttk.Combobox(frame_cliente, textvariable=combo_cliente_var, values=lista_nombres, state="readonly", font=FUENTE_CUERPO)
        combo_clientes.pack(fill="x", pady=(0, 15), ipady=5)

        campos_cliente = {"Nombre(s):": "nombre", "Apellidos:": "apellidos", "Telefono:": "telefono", "Email (Opcional):": "email"}
        entries_cliente = {}
        for label, key in campos_cliente.items():
            tk.Label(frame_cliente, text=label, font=FUENTE_CUERPO, bg=COLOR_FONDO_APP, fg=COLOR_TEXTO_OSCURO, anchor="w").pack(fill="x", pady=(5,0))
            entry_frame, entry = crear_entry_estilizado(frame_cliente)
            entry_frame.pack(fill="x", pady=(2, 0))
            entries_cliente[key] = entry

        # Función para bloquear/desbloquear campos si elige uno existente
        def toggle_campos_cliente(*args):
            seleccion = combo_cliente_var.get()
            if clientes_map.get(seleccion) is None: # Si es "Nuevo Cliente"
                for entry in entries_cliente.values():
                    entry.configure(state="normal")
            else: # Si es un cliente existente
                for entry in entries_cliente.values():
                    entry.delete(0, tk.END)
                    entry.configure(state="disabled")

        combo_cliente_var.trace_add("write", toggle_campos_cliente)

        tk.Label(form_content, text="Datos del Celular", font=FUENTE_SUBTITULO, bg=COLOR_FONDO_APP, fg=COLOR_PRIMARIO).pack(pady=(30, 5))
        tk.Frame(form_content, height=2, bg=COLOR_BORDE).pack(fill="x", pady=(0, 15))

        frame_celular = tk.Frame(form_content, bg=COLOR_FONDO_APP)
        frame_celular.pack(fill="x")

        campos_celular = {"Marca:": "marca", "Modelo:": "modelo", "IMEI (Opcional):": "imei", "Color:": "color", "Descripcion de la Falla:": "descripcion"}
        entries_celular = {}
        for label, key in campos_celular.items():
            tk.Label(frame_celular, text=label, font=FUENTE_CUERPO, bg=COLOR_FONDO_APP, fg=COLOR_TEXTO_OSCURO, anchor="w").pack(fill="x", pady=(5,0))
            if key == "descripcion":
                text_frame, entry = crear_text_estilizado(frame_celular, height=3)
                text_frame.pack(fill="x", pady=(2, 0))
            else:
                entry_frame, entry = crear_entry_estilizado(frame_celular)
                entry_frame.pack(fill="x", pady=(2, 0))
            entries_celular[key] = entry

        def guardar():
            datos_celular = {}
            for k, v in entries_celular.items():
                if isinstance(v, tk.Text): datos_celular[k] = v.get("1.0", "end-1c")
                else: datos_celular[k] = v.get()
            
            if not datos_celular['marca'] or not datos_celular['modelo']:
                return messagebox.showwarning("Datos Incompletos", "Marca y modelo del celular son obligatorios.", parent=self.ventana)

            id_cliente_sel = clientes_map.get(combo_cliente_var.get())
            payload = {"taller_id": mi_taller_id, "equipo": datos_celular}

            if id_cliente_sel is None: # Es un cliente nuevo
                datos_cliente = {k: v.get() for k, v in entries_cliente.items()}
                if not datos_cliente['nombre'] or not datos_cliente['apellidos'] or not datos_cliente['telefono']:
                    return messagebox.showwarning("Datos Incompletos", "Nombre, apellidos y teléfono del nuevo cliente son obligatorios.", parent=self.ventana)
                payload["cliente"] = datos_cliente
            else: # Es un cliente existente
                payload["id_cliente"] = id_cliente_sel

            try:
                res = requests.post("https://www.ultracel.lat/api/clientes/registrar-equipo", json=payload)
                if res.status_code == 200:
                    messagebox.showinfo("Éxito", "Celular registrado correctamente.\nEl técnico ya lo tiene en su fila de pendientes.", parent=self.ventana)
                    self.mostrar_admin_clientes()
                else:
                    messagebox.showerror("Error", f"No se pudo registrar: {res.text}", parent=self.ventana)
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "Fallo de conexión al servidor.", parent=self.ventana)

        botones_frame = tk.Frame(form_content, bg=COLOR_FONDO_APP)
        botones_frame.pack(fill="x", pady=30)

        crear_boton(botones_frame, "\U0001F4BE Registrar Celular", guardar, COLOR_EXITO, fuente=FUENTE_BOTON, height=2).pack(side="left", expand=True, fill="x", padx=(0, 10))
        crear_boton(botones_frame, "Cancelar", self.mostrar_admin_clientes, COLOR_PELIGRO, fuente=FUENTE_CUERPO_BOLD, height=2).pack(side="left", expand=True, fill="x")

        self.ventana.after(100, lambda: canvas.configure(scrollregion=canvas.bbox("all")))
    
    def actualizar_carrito(self):
        self.carrito_text.delete("1.0", tk.END)
        for i, (nombre, precio) in enumerate(self.carrito):
            self.carrito_text.insert(tk.END, f"{i+1}. {nombre} - ${precio:.2f}\n")
        total = sum(p for _, p in self.carrito)
        self.total_var.set(f"${total:.2f}")
    def agregar(self, nombre, precio):
        self.carrito.append((nombre, precio))
        self.actualizar_carrito()
    def eliminar_producto(self):
        if not self.carrito:
            messagebox.showinfo("Carrito vacio", "No hay productos para eliminar.")
            return
        try:
            index = simpledialog.askstring("Eliminar", "Numero de producto a eliminar:")
            if index is None:
                return
            index = int(index) - 1
            if 0 <= index < len(self.carrito):
                eliminado = self.carrito.pop(index)
                messagebox.showinfo("Producto eliminado", f"Se elimino: {eliminado[0]}")
                self.actualizar_carrito()
            else:
                messagebox.showwarning("Indice invalido", "No existe ese numero de producto.")
        except:
            messagebox.showerror("Error", "Entrada invalida.")


if __name__ == "__main__":
    id_logueado = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    app = PanelVendedor(id_vendedor=id_logueado)
    