import tkinter as tk
from tkinter import ttk

# 🎨 Colores base
BG_COLOR = "#F5F5F5"
HEADER_COLOR = "#005187"
TEXT_COLOR = "#212121"
CARD_BG = "#fcffff"

# 📦 Datos ficticios (original sin ordenar)
original_pedidos = [
    {"nombre": "Pantalla OLED", "descripcion": "Samsung Galaxy S21", "precio": 1200, "fecha": "2025-07-15"},
    {"nombre": "Batería 5000mAh", "descripcion": "Xiaomi Redmi Note", "precio": 650, "fecha": "2025-07-12"},
    {"nombre": "Cámara frontal", "descripcion": "iPhone 12", "precio": 800, "fecha": "2025-07-18"},
    {"nombre": "Puerto de carga", "descripcion": "Motorola G Power", "precio": 300, "fecha": "2025-07-20"},
    {"nombre": "Cristal templado", "descripcion": "Lenovo Tab M10", "precio": 150, "fecha": "2025-07-11"},
]

def ventana_pedidos():
    ventana = tk.Toplevel()
    ventana.title("Pedidos")
    ventana.geometry("420x520")
    ventana.configure(bg=BG_COLOR)

    tk.Label(ventana, text="📦 Pedidos", font=("Helvetica", 18, "bold"),
             bg=BG_COLOR, fg=HEADER_COLOR).pack(pady=(20, 10))

    # 🎛️ Filtro
    filtro_frame = tk.Frame(ventana, bg=BG_COLOR)
    filtro_frame.pack(pady=5)

    tk.Label(filtro_frame, text="Filtrar por:", font=("Helvetica", 12),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(side="left", padx=5)

    opciones_filtro = ["Precio", "Fecha de Entrega"]
    filtro_spinner = ttk.Combobox(filtro_frame, values=opciones_filtro, state="readonly", width=20)
    filtro_spinner.pack(side="left")

    # 📋 Contenedor de pedidos
    pedidos_frame = tk.Frame(ventana, bg=BG_COLOR)
    pedidos_frame.pack(pady=10, fill="both", expand=True)

    # Función para mostrar los pedidos en pantalla
    def mostrar_pedidos(pedidos):
        # Limpiar el frame antes de re-renderizar
        for widget in pedidos_frame.winfo_children():
            widget.destroy()

        for pedido in pedidos:
            card = tk.Frame(pedidos_frame, bg=CARD_BG, bd=1, relief="solid")
            card.pack(pady=5, padx=20, fill="x")

            texto = (
                f"{pedido['nombre']}\n{pedido['descripcion']}"
                f"\nPrecio: ${pedido['precio']}\nEntrega: {pedido['fecha']}"
            )
            tk.Label(card, text=texto, font=("Helvetica", 11),
                     bg=CARD_BG, fg=TEXT_COLOR, justify="left").pack(padx=10, pady=10)

    # 🧠 Filtrado dinámico
    def filtrar_pedidos(event=None):
        criterio = filtro_spinner.get()
        pedidos_ordenados = original_pedidos.copy()

        if criterio == "Precio":
            pedidos_ordenados.sort(key=lambda x: x["precio"])
        elif criterio == "Fecha de Entrega":
            pedidos_ordenados.sort(key=lambda x: x["fecha"])

        mostrar_pedidos(pedidos_ordenados)

    filtro_spinner.bind("<<ComboboxSelected>>", filtrar_pedidos)

    # Mostrar por defecto
    mostrar_pedidos(original_pedidos)
