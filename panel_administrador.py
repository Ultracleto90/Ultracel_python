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
import reporte_corte

# --- PALETA DE COLORES "ENTERPRISE" ---
COLOR_BARRA_LATERAL = "#001f3f"  # Azul Marino Oscuro
COLOR_CUERPO        = "#f4f7f9"  # Gris muy claro
COLOR_PRIMARIO      = "#005187"  # Azul Corporativo
COLOR_ACCENTO       = "#00a8ff"  # Azul Brillante
COLOR_TEXTO         = "#2c3e50"  # Gris Oscuro
COLOR_BLANCO        = "#ffffff"

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
        self.ventana.geometry("1150x750")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg=COLOR_CUERPO)

        # Contenedores principales
        self.sidebar = tk.Frame(self.ventana, bg=COLOR_BARRA_LATERAL, width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main_content = tk.Frame(self.ventana, bg=COLOR_CUERPO)
        self.main_content.pack(side="right", fill="both", expand=True)

        self.setup_sidebar()
        self.crear_panel_principal() # Carga el dashboard por defecto

        self.ventana.mainloop()

    

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
                  command=reporte_corte.ventana_corte_caja).pack(pady=20)

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
                url_api = "http://localhost/api/empleados"
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
    def editar_usuario_modal(self, id_u):
        # 1. Obtenemos los datos del usuario desde Laravel
        try:
            res = requests.post("http://localhost/api/empleado/ver", json={"id": id_u})
            if res.status_code != 200:
                return messagebox.showerror("Error", "No se pudo cargar el usuario.")
            u = res.json().get('empleado', {})
        except requests.exceptions.ConnectionError:
            return messagebox.showerror("Error", "Sin conexión al servidor.")

        ventana_edit = tk.Toplevel(self.ventana)
        ventana_edit.title("Editar Perfil de Usuario")
        ventana_edit.geometry("400x600")
        ventana_edit.configure(bg=COLOR_BLANCO)
        ventana_edit.grab_set()

        tk.Label(ventana_edit, text="DETALLES DEL USUARIO", font=("Segoe UI", 14, "bold"), 
                 bg=COLOR_BLANCO, fg=COLOR_PRIMARIO).pack(pady=25)

        form = tk.Frame(ventana_edit, bg=COLOR_BLANCO, padx=40)
        form.pack(fill="both")

        entries = {}
        # Mapeamos a los nombres de la BD de Laravel (email, name)
        campos = {
            'email': ('Usuario Login (Email):', u.get('email', '')), 
            'name': ('Nombre Completo:', u.get('name', '')), 
            'especialidad': ('Especialidad:', u.get('especialidad', ''))
        }
        
        for key, (lbl, val) in campos.items():
            tk.Label(form, text=lbl, bg=COLOR_BLANCO, font=("Segoe UI", 9, "bold"), fg="#666").pack(anchor="w")
            e = tk.Entry(form, font=("Segoe UI", 11), bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9")
            
            # --- EL PARCHE ANTI-BERRINCHES DE TKINTER ---
            # Si la base de datos manda un None, lo convertimos a texto vacío ("")
            texto_seguro = val if val is not None else ""
            e.insert(0, texto_seguro)
            # --------------------------------------------
            
            e.pack(fill="x", pady=(5, 12), ipady=5)
            entries[key] = e

        tk.Label(form, text="Rol:", bg=COLOR_BLANCO, font=("Segoe UI", 9, "bold"), fg="#666").pack(anchor="w")
        rol_var = tk.StringVar(value=u.get('rol', 'Vendedor'))
        ttk.Combobox(form, textvariable=rol_var, values=["Admin", "Tecnico", "Vendedor", "Repartidor"], state="readonly").pack(fill="x", pady=5)

        perm_var = tk.BooleanVar(value=bool(u.get('permitido', 1)))
        tk.Checkbutton(form, text="¿Habilitar acceso al sistema?", variable=perm_var, bg=COLOR_BLANCO, font=("Segoe UI", 10)).pack(pady=20)

        def salvar():
            payload = {
                "id": id_u,
                "email": entries['email'].get(),
                "name": entries['name'].get(),
                "especialidad": entries['especialidad'].get(),
                "rol": rol_var.get(),
                "permitido": 1 if perm_var.get() else 0
            }
            try:
                res_save = requests.post("http://localhost/api/empleado/actualizar", json=payload)
                if res_save.status_code == 200:
                    ventana_edit.destroy()
                    self.admin_usuarios() # Recargar tabla principal
                else:
                    messagebox.showerror("Error", "No se pudo actualizar.")
            except:
                messagebox.showerror("Error", "Error de conexión.")

        tk.Button(ventana_edit, text="GUARDAR CAMBIOS", bg=COLOR_PRIMARIO, fg="white", 
                  font=("Segoe UI", 11, "bold"), relief="flat", command=salvar).pack(pady=20, fill="x", padx=40)

    # --- 4. MODAL: AGREGAR NUEVO USUARIO ---
    def agregar_usuarios(self):
        # Necesitamos saber a qué taller pertenece este nuevo usuario
        mi_taller_id = obtener_taller_id()
        if not mi_taller_id:
            return messagebox.showerror("Error", "No hay licencia activa.")

        ventana_agregar = tk.Toplevel(self.ventana)
        ventana_agregar.title("Registrar Nuevo Usuario")
        ventana_agregar.geometry("420x600")
        ventana_agregar.configure(bg=COLOR_BLANCO)
        ventana_agregar.grab_set()

        tk.Label(ventana_agregar, text="NUEVO PERSONAL", font=("Segoe UI", 15, "bold"), 
                 bg=COLOR_BLANCO, fg=COLOR_PRIMARIO).pack(pady=25)
        
        form = tk.Frame(ventana_agregar, bg=COLOR_BLANCO, padx=45)
        form.pack(fill="both")

        entries = {}
        campos = {'email': 'Usuario Login (Email):', 'name': 'Nombre Completo:', 'especialidad': 'Especialidad:'}

        for key, text in campos.items():
            tk.Label(form, text=text, font=("Segoe UI", 9, "bold"), bg=COLOR_BLANCO, fg="#666").pack(anchor="w")
            e = tk.Entry(form, font=("Segoe UI", 11), bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9")
            e.pack(fill="x", pady=(5, 12), ipady=5)
            entries[key] = e

        tk.Label(form, text="Rol del Usuario:", font=("Segoe UI", 9, "bold"), bg=COLOR_BLANCO, fg="#666").pack(anchor="w")
        rol_var = tk.StringVar(value="Vendedor")
        ttk.Combobox(form, textvariable=rol_var, values=["Admin", "Tecnico", "Vendedor", "Repartidor"], state="readonly").pack(fill="x", pady=5)

        def guardar():
            passw = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            if not entries['email'].get() or not entries['name'].get():
                return messagebox.showwarning("Faltan datos", "Complete los campos obligatorios.")

            payload = {
                "email": entries['email'].get(),
                "name": entries['name'].get(),
                "especialidad": entries['especialidad'].get(),
                "rol": rol_var.get(),
                "password": passw,
                "taller_id": mi_taller_id
            }

            try:
                res = requests.post("http://localhost/api/empleado/crear", json=payload)
                if res.status_code == 200:
                    messagebox.showinfo("Registro Exitoso", f"Usuario: {entries['email'].get()}\nContraseña Temporal: {passw}\n\n¡Guarda esta contraseña!")
                    ventana_agregar.destroy()
                    self.admin_usuarios() # Recargar tabla principal
                else:
                    messagebox.showerror("Error", "No se pudo crear. Asegúrate de que el email no esté repetido.")
            except Exception as e: 
                messagebox.showerror("Error", "Problema al conectar con la API.")

        tk.Button(ventana_agregar, text="CREAR USUARIO", bg=COLOR_PRIMARIO, fg="white", 
                  font=("Segoe UI", 11, "bold"), relief="flat", command=guardar).pack(pady=35, fill="x", padx=45)

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
                res = requests.post("http://localhost/api/material/admin-listar", json={"taller_id": mi_taller_id})
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
                payload = {
                    "id_solicitud": id_s,
                    "estado": nuevo
                }
                res = requests.post("http://localhost/api/material/actualizar-estado", json=payload)
                
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
    app = PanelAdministrador()