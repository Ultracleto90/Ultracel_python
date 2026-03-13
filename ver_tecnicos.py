import tkinter as tk
from tkinter import ttk

# 🎨 Paleta de colores
BG_COLOR = "#F5F5F5"
HEADER_COLOR = "#005187"
TEXT_COLOR = "#212121"
CARD_BG = "#fcffff"

# 🧑‍🔧 Técnicos ficticios
original_tecnicos = [
    {"nombre": "Luis Martínez", "especialidad": "Pantallas OLED", "edad": 32,
     "pendientes": 2, "terminados": 15, "ubicacion": "Taller Norte"},
    {"nombre": "Ana Gómez", "especialidad": "Baterías y energía", "edad": 28,
     "pendientes": 1, "terminados": 20, "ubicacion": "Taller Central"},
    {"nombre": "Carlos Ruiz", "especialidad": "Cámaras y sensores", "edad": 35,
     "pendientes": 4, "terminados": 10, "ubicacion": "Taller Sur"},
    {"nombre": "María López", "especialidad": "Software y calibración", "edad": 30,
     "pendientes": 0, "terminados": 25, "ubicacion": "Taller Este"},
    {"nombre": "Jorge Díaz", "especialidad": "Puertos de carga", "edad": 40,
     "pendientes": 3, "terminados": 12, "ubicacion": "Taller Norte"},
]

def ventana_ver_tecnicos():
    ventana = tk.Toplevel()
    ventana.title("Ver Técnicos")
    ventana.geometry("420x520")
    ventana.configure(bg=BG_COLOR)

    tk.Label(ventana, text="🧑‍🔧 Técnicos del Taller", font=("Helvetica", 18, "bold"),
             bg=BG_COLOR, fg=HEADER_COLOR).pack(pady=(20, 10))

    # 🎛️ Filtro por carga de trabajo
    filtro_frame = tk.Frame(ventana, bg=BG_COLOR)
    filtro_frame.pack(pady=5)

    tk.Label(filtro_frame, text="Ordenar por:", font=("Helvetica", 12),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(side="left", padx=5)

    opciones_filtro = ["Trabajos Pendientes", "Trabajos Terminados"]
    filtro_spinner = ttk.Combobox(filtro_frame, values=opciones_filtro, state="readonly", width=20)
    filtro_spinner.pack(side="left")

    # 📋 Área de técnicos
    tecnicos_frame = tk.Frame(ventana, bg=BG_COLOR)
    tecnicos_frame.pack(pady=10, fill="both", expand=True)

    def mostrar_tecnicos(lista):
        for widget in tecnicos_frame.winfo_children():
            widget.destroy()

        for t in lista:
            card = tk.Frame(tecnicos_frame, bg=CARD_BG, bd=1, relief="solid")
            card.pack(pady=5, padx=20, fill="x")

            texto = (
                f"👤 {t['nombre']}\nEspecialidad: {t['especialidad']}\nEdad: {t['edad']} años"
                f"\nPendientes: {t['pendientes']} | Terminados: {t['terminados']}"
                f"\nUbicación: {t['ubicacion']}"
            )
            tk.Label(card, text=texto, font=("Helvetica", 11),
                     bg=CARD_BG, fg=TEXT_COLOR, justify="left").pack(padx=10, pady=10)

    def filtrar_tecnicos(event=None):
        criterio = filtro_spinner.get()
        lista_ordenada = original_tecnicos.copy()

        if criterio == "Trabajos Pendientes":
            lista_ordenada.sort(key=lambda x: x["pendientes"], reverse=True)
        elif criterio == "Trabajos Terminados":
            lista_ordenada.sort(key=lambda x: x["terminados"], reverse=True)

        mostrar_tecnicos(lista_ordenada)

    filtro_spinner.bind("<<ComboboxSelected>>", filtrar_tecnicos)
    mostrar_tecnicos(original_tecnicos)
