import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

COLOR_HEADER = "#005187"
COLOR_TITULO = "#003B5C"
COLOR_FONDO = "#f0f4f8"
COLOR_PANEL = "#ffffff"
COLOR_BORDE = "#d0d9e1"
COLOR_BOTON_ACCION = "#6c757d"

def obtener_taller_id():
    """Lee el archivo de licencia para saber a qué taller pertenece esta PC"""
    try:
        with open("licencia.json", "r") as f:
            datos = json.load(f)
            return datos.get("taller_id")
    except:
        return None

def ventana_corte_caja():
    ventana_corte = tk.Toplevel()
    ventana_corte.title("REPORTE DE VENTAS - SISTEMA")
    ventana_corte.geometry("1000x600")
    ventana_corte.configure(bg=COLOR_FONDO)

    # Titulo superior
    tk.Label(ventana_corte, text="HISTORIAL DE VENTAS Y CORTE", font=("Segoe UI", 16, "bold"), 
             bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=15)
    
    main_frame = tk.Frame(ventana_corte, bg=COLOR_FONDO)
    main_frame.pack(fill="both", expand=True, padx=20, pady=5)
    main_frame.grid_columnconfigure(0, weight=3)
    main_frame.grid_columnconfigure(1, weight=2)

    # Lado Izquierdo: Lista
    col_izq = tk.Frame(main_frame, bg=COLOR_FONDO)
    col_izq.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
    
    tk.Label(col_izq, text="REGISTRO GENERAL", font=("Segoe UI", 10, "bold"), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(anchor="w")
    
    tree_ventas = ttk.Treeview(col_izq, columns=("ID", "Fecha", "Cliente", "Vendedor", "Total"), show="headings")
    for col in ("ID", "Fecha", "Cliente", "Vendedor", "Total"):
        tree_ventas.heading(col, text=col.upper())
        tree_ventas.column(col, anchor="center", width=80)
    tree_ventas.pack(fill="both", expand=True, pady=10)

    # Lado Derecho: Detalles
    col_der = tk.Frame(main_frame, bg=COLOR_PANEL, highlightbackground=COLOR_BORDE, highlightthickness=1)
    col_der.grid(row=0, column=1, sticky="nsew")
    
    tk.Label(col_der, text="DETALLES DE SELECCION", font=("Segoe UI", 10, "bold"), bg=COLOR_PANEL, fg=COLOR_TITULO).pack(pady=10)
    
    tree_detalles = ttk.Treeview(col_der, columns=("Cant", "Desc", "P. Unit", "Subtotal"), show="headings")
    for col in ("Cant", "Desc", "P. Unit", "Subtotal"):
        tree_detalles.heading(col, text=col.upper())
        tree_detalles.column(col, anchor="center", width=70)
    tree_detalles.pack(fill="both", expand=True, padx=10, pady=10)

    # Boton Regresar
    btn_frame = tk.Frame(ventana_corte, bg=COLOR_FONDO)
    btn_frame.pack(fill="x", padx=20, pady=15)
    
    tk.Button(btn_frame, text="REGRESAR AL PANEL PRINCIPAL", font=("Segoe UI", 9, "bold"),
              bg=COLOR_BOTON_ACCION, fg="white", relief="flat", padx=15, pady=8,
              command=ventana_corte.destroy).pack(side="left")

    # --- LÓGICA CONECTADA A LA API ---
    def cargar_datos():
        for i in tree_ventas.get_children(): tree_ventas.delete(i)
        
        mi_taller_id = obtener_taller_id()
        if not mi_taller_id: return
        
        try:
            # Reutilizamos la ruta maestra de historial de ventas
            res = requests.post("http://localhost/api/pos/historial-ventas", json={"taller_id": mi_taller_id})
            if res.status_code == 200:
                for v in res.json().get('ventas', []):
                    tree_ventas.insert("", "end", values=(
                        v['id_venta'], v['fecha'], v['cliente'], v['vendedor'], f"$ {float(v['monto_total']):,.2f}"
                    ))
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "No se pudo conectar con el servidor.")

    def mostrar_detalles_venta(event):
        sel = tree_ventas.selection()
        if not sel: return
        id_venta = tree_ventas.item(sel[0], 'values')[0]
        
        for i in tree_detalles.get_children(): tree_detalles.delete(i)
        
        try:
            # Reutilizamos la ruta de detalles de venta
            res = requests.post("http://localhost/api/pos/detalles-venta", json={"id_venta": id_venta})
            if res.status_code == 200:
                for d in res.json().get('detalles', []):
                    subtotal = d['cantidad'] * d['precio_unitario']
                    tree_detalles.insert("", "end", values=(
                        d['cantidad'], d['descripcion_linea'],
                        f"${d['precio_unitario']:.2f}", f"${subtotal:.2f}"
                    ))
        except: pass

    # Conectamos el clic en la tabla con la función de detalles
    tree_ventas.bind("<<TreeviewSelect>>", mostrar_detalles_venta)
    cargar_datos()