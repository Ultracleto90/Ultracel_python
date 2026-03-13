import os
import json
import sys
import tkinter as tk
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
    """Revisa si el archivo de licencia existe en la computadora"""
    if os.path.exists(ARCHIVO_LICENCIA):
        try:
            with open(ARCHIVO_LICENCIA, 'r') as file:
                datos = json.load(file)
                # Aquí podríamos validar si la fecha ya venció localmente, 
                # pero por ahora solo confirmamos que el archivo existe.
                return True
        except:
            return False
    return False

def guardar_licencia(datos_licencia):
    """Crea el archivo oculto cuando el pago/activación es exitoso"""
    with open(ARCHIVO_LICENCIA, 'w') as file:
        json.dump(datos_licencia, file)

def iniciar_sesion():
    root = tk.Tk()
    root.title("Ultracel Core | v3.0")
    root.geometry("850x500")
    
    # Centrado perfecto
    ws, hs = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = (ws // 2) - (425), (hs // 2) - (250)
    root.geometry(f"850x500+{x}+{y}")
    root.resizable(False, False)
    root.configure(bg="white")

    # CANVAS PARA EL FONDO Y PANELES 
    main_canvas = tk.Canvas(root, width=850, height=500, highlightthickness=0, bg="white")
    main_canvas.pack(fill="both", expand=True)

    # 1. Panel Lateral Estilizado (Izquierda)
    # Dibujamos un rectángulo que simula el fondo de marca
    main_canvas.create_rectangle(0, 0, 350, 500, fill=COLOR_DEGRADADO_1, outline="")
    
    # Intentar cargar imagen de fondo para el panel lateral
    if getattr(sys, 'frozen', False): base_path = sys._MEIPASS
    else: base_path = os.path.dirname(__file__)
    
    img_path = os.path.join(base_path, "assets", "logo_ultracel.png")
    try:
        side_img = Image.open(img_path).resize((600, 600))
        side_img_blur = side_img.filter(ImageFilter.GaussianBlur(radius=20))
        side_tk = ImageTk.PhotoImage(side_img_blur)
        main_canvas.create_image(-100, 250, image=side_tk, alpha=0.3) # Efecto de marca de agua
        main_canvas.side_img = side_tk
    except: pass

    # Texto de Marca en el Panel Lateral
    main_canvas.create_text(175, 220, text="ULTRACEL", font=("Helvetica", 32, "bold"), fill="white")
    main_canvas.create_text(175, 260, text="SISTEMA DE GESTIÓN INTEGRAL", font=("Helvetica", 8), fill=COLOR_ACCENTO)
    main_canvas.create_line(120, 280, 230, 280, fill=COLOR_ACCENTO, width=2)

    # 2. Panel de Formulario (Derecha)
    # Usamos un Frame para contener los widgets de forma limpia
    form_frame = tk.Frame(root, bg="white")
    main_canvas.create_window(600, 250, window=form_frame, width=400, height=450)

    # --- WIDGETS DEL FORMULARIO ---
    tk.Label(form_frame, text="BIENVENIDO", font=("Arial", 10, "bold"), bg="white", fg=COLOR_ACCENTO).pack(pady=(20, 0))
    tk.Label(form_frame, text="Acceder a su Cuenta", font=("Segoe UI Light", 22), bg="white", fg=COLOR_TEXTO_MAIN).pack(pady=(0, 40))

    # Estilo de Entry Personalizado
    def create_modern_entry(parent, label_text, is_pass=False):
        tk.Label(parent, text=label_text, font=("Arial", 8, "bold"), bg="white", fg="#b2bec3").pack(anchor="w", padx=40)
        entry = tk.Entry(parent, font=("Segoe UI", 12), bg=COLOR_INPUT_BG, relief="flat", 
                         highlightthickness=1, highlightbackground="#dfe6e9", 
                         highlightcolor=COLOR_ACCENTO, show="*" if is_pass else "")
        entry.pack(fill="x", padx=40, pady=(5, 20), ipady=10)
        return entry

    user_entry = create_modern_entry(form_frame, "NOMBRE DE USUARIO")
    pass_entry = create_modern_entry(form_frame, "CONTRASEÑA SEGURA", is_pass=True)



    def handle_activacion():
    
        email_admin = user_entry.get() 
        password_admin = pass_entry.get()

        if not email_admin or not password_admin:
            messagebox.showwarning("Campos vacíos", "Ingresa tu correo y contraseña de administrador.")
            return

        url_api = "http://localhost/api/activar-licencia"
        payload = {
            "email": email_admin,
            "password": password_admin
        }

        try:
            respuesta = requests.post(url_api, json=payload)

            if respuesta.status_code == 200:
                datos = respuesta.json()
                
                # ¡Laravel dijo que sí pagó! Guardamos el token en la PC
                guardar_licencia(datos['datos_licencia'])
                
                messagebox.showinfo("¡Software Activado!", datos['message'])
                
                # Limpiamos las cajas de texto
                user_entry.delete(0, tk.END)
                pass_entry.delete(0, tk.END)
                
                # AQUI: Cambiamos el comportamiento del botón para que ahora 
                # sea un Login normal de cajeros/técnicos
                btn_container.itemconfig(btn_text, text="INICIAR SESIÓN")
                
                
            elif respuesta.status_code in [401, 403]:
                # Laravel dice: No pagaste, tu licencia venció o no eres el admin
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

        # 2. Preparar el mensaje para tu API de Laravel
        url_api = "http://localhost/api/login"
        payload = {
            "email": email_ingresado,
            "password": password_ingresado
        }

        try:
            # 3. Tocar la puerta de la API usando requests
            respuesta = requests.post(url_api, json=payload)

            # 4. Laravel dice: ¡Pásale!
            if respuesta.status_code == 200:
                datos = respuesta.json()
                usuario = datos['usuario']
                
                messagebox.showinfo("¡Acceso Concedido!", f"Bienvenido al sistema, {usuario['name']}")
                
                # Por ahora solo cerramos la ventana al tener éxito
                root.destroy()
                
            # Laravel dice: ¡Contraseña equivocada!
            elif respuesta.status_code == 401:
                messagebox.showerror("Acceso Denegado", "El correo o la contraseña son incorrectos.")
                
            # Laravel dice: ¡Algo explotó internamente!
            else:
                messagebox.showerror("Error", f"Error en el servidor: {respuesta.status_code}")

        except requests.exceptions.ConnectionError:
            # Python dice: ¡Laravel no me contesta!
            messagebox.showerror("Error de Conexión", "No se pudo conectar con el servidor. Verifica que Docker esté encendido.")



            
    # --- BOTÓN DE ACCIÓN "GLOSSY" ---
    btn_container = tk.Canvas(form_frame, width=320, height=50, bg="white", highlightthickness=0)
    btn_container.pack(pady=10)
    
    
    
    # 1. Leemos el "Punto de Guardado" antes de dibujar el botón
    esta_activado = verificar_activacion_local()
    
    # 2. Decidimos qué texto va a llevar el dibujo
    texto_del_boton = "INICIAR SESIÓN" if esta_activado else "ACTIVAR LICENCIA"

    # 3. El Switch Inteligente: Decide a qué función llamar cuando le den clic
    def on_btn_click(e): 
        if verificar_activacion_local():
            handle_login()
        else:
            handle_activacion()
    
    # Dibujar botón redondeado manualmente en el canvas para estética pro
    btn_shape = btn_container.create_rectangle(0, 0, 320, 50, fill=COLOR_DEGRADADO_2, outline="")
    
    # 4. Inyectamos la variable del texto aquí:
    btn_text = btn_container.create_text(160, 25, text=texto_del_boton, fill="white", font=("Arial", 10, "bold"))
    
    # Efectos Hover para el botón manual (Esto se queda idéntico)
    btn_container.tag_bind(btn_shape, "<Enter>", lambda e: btn_container.itemconfig(btn_shape, fill=COLOR_DEGRADADO_1))
    btn_container.tag_bind(btn_shape, "<Leave>", lambda e: btn_container.itemconfig(btn_shape, fill=COLOR_DEGRADADO_2))
    btn_container.tag_bind(btn_text, "<Enter>", lambda e: btn_container.itemconfig(btn_shape, fill=COLOR_DEGRADADO_1))
    
    # 5. Conectamos el clic al Switch Inteligente
    btn_container.tag_bind(btn_shape, "<Button-1>", on_btn_click)
    btn_container.tag_bind(btn_text, "<Button-1>", on_btn_click)
    btn_container.config(cursor="hand2")

    # Footer
    tk.Label(form_frame, text="Olvidé mi contraseña", font=("Arial", 8), bg="white", fg=COLOR_ACCENTO, cursor="hand2").pack(pady=10)
    
    # Fade-In
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