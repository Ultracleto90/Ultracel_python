import os
import json
import sys
import subprocess
import requests
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image

import panel_administrador
import tecnico
import vendedor

# --- CONFIGURACIÓN INICIAL DEL MOTOR GRÁFICO ---
# Modo oscuro por defecto y color de acento azul
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")

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
    app = ctk.CTk()
    app.title("Ultracel Core | v3.0")
    
    # --- LA MAGIA RESPONSIVA (Mantenida intacta) ---
    ws = app.winfo_screenwidth()
    hs = app.winfo_screenheight()
    w = max(int(ws * 0.6), 850)
    h = max(int(hs * 0.6), 500)
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    app.geometry(f"{w}x{h}+{x}+{y}")
    app.minsize(850, 500)

    # Maximizar ventana según SO
    try:
        app.state('zoomed') 
    except:
        try:
            app.attributes('-zoomed', True)
        except:
            pass

    # --- GRID LAYOUT (40% Izquierda / 60% Derecha) ---
    app.grid_columnconfigure(0, weight=4)
    app.grid_columnconfigure(1, weight=6)
    app.grid_rowconfigure(0, weight=1)

    # ==========================================
    # PANEL LATERAL (IZQUIERDA) - BRANDING
    # ==========================================
    # fg_color acepta una tupla: (Color Modo Claro, Color Modo Oscuro)
    left_frame = ctk.CTkFrame(app, corner_radius=0, fg_color=("#005187", "#0B1120")) 
    left_frame.grid(row=0, column=0, sticky="nsew")
    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    # Contenedor centrado en el panel izquierdo
    left_content = ctk.CTkFrame(left_frame, fg_color="transparent")
    left_content.grid(row=0, column=0)

    # Intentar cargar imagen de fondo (Adaptada para CustomTkinter)
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
    img_path = os.path.join(base_path, "assets", "logo_ultracel.png")
    try:
        # CTkImage maneja resoluciones altas automáticamente
        logo_img = ctk.CTkImage(light_image=Image.open(img_path), dark_image=Image.open(img_path), size=(200, 200))
        logo_label = ctk.CTkLabel(left_content, image=logo_img, text="")
        logo_label.pack(pady=(0, 20))
    except: 
        pass # Si no hay imagen, no rompe el programa

    ctk.CTkLabel(left_content, text="ULTRACEL", font=ctk.CTkFont(size=36, weight="bold"), text_color="white").pack()
    ctk.CTkLabel(left_content, text="SISTEMA DE GESTIÓN INTEGRAL", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3B82F6").pack(pady=(0, 20))

    # ==========================================
    # PANEL DEL FORMULARIO (DERECHA)
    # ==========================================
    right_frame = ctk.CTkFrame(app, corner_radius=0, fg_color=("gray95", "#111827"))
    right_frame.grid(row=0, column=1, sticky="nsew")
    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    # Switch para alternar Tema (Arriba a la derecha)
    def toggle_mode():
        if switch_var.get() == "on":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    switch_var = ctk.StringVar(value="on")
    theme_switch = ctk.CTkSwitch(right_frame, text="Modo Oscuro", command=toggle_mode, variable=switch_var, onvalue="on", offvalue="off", progress_color="#3B82F6")
    theme_switch.place(relx=0.95, rely=0.05, anchor="ne")

    # Contenedor del formulario (Transparencia dinámica activada)
    form_frame = ctk.CTkFrame(right_frame, fg_color=("white", "#1F2937"), bg_color="transparent", corner_radius=15, border_width=1, border_color=("gray85", "#374151"))
    form_frame.grid(row=0, column=0)

    # Títulos (Dejamos que CTk clone el fondo automáticamente)
    ctk.CTkLabel(form_frame, text="BIENVENIDO", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3B82F6", bg_color="transparent").pack(anchor="w", padx=40, pady=(40, 5))
    ctk.CTkLabel(form_frame, text="Acceder a su Cuenta", font=ctk.CTkFont(size=28, weight="bold"), bg_color="transparent").pack(anchor="w", padx=40, pady=(0, 30))

    # Inputs Modernos "Efecto Enterprise"
    ctk.CTkLabel(form_frame, text="CORREO ELECTRÓNICO", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray50", bg_color="transparent").pack(anchor="w", padx=40)
    user_entry = ctk.CTkEntry(form_frame, width=350, height=45, placeholder_text="ejemplo@ultracel.lat", font=ctk.CTkFont(size=14), corner_radius=8, border_width=1, border_color=("#D1D5DB", "#374151"), fg_color=("gray95", "#111827"), bg_color="transparent")
    user_entry.pack(padx=40, pady=(5, 20))

    ctk.CTkLabel(form_frame, text="CONTRASEÑA", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray50", bg_color="transparent").pack(anchor="w", padx=40)
    pass_entry = ctk.CTkEntry(form_frame, width=350, height=45, placeholder_text="••••••••", show="*", font=ctk.CTkFont(size=14), corner_radius=8, border_width=1, border_color=("#D1D5DB", "#374151"), fg_color=("gray95", "#111827"), bg_color="transparent")
    pass_entry.pack(padx=40, pady=(5, 30))
    
    # Efecto Focus (Se queda igual, no lo borres)
    user_entry.bind("<FocusIn>", lambda e: user_entry.configure(border_color="#3B82F6"))
    user_entry.bind("<FocusOut>", lambda e: user_entry.configure(border_color=("#D1D5DB", "#374151")))
    pass_entry.bind("<FocusIn>", lambda e: pass_entry.configure(border_color="#3B82F6"))
    pass_entry.bind("<FocusOut>", lambda e: pass_entry.configure(border_color=("#D1D5DB", "#374151")))
    # ==========================================
    # LÓGICA DE API Y BOTONES
    # ==========================================
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
                messagebox.showinfo("Software Activado", datos['message'])
                user_entry.delete(0, ctk.END)
                pass_entry.delete(0, ctk.END)
                main_btn.configure(text="INICIAR SESIÓN")
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

                # Candado Frontend
                try:
                    with open(ARCHIVO_LICENCIA, 'r') as file:
                        taller_licencia = json.load(file).get('taller_id')
                    
                    if str(user_taller_id) != str(taller_licencia):
                        return messagebox.showerror("Acceso Denegado", "Tu usuario no pertenece a esta sucursal.")
                except:
                    return messagebox.showerror("Error", "Licencia corrupta. Vuelve a activar el software.")
                
                id_usuario = int(datos.get('id', 1))
                
                app.destroy() # Destruimos la ventana de login
                
                # ✨ REDIRECCIÓN NATIVA (Ejecución en un solo archivo) ✨
                if rol == "admin":
                    # IMPORTANTE: Revisa que tu clase principal en ese archivo se llame así
                    panel_administrador.PanelAdministrador(id_usuario) 
                elif rol.lower() == "tecnico":
                    # IMPORTANTE: Revisa que tu clase principal se llame así
                    tecnico.PanelTecnico(id_usuario)
                elif rol.lower() in ["vendedor", "recepcionista"]:
                    # En tu archivo vendedor.py la clase se llama PanelVendedor
                    vendedor.PanelVendedor(id_usuario)
                else:
                    messagebox.showerror("Error Crítico", f"El rol '{rol}' no tiene un panel asignado.")
            elif respuesta.status_code == 401:
                messagebox.showerror("Acceso Denegado", "El correo o la contraseña son incorrectos.")
            elif respuesta.status_code == 403:
                messagebox.showerror("Acceso Bloqueado", "Tu cuenta ha sido deshabilitada por el administrador.")
            else:
                messagebox.showerror("Error", f"Error en el servidor: {respuesta.status_code}")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error de Conexión", "No se pudo conectar con el servidor.")

    def on_btn_click(e=None): 
        handle_login() if verificar_activacion_local() else handle_activacion()

    esta_activado = verificar_activacion_local()
    texto_del_boton = "INICIAR SESIÓN" if esta_activado else "ACTIVAR LICENCIA"


    # Botón Principal (Transparencia nativa)
    main_btn = ctk.CTkButton(form_frame, text=texto_del_boton, width=350, height=45, font=ctk.CTkFont(size=14, weight="bold"), corner_radius=8, fg_color="#2563EB", hover_color="#1D4ED8", border_width=2, border_color="#3B82F6", bg_color="transparent", command=on_btn_click)
    main_btn.pack(padx=40, pady=(10, 15))

    # Link "Olvidé mi contraseña" 
    forgot_lbl = ctk.CTkLabel(form_frame, text="¿Olvidaste tu contraseña?", font=ctk.CTkFont(size=12, underline=True), text_color="#3B82F6", cursor="hand2", bg_color="transparent")
    forgot_lbl.pack(pady=(0, 40))

    # Enter para enviar
    app.bind("<Return>", lambda e: on_btn_click())
    
    app.mainloop()

if __name__ == "__main__":
    iniciar_sesion()