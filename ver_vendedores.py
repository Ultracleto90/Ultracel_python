import tkinter as tk
from tkinter import ttk

BG_COLOR = "#F5F5F5"
HEADER_COLOR = "#005187"
TEXT_COLOR = "#212121"
CARD_BG = "#fcffff"

vendedores = [
    {"nombre": "Sofía Herrera", "especialidad": "Accesorios móviles", "edad": 26, "ventas": 120, "zona": "Sucursal Centro"},
    {"nombre": "Marco León", "especialidad": "Tabletas", "edad": 33, "ventas": 95, "zona": "Sucursal Norte"},
    {"nombre": "Lucía Gómez", "especialidad": "Smartphones", "edad": 29, "ventas": 140, "zona": "Sucursal Sur"},
    {"nombre": "Pedro Sánchez", "especialidad": "Refacciones", "edad": 38, "ventas": 80, "zona": "Sucursal Este"},
    {"nombre": "Valeria Cruz", "especialidad": "Cargadores y cables", "edad": 31, "ventas": 110, "zona": "Sucursal Oeste"},
]

def ventana_ver_vendedores():
    ventana = tk.Toplevel()
    ventana.title("Ver Vendedores")
    ventana.geometry("420x520")
    ventana.configure(bg=BG_COLOR)

    tk.Label(ventana, text="🛍️ Vendedores del Negocio", font=("Helvetica", 18, "bold"),
             bg=BG_COLOR, fg=HEADER_COLOR).pack(pady=(20, 10))

    filtro_frame = tk.Frame(ventana, bg=BG_COLOR)
    filtro_frame.pack(pady=5)

    tk.Label(filtro_frame, text="Ordenar por:", font=("Helvetica", 12),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(side="left", padx=5)

    opciones = ["Ventas Realizadas", "Edad"]
    filtro_spinner = ttk.Combobox(filtro_frame, values=opciones, state="readonly", width=20)
    filtro_spinner.pack(side="left")

    frame_lista = tk.Frame(ventana, bg=BG_COLOR)
    frame_lista.pack(pady=10, fill="both", expand=True)

    def mostrar(lista):
        for widget in frame_lista.winfo_children():
            widget.destroy()

        for v in lista:
            card = tk.Frame(frame_lista, bg=CARD_BG, bd=1, relief="solid")
            card.pack(pady=5, padx=20, fill="x")

            texto = (
                f"👤 {v['nombre']}\nEspecialidad: {v['especialidad']}\nEdad: {v['edad']} años"
                f"\nVentas: {v['ventas']}\nZona: {v['zona']}"
            )
            tk.Label(card, text=texto, font=("Helvetica", 11),
                     bg=CARD_BG, fg=TEXT_COLOR, justify="left").pack(padx=10, pady=10)

    def filtrar(event=None):
        criterio = filtro_spinner.get()
        ordenada = vendedores.copy()

        if criterio == "Ventas Realizadas":
            ordenada.sort(key=lambda x: x["ventas"], reverse=True)
        elif criterio == "Edad":
            ordenada.sort(key=lambda x: x["edad"])

        mostrar(ordenada)

    filtro_spinner.bind("<<ComboboxSelected>>", filtrar)
    mostrar(vendedores)
