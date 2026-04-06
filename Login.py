import os
import json
import sys
import tkinter as tk
import subprocess
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter
import requests

# --- CONFIGURACIÓN DE IDENTIDAD VISUAL ---
COLOR_DEGRADADO_1 = "#001f3f"  # Azul Medianoche
COLOR_DEGRADADO_2 = "#005187"  # Azul Ultracel
COLOR_ACCENTO     = "#00d2ff"  # Cian Neón para detalles
COLOR_TEXTO_MAIN  = "#2d3436"  # Gris casi negro
COLOR_INPUT_BG    = "#f5f6fa"  # Gris seda

ARCHIVO_LICENCIA = "licencia.json"

def verificar_activacion_local():
    if os.path.exists(ARCHIVO_LICENCIA):
        try:
            with open(ARCHIVO_LICENCIA, 'r') as file:
                datos = json.load(file)
                return True
        except:
            return False
    return False

def guardar_licencia(datos_licencia):
    with open(ARCHIVO_LICENCIA, 'w') as file:
        json.dump(datos_licencia, file)

def iniciar_sesion():
    root = tk.Tk()
    root.title("Ultracel Core | v3.0")
    
    # --- LA MAGIA RESPONSIVA: Tamaño basado en el % de la pantalla ---
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    
    # Tomamos el 60% del ancho y 60% del alto de la pantalla actual
    w = int(ws * 0.6)
    h = int(hs * 0.6)
    
    # Establecemos un tamaño mínimo para que no se apachurre demasiado
    w = max(w, 850)
    h = max(h, 500)
    
    # Centrado matemático
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.minsize(850, 500)
    root.configure(bg="white")

    # --- EL TRUCO PARA ABRIR MAXIMIZADO ---
    try:
        root.state('zoomed') # Comando para Windows
    except:
        root.attributes('-zoomed', True) # Comando para Linux

    # --- PANEL LATERAL (IZQUIERDA) - Ocupa el 40% del ancho (relwidth=0.4) ---
    left_panel = tk.Frame(root, bg=COLOR_DEGRADADO_1)
    left_panel.place(relx=0, rely=0, relwidth=0.4, relheight=1.0)
    
    # Contenedor centrado para los textos e imagen del panel izquierdo
    left_content = tk.Frame(left_panel, bg=COLOR_DEGRADADO_1)
    left_content.place(relx=0.5, rely=0.5, anchor="center")

    # Intentar cargar imagen de fondo para el panel lateral
    if getattr(sys, 'frozen', False): base_path = sys._MEIPASS
    else: base_path = os.path.dirname(__file__)
    
    img_path = os.path.join(base_path, "assets", "logo_ultracel.png")
    try:
        side_img = Image.open(img_path).resize((250, 250))
        side_img_blur = side_img.filter(ImageFilter.GaussianBlur(radius=5))
        side_tk = ImageTk.PhotoImage(side_img_blur)
        lbl_img = tk.Label(left_content, image=side_tk, bg=COLOR_DEGRADADO_1)
        lbl_img.image = side_tk
        lbl_img.pack(pady=10)
    except: pass

    tk.Label(left_content, text="ULTRACEL", font=("Helvetica", 32, "bold"), bg=COLOR_DEGRADADO_1, fg="white").pack()
    tk.Label(left_content, text="SISTEMA DE GESTIÓN INTEGRAL", font=("Helvetica", 9), bg=COLOR_DEGRADADO_1, fg=COLOR_ACCENTO).pack(pady=(0, 10))
    tk.Frame(left_content, bg=COLOR_ACCENTO, height=2, width=100).pack(pady=5)

    # --- PANEL DEL FORMULARIO (DERECHA) - Ocupa el 60% del ancho (relwidth=0.6) ---
    right_panel = tk.Frame(root, bg="white")
    right_panel.place(relx=0.4, rely=0, relwidth=0.6, relheight=1.0)
    
    # Contenedor del formulario anclado exactamente en el centro
    form_frame = tk.Frame(right_panel, bg="white")
    form_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)

    # --- WIDGETS DEL FORMULARIO ---
    tk.Label(form_frame, text="BIENVENIDO", font=("Arial", 10, "bold"), bg="white", fg=COLOR_ACCENTO).pack(pady=(10, 0))
    tk.Label(form_frame, text="Acceder a su Cuenta", font=("Segoe UI Light", 24), bg="white", fg=COLOR_TEXTO_MAIN).pack(pady=(0, 30))

    def create_modern_entry(parent, label_text, is_pass=False):
        tk.Label(parent, text=label_text, font=("Arial", 8, "bold"), bg="white", fg="#b2bec3").pack(anchor="w", padx=10)
        entry = tk.Entry(parent, font=("Segoe UI", 12), bg=COLOR_INPUT_BG, relief="flat", 
                         highlightthickness=1, highlightbackground="#dfe6e9", 
                         highlightcolor=COLOR_ACCENTO, show="*" if is_pass else "")
        entry.pack(fill="x", padx=10, pady=(5, 20), ipady=10)
        return entry

    user_entry = create_modern_entry(form_frame, "NOMBRE DE USUARIO")
    pass_entry = create_modern_entry(form_frame, "CONTRASEÑA SEGURA", is_pass=True)

    # --- LÓGICA DE BOTONES (Mantenida intacta) ---
    def handle_activacion():
        email_admin = user_entry.get() 
        password_admin = pass_entry.get()

        if not email_admin or not password_admin:
            messagebox.showwarning("Campos vacíos", "Ingresa tu correo y contraseña de administrador.")
            return

        url_api = "https://www.ultracel.lat/api/activar-licencia"
        payload = {"email": email_admin, "password": password_admin}

        try:
            respuesta = requests.post(url_api, json=payload)
            if respuesta.status_code == 200:
                datos = respuesta.json()
                guardar_licencia(datos['datos_licencia'])
                messagebox.showinfo("¡Software Activado!", datos['message'])
                user_entry.delete(0, tk.END)
                pass_entry.delete(0, tk.END)
                btn_container.itemconfig(btn_text, text="INICIAR SESIÓN")
            elif respuesta.status_code in [401, 403]:
                error_msg = respuesta.json().get('message', 'Error de validación')
                messagebox.showerror("Error de Activación", error_msg)
            else:
                messagebox.showerror("Error", f"Error en el servidor: {respuesta.status_code}")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "No se pudo conectar con el servidor central.")

    def handle_login():
        email_ingresado = user_entry.get() 
        password_ingresado = pass_entry.get()

        if not email_ingresado or not password_ingresado:
            messagebox.showwarning("Campos vacíos", "Por favor ingresa tu correo y contraseña.")
            return

        url_api = "https://www.ultracel.lat/api/login"
        payload = {"email": email_ingresado, "password": password_ingresado}

        try:
            respuesta = requests.post(url_api, json=payload)
            if respuesta.status_code == 200:
                datos = respuesta.json()
                rol = datos.get('rol')
                nombre = datos.get('name')
                user_taller_id = datos.get('taller_id')

                # 🔒 CANDADO MAESTRO FRONTEND: Evitar que un empleado de otra sucursal inicie sesión aquí
                try:
                    with open(ARCHIVO_LICENCIA, 'r') as file:
                        taller_licencia = json.load(file).get('taller_id')
                    
                    if str(user_taller_id) != str(taller_licencia):
                        return messagebox.showerror("Acceso Denegado 🛡️", "Tu usuario no pertenece a esta sucursal.")
                except:
                    return messagebox.showerror("Error", "Licencia corrupta. Vuelve a activar el software.")
                
                # ¡Atrapamos el ID y lo convertimos a texto para mandarlo!
                id_usuario = str(datos.get('id', 1))
                
                messagebox.showinfo("¡Acceso Concedido!", f"Bienvenido al sistema, {nombre}\nRol detectado: {rol}")
                root.destroy()
                
                # Le mandamos el id_usuario como un parámetro oculto al abrir el archivo
                if rol == "admin": subprocess.Popen([sys.executable, "panel_administrador.py", id_usuario])
                elif rol == "tecnico" or rol == "Tecnico": subprocess.Popen([sys.executable, "tecnico.py", id_usuario])
                elif rol.lower() == "vendedor" or rol == "Vendedor": subprocess.Popen([sys.executable, "vendedor.py", id_usuario])
                else: messagebox.showerror("Error Crítico", f"El rol '{rol}' no tiene un panel asignado.")
            elif respuesta.status_code == 401:
                messagebox.showerror("Acceso Denegado", "El correo o la contraseña son incorrectos.")
            elif respuesta.status_code == 403:
                messagebox.showerror("Acceso Bloqueado", "Tu cuenta ha sido deshabilitada por el administrador.")
            else:
                messagebox.showerror("Error", f"Error en el servidor: {respuesta.status_code}")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error de Conexión", "No se pudo conectar con el servidor.")

    # --- BOTÓN DE ACCIÓN "GLOSSY" ---
    btn_container = tk.Canvas(form_frame, height=50, bg="white", highlightthickness=0)
    btn_container.pack(fill="x", padx=10, pady=20)
    
    esta_activado = verificar_activacion_local()
    texto_del_boton = "INICIAR SESIÓN" if esta_activado else "ACTIVAR LICENCIA"

    def on_btn_click(e): 
        handle_login() if verificar_activacion_local() else handle_activacion()
    
    # Dibujar el botón dinámico 
    def draw_button(event):
        btn_container.delete("all")
        w = event.width
        btn_shape = btn_container.create_rectangle(0, 0, w, 50, fill=COLOR_DEGRADADO_2, outline="", tags="btn")
        global btn_text
        btn_text = btn_container.create_text(w/2, 25, text=texto_del_boton, fill="white", font=("Arial", 10, "bold"), tags="txt")
        
        btn_container.tag_bind("btn", "<Enter>", lambda e: btn_container.itemconfig(btn_shape, fill=COLOR_DEGRADADO_1))
        btn_container.tag_bind("btn", "<Leave>", lambda e: btn_container.itemconfig(btn_shape, fill=COLOR_DEGRADADO_2))
        btn_container.tag_bind("txt", "<Enter>", lambda e: btn_container.itemconfig(btn_shape, fill=COLOR_DEGRADADO_1))
        
        btn_container.tag_bind("btn", "<Button-1>", on_btn_click)
        btn_container.tag_bind("txt", "<Button-1>", on_btn_click)

    btn_container.bind("<Configure>", draw_button)
    btn_container.config(cursor="hand2")

    tk.Label(form_frame, text="Olvidé mi contraseña", font=("Arial", 8), bg="white", fg=COLOR_ACCENTO, cursor="hand2").pack(pady=5)
    
    root.attributes("-alpha", 0.0)
    def fade():
        curr = root.attributes("-alpha")
        if curr < 1.0:
            root.attributes("-alpha", curr + 0.1)
            root.after(25, fade)
    fade()

    root.bind("<Return>", lambda e: on_btn_click(e))
    root.mainloop()

if __name__ == "__main__":
    iniciar_sesion()