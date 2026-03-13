import tkinter as tk
from datetime import datetime

# 🎨 Colores base
BG_COLOR = "#F5F5F5"
HEADER_COLOR = "#005187"
TEXT_COLOR = "#212121"
CARD_BG = "#fcffff"
PROVEEDOR_COLOR = "#e0f7fa"
ADMIN_COLOR = "#d1c4e9"

mensajes = [
    {"usuario": "Proveedor", "texto": "Hola, ¿en qué puedo ayudarte?", "hora": "10:45"},
    {"usuario": "Admin", "texto": "Necesito una pantalla OLED para un Galaxy S21", "hora": "10:46"},
    {"usuario": "Proveedor", "texto": "Sí tengo en existencia, ¿cantidad?", "hora": "10:47"}
]

def ventana_realizar_pedido():
    ventana = tk.Toplevel()
    ventana.title("Chat con Proveedor")
    ventana.geometry("420x520")
    ventana.configure(bg=BG_COLOR)

    tk.Label(ventana, text="💬 Realizar Pedido", font=("Helvetica", 18, "bold"),
             bg=BG_COLOR, fg=HEADER_COLOR).pack(pady=(20, 10))

    chat_frame = tk.Frame(ventana, bg=BG_COLOR)
    chat_frame.pack(fill="both", expand=True, padx=10)

    canvas = tk.Canvas(chat_frame, bg=BG_COLOR)
    scrollbar = tk.Scrollbar(chat_frame, command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=BG_COLOR)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def render_mensajes():
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        for msg in mensajes:
            bubble_bg = PROVEEDOR_COLOR if msg["usuario"] == "Proveedor" else ADMIN_COLOR
            anchor = "w" if msg["usuario"] == "Proveedor" else "e"

            mensaje_frame = tk.Frame(scroll_frame, bg=BG_COLOR)
            mensaje_frame.pack(fill="x", padx=10, pady=2, anchor=anchor)

            contenido = f"{msg['usuario']} ({msg['hora']}):\n{msg['texto']}"
            tk.Label(mensaje_frame, text=contenido, bg=bubble_bg,
                     font=("Helvetica", 10), fg=TEXT_COLOR,
                     justify="left", wraplength=300,
                     padx=10, pady=5).pack(anchor=anchor)

    # 📨 Enviar mensaje
    entry_frame = tk.Frame(ventana, bg=BG_COLOR)
    entry_frame.pack(fill="x", padx=10, pady=5)

    entry_msg = tk.Entry(entry_frame, font=("Helvetica", 12), width=30)
    entry_msg.pack(side="left", padx=(0, 5))

    def enviar_mensaje():
        texto = entry_msg.get()
        if texto.strip():
            hora_actual = datetime.now().strftime("%H:%M")
            mensajes.append({"usuario": "Admin", "texto": texto, "hora": hora_actual})
            entry_msg.delete(0, tk.END)
            render_mensajes()
            canvas.yview_moveto(1)

    tk.Button(entry_frame, text="Enviar", bg=HEADER_COLOR, fg="white",
              font=("Helvetica", 10), command=enviar_mensaje).pack(side="right")

    render_mensajes()
