import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageFilter
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


def crear_boton(parent, texto, comando, color_bg, color_fg=COLOR_TEXTO_BLANCO,
                fuente=FUENTE_BOTON, height=1, ancho=None, padx_btn=12, pady_btn=6):
    """Crea un boton estilizado con efecto hover."""
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


def crear_entry_estilizado(parent, font=FUENTE_CUERPO, width=None):
    """Crea un Entry con borde sutil y padding."""
    frame = tk.Frame(parent, bg=COLOR_BORDE, bd=0, highlightthickness=0)
    entry = tk.Entry(frame, font=font, bd=0, bg=COLOR_TEXTO_BLANCO,
                     fg=COLOR_TEXTO_OSCURO, insertbackground=COLOR_SECUNDARIO,
                     highlightthickness=0)
    if width:
        entry.configure(width=width)
    entry.pack(fill="x", padx=1, pady=1, ipady=6)
    return frame, entry


def crear_text_estilizado(parent, height=3, font=FUENTE_CUERPO):
    """Crea un Text widget con borde sutil."""
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


class PanelTecnico:
    def __init__(self, id_tecnico=None):
        self.id_tecnico_logueado = id_tecnico if id_tecnico else 2
        self.ventana = tk.Tk()
        self.ventana.title("Panel Tecnico - ULTRA-CEL")
        self.ventana.geometry("900x600")
        self.ventana.minsize(800, 500)
        self.ventana.resizable(True, True)
        self.ventana.configure(bg=COLOR_FONDO_APP)

        configurar_estilos_ttk()

        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(__file__)

            image_path = os.path.join(base_path, "assets", "fondo.png")
            fondo_original = Image.open(image_path).resize((900, 600))
            fondo_blur = fondo_original.filter(ImageFilter.GaussianBlur(radius=12))
            self.fondo_tk = ImageTk.PhotoImage(fondo_blur)

            self.canvas_fondo = tk.Canvas(self.ventana, width=900, height=600, highlightthickness=0)
            self.canvas_fondo.pack(fill="both", expand=True)
            self.canvas_fondo.create_image(0, 0, anchor="nw", image=self.fondo_tk)
            self._overlay_id = self.canvas_fondo.create_rectangle(0, 0, 900, 600, fill=COLOR_FONDO_APP, stipple="gray25", outline="")
        except Exception as e:
            print(f"Error cargando fondo: {e}")
            self.ventana.configure(bg=COLOR_FONDO_APP)
            self.canvas_fondo = tk.Canvas(self.ventana, width=900, height=600,
                                          highlightthickness=0, bg=COLOR_FONDO_APP)
            self.canvas_fondo.pack(fill="both", expand=True)
            self._overlay_id = None

        # --- Panel flotante con sombra sutil ---
        self._shadow_id = self.canvas_fondo.create_rectangle(23, 23, 883, 563,
                                           fill="#C8D6E5", outline="", stipple="gray12")
        self.panel_flotante = tk.Frame(self.canvas_fondo, bg=COLOR_FONDO_PANEL,
                                       highlightbackground=COLOR_BORDE,
                                       highlightthickness=1)
        self._panel_win_id = self.canvas_fondo.create_window(450, 300, window=self.panel_flotante,
                                        anchor="center", width=860, height=560)

        self.menu_visible = False

        #  Boton Hamburguesa estilizado 
        self.boton_menu = tk.Button(self.panel_flotante, text="  \u2630  Menu  ",
                                    font=FUENTE_MENU, bg=COLOR_PRIMARIO,
                                    fg=COLOR_TEXTO_BLANCO, relief="flat",
                                    cursor="hand2", bd=0, padx=10, pady=4,
                                    activebackground=COLOR_MENU_HOVER,
                                    activeforeground=COLOR_TEXTO_BLANCO,
                                    command=self.toggle_menu)
        self.boton_menu.place(x=10, y=10)

        #  Menu lateral 
        self.menu_lateral = tk.Frame(self.canvas_fondo, bg=COLOR_MENU_BG, width=0)
        self.menu_lateral.place(x=0, y=0, relheight=1)
        self.menu_lateral.pack_propagate(False)
        self.crear_menu_lateral()

        # Panel dinamico (contenido principal) 
        self.panel_dinamico = tk.Frame(self.panel_flotante, bg=COLOR_FONDO_PANEL)
        self.panel_dinamico.place(x=10, y=60, relwidth=1.0, relheight=1.0, width=-20, height=-70)

        # Responsividad 
        self.canvas_fondo.bind("<Configure>", self._on_resize)

        self.cargar_pendientes()
        self.ventana.mainloop()

    #  METODOS DE LA CLASE 

    def _on_resize(self, event):
        """Actualiza los elementos del canvas al redimensionar la ventana."""
        w = event.width
        h = event.height
        # Overlay de fondo
        if hasattr(self, '_overlay_id') and self._overlay_id:
            self.canvas_fondo.coords(self._overlay_id, 0, 0, w, h)
        # Sombra del panel
        margen = 20
        self.canvas_fondo.coords(self._shadow_id, margen + 3, margen + 3, w - margen + 3, h - margen + 3)
        # Panel flotante centrado
        self.canvas_fondo.coords(self._panel_win_id, w / 2, h / 2)
        self.canvas_fondo.itemconfigure(self._panel_win_id, width=w - margen * 2, height=h - margen * 2)

    def conectar_bd(self):
        try:
            return mysql.connector.connect(host="localhost",user="root",password="",database="ultracel")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexion", f"No se pudo conectar: {err}")
            return None

    def toggle_menu(self):
        destino = 180 if not self.menu_visible else 0
        paso = 12
        ancho_actual = self.menu_lateral.winfo_width()
        def animar():
            nonlocal ancho_actual
            if self.menu_visible and ancho_actual > destino: ancho_actual -= paso
            elif not self.menu_visible and ancho_actual < destino: ancho_actual += paso
            self.menu_lateral.place_configure(width=ancho_actual)
            if abs(ancho_actual - destino) > paso:
                self.ventana.after(10, animar)
            else:
                self.menu_visible = not self.menu_visible
                if not self.menu_visible: self.menu_lateral.place_configure(width=0)
        animar()

    def crear_menu_lateral(self):
        self.menu_lateral.configure(bg=COLOR_MENU_BG)

        # --- Encabezado del menu ---
        header_frame = tk.Frame(self.menu_lateral, bg=COLOR_MENU_BG)
        header_frame.pack(fill="x", pady=(25, 5))

        tk.Label(header_frame, text="ULTRA-CEL", font=FUENTE_MENU_TITULO,
                 bg=COLOR_MENU_BG, fg=COLOR_TEXTO_BLANCO).pack()
        tk.Label(header_frame, text="Panel Tecnico", font=FUENTE_ETIQUETA,
                 bg=COLOR_MENU_BG, fg=COLOR_ACENTO).pack()

        # Separador
        sep_frame = tk.Frame(self.menu_lateral, bg=COLOR_MENU_HOVER, height=1)
        sep_frame.pack(fill="x", padx=20, pady=(15, 10))

        # Opciones del menu 
        opciones = [
            ("\u2B05  Regresar",       self.toggle_menu),
            ("\U0001F4DD  Pendientes",  self.cargar_pendientes),
            ("\U0001F4E6  Inventario",  self.cargar_inventario),
            ("\U0001FA7A  Diagnostico", self.cargar_diagnostico),
            ("\U0001F4D1  Reporte",     self.cargar_reporte_material)
        ]

        for texto, comando in opciones:
            btn_frame = tk.Frame(self.menu_lateral, bg=COLOR_MENU_BG)
            btn_frame.pack(fill="x")

            btn = tk.Button(btn_frame, text=texto, anchor="w",
                            bg=COLOR_MENU_BG, fg=COLOR_TEXTO_BLANCO, relief="flat",
                            font=FUENTE_MENU, padx=25, pady=12, bd=0,
                            activebackground=COLOR_MENU_HOVER,
                            activeforeground=COLOR_TEXTO_BLANCO, cursor="hand2",
                            command=lambda c=comando, t=texto: [c(), self.toggle_menu() if t != "\u2B05  Regresar" else None])
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

        #  Boton Salir (fijado al fondo) 
        btn_salir = tk.Button(self.menu_lateral, text="\u23FB  Cerrar Sesion", anchor="center",
                              bg=COLOR_PELIGRO, fg=COLOR_TEXTO_BLANCO, relief="flat",
                              font=FUENTE_BOTON, pady=12, bd=0, cursor="hand2",
                              activebackground=_aclarar_color(COLOR_PELIGRO, 20),
                              activeforeground=COLOR_TEXTO_BLANCO,
                              command=self.volver_al_login)
        btn_salir.place(relx=0, rely=0.92, relwidth=1)

    def limpiar_panel(self):
        for widget in self.panel_dinamico.winfo_children():
            widget.destroy()

    def cargar_pendientes(self):
        self.limpiar_panel()

        #  Encabezado 
        header = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        header.pack(fill="x", padx=15, pady=(10, 5))
        tk.Label(header, text="\U0001F4CB Dispositivos Pendientes",
                 font=FUENTE_TITULO, bg=COLOR_FONDO_PANEL,
                 fg=COLOR_PRIMARIO).pack(anchor="w")
        tk.Label(header, text="Doble clic en una fila para ver los detalles completos",
                 font=FUENTE_ETIQUETA, bg=COLOR_FONDO_PANEL,
                 fg=COLOR_TEXTO_GRIS).pack(anchor="w")

        tk.Frame(self.panel_dinamico, height=2, bg=COLOR_BORDE).pack(fill="x", padx=15, pady=(5, 10))

        # --- Treeview ---
        tree_frame = tk.Frame(self.panel_dinamico, bg=COLOR_BORDE, bd=0)
        tree_frame.pack(pady=0, padx=15, fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Dispositivo", "Problema Reportado"), show="headings", height=15, style="Custom.Treeview")
        self.tree.heading("ID", text="ID Orden")
        self.tree.heading("Dispositivo", text="Dispositivo")
        self.tree.heading("Problema Reportado", text="Problema Reportado")
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Dispositivo", width=200)
        self.tree.column("Problema Reportado", width=350)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview, style="Custom.Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", padx=(0, 1), pady=1)
        self.tree.pack(fill="both", expand=True, padx=1, pady=1)

        self.tree.tag_configure('evenrow', background=COLOR_FILA_PAR)
        self.tree.tag_configure('oddrow', background=COLOR_FILA_IMPAR)

        mi_taller_id = obtener_taller_id()
        if not mi_taller_id:
            return messagebox.showerror("Error", "No hay licencia activa.")
            
        for i in self.tree.get_children(): self.tree.delete(i)

        try:
            url_api = "http://localhost/api/reparaciones/pendientes"
            respuesta = requests.post(url_api, json={"taller_id": mi_taller_id})
            
            if respuesta.status_code == 200:
                reparaciones = respuesta.json().get('reparaciones', [])
                for idx, rep in enumerate(reparaciones):
                    tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                    self.tree.insert("", "end", values=(rep.get('id_reparacion'), rep.get('dispositivo'), rep.get('problema_reportado')), tags=(tag,))
        except:
            messagebox.showerror("Error", "Sin conexión al servidor.")

        # VINCULAMOS LA FUNCIÓN RESCATADA
        self.tree.bind("<Double-1>", self.mostrar_detalles_reparacion)

    # --- LA FUNCIÓN RESCATADA Y CONECTADA A LARAVEL ---
    def mostrar_detalles_reparacion(self, event):
        item_seleccionado = self.tree.selection()
        if not item_seleccionado: return
        
        id_reparacion = self.tree.item(item_seleccionado[0], 'values')[0]

        # Pedimos los detalles a Laravel
        try:
            res = requests.post("http://localhost/api/reparaciones/detalles", json={"id_reparacion": id_reparacion})
            if res.status_code == 200:
                detalles = res.json().get('detalles', {})
            else:
                return messagebox.showerror("Error", "No se pudo cargar la información.")
        except:
            return messagebox.showerror("Error", "Sin conexión al servidor.")

        ventana_detalles = tk.Toplevel(self.ventana)
        ventana_detalles.title(f"Detalles de Reparacion #{id_reparacion}")
        ventana_detalles.geometry("480x580")
        ventana_detalles.configure(bg=COLOR_FONDO_SECCION)
        ventana_detalles.resizable(False, False)

        top_bar = tk.Frame(ventana_detalles, bg=COLOR_PRIMARIO, height=50)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)
        tk.Label(top_bar, text=f"\U0001F527  Reparacion #{id_reparacion}", font=FUENTE_SUBTITULO, bg=COLOR_PRIMARIO, fg=COLOR_TEXTO_BLANCO).pack(side="left", padx=20, pady=10)

        main_frame = tk.Frame(ventana_detalles, bg=COLOR_FONDO_SECCION, padx=25, pady=15)
        main_frame.pack(fill="both", expand=True)

        def marcar_como_terminado():
            if messagebox.askyesno("Confirmar", "¿Estás seguro de que has terminado esta reparación?"):
                try:
                    res_up = requests.post("http://localhost/api/reparaciones/terminar", json={"id_reparacion": id_reparacion})
                    if res_up.status_code == 200:
                        messagebox.showinfo("Exito", f"Reparacion #{id_reparacion} marcada como 'Reparada'.", parent=ventana_detalles)
                        ventana_detalles.destroy()
                        self.cargar_pendientes()
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar.")
                except:
                    messagebox.showerror("Error", "Sin conexión al servidor.")

        def crear_seccion(parent, titulo):
            sec_frame = tk.Frame(parent, bg=COLOR_FONDO_SECCION)
            sec_frame.pack(fill="x", pady=(14, 0))
            tk.Label(sec_frame, text=titulo, font=FUENTE_SUBTITULO, bg=COLOR_FONDO_SECCION, fg=COLOR_PRIMARIO).pack(anchor="w")
            tk.Frame(parent, height=2, bg=COLOR_SECUNDARIO).pack(fill="x", pady=(3, 6))

        def crear_detalle(parent, campo, valor):
            frame = tk.Frame(parent, bg=COLOR_FONDO_SECCION)
            frame.pack(fill="x", pady=2)
            tk.Label(frame, text=f"{campo}:", font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_SECCION, fg=COLOR_TEXTO_OSCURO).pack(side="left")
            tk.Label(frame, text=valor if valor else 'N/A', font=FUENTE_CUERPO, bg=COLOR_FONDO_SECCION, fg=COLOR_TEXTO_GRIS, wraplength=300, justify="left").pack(side="left", padx=8)

        crear_seccion(main_frame, "Datos del Equipo")
        crear_detalle(main_frame, "Dispositivo", f"{detalles.get('marca')} {detalles.get('modelo')}")
        crear_detalle(main_frame, "Tipo", detalles.get('tipo_equipo'))
        crear_detalle(main_frame, "IMEI/Serie", detalles.get('imei_o_serie'))
        crear_detalle(main_frame, "Clave Acceso", detalles.get('clave_acceso'))

        crear_seccion(main_frame, "Datos del Cliente")
        crear_detalle(main_frame, "Nombre", f"{detalles.get('nombre')} {detalles.get('apellidos')}")
        crear_detalle(main_frame, "Telefono", detalles.get('telefono'))

        crear_seccion(main_frame, "Detalles de la Reparacion")
        crear_detalle(main_frame, "Problema Reportado", detalles.get('problema_reportado'))
        crear_detalle(main_frame, "Tecnico Asignado", detalles.get('tecnico_asignado', 'Sin asignar'))
        crear_detalle(main_frame, "Estado Actual", detalles.get('estado'))

        if detalles.get('estado') not in ['Reparado', 'Entregado', 'No Reparado']:
            btn = crear_boton(main_frame, "Terminar Reparacion", marcar_como_terminado, COLOR_EXITO, height=2)
            btn.pack(fill="x", pady=(25, 0))

    def cargar_inventario(self):
        self.limpiar_panel()

        # --- Encabezado ---
        header = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        header.pack(fill="x", padx=15, pady=(10, 0))
        tk.Label(header, text="Consulta de Inventario General",
                 font=FUENTE_TITULO, bg=COLOR_FONDO_PANEL,
                 fg=COLOR_PRIMARIO).pack(anchor="w")
        tk.Label(header, text="Busca todas las refacciones y productos disponibles en el taller",
                 font=FUENTE_ETIQUETA, bg=COLOR_FONDO_PANEL,
                 fg=COLOR_TEXTO_GRIS).pack(anchor="w", pady=(2, 0))

        tk.Frame(self.panel_dinamico, height=2, bg=COLOR_BORDE).pack(fill="x", padx=15, pady=(8, 10))

        # Frame para Busqueda
        controles_frame = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        controles_frame.pack(fill="x", pady=(0, 10), padx=15)

        tk.Label(controles_frame, text="Buscar:", font=FUENTE_CUERPO_BOLD,
                 bg=COLOR_FONDO_PANEL).pack(side="left", padx=(0, 5))
        search_var = tk.StringVar()
        search_frame, search_entry = crear_entry_estilizado(controles_frame, width=45)
        search_entry.configure(textvariable=search_var)
        search_frame.pack(side="left", fill="x", expand=True)

        #  Treeview para inventario 
        tree_container = tk.Frame(self.panel_dinamico, bg=COLOR_BORDE)
        tree_container.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        tree_inventario = ttk.Treeview(tree_container,
                                    columns=("SKU", "Producto", "Tipo", "Stock", "Precio Venta", "Ubicacion"),
                                    show="headings", style="Custom.Treeview")

        cols = {"SKU": 80, "Producto": 150, "Tipo": 100, "Stock": 60, "Precio Venta": 100, "Ubicacion": 120}
        for col, width in cols.items():
            tree_inventario.heading(col, text=col)
            tree_inventario.column(col, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(tree_container, orient="vertical",
                                  command=tree_inventario.yview,
                                  style="Custom.Vertical.TScrollbar")
        tree_inventario.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", padx=(0, 1), pady=1)
        tree_inventario.pack(fill="both", expand=True, padx=1, pady=1)

        tree_inventario.tag_configure('oddrow', background=COLOR_FILA_IMPAR)
        tree_inventario.tag_configure('evenrow', background=COLOR_FILA_PAR)

        # Logica de la Base de Datos 
        def actualizar_lista_inventario(*args):
            for i in tree_inventario.get_children():
                tree_inventario.delete(i)

            termino_busqueda = search_var.get()
            mi_taller_id = obtener_taller_id()
            
            if not mi_taller_id:
                return

            try:
                url_api = "http://localhost/api/inventario/buscar"
                payload = {
                    "taller_id": mi_taller_id,
                    "termino": termino_busqueda
                }
                respuesta = requests.post(url_api, json=payload)

                if respuesta.status_code == 200:
                    productos = respuesta.json().get('productos', [])
                    for i, prod in enumerate(productos):
                        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                        precio_val = prod.get('precio_venta')
                        # Formateamos el precio para que se vea bien
                        precio_formato = f"${float(precio_val):.2f}" if precio_val is not None else "N/A"
                        
                        tree_inventario.insert("", "end", values=(
                            prod.get('sku'), 
                            prod.get('nombre_producto'), 
                            prod.get('tipo_producto'),
                            prod.get('stock'), 
                            precio_formato, 
                            prod.get('ubicacion_almacen')
                        ), tags=(tag,))
            except requests.exceptions.ConnectionError:
                pass # Usamos pass en lugar de messagebox para evitar spam si escriben muy rápido

        search_var.trace_add("write", actualizar_lista_inventario)
        actualizar_lista_inventario()

    

    def cargar_diagnostico(self):
        self.limpiar_panel()

        # Este es el encabezado 
        header = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        header.pack(fill="x", padx=15, pady=(10, 0))
        tk.Label(header, text="Generar Diagnostico y Presupuesto",
                 font=FUENTE_TITULO, bg=COLOR_FONDO_PANEL,
                 fg=COLOR_PRIMARIO).pack(anchor="w")
        tk.Label(header, text="Selecciona una reparacion pendiente para diagnosticar",
                 font=FUENTE_ETIQUETA, bg=COLOR_FONDO_PANEL,
                 fg=COLOR_TEXTO_GRIS).pack(anchor="w", pady=(2, 0))

        tk.Frame(self.panel_dinamico, height=2, bg=COLOR_BORDE).pack(fill="x", padx=15, pady=(8, 10))

        # --- Seleccion de reparacion ---
        seleccion_frame = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        seleccion_frame.pack(fill="x", padx=15)

        tk.Label(seleccion_frame, text="Reparacion Pendiente:",
                 font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_PANEL).pack(side="left")

        id_reparacion_var = tk.StringVar()
        combo_reparaciones = ttk.Combobox(seleccion_frame, textvariable=id_reparacion_var,
                                          state="readonly", width=40, font=FUENTE_CUERPO,
                                          style="Custom.TCombobox")
        combo_reparaciones.pack(side="left", padx=10)

        #  Contenedor para el formulario 
        form_container = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        form_container.pack(fill="both", expand=True, padx=15, pady=10)

        # Llenar Combobox
        mi_taller_id = obtener_taller_id()
        if not mi_taller_id:
            return messagebox.showerror("Error", "No hay licencia activa.")

        try:
            url_api = "http://localhost/api/reparaciones/pendientes"
            respuesta = requests.post(url_api, json={"taller_id": mi_taller_id})
            
            if respuesta.status_code == 200:
                reparaciones = respuesta.json().get('reparaciones', [])
                # ¡AQUÍ ES DONDE SE LLENA AHORA!
                combo_reparaciones['values'] = [
                    f"{r.get('id_reparacion')} - {r.get('dispositivo')}" 
                    for r in reparaciones
                ]
            else:
                messagebox.showerror("Error", "No se pudieron cargar las reparaciones pendientes.")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "Sin conexión al servidor.")

        

        def on_reparacion_seleccionada(event):
            for widget in form_container.winfo_children():
                widget.destroy()

            id_reparacion_seleccionada = int(id_reparacion_var.get().split(' - ')[0])

            col_frame = tk.Frame(form_container, bg=COLOR_FONDO_PANEL)
            col_frame.pack(fill="both", expand=True)
            col_frame.grid_columnconfigure(0, weight=1)
            col_frame.grid_columnconfigure(1, weight=1)

            # --- COLUMNA IZQUIERDA ---
            col_izquierda = tk.Frame(col_frame, bg=COLOR_FONDO_PANEL, padx=5)
            col_izquierda.grid(row=0, column=0, sticky="nsew")

            tk.Label(col_izquierda, text="Diagnostico Tecnico:",
                     font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_PANEL,
                     fg=COLOR_TEXTO_OSCURO).pack(anchor="w", pady=(0, 4))
            diag_frame, diagnostico_text = crear_text_estilizado(col_izquierda, height=5)
            diag_frame.pack(fill="x", pady=(0, 10))

            presupuesto_frame = tk.Frame(col_izquierda, bg=COLOR_FONDO_PANEL)
            presupuesto_frame.pack(fill="x", pady=(0, 10))
            tk.Label(presupuesto_frame, text="Presupuesto Total $:",
                     font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_PANEL,
                     fg=COLOR_TEXTO_OSCURO).pack(side="left")
            pres_frame, presupuesto_entry = crear_entry_estilizado(presupuesto_frame, width=15)
            pres_frame.pack(side="left", padx=(8, 0))

            tk.Label(col_izquierda, text="Piezas a Utilizar:",
                     font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_PANEL,
                     fg=COLOR_TEXTO_OSCURO).pack(anchor="w", pady=(8, 4))

            piezas_container = tk.Frame(col_izquierda, bg=COLOR_BORDE)
            piezas_container.pack(fill="x", expand=True)
            tree_piezas_usadas = ttk.Treeview(piezas_container,
                                              columns=("ID", "Nombre", "Precio"),
                                              show="headings", height=5,
                                              style="Custom.Treeview")
            tree_piezas_usadas.heading("ID", text="ID")
            tree_piezas_usadas.heading("Nombre", text="Nombre")
            tree_piezas_usadas.heading("Precio", text="Precio")
            tree_piezas_usadas.column("ID", width=40)
            tree_piezas_usadas.column("Nombre", width=150)
            tree_piezas_usadas.column("Precio", width=80)
            tree_piezas_usadas.pack(fill="x", expand=True, padx=1, pady=1)

            # --- COLUMNA DERECHA ---
            col_derecha = tk.Frame(col_frame, bg=COLOR_FONDO_PANEL, padx=5)
            col_derecha.grid(row=0, column=1, sticky="nsew")

            tk.Label(col_derecha, text="Inventario Disponible:",
                     font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_PANEL,
                     fg=COLOR_TEXTO_OSCURO).pack(anchor="w", pady=(0, 4))

            inv_container = tk.Frame(col_derecha, bg=COLOR_BORDE)
            inv_container.pack(fill="x", expand=True)
            tree_inventario = ttk.Treeview(inv_container,
                                           columns=("ID", "Nombre", "Stock", "Precio"),
                                           show="headings", height=8,
                                           style="Custom.Treeview")
            tree_inventario.heading("ID", text="ID")
            tree_inventario.heading("Nombre", text="Nombre")
            tree_inventario.heading("Stock", text="Stock")
            tree_inventario.heading("Precio", text="Precio")
            tree_inventario.column("ID", width=40)
            tree_inventario.column("Nombre", width=150)
            tree_inventario.column("Stock", width=40)
            tree_inventario.column("Precio", width=80)
            tree_inventario.pack(fill="x", expand=True, padx=1, pady=1)

            # --- LLAMADA API: Cargar inventario disponible ---
            mi_taller_id = obtener_taller_id()
            if mi_taller_id:
                try:
                    res_inv = requests.post("http://localhost/api/diagnostico/inventario", json={"taller_id": mi_taller_id})
                    if res_inv.status_code == 200:
                        inventario = res_inv.json().get('inventario', [])
                        for prod in inventario:
                            tree_inventario.insert("", "end", values=(
                                prod.get('id_producto'), 
                                prod.get('nombre_producto'), 
                                prod.get('stock'), 
                                prod.get('precio_venta')
                            ))
                except requests.exceptions.ConnectionError:
                    messagebox.showerror("Error", "No se pudo cargar el inventario.")

            # --- Botones de acción ---
            botones_grid_frame = tk.Frame(col_izquierda, bg=COLOR_FONDO_PANEL)
            botones_grid_frame.pack(fill="x", pady=10)
            botones_grid_frame.grid_columnconfigure(1, weight=1)

            def anadir_pieza():
                item_sel = tree_inventario.selection()
                if not item_sel: return
                pieza_data = tree_inventario.item(item_sel[0], 'values')
                # Insertamos ID, Nombre y Precio (ignorando el stock)
                tree_piezas_usadas.insert("", "end", values=(pieza_data[0], pieza_data[1], pieza_data[3]))
            
            def quitar_pieza():
                item_sel = tree_piezas_usadas.selection()
                if not item_sel: return
                tree_piezas_usadas.delete(item_sel[0])

            def guardar_diagnostico():
                diagnostico = diagnostico_text.get("1.0", "end-1c")
                presupuesto = presupuesto_entry.get()
                
                # Formateamos las piezas para enviarlas a Laravel
                piezas_a_usar = []
                for item in tree_piezas_usadas.get_children():
                    val = tree_piezas_usadas.item(item, 'values')
                    piezas_a_usar.append({
                        "id_producto": val[0],
                        "precio": val[2]
                    })

                if not diagnostico or not presupuesto or not piezas_a_usar:
                    return messagebox.showwarning("Datos Incompletos", "Debes rellenar el diagnóstico, el presupuesto y seleccionar al menos una pieza.")

                if messagebox.askyesno("Confirmar", "¿Guardar este diagnóstico y presupuesto?"):
                    try:
                        payload = {
                            "id_reparacion": id_reparacion_seleccionada,
                            "diagnostico": diagnostico,
                            "presupuesto": presupuesto,
                            "piezas": piezas_a_usar
                        }
                        res_save = requests.post("http://localhost/api/diagnostico/guardar", json=payload)
                        
                        if res_save.status_code == 200:
                            messagebox.showinfo("Éxito", res_save.json().get('message', 'Diagnóstico guardado.'))
                            self.cargar_pendientes()
                        else:
                            messagebox.showerror("Error", "No se pudo guardar el diagnóstico.")
                    except requests.exceptions.ConnectionError:
                        messagebox.showerror("Error", "Sin conexión al servidor.")

            btn_anadir = crear_boton(botones_grid_frame, "Anadir Pieza ->", anadir_pieza, COLOR_SECUNDARIO, fuente=FUENTE_CUERPO_BOLD)
            btn_anadir.grid(row=0, column=0, padx=3, pady=5)

            btn_quitar = crear_boton(botones_grid_frame, "<- Quitar Pieza", quitar_pieza, COLOR_PELIGRO, fuente=FUENTE_CUERPO_BOLD)
            btn_quitar.grid(row=0, column=2, padx=3, pady=5)

            btn_guardar_diag = crear_boton(botones_grid_frame, "Guardar Diagnostico", guardar_diagnostico, COLOR_EXITO, fuente=FUENTE_CUERPO_BOLD)
            btn_guardar_diag.grid(row=0, column=3, padx=3, pady=5, sticky="ew")

        combo_reparaciones.bind("<<ComboboxSelected>>", on_reparacion_seleccionada)

    def cargar_reporte_material(self):
        self.limpiar_panel()

        #  Encabezado 
        header = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        header.pack(fill="x", padx=15, pady=(10, 0))
        tk.Label(header, text="Reporte y Solicitud de Material",
                 font=FUENTE_TITULO, bg=COLOR_FONDO_PANEL,
                 fg=COLOR_PRIMARIO).pack(anchor="w")
        tk.Label(header, text="Solicita material o herramientas al administrador",
                 font=FUENTE_ETIQUETA, bg=COLOR_FONDO_PANEL,
                 fg=COLOR_TEXTO_GRIS).pack(anchor="w", pady=(2, 0))

        tk.Frame(self.panel_dinamico, height=2, bg=COLOR_BORDE).pack(fill="x", padx=15, pady=(8, 10))

        #  Frame principal con dos columnas 
        main_frame = tk.Frame(self.panel_dinamico, bg=COLOR_FONDO_PANEL)
        main_frame.pack(fill="both", expand=True, padx=15)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)

        # COLUMNA IZQUIERDA: Formulario 
        form_frame = tk.Frame(main_frame, bg=COLOR_FONDO_SECCION,
                              highlightbackground=COLOR_BORDE, highlightthickness=1)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        form_inner = tk.Frame(form_frame, bg=COLOR_FONDO_SECCION, padx=15, pady=15)
        form_inner.pack(fill="both", expand=True)

        tk.Label(form_inner, text="Crear Nueva Solicitud",
                 font=FUENTE_SUBTITULO, bg=COLOR_FONDO_SECCION,
                 fg=COLOR_PRIMARIO).pack(anchor="w", pady=(0, 12))

        tk.Label(form_inner, text="Nombre del Producto o Herramienta:",
                 font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_SECCION,
                 fg=COLOR_TEXTO_OSCURO).pack(anchor="w")
        nombre_frame, nombre_prod_entry = crear_entry_estilizado(form_inner)
        nombre_frame.pack(fill="x", pady=(2, 10))

        tk.Label(form_inner, text="Cantidad Necesaria:",
                 font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_SECCION,
                 fg=COLOR_TEXTO_OSCURO).pack(anchor="w")
        cantidad_spinbox = tk.Spinbox(form_inner, from_=1, to=100, font=FUENTE_CUERPO,
                                      bg=COLOR_TEXTO_BLANCO, fg=COLOR_TEXTO_OSCURO,
                                      bd=1, relief="solid",
                                      buttonbackground=COLOR_FONDO_APP)
        cantidad_spinbox.pack(fill="x", ipady=4, pady=(2, 10))

        tk.Label(form_inner, text="Descripcion (Opcional):",
                 font=FUENTE_CUERPO_BOLD, bg=COLOR_FONDO_SECCION,
                 fg=COLOR_TEXTO_OSCURO).pack(anchor="w")
        desc_frame, descripcion_text = crear_text_estilizado(form_inner, height=5)
        desc_frame.pack(fill="x", expand=True, pady=(2, 15))

        # COLUMNA DERECHA: Lista de Solicitudes 
        lista_frame = tk.Frame(main_frame, bg=COLOR_FONDO_PANEL)
        lista_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        tk.Label(lista_frame, text="Mis Solicitudes",
                 font=FUENTE_SUBTITULO, bg=COLOR_FONDO_PANEL,
                 fg=COLOR_PRIMARIO).pack(anchor="w", pady=(0, 8))

        tree_container = tk.Frame(lista_frame, bg=COLOR_BORDE)
        tree_container.pack(fill="both", expand=True)

        tree_solicitudes = ttk.Treeview(tree_container,
                                        columns=("Fecha", "Producto", "Cantidad", "Estado"),
                                        show="headings", height=15,
                                        style="Custom.Treeview")
        tree_solicitudes.heading("Fecha", text="Fecha")
        tree_solicitudes.heading("Producto", text="Producto")
        tree_solicitudes.heading("Cantidad", text="Cant.")
        tree_solicitudes.heading("Estado", text="Estado")
        tree_solicitudes.column("Fecha", width=100)
        tree_solicitudes.column("Producto", width=150)
        tree_solicitudes.column("Cantidad", width=50, anchor="center")
        tree_solicitudes.column("Estado", width=100, anchor="center")

        scrollbar_sol = ttk.Scrollbar(tree_container, orient="vertical",
                                      command=tree_solicitudes.yview,
                                      style="Custom.Vertical.TScrollbar")
        tree_solicitudes.configure(yscrollcommand=scrollbar_sol.set)
        scrollbar_sol.pack(side="right", fill="y", padx=(0, 1), pady=1)
        tree_solicitudes.pack(fill="both", expand=True, padx=1, pady=1)

        tree_solicitudes.tag_configure('evenrow', background=COLOR_FILA_PAR)
        tree_solicitudes.tag_configure('oddrow', background=COLOR_FILA_IMPAR)

        def actualizar_lista_solicitudes():
            for i in tree_solicitudes.get_children():
                tree_solicitudes.delete(i)

            try:
                res = requests.post("http://localhost/api/material/listar", json={"id_tecnico": self.id_tecnico_logueado})
                if res.status_code == 200:
                    solicitudes = res.json().get('solicitudes', [])
                    for idx, s in enumerate(solicitudes):
                        tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                        tree_solicitudes.insert("", "end", values=(
                            s.get('fecha'), 
                            s.get('nombre_producto'), 
                            s.get('cantidad_solicitada'), 
                            s.get('estado_solicitud')
                        ), tags=(tag,))
            except requests.exceptions.ConnectionError:
                pass # Evitamos spam de errores si recarga rápido

        def enviar_solicitud():
            nombre = nombre_prod_entry.get()
            cantidad = cantidad_spinbox.get()
            descripcion = descripcion_text.get("1.0", "end-1c")

            if not nombre or not cantidad.isdigit():
                return messagebox.showwarning("Datos Invalidos", "El nombre del producto y una cantidad numerica son obligatorios.")

            mi_taller_id = obtener_taller_id()
            if not mi_taller_id:
                return messagebox.showerror("Error", "No hay licencia activa.")

            try:
                payload = {
                    "id_tecnico": self.id_tecnico_logueado,
                    "taller_id": mi_taller_id,
                    "nombre_producto": nombre,
                    "cantidad": int(cantidad),
                    "descripcion": descripcion
                }
                res = requests.post("http://localhost/api/material/crear", json=payload)
                
                if res.status_code == 200:
                    messagebox.showinfo("Éxito", "Tu solicitud de material ha sido enviada al administrador.")
                    # Limpiar formulario
                    nombre_prod_entry.delete(0, tk.END)
                    descripcion_text.delete("1.0", tk.END)
                    # Actualizar lista
                    actualizar_lista_solicitudes()
                else:
                    messagebox.showerror("Error", "No se pudo enviar la solicitud al servidor.")
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "Sin conexión al servidor.")

            messagebox.showinfo("Exito", "Tu solicitud de material ha sido enviada al administrador.")

            # Limpiar formulario
            nombre_prod_entry.delete(0, tk.END)
            descripcion_text.delete("1.0", tk.END)

            # Actualizar la lista de la derecha
            actualizar_lista_solicitudes()

        # Boton de enviar 
        btn_enviar = crear_boton(form_inner, "Enviar Solicitud",
                                 enviar_solicitud, COLOR_SECUNDARIO, height=2)
        btn_enviar.pack(fill="x")

        # Cargar la lista de solicitudes por primera vez
        actualizar_lista_solicitudes()

    def volver_al_login(self):
        if messagebox.askyesno("Confirmacion", "Deseas cerrar sesion y volver al login?"):
            self.ventana.destroy()
            from Login import iniciar_sesion
            iniciar_sesion()


if __name__ == "__main__":
    PanelTecnico()