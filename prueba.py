from PIL import Image, ImageTk, ImageFilter
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# 🎨 Paleta de colores unificada
COLOR_HEADER       = "#005187"
COLOR_BOTON        = "#4d82bc"
COLOR_TEXTO_BLANCO = "#ffffff"
COLOR_GLASS_BG     = "#ffffff"
# Encabezado y elementos principales
COLOR_HEADER       = "#005187"   # Azul profundo para encabezados y menú lateral
COLOR_TITULO       = "#003B5C"   # Azul oscuro para títulos y etiquetas destacadas

# Botones y acciones
COLOR_BOTON        = "#4d82bc"   # Azul medio para botones activos
COLOR_HOVER        = "#3b6ea5"   # Azul más oscuro para hover o botones secundarios
COLOR_ALERTA       = "#d9534f"   # Rojo suave para advertencias o errores

# Fondos y paneles
COLOR_GLASS_BG     = "#ffffff"   # Blanco para paneles flotantes tipo glass
COLOR_FONDO        = "#f0f4f8"   # Gris claro para fondo general
COLOR_PANEL        = "#e6ecf2"   # Gris azulado para secciones internas

# Texto
COLOR_BLANCO = "#ffffff"         # Blanco para texto sobre botones oscuros
COLOR_TEXTO_OSCURO = "#1c1c1c"   # Negro suave para texto general
COLOR_TEXTO_GRIS   = "#666666"   # Gris medio para texto secundario

# Bordes y detalles
COLOR_BORDE        = "#cccccc"   # Gris claro para bordes y separadores
COLOR_SEPARADOR    = "#999999"   # Gris medio para líneas divisorias

class PanelVendedor:

    
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Panel Vendedor")
        self.ventana.geometry("900x600")
        self.ventana.resizable(False, False)

        # 🖼 Fondo difuminado
        try:
            fondo = Image.open("assets/fondo.png").resize((900, 600))
            fondo_blur = fondo.filter(ImageFilter.GaussianBlur(10))
            self.fondo_img = ImageTk.PhotoImage(fondo_blur)

            self.canvas_fondo = tk.Canvas(self.ventana, width=900, height=600, highlightthickness=0)
            self.canvas_fondo.pack(fill="both", expand=True)
            self.canvas_fondo.create_image(0, 0, anchor="nw", image=self.fondo_img)
            self.canvas_fondo.create_rectangle(0, 0, 900, 600, fill="#ffffff", stipple="gray25", outline="")
        except:
            self.ventana.configure(bg=COLOR_GLASS_BG)

        # 🧱 Panel flotante
        self.panel_flotante = tk.Frame(self.canvas_fondo, bg=COLOR_GLASS_BG)
        self.canvas_fondo.create_window(450, 300, window=self.panel_flotante, anchor="center", width=860, height=560)

        # ☰ Menú animado
        self.menu_visible = False
        self.boton_menu = tk.Button(self.panel_flotante, text="☰ Menú", font=("Arial", 12),
                                    bg=COLOR_HEADER, fg=COLOR_TEXTO_BLANCO, relief="flat",
                                    command=self.toggle_menu)
        self.boton_menu.place(x=10, y=10)

        # 📦 Menú lateral
        self.menu_lateral = tk.Frame(self.canvas_fondo, bg=COLOR_HEADER, width=0)
        self.menu_lateral.place(x=0, y=0, relheight=1)
        self.menu_lateral.pack_propagate(False)

        self.crear_menu_lateral()

        # 💡 Área dinámica
        self.panel_dinamico = tk.Frame(self.panel_flotante, bg=COLOR_GLASS_BG)
        self.panel_dinamico.place(x=180, y=60, width=650, height=480)

        # Vista inicial
        self.mostrar_venta_rapida()
        self.ventana.mainloop()

    def toggle_menu(self):
        destino = 180 if not self.menu_visible else 0
        paso = 12
        ancho_actual = self.menu_lateral.winfo_width()

        def animar():
            nonlocal ancho_actual
            if self.menu_visible and ancho_actual > destino:
                ancho_actual -= paso
            elif not self.menu_visible and ancho_actual < destino:
                ancho_actual += paso

            self.menu_lateral.place_configure(width=ancho_actual)
            if abs(ancho_actual - destino) > paso:
                self.ventana.after(10, animar)
            else:
                self.menu_visible = not self.menu_visible
                if not self.menu_visible:
                    self.menu_lateral.place_configure(width=0)

        animar()

    def crear_menu_lateral(self):
        # 🔙 Botón Regresar
        tk.Button(self.menu_lateral, text="⬅️ Regresar", anchor="w", width=22,
                bg=COLOR_HEADER, fg=COLOR_TEXTO_BLANCO, relief="flat",
                font=("Segoe UI", 10), command=self.toggle_menu).pack(pady=(10, 5))
        
        #  Separador visual
        tk.Label(self.menu_lateral, text="─" * 22, bg=COLOR_HEADER, fg=COLOR_TEXTO_BLANCO).pack(pady=(10, 0))
        tk.Label(self.menu_lateral, text="Herramientas", anchor="w", width=22,
                font=("Segoe UI", 10, "bold"), bg=COLOR_HEADER,
                fg=COLOR_TEXTO_BLANCO).pack(pady=(5, 10))

        #  Opciones principales
        opciones = [
            ("🛒 Realizar Venta", self.mostrar_venta_rapida),
            ("📜 Historial de Ventas", self.mostrar_historial),
            ("📦 Inventario", self.mostrar_inventario),
            ("👥 Admin Clientes", self.mostrar_admin_clientes),
            ("📤 Salida Dispositivos", self.mostrar_salida_dispositivos),
            ("🛒 Gestionar Compras", self.mostrar_gestion_compras)
        ]

        for texto, comando in opciones:
            def combinado(c=comando):
                c()
                self.toggle_menu()
            tk.Button(self.menu_lateral, text=texto, anchor="w", width=22,
                    bg=COLOR_HEADER, fg=COLOR_TEXTO_BLANCO, relief="flat",
                    font=("Segoe UI", 10), command=combinado).pack(pady=7)

        

        # ⏻ Botón Salir en parte baja
        tk.Button(self.menu_lateral, text="⏻ Salir", anchor="center", width=22,
                bg=COLOR_HEADER, fg=COLOR_TEXTO_BLANCO, relief="flat",
                font=("Segoe UI", 10), command=self.ventana.destroy).place(relx=0.5, rely=0.95, anchor="center")

    def limpiar_panel(self):
        for widget in self.panel_dinamico.winfo_children():
            widget.destroy()

    def mostrar_venta_rapida(self):
        self.limpiar_panel()
        tk.Label(self.panel_dinamico, text="Venta Rápida", font=("Arial", 14, "bold"),
                bg=COLOR_GLASS_BG, fg=COLOR_HEADER).pack(pady=10)

        productos = [("Cable USB", 60), ("Cargador", 120), ("Audífonos", 200)]
        self.total_var = tk.StringVar(value="$0.00")
        self.carrito = []

        frame_botones = tk.Frame(self.panel_dinamico, bg=COLOR_GLASS_BG)
        frame_botones.pack(pady=5)

        for nombre, precio in productos:
            tk.Button(frame_botones, text=f"{nombre}\n${precio}", width=12,
                    bg=COLOR_BOTON, fg=COLOR_TEXTO_BLANCO,
                    command=lambda n=nombre, p=precio: self.agregar(n, p)).pack(side="left", padx=10)

        # 🧾 Carrito visual
        self.carrito_text = tk.Text(self.panel_dinamico, height=8, width=50, bg=COLOR_GLASS_BG,
                                    fg=COLOR_HEADER, font=("Arial", 10), relief="solid", borderwidth=1)
        self.carrito_text.pack(pady=10)

        # ❌ Botón para eliminar producto
        tk.Button(self.panel_dinamico, text="Eliminar Producto", font=("Arial", 10),
                bg=COLOR_HEADER, fg=COLOR_TEXTO_BLANCO,
                command=self.eliminar_producto).pack(pady=5)

        # 💰 Total
        tk.Label(self.panel_dinamico, text="Total:", bg=COLOR_GLASS_BG, fg=COLOR_HEADER).pack()
        tk.Label(self.panel_dinamico, textvariable=self.total_var, font=("Arial", 14),
                bg=COLOR_GLASS_BG).pack()

        # ✅ Botón para confirmar venta
        def confirmar_venta():
            if not self.carrito:
                messagebox.showwarning("Carrito vacío", "No hay productos en el carrito.")
                return
            total = self.total_var.get()
            productos_lista = "\n".join([f"{i+1}. {n} - ${p}" for i, (n, p) in enumerate(self.carrito)])
            respuesta = messagebox.askyesno(
                "Confirmar Venta",
                f"¿Desea confirmar la venta?\n\nProductos:\n{productos_lista}\n\nTotal: {total}"
            )
            if respuesta:
                messagebox.showinfo("Venta realizada", "¡La venta ha sido confirmada!")
                self.carrito.clear()
                self.actualizar_carrito()

        tk.Button(self.panel_dinamico, text="Confirmar Venta", font=("Arial", 12, "bold"),
                  bg=COLOR_BOTON, fg=COLOR_BLANCO, command=confirmar_venta).pack(pady=10)
        
    def mostrar_admin_clientes(self):
        self.limpiar_panel()
        tk.Label(
            self.panel_dinamico,
            text="Administrar Clientes",
            font=("Arial", 14, "bold"),
            bg=COLOR_GLASS_BG,
            fg=COLOR_HEADER
        ).pack(pady=10)

        # 🧰 Botones de acción
        botones = [
            ("Nuevo", COLOR_BOTON),
            ("Modificar", COLOR_BOTON),
            ("Eliminar", COLOR_ALERTA),
            ("Filtro", COLOR_HOVER),
            ("Consultar todos", COLOR_BOTON)
        ]
        frame_botones = tk.Frame(self.panel_dinamico, bg=COLOR_GLASS_BG)
        frame_botones.pack(pady=5)

        for i, (b, color) in enumerate(botones):
            tk.Button(
                frame_botones,
                text=b,
                bg=color,
                fg=COLOR_BLANCO,
                font=("Segoe UI", 10, "bold"),
                width=14,
                relief="flat",
                activebackground=COLOR_HEADER if color != COLOR_ALERTA else COLOR_ALERTA,
                activeforeground=COLOR_BLANCO,
                cursor="hand2"
            ).grid(row=0, column=i, padx=6, pady=2)

        # 🧾 Tabla de clientes
        cols = ["ID", "Nombre", "Dispositivo", "Dirección", "Fecha"]
        tabla = tk.Frame(
            self.panel_dinamico,
            bg=COLOR_BLANCO,
            highlightbackground=COLOR_BORDE,
            highlightthickness=1
        )
        tabla.pack(pady=12, fill="x", padx=10)

        # Encabezados
        for i, col in enumerate(cols):
            tk.Label(
                tabla,
                text=col,
                bg=COLOR_HEADER,
                fg=COLOR_BLANCO,
                font=("Segoe UI", 10, "bold"),
                borderwidth=1,
                relief="solid",
                width=15
            ).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        # Ejemplo de cliente
        datos = [
            ("001", "Carlos", "Tablet", "CDMX", "05/08/2025"),
            ("002", "Ana", "Celular", "Guadalajara", "12/09/2025"),
            ("003", "Luis", "Laptop", "Monterrey", "21/10/2025")
        ]
        for r, fila in enumerate(datos, start=1):
            for c, valor in enumerate(fila):
                tk.Label(
                    tabla,
                    text=valor,
                    bg=COLOR_PANEL if r % 2 == 0 else COLOR_BLANCO,
                    fg=COLOR_TEXTO_OSCURO,
                    font=("Segoe UI", 10),
                    borderwidth=1,
                    relief="solid"
                ).grid(row=r, column=c, sticky="nsew", padx=1, pady=1)

        # Separador visual inferior
        tk.Label(
            self.panel_dinamico,
            text="─" * 70,
            bg=COLOR_GLASS_BG,
            fg=COLOR_SEPARADOR
        ).pack(pady=(10, 0))
    def mostrar_salida_dispositivos(self):
        self.limpiar_panel()
        tk.Label(self.panel_dinamico, text="Salida de Dispositivos", font=("Arial", 14, "bold"),
                bg=COLOR_GLASS_BG, fg=COLOR_HEADER).pack(pady=10)

        entradas = ["Producto", "Salida", "Fecha", "Lugar", "Estado"]
        self.salida_vars = {}

        for i, e in enumerate(entradas):
            tk.Label(self.panel_dinamico, text=e+":", bg=COLOR_GLASS_BG, fg=COLOR_HEADER).place(x=30, y=60 + i*40)
            var = tk.StringVar()
            self.salida_vars[e] = var
            tk.Entry(self.panel_dinamico, textvariable=var).place(x=130, y=60 + i*40)

        def registrar_salida():
            datos = {k: v.get() for k, v in self.salida_vars.items()}
            messagebox.showinfo("Salida registrada", f"Datos:\n" + "\n".join(f"{k}: {v}" for k, v in datos.items()))

        tk.Button(self.panel_dinamico, text="Registrar Salida", bg=COLOR_BOTON, fg=COLOR_TEXTO_BLANCO,
                command=registrar_salida).place(x=130, y=280)
    def mostrar_gestion_compras(self):
        self.limpiar_panel()
        tk.Label(self.panel_dinamico, text="Gestionar Compras", font=("Arial", 14, "bold"),
                bg=COLOR_GLASS_BG, fg=COLOR_HEADER).pack(pady=10)

        campos = ["Producto", "Cantidad", "Precio", "Fecha"]
        self.compra_vars = {}

        for i, campo in enumerate(campos):
            tk.Label(self.panel_dinamico, text=campo + ":", bg=COLOR_GLASS_BG, fg=COLOR_HEADER).place(x=40, y=60 + i*40)
            var = tk.StringVar()
            self.compra_vars[campo] = var
            tk.Entry(self.panel_dinamico, textvariable=var).place(x=140, y=60 + i*40)

        def registrar_compra():
            datos = {k: v.get() for k, v in self.compra_vars.items()}
            messagebox.showinfo("Compra registrada", f"Datos:\n" + "\n".join(f"{k}: {v}" for k, v in datos.items()))

        tk.Button(self.panel_dinamico, text="Registrar Compra", bg=COLOR_BOTON, fg=COLOR_TEXTO_BLANCO,
                command=registrar_compra).place(x=140, y=240)
    

    def agregar(self, nombre, precio):
        self.carrito.append((nombre, precio))
        texto = "\n".join([f"{i+1}. {n} - ${p}" for i, (n, p) in enumerate(self.carrito)])
        self.carrito_label.config(text=texto)
        self.total_var.set(f"${sum(p for _, p in self.carrito):.2f}")

    def mostrar_historial(self):
        self.limpiar_panel()
        tk.Label(
            self.panel_dinamico,
            text="Historial de Ventas",
            font=("Arial", 14, "bold"),
            bg=COLOR_GLASS_BG,
            fg=COLOR_HEADER
        ).pack(pady=10)

        # 🧰 Barra de filtros y búsqueda
        filtro_frame = tk.Frame(self.panel_dinamico, bg=COLOR_GLASS_BG)
        filtro_frame.pack(pady=(0, 10), fill="x", padx=10)
        tk.Label(
            filtro_frame,
            text="🔎 Buscar:",
            bg=COLOR_GLASS_BG,
            fg=COLOR_HEADER,
            font=("Arial", 10, "bold")
        ).pack(side="left", padx=(0, 5))
        tk.Entry(
            filtro_frame,
            width=20,
            relief="solid",
            borderwidth=1,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_OSCURO
        ).pack(side="left", padx=(0, 10))
        tk.Button(
            filtro_frame,
            text="Filtrar",
            bg=COLOR_BOTON,
            fg=COLOR_BLANCO,
            font=("Arial", 10),
            relief="flat"
        ).pack(side="left")

        # Ejemplo de historial de ventas relacionadas con productos de venta rápida
        ventas = [
            {"ID": "V001", "Producto": "Cable USB", "Cantidad": 2, "Total": 120, "Fecha": "10/06/2024"},
            {"ID": "V002", "Producto": "Cargador", "Cantidad": 1, "Total": 120, "Fecha": "11/06/2024"},
            {"ID": "V003", "Producto": "Audífonos", "Cantidad": 3, "Total": 600, "Fecha": "12/06/2024"},
        ]

        cols = ["ID", "Producto", "Cantidad", "Total", "Fecha"]
        tabla = tk.Frame(self.panel_dinamico, bg=COLOR_BLANCO, highlightbackground=COLOR_BORDE, highlightthickness=1)
        tabla.pack(pady=10, fill="x", padx=10)

        # Encabezados
        for i, col in enumerate(cols):
            tk.Label(
                tabla,
                text=col,
                bg=COLOR_HEADER,
                fg=COLOR_BLANCO,
                font=("Arial", 10, "bold"),
                borderwidth=1,
                relief="solid",
                width=15
            ).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        # Filas de ventas
        for r, venta in enumerate(ventas, start=1):
            for c, col in enumerate(cols):
                tk.Label(
                    tabla,
                    text=str(venta[col]),
                    bg=COLOR_PANEL if r % 2 == 0 else COLOR_BLANCO,
                    fg=COLOR_TEXTO_OSCURO,
                    font=("Arial", 10),
                    borderwidth=1,
                    relief="solid"
                ).grid(row=r, column=c, sticky="nsew", padx=1, pady=1)

        # Separador visual inferior
        tk.Label(
            self.panel_dinamico,
            text="─" * 70,
            bg=COLOR_GLASS_BG,
            fg=COLOR_SEPARADOR
        ).pack(pady=(10, 0))

    def mostrar_inventario(self):
        self.limpiar_panel()
        tk.Label(
            self.panel_dinamico,
            text="Inventario del Vendedor",
            font=("Arial", 14, "bold"),
            bg=COLOR_GLASS_BG,
            fg=COLOR_HEADER
        ).pack(pady=10)

        # Ejemplo de inventario
        inventario = [
            {"ID": "P001", "Producto": "Cable USB", "Cantidad": 15, "Precio": 60, "Ubicación": "Almacén A"},
            {"ID": "P002", "Producto": "Cargador", "Cantidad": 8, "Precio": 120, "Ubicación": "Almacén B"},
            {"ID": "P003", "Producto": "Audífonos", "Cantidad": 20, "Precio": 200, "Ubicación": "Almacén A"},
        ]

        cols = ["ID", "Producto", "Cantidad", "Precio", "Ubicación"]
        tabla = tk.Frame(self.panel_dinamico, bg=COLOR_BLANCO, highlightbackground=COLOR_BORDE, highlightthickness=1)
        tabla.pack(pady=10, fill="x", padx=10)

        # Encabezados
        for i, col in enumerate(cols):
            tk.Label(
                tabla,
                text=col,
                bg=COLOR_HEADER,
                fg=COLOR_BLANCO,
                font=("Arial", 10, "bold"),
                borderwidth=1,
                relief="solid",
                width=15
            ).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        # Filas de inventario
        for r, item in enumerate(inventario, start=1):
            for c, col in enumerate(cols):
                tk.Label(
                    tabla,
                    text=str(item[col]),
                    bg=COLOR_PANEL if r % 2 == 0 else COLOR_BLANCO,
                    fg=COLOR_TEXTO_OSCURO,
                    font=("Arial", 10),
                    borderwidth=1,
                    relief="solid"
                ).grid(row=r, column=c, sticky="nsew", padx=1, pady=1)

        # Separador visual inferior
        tk.Label(
            self.panel_dinamico,
            text="─" * 70,
            bg=COLOR_GLASS_BG,
            fg=COLOR_SEPARADOR
        ).pack(pady=(10, 0))

    

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
            messagebox.showinfo("Carrito vacío", "No hay productos para eliminar.")
            return
        try:
            index = simpledialog.askstring("Eliminar", "Número de producto a eliminar:")
            if index is None:
                return
            index = int(index) - 1
            if 0 <= index < len(self.carrito):
                eliminado = self.carrito.pop(index)
                messagebox.showinfo("Producto eliminado", f"Se eliminó: {eliminado[0]}")
                self.actualizar_carrito()
            else:
                messagebox.showwarning("Índice inválido", "No existe ese número de producto.")
        except:
            messagebox.showerror("Error", "Entrada inválida.")
if __name__ == "__main__":
    PanelVendedor()