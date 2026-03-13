import tkinter as tk
from tkinter import ttk

BG_COLOR = "#F5F5F5"
HEADER_COLOR = "#005187"
TEXT_COLOR = "#212121"
CARD_BG = "#fcffff"

repartidores = [
    {"nombre": "Daniel Pérez", "zona": "Centro", "edad": 29, "entregas": 45, "pendientes": 3, "vehiculo": "Moto"},
    {"nombre": "Laura Sánchez", "zona": "Norte", "edad": 34, "entregas": 60, "pendientes": 1, "vehiculo": "Bicicleta"},
    {"nombre": "José Ramírez", "zona": "Sur", "edad": 27, "entregas": 38, "pendientes": 5, "vehiculo": "Auto"},
    {"nombre": "Elena Torres", "zona": "Este", "edad": 31, "entregas": 50, "pendientes": 0, "vehiculo": "Moto"},
    {"nombre": "Miguel Díaz", "zona": "Oeste", "edad": 40, "entregas": 42, "pendientes": 2, "vehiculo": "Camioneta"},
]

def ventana_ver_repartidores():
    ventana = tk.Toplevel()
    ventana.title("Ver Repartidores")
    ventana.geometry("420x520")
    ventana.configure(bg=BG_COLOR)

    tk.Label(ventana, text="🚚 Repartidores Activos", font=("Helvetica", 18, "bold"),
             bg=BG_COLOR, fg=HEADER_COLOR).pack(pady=(20, 10))

    filtro_frame = tk.Frame(ventana, bg=BG_COLOR)
    filtro_frame.pack(pady=5)

    tk.Label(filtro_frame, text="Ordenar por:", font=("Helvetica", 12),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(side="left", padx=5)

    opciones = ["Entregas Realizadas", "Pendientes"]
    filtro_spinner = ttk.Combobox(filtro_frame, values=opciones, state="readonly", width=20)
    filtro_spinner.pack(side="left")

    frame_lista = tk.Frame(ventana, bg=BG_COLOR)
    frame_lista.pack(pady=10, fill="both", expand=True)

    def mostrar(lista):
        for widget in frame_lista.winfo_children():
            widget.destroy()

        for r in lista:
            card = tk.Frame(frame_lista, bg=CARD_BG, bd=1, relief="solid")
            card.pack(pady=5, padx=20, fill="x")

            texto = (
                f"👤 {r['nombre']}\nZona: {r['zona']}\nEdad: {r['edad']} años"
                f"\nEntregas: {r['entregas']} | Pendientes: {r['pendientes']}"
                f"\nVehículo: {r['vehiculo']}"
            )
            tk.Label(card, text=texto, font=("Helvetica", 11),
                     bg=CARD_BG, fg=TEXT_COLOR, justify="left").pack(padx=10, pady=10)

    def filtrar(event=None):
        criterio = filtro_spinner.get()
        ordenada = repartidores.copy()

        if criterio == "Entregas Realizadas":
            ordenada.sort(key=lambda x: x["entregas"], reverse=True)
        elif criterio == "Pendientes":
            ordenada.sort(key=lambda x: x["pendientes"], reverse=True)

        mostrar(ordenada)

    filtro_spinner.bind("<<ComboboxSelected>>", filtrar)
    mostrar(repartidores)
