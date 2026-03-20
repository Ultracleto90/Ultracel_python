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
                url_api = "http://localhost/api/pos/clientes"
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
        botones_carrito_frame = tk.Frame(col_derecha, bg=COLOR_NOTA_VENTA_BG)
        botones_carrito_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        crear_boton(botones_carrito_frame, "Quitar Item", self.quitar_item_carrito,
                    COLOR_PELIGRO, fuente=FUENTE_CUERPO_BOLD).pack(side="left")
        btn_add_reparacion = crear_boton(botones_carrito_frame, "Finalizar y Cobrar",
                    lambda: self.finalizar_venta(clientes_map.get(cliente_var.get()), self.id_vendedor_logueado),
                    COLOR_EXITO, fuente=FUENTE_CUERPO_BOLD)
        btn_add_reparacion.pack(side="right", fill="x", expand=True, ipady=5, padx=(10, 0))
        # Botones de accion en la columna izquierda
        botones_accion_frame = tk.Frame(col_izquierda, bg=COLOR_FONDO_PANEL)
        botones_accion_frame.pack(fill="x", pady=(5, 0))
        crear_boton(botones_accion_frame, "Agregar Producto \u2192",
                    lambda: self.agregar_item_carrito(tree_productos, "producto"),
                    COLOR_SECUNDARIO, fuente=FUENTE_CUERPO_BOLD).pack(side="left", expand=True, fill="x", padx=(0,5))
        btn_add_reparacion_izq = crear_boton(botones_accion_frame, "Agregar Reparacion \u2192",
                    lambda: self.agregar_item_carrito(self.tree_reparaciones, "reparacion"),
                    COLOR_SECUNDARIO, fuente=FUENTE_CUERPO_BOLD)
        btn_add_reparacion_izq.pack(side="left", expand=True, fill="x")
        btn_add_reparacion_izq.configure(state="disabled")
        def buscar_productos(*args):
            termino = search_var.get()
            mi_taller_id = obtener_taller_id()
            if not mi_taller_id: return

            for i in tree_productos.get_children(): tree_productos.delete(i)
            try:
                res = requests.post("http://localhost/api/pos/buscar-productos", json={"taller_id": mi_taller_id, "termino": termino})
                if res.status_code == 200:
                    for p in res.json().get('productos', []):
                        tree_productos.insert("", "end", values=(p['id_producto'], p['nombre_producto'], f"${p['precio_venta']:.2f}"))
            except requests.exceptions.ConnectionError:
                pass

        search_var.trace_add("write", buscar_productos)
        buscar_productos()

        def on_cliente_seleccionado(*args):
            for i in self.tree_reparaciones.get_children(): self.tree_reparaciones.delete(i)
            btn_add_reparacion_izq.config(state="disabled")
            
            id_cliente = clientes_map.get(cliente_var.get())
            if not id_cliente:
                reparaciones_frame.pack_forget()
                return
            
            reparaciones_frame.pack(fill="x", pady=5)
            try:
                res = requests.post("http://localhost/api/pos/reparaciones-cliente", json={"id_cliente": id_cliente})
                if res.status_code == 200:
                    reparaciones = res.json().get('reparaciones', [])
                    for r in reparaciones:
                        presupuesto = f"${r['presupuesto']:.2f}" if r['presupuesto'] else "Sin Presupuesto"
                        self.tree_reparaciones.insert("", "end", values=(r['id_reparacion'], r['equipo'], presupuesto))
                    if reparaciones:
                        btn_add_reparacion_izq.config(state="normal")
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "No se pudo conectar al servidor.")

        combo_clientes.bind("<<ComboboxSelected>>", on_cliente_seleccionado)
    def agregar_item_carrito(self, treeview, tipo_item):
        item_seleccionado = treeview.selection()
        if not item_seleccionado: return
        
        valores = treeview.item(item_seleccionado[0], 'values')
        
        if tipo_item == "producto":
            id_item, desc, precio_str = valores
            precio = float(precio_str.replace('$', ''))
            # Guardamos el ID del producto y el tipo en el iid del treeview
            self.tree_carrito.insert("", "end", iid=f"P{id_item}", values=(1, desc, f"${precio:.2f}", f"${precio:.2f}"))
        
        elif tipo_item == "reparacion":
            id_item, desc, precio_str = valores
            precio = float(precio_str.replace('$', ''))
            # Guardamos el ID de la reparacion y el tipo
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
            res = requests.post("http://localhost/api/pos/procesar-venta", json=payload)
            
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
        contenedor.grid(row=0, column=0, sticky="nsew")
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
                res = requests.post("http://localhost/api/pos/clientes", json={"taller_id": mi_taller_id})
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
    def abrir_formulario_producto(self, id_producto_a_editar=None):
        ventana_formulario = tk.Toplevel(self.ventana)
        ventana_formulario.configure(bg=COLOR_FONDO_APP)
        ventana_formulario.geometry("480x650")
        ventana_formulario.resizable(False, False)
        # --- Barra de titulo personalizada ---
        barra_titulo = tk.Frame(ventana_formulario, bg=COLOR_PRIMARIO, height=50)
        barra_titulo.pack(fill="x")
        barra_titulo.pack_propagate(False)
        # --- Frame con Canvas y Scrollbar para scroll vertical ---
        canvas = tk.Canvas(ventana_formulario, bg=COLOR_FONDO_APP, highlightthickness=0)
        scrollbar = ttk.Scrollbar(ventana_formulario, orient="vertical", command=canvas.yview,
                                  style="Custom.Vertical.TScrollbar")
        scroll_frame = tk.Frame(canvas, bg=COLOR_FONDO_APP)
        # Vincular el frame al canvas
        scroll_frame_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(scroll_frame_id, width=canvas.winfo_width())
        scroll_frame.bind("<Configure>", on_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # Permitir scroll con la rueda del mouse
        def _on_mousewheel(event):
            if event.delta:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            else:  # Linux
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)
        producto_existente = None
        if id_producto_a_editar:
            ventana_formulario.title("Editar Producto")
            tk.Label(barra_titulo, text="\u270F Editar Producto", font=FUENTE_SUBTITULO, bg=COLOR_PRIMARIO, fg=COLOR_TEXTO_BLANCO).pack(side="left", padx=15, pady=10)
            try:
                res = requests.post("http://localhost/api/inventario/obtener", json={"id_producto": id_producto_a_editar})
                if res.status_code == 200: producto_existente = res.json().get('producto')
            except: pass
        else:
            ventana_formulario.title("Agregar Nuevo Producto")
            tk.Label(barra_titulo, text="\u2795 Agregar Nuevo Producto", font=FUENTE_SUBTITULO, bg=COLOR_PRIMARIO, fg=COLOR_TEXTO_BLANCO).pack(side="left", padx=15, pady=10)

        tk.Label(scroll_frame, text="Detalles del Producto", font=FUENTE_TITULO,
                 bg=COLOR_FONDO_APP, fg=COLOR_PRIMARIO).pack(pady=(15, 10))
        form_frame = tk.Frame(scroll_frame, bg=COLOR_FONDO_APP, padx=20)
        form_frame.pack(fill="x")
        entries = {}
        campos = {
            "SKU (Codigo Unico):": "sku",
            "Nombre del Producto:": "nombre_producto",
            "Marca Compatible:": "marca_compatible",
            "Modelo Compatible:": "modelo_compatible",
            "Stock (Cantidad):": "stock",
            "Precio de Compra $:": "precio_compra",
            "Precio de Venta $:": "precio_venta",
            "Ubicacion en Almacen:": "ubicacion_almacen",
            "Descripcion:": "descripcion"
        }
        for label, key in campos.items():
            tk.Label(form_frame, text=label, font=FUENTE_CUERPO, bg=COLOR_FONDO_APP,
                     fg=COLOR_TEXTO_OSCURO, anchor="w").pack(fill="x", pady=(8,0))
            valor_inicial = str(producto_existente.get(key, '')) if producto_existente else ''
            if key == "descripcion":
                text_frame, entry = crear_text_estilizado(form_frame, height=3)
                entry.insert("1.0", valor_inicial)
                text_frame.pack(fill="x", pady=(2, 0))
            else:
                entry_frame, entry = crear_entry_estilizado(form_frame)
                entry.insert(0, valor_inicial)
                entry_frame.pack(fill="x", pady=(2, 0))
            entries[key] = entry
        def guardar_producto():
            datos_form = {}
            for key, widget in entries.items():
                if isinstance(widget, tk.Text): datos_form[key] = widget.get("1.0", "end-1c")
                else: datos_form[key] = widget.get()
                
            if not datos_form['sku'] or not datos_form['nombre_producto'] or not datos_form['stock'].isdigit():
                return messagebox.showwarning("Datos Invalidos", "El SKU, Nombre y Stock (numerico) son obligatorios.", parent=ventana_formulario)
            
            mi_taller_id = obtener_taller_id()
            if not mi_taller_id: return
            
            payload = {
                "taller_id": mi_taller_id,
                "id_producto": id_producto_a_editar,
                "sku": datos_form['sku'],
                "nombre_producto": datos_form['nombre_producto'],
                "descripcion": datos_form['descripcion'],
                "marca_compatible": datos_form['marca_compatible'],
                "modelo_compatible": datos_form['modelo_compatible'],
                "stock": int(datos_form['stock']),
                "precio_compra": float(datos_form['precio_compra']) if datos_form['precio_compra'] else None,
                "precio_venta": float(datos_form['precio_venta']) if datos_form['precio_venta'] else 0.0,
                "ubicacion_almacen": datos_form['ubicacion_almacen']
            }
            
            try:
                res = requests.post("http://localhost/api/inventario/guardar", json=payload)
                data = res.json()
                if res.status_code == 200 and data.get('status'):
                    messagebox.showinfo("Exito", data.get('message'), parent=ventana_formulario)
                    ventana_formulario.destroy()
                    self.mostrar_inventario()
                else:
                    messagebox.showerror("Error", data.get('message', 'Fallo al guardar.'), parent=ventana_formulario)
            except:
                messagebox.showerror("Error", "Fallo de conexion.", parent=ventana_formulario)

        crear_boton(scroll_frame, "\U0001F4BE Guardar Producto", guardar_producto,
                    COLOR_EXITO, fuente=FUENTE_BOTON, height=2).pack(fill="x", padx=20, pady=20)
        # Forzar actualizacion del scrollregion al inicio
        ventana_formulario.after(100, lambda: canvas.configure(scrollregion=canvas.bbox("all")))
    def eliminar_producto_seleccionado(self):
        item_sel = self.tree_inventario.selection()
        if not item_sel: return messagebox.showwarning("Ninguna Seleccion", "Por favor, selecciona un producto.")
        
        sku_a_eliminar = self.tree_inventario.item(item_sel[0], 'values')[0]
        nombre_a_eliminar = self.tree_inventario.item(item_sel[0], 'values')[1]
        
        if messagebox.askyesno("Confirmar Eliminacion", f"¿Estas seguro de eliminar permanentemente el producto:\n\n{nombre_a_eliminar} (SKU: {sku_a_eliminar})?"):
            mi_taller_id = obtener_taller_id()
            if not mi_taller_id: return
            try:
                res = requests.post("http://localhost/api/inventario/eliminar", json={"sku": sku_a_eliminar, "taller_id": mi_taller_id})
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
        
    def mostrar_historial_cliente(self, event):
        item_sel = self.tree_clientes.selection()
        if not item_sel: return
        
        id_cliente = self.tree_clientes.item(item_sel[0], 'values')[0]
        nombre_cliente = self.tree_clientes.item(item_sel[0], 'values')[1]
        # --- Buscar el historial de reparaciones en la BD ---
        try:
            res = requests.post("http://localhost/api/clientes/historial", json={"id_cliente": id_cliente})
            if res.status_code == 200:
                historial = res.json().get('historial', [])
                if not historial:
                    tree_historial.insert("", "end", values=("", "", "Este cliente no tiene reparaciones.", "", ""))
                else:
                    for i, rep in enumerate(historial):
                        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                        presupuesto = f"${rep['presupuesto']:.2f}" if rep['presupuesto'] else "N/A"
                        tree_historial.insert("", "end", values=(
                            rep['id_reparacion'], rep['fecha'], rep['dispositivo'], rep['estado'], presupuesto
                        ), tags=(tag,))
        except: pass
        # --- Crear la ventana de historial ---
        ventana_historial = tk.Toplevel(self.ventana)
        ventana_historial.title(f"Historial de {nombre_cliente}")
        ventana_historial.geometry("650x450")
        ventana_historial.configure(bg=COLOR_FONDO_APP)
        # --- Barra de titulo ---
        barra_titulo = tk.Frame(ventana_historial, bg=COLOR_PRIMARIO, height=50)
        barra_titulo.pack(fill="x")
        barra_titulo.pack_propagate(False)
        tk.Label(barra_titulo, text=f"Historial de Reparaciones - {nombre_cliente}",
                 font=FUENTE_SUBTITULO, bg=COLOR_PRIMARIO,
                 fg=COLOR_TEXTO_BLANCO).pack(side="left", padx=15, pady=10)
        tree_frame = tk.Frame(ventana_historial, bg=COLOR_FONDO_APP)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        tree_historial = ttk.Treeview(tree_frame,
                                       columns=("ID", "Fecha", "Dispositivo", "Estado", "Presupuesto"),
                                       show="headings", style="Custom.Treeview")
        tree_historial.heading("ID", text="ID Orden"); tree_historial.heading("Fecha", text="Fecha");
        tree_historial.heading("Dispositivo", text="Dispositivo"); tree_historial.heading("Estado", text="Estado");
        tree_historial.heading("Presupuesto", text="Presupuesto");
        tree_historial.column("ID", width=60, anchor="center"); tree_historial.column("Fecha", width=100);
        tree_historial.column("Dispositivo", width=180); tree_historial.column("Estado", width=120);
        tree_historial.column("Presupuesto", width=100, anchor="e");
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical",
                                  command=tree_historial.yview,
                                  style="Custom.Vertical.TScrollbar")
        tree_historial.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree_historial.pack(side="left", fill="both", expand=True)
        
        if not historial:
            tree_historial.insert("", "end", values=("", "", "Este cliente no tiene reparaciones registradas.", "", ""))
        else:
            for i, reparacion in enumerate(historial):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                presupuesto_formato = f"${reparacion['presupuesto']:.2f}" if reparacion['presupuesto'] else "N/A"
                tree_historial.insert("", "end", values=(
                    reparacion['id_reparacion'], reparacion['fecha'],
                    reparacion['dispositivo'], reparacion['estado'],
                    presupuesto_formato
                ), tags=(tag,))
            tree_historial.tag_configure('oddrow', background=COLOR_FILA_IMPAR)
            tree_historial.tag_configure('evenrow', background=COLOR_FILA_PAR)
    
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
                res = requests.post("http://localhost/api/pos/historial-ventas", json={"taller_id": mi_taller_id})
                if res.status_code == 200:
                    for idx, v in enumerate(res.json().get('ventas', [])):
                        tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                        tree_ventas.insert("", "end", values=(
                            v['id_venta'], v['fecha'], v['cliente'],
                            v['vendedor'], f"${v['monto_total']:.2f}"
                        ), tags=(tag,))
                    tree_ventas.tag_configure('oddrow', background=COLOR_FILA_IMPAR)
                    tree_ventas.tag_configure('evenrow', background=COLOR_FILA_PAR)
            except: pass

        def mostrar_detalles_venta(event):
            item_seleccionado = tree_ventas.selection()
            if not item_seleccionado: return
            id_venta = tree_ventas.item(item_seleccionado[0], 'values')[0]
            
            for i in tree_detalles.get_children(): tree_detalles.delete(i)
            try:
                res = requests.post("http://localhost/api/pos/detalles-venta", json={"id_venta": id_venta})
                if res.status_code == 200:
                    for d in res.json().get('detalles', []):
                        subtotal = d['cantidad'] * d['precio_unitario']
                        tree_detalles.insert("", "end", values=(
                            d['cantidad'], d['descripcion_linea'],
                            f"${d['precio_unitario']:.2f}", f"${subtotal:.2f}"
                        ))
            except: pass
                
        # --- CONEXION DE EVENTOS ---
        tree_ventas.bind("<<TreeviewSelect>>", mostrar_detalles_venta)
        cargar_lista_ventas()
    import tkinter as tk
    from tkinter import ttk, messagebox, simpledialog
    def mostrar_inventario(self):
        self.limpiar_panel()
        contenedor = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        contenedor.grid(row=0, column=0, sticky="nsew")
        # --- Encabezado ---
        header = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL)
        header.pack(fill="x", padx=20, pady=(10, 5))
        tk.Label(header, text="\U0001F4E6 Gestion de Inventario para Venta", font=FUENTE_TITULO,
                 bg=COLOR_FONDO_PANEL, fg=COLOR_PRIMARIO).pack(anchor="w")
        tk.Label(header, text="Busca, agrega, edita o elimina productos del inventario",
                 font=FUENTE_ETIQUETA, bg=COLOR_FONDO_PANEL,
                 fg=COLOR_TEXTO_GRIS).pack(anchor="w")
        # Separador
        tk.Frame(contenedor, height=2, bg=COLOR_BORDE).pack(fill="x", padx=20, pady=(5, 10))
        # --- Frame para Controles (Botones y Busqueda) ---
        controles_frame = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL)
        controles_frame.pack(fill="x", pady=10, padx=20)
        
        # Botones de Accion
        crear_boton(controles_frame, "\u2795 Nuevo Producto", self.abrir_formulario_producto,
                    COLOR_EXITO, fuente=FUENTE_CUERPO_BOLD).pack(side="left", padx=(0,10))
        def editar_seleccion_inv():
            item_sel = self.tree_inventario.selection()
            if not item_sel: return messagebox.showwarning("Seleccion", "Selecciona un producto.")
            
            sku_sel = self.tree_inventario.item(item_sel[0], 'values')[0]
            mi_taller_id = obtener_taller_id()
            if not mi_taller_id: return
            
            try:
                res = requests.post("http://localhost/api/inventario/obtener-por-sku", json={"sku": sku_sel, "taller_id": mi_taller_id})
                if res.status_code == 200 and res.json().get('id_producto'):
                    self.abrir_formulario_producto(res.json().get('id_producto'))
            except: pass

           
        crear_boton(controles_frame, "\u270F Editar Seleccionado", editar_seleccion_inv,
                    COLOR_ADVERTENCIA, fuente=FUENTE_CUERPO_BOLD).pack(side="left", padx=(0,10))
        crear_boton(controles_frame, "\u274C Eliminar", self.eliminar_producto_seleccionado,
                    COLOR_PELIGRO, fuente=FUENTE_CUERPO_BOLD).pack(side="left")
        
        # Barra de Busqueda
        search_var = tk.StringVar()
        search_frame_outer = tk.Frame(controles_frame, bg=COLOR_FONDO_PANEL)
        search_frame_outer.pack(side="right", fill="x", expand=True)
        tk.Label(search_frame_outer, text="\U0001F50D Buscar:", font=FUENTE_CUERPO,
                 bg=COLOR_FONDO_PANEL, fg=COLOR_TEXTO_OSCURO).pack(side="left", padx=(10, 5))
        search_entry_frame, search_entry = crear_entry_estilizado(search_frame_outer, textvariable=search_var)
        search_entry_frame.pack(side="left", fill="x", expand=True)
        # --- Treeview para mostrar el inventario ---
        tree_frame = tk.Frame(contenedor, bg=COLOR_FONDO_PANEL)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self.tree_inventario = ttk.Treeview(tree_frame,
                                             columns=("SKU", "Producto", "Descripcion", "Stock", "Precio"),
                                             show="headings", style="Custom.Treeview")
        
        cols = {"SKU": 100, "Producto": 200, "Descripcion": 250, "Stock": 80, "Precio": 100}
        for col, width in cols.items():
            self.tree_inventario.heading(col, text=col)
            self.tree_inventario.column(col, width=width, anchor="w" if col != "Stock" else "center")
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical",
                                  command=self.tree_inventario.yview,
                                  style="Custom.Vertical.TScrollbar")
        self.tree_inventario.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree_inventario.pack(side="left", fill="both", expand=True)
        
        self.tree_inventario.tag_configure('oddrow', background=COLOR_FILA_IMPAR)
        self.tree_inventario.tag_configure('evenrow', background=COLOR_FILA_PAR)
        # --- Logica de la Base de Datos ---
        def actualizar_lista_inventario(*args):
            for i in self.tree_inventario.get_children():
                self.tree_inventario.delete(i)
            
            termino_busqueda = search_var.get()
            mi_taller_id = obtener_taller_id()
            if not mi_taller_id: return
            
            try:
                # Usamos la ruta de POSController que creamos en el paso anterior
                res = requests.post("http://localhost/api/pos/buscar-productos", json={"taller_id": mi_taller_id, "termino": termino_busqueda})
                if res.status_code == 200:
                    for i, prod in enumerate(res.json().get('productos', [])):
                        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                        precio_formato = f"${prod['precio_venta']:.2f}"
                        # Asumo que las columnas en tree_inventario son (SKU, Nombre, Descripcion, Stock, Precio)
                        # Nota: El endpoint buscarProductos devuelve id_producto, nombre_producto, precio_venta. Si necesitas SKU y stock, asegúrate de que el endpoint los seleccione.
                        self.tree_inventario.insert("", "end", values=(
                            prod.get('sku', prod.get('id_producto')), 
                            prod.get('nombre_producto'), 
                            prod.get('descripcion', ''),
                            prod.get('stock', ''), 
                            precio_formato
                        ), tags=(tag,))
            except requests.exceptions.ConnectionError:
                pass

        search_var.trace_add("write", actualizar_lista_inventario)
        actualizar_lista_inventario()
    def abrir_formulario_cliente(self, id_cliente_a_editar=None):
        ventana_formulario = tk.Toplevel(self.ventana)
        ventana_formulario.configure(bg=COLOR_FONDO_APP)
        ventana_formulario.geometry("430x450")
        ventana_formulario.resizable(False, False)
        
        # --- Barra de titulo personalizada ---
        barra_titulo = tk.Frame(ventana_formulario, bg=COLOR_PRIMARIO, height=50)
        barra_titulo.pack(fill="x")
        barra_titulo.pack_propagate(False)
        
        cliente_existente = None
        
        # Si hay un ID, pedimos los datos a Laravel en lugar de MySQL
        if id_cliente_a_editar:
            ventana_formulario.title("Editar Cliente")
            tk.Label(barra_titulo, text="\u270F Editar Cliente", font=FUENTE_SUBTITULO,
                     bg=COLOR_PRIMARIO, fg=COLOR_TEXTO_BLANCO).pack(side="left", padx=15, pady=10)
            
            try:
                res = requests.post("http://localhost/api/clientes/obtener", json={"id_cliente": id_cliente_a_editar})
                if res.status_code == 200:
                    cliente_existente = res.json().get('cliente', {})
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "No se pudo conectar al servidor para obtener los datos del cliente.", parent=ventana_formulario)
                ventana_formulario.destroy()
                return
        else:
            ventana_formulario.title("Agregar Nuevo Cliente")
            tk.Label(barra_titulo, text="\U0001F464 Agregar Nuevo Cliente", font=FUENTE_SUBTITULO,
                     bg=COLOR_PRIMARIO, fg=COLOR_TEXTO_BLANCO).pack(side="left", padx=15, pady=10)
                     
        tk.Label(ventana_formulario, text="Datos del Cliente", font=FUENTE_TITULO,
                 bg=COLOR_FONDO_APP, fg=COLOR_PRIMARIO).pack(pady=(15, 10))
                 
        form_frame = tk.Frame(ventana_formulario, bg=COLOR_FONDO_APP, padx=20)
        form_frame.pack(fill="x")
        
        entries = {}
        campos = {"Nombre(s):": "nombre", "Apellidos:": "apellidos", "Telefono:": "telefono", "Email (Opcional):": "email"}
        
        # Dibujamos las cajas de texto y las rellenamos si hay datos
        for label, key in campos.items():
            tk.Label(form_frame, text=label, font=FUENTE_CUERPO, bg=COLOR_FONDO_APP,
                     fg=COLOR_TEXTO_OSCURO, anchor="w").pack(fill="x", pady=(8,0))
            
            # Sacamos el valor del diccionario que nos devolvió Laravel (o lo dejamos en blanco)
            valor_inicial = str(cliente_existente.get(key, '')) if cliente_existente else ''
            
            entry_frame, entry = crear_entry_estilizado(form_frame)
            entry.insert(0, valor_inicial)
            entry_frame.pack(fill="x", pady=(2, 0))
            entries[key] = entry
        def guardar_cliente():
            datos_form = {key: widget.get() for key, widget in entries.items()}
            if not datos_form['nombre'] or not datos_form['apellidos'] or not datos_form['telefono']:
                return messagebox.showwarning("Datos Incompletos", "El nombre, apellidos y telefono son obligatorios.", parent=ventana_formulario)
            
            mi_taller_id = obtener_taller_id()
            if not mi_taller_id: return messagebox.showerror("Error", "Licencia inválida.")

            payload = {
                "taller_id": mi_taller_id,
                "id_cliente": id_cliente_a_editar,
                "nombre": datos_form['nombre'],
                "apellidos": datos_form['apellidos'],
                "telefono": datos_form['telefono'],
                "email": datos_form['email']
            }

            try:
                res = requests.post("http://localhost/api/clientes/guardar", json=payload)
                data = res.json()
                if res.status_code == 200 and data.get('status'):
                    messagebox.showinfo("Éxito", data.get('message'), parent=ventana_formulario)
                    ventana_formulario.destroy()
                    self.mostrar_admin_clientes()
                else:
                    msg = data.get('message', 'Error desconocido.')
                    if "El teléfono ya está registrado" in msg:
                        messagebox.showerror("Error de Duplicado", msg, parent=ventana_formulario)
                    else:
                        messagebox.showerror("Error", msg, parent=ventana_formulario)
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "Fallo de conexión.", parent=ventana_formulario)
        crear_boton(ventana_formulario, "\U0001F4BE Guardar Cliente", guardar_cliente,
                    COLOR_EXITO, fuente=FUENTE_BOTON, height=2).pack(fill="x", padx=20, pady=20)
        
    # Agregala como un nuevo metodo de la clase PanelVendedor
    def agregar_celular_nuevo(self):
        # Ventana para registrar cliente y celular
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Registrar Nuevo Celular para Reparacion")
        ventana.geometry("450x550")
        ventana.configure(bg=COLOR_FONDO_APP)
        ventana.resizable(False, False)
        # --- Barra de titulo personalizada ---
        barra_titulo = tk.Frame(ventana, bg=COLOR_PRIMARIO, height=50)
        barra_titulo.pack(fill="x")
        barra_titulo.pack_propagate(False)
        tk.Label(barra_titulo, text="\U0001F4F1 Registrar Nuevo Celular", font=FUENTE_SUBTITULO,
                 bg=COLOR_PRIMARIO, fg=COLOR_TEXTO_BLANCO).pack(side="left", padx=15, pady=10)
        # --- Frame con Canvas y Scrollbar para scroll vertical ---
        canvas = tk.Canvas(ventana, bg=COLOR_FONDO_APP, highlightthickness=0)
        scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=canvas.yview,
                                  style="Custom.Vertical.TScrollbar")
        scroll_frame = tk.Frame(canvas, bg=COLOR_FONDO_APP)
        # Vincular el frame al canvas
        scroll_frame_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        def on_configure(event):
            # Ajustar el scrollregion al tamano del frame interno
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Ajustar el ancho del frame al canvas
            canvas.itemconfig(scroll_frame_id, width=canvas.winfo_width())
        scroll_frame.bind("<Configure>", on_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # Permitir scroll con la rueda del mouse
        def _on_mousewheel(event):
            if event.delta:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            else:  # Linux
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)
        # --- CONTENIDO DEL FORMULARIO ---
        tk.Label(scroll_frame, text="Datos del Cliente", font=FUENTE_SUBTITULO,
                 bg=COLOR_FONDO_APP, fg=COLOR_PRIMARIO).pack(pady=(15, 5))
        # Separador
        tk.Frame(scroll_frame, height=2, bg=COLOR_BORDE).pack(fill="x", padx=20, pady=(0, 5))
        frame_cliente = tk.Frame(scroll_frame, bg=COLOR_FONDO_APP)
        frame_cliente.pack(fill="x", padx=20)
        campos_cliente = {
            "Nombre(s):": "nombre",
            "Apellidos:": "apellidos",
            "Telefono:": "telefono",
            "Email (Opcional):": "email"
        }
        entries_cliente = {}
        for label, key in campos_cliente.items():
            tk.Label(frame_cliente, text=label, font=FUENTE_CUERPO, bg=COLOR_FONDO_APP,
                     fg=COLOR_TEXTO_OSCURO, anchor="w").pack(fill="x", pady=(5,0))
            entry_frame, entry = crear_entry_estilizado(frame_cliente)
            entry_frame.pack(fill="x", pady=(2, 0))
            entries_cliente[key] = entry
        tk.Label(scroll_frame, text="Datos del Celular", font=FUENTE_SUBTITULO,
                 bg=COLOR_FONDO_APP, fg=COLOR_PRIMARIO).pack(pady=(20, 5))
        # Separador
        tk.Frame(scroll_frame, height=2, bg=COLOR_BORDE).pack(fill="x", padx=20, pady=(0, 5))
        frame_celular = tk.Frame(scroll_frame, bg=COLOR_FONDO_APP)
        frame_celular.pack(fill="x", padx=20)
        campos_celular = {
            "Marca:": "marca",
            "Modelo:": "modelo",
            "IMEI (Opcional):": "imei",
            "Color:": "color",
            "Descripcion del Falla:": "descripcion"
        }
        entries_celular = {}
        for label, key in campos_celular.items():
            tk.Label(frame_celular, text=label, font=FUENTE_CUERPO, bg=COLOR_FONDO_APP,
                     fg=COLOR_TEXTO_OSCURO, anchor="w").pack(fill="x", pady=(5,0))
            if key == "descripcion":
                text_frame, entry = crear_text_estilizado(frame_celular, height=3)
                text_frame.pack(fill="x", pady=(2, 0))
            else:
                entry_frame, entry = crear_entry_estilizado(frame_celular)
                entry_frame.pack(fill="x", pady=(2, 0))
            entries_celular[key] = entry
        def guardar():
            # Validaciones locales (igual que las tuyas)
            datos_cliente = {k: v.get() for k, v in entries_cliente.items()}
            if not datos_cliente['nombre'] or not datos_cliente['apellidos'] or not datos_cliente['telefono']:
                return messagebox.showwarning("Datos Incompletos", "Nombre, apellidos y telefono del cliente son obligatorios.", parent=ventana)
            
            datos_celular = {}
            for k, v in entries_celular.items():
                if isinstance(v, tk.Text): datos_celular[k] = v.get("1.0", "end-1c")
                else: datos_celular[k] = v.get()
            
            if not datos_celular['marca'] or not datos_celular['modelo']:
                return messagebox.showwarning("Datos Incompletos", "Marca y modelo del celular son obligatorios.", parent=ventana)

            mi_taller_id = obtener_taller_id()
            if not mi_taller_id: return messagebox.showerror("Error", "Licencia inválida.", parent=ventana)

            payload = {
                "taller_id": mi_taller_id,
                "cliente": datos_cliente,
                "equipo": datos_celular
            }

            try:
                res = requests.post("http://localhost/api/clientes/registrar-equipo", json=payload)
                if res.status_code == 200:
                    messagebox.showinfo("Éxito", "Celular y cliente registrados correctamente.\nEl técnico podrá ver el dispositivo como pendiente.", parent=ventana)
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", res.json().get('message', 'No se pudo registrar.'), parent=ventana)
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "Fallo de conexión al servidor.", parent=ventana)
        # --- Botones de accion (Guardar y Cancelar) ---
        botones_frame = tk.Frame(scroll_frame, bg=COLOR_FONDO_APP)
        botones_frame.pack(fill="x", padx=20, pady=20)
        crear_boton(botones_frame, "\U0001F4BE Registrar Celular", guardar,
                    COLOR_EXITO, fuente=FUENTE_BOTON, height=2).pack(side="left", expand=True, fill="x", padx=(0, 10))
        crear_boton(botones_frame, "Cancelar", ventana.destroy,
                    COLOR_PELIGRO, fuente=FUENTE_CUERPO_BOLD, height=2).pack(side="left", expand=True, fill="x")
        # Forzar actualizacion del scrollregion al inicio
        ventana.after(100, lambda: canvas.configure(scrollregion=canvas.bbox("all")))
    def eliminar_cliente_seleccionado(self):
        item_seleccionado = self.tree_clientes.selection()
        if not item_seleccionado:
            return messagebox.showwarning("Ninguna Selección", "Por favor, selecciona un cliente de la lista para eliminar.")
        
        id_a_eliminar = self.tree_clientes.item(item_seleccionado[0], 'values')[0]
        nombre_a_eliminar = self.tree_clientes.item(item_seleccionado[0], 'values')[1]
        
        if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar a '{nombre_a_eliminar}'?\n\nADVERTENCIA: Se borrarán también todos sus equipos y reparaciones asociadas."):
            try:
                res = requests.post("http://localhost/api/clientes/eliminar", json={"id_cliente": id_a_eliminar})
                if res.status_code == 200:
                    messagebox.showinfo("Eliminado", "El cliente ha sido eliminado correctamente.")
                    self.mostrar_admin_clientes()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el cliente.")
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error de Red", "Fallo de conexión al servidor.")
    
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
    app = PanelVendedor()