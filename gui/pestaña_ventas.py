import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class PestañaVentas:
    def __init__(self, parent_frame, app):
        self.marco_base = parent_frame
        self.app = app # Referencia a la VentanaPrincipal (para usar la BD y el mapa)
        self.construir()

    def construir(self):
        # CAJA
        self.marco_caja = ctk.CTkFrame(self.marco_base, corner_radius=8, fg_color="#2b2b2b")
        self.marco_caja.pack(pady=5, fill="x", padx=10)
        self.lbl_estado_caja = ctk.CTkLabel(self.marco_caja, text="CAJA CERRADA", font=("Roboto", 16, "bold"))
        self.lbl_estado_caja.grid(row=0, column=0, padx=20, pady=10)
        self.lbl_datos_caja = ctk.CTkLabel(self.marco_caja, text="", font=("Roboto", 14))
        self.lbl_datos_caja.grid(row=0, column=1, padx=20, pady=10)
        self.ent_monto_caja = ctk.CTkEntry(self.marco_caja, placeholder_text="Monto Inicial $", width=120)
        self.btn_caja = ctk.CTkButton(self.marco_caja, text="Abrir Caja", command=self.gestionar_caja, width=120)
        self.btn_caja.grid(row=0, column=3, padx=10, pady=10)

        # VENTA
        marco_v = ctk.CTkFrame(self.marco_base, corner_radius=8)
        marco_v.pack(pady=10, fill="x", padx=10)
        ctk.CTkLabel(marco_v, text="Nueva Venta", font=("Roboto", 16, "bold")).grid(row=0, column=0, columnspan=6, pady=5)
        self.ent_buscar = ctk.CTkEntry(marco_v, placeholder_text="🔎 Buscar...", width=140)
        self.ent_buscar.grid(row=1, column=0, padx=5, pady=10)
        self.ent_buscar.bind("<KeyRelease>", self.filtrar_productos)
        self.opt_venta_prod = ctk.CTkOptionMenu(marco_v, values=["No hay stock"], width=230)
        self.opt_venta_prod.grid(row=1, column=1, padx=5)
        self.opt_tipo_v = ctk.CTkOptionMenu(marco_v, values=["Unidad", "Pack"], width=90)
        self.opt_tipo_v.grid(row=1, column=2, padx=5)
        self.ent_cant_v = ctk.CTkEntry(marco_v, placeholder_text="Cant.", width=60)
        self.ent_cant_v.grid(row=1, column=3, padx=5)
        self.opt_pago = ctk.CTkOptionMenu(marco_v, values=["Efectivo", "Mercado Pago"], width=130)
        self.opt_pago.grid(row=1, column=4, padx=5)
        ctk.CTkButton(marco_v, text="REGISTRAR", fg_color="#2ecc71", hover_color="#27ae60", font=("Roboto", 14, "bold"), command=self.vender, width=110).grid(row=1, column=5, padx=5)

        # HISTORIAL
        marco_hist = ctk.CTkFrame(self.marco_base, fg_color="transparent")
        marco_hist.pack(fill="x", padx=10, pady=(10,0))
        ctk.CTkLabel(marco_hist, text="Historial de Ventas", font=("Roboto", 16, "bold")).pack(side="left")
        self.ent_fecha = ctk.CTkEntry(marco_hist, placeholder_text="DD/MM/AAAA", width=120)
        self.ent_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.ent_fecha.pack(side="right", padx=5)
        ctk.CTkButton(marco_hist, text="Buscar Fecha", width=100, command=self.actualizar_historial).pack(side="right", padx=5)
        self.marco_hist_v = ctk.CTkScrollableFrame(self.marco_base, width=1000, height=350)
        self.marco_hist_v.pack(pady=5, padx=10, fill="both", expand=True)

    def filtrar_productos(self, event=None):
        texto = self.ent_buscar.get().lower()
        if not self.app.mapa_productos: return
        filtrados = [p for p in self.app.mapa_productos.keys() if texto in p.lower()]
        if filtrados:
            self.opt_venta_prod.configure(values=filtrados); self.opt_venta_prod.set(filtrados[0])
        else:
            self.opt_venta_prod.configure(values=["Sin coincidencias"]); self.opt_venta_prod.set("Sin coincidencias")

    def gestionar_caja(self):
        caja = self.app.db.obtener_estado_caja()
        if not caja or caja[2] == 'CERRADA':
            try:
                monto = float(self.ent_monto_caja.get() or 0)
                self.app.db.abrir_caja(monto)
                self.ent_monto_caja.delete(0, 'end')
                messagebox.showinfo("Caja", "Turno Iniciado.")
            except: messagebox.showerror("Error", "Monto inválido.")
        else:
            if messagebox.askyesno("Cerrar Turno", f"¿Confirmas el cierre?\nEfectivo esperado: ${caja[4]:.2f}"):
                self.app.db.cerrar_caja(caja[4], 0)
                messagebox.showinfo("Caja", "Turno Cerrado.")
        self.app.actualizar_todo()

    def vender(self):
        caja = self.app.db.obtener_estado_caja()
        if not caja or caja[2] == 'CERRADA':
            messagebox.showwarning("Caja", "Abre el turno primero."); return
        try:
            prod = self.opt_venta_prod.get()
            if prod in ["No hay stock", "Sin coincidencias"]: return
            info = self.app.mapa_productos[prod]
            tipo_v = self.opt_tipo_v.get(); cant = int(self.ent_cant_v.get()); pago = self.opt_pago.get()

            # --- CORRECCIÓN DE BUG: Validar si tiene pack ---
            if tipo_v == "Pack" and info['precio_p'] == 0:
                messagebox.showerror("Error de Venta", f"El producto '{prod}' no se vende por pack cerrado.")
                return

            cant_desc = cant if tipo_v == "Unidad" else cant * info['u_pack']
            if cant_desc > info['stock']:
                messagebox.showerror("Error", f"Stock insuficiente. Quedan {info['stock']} unidades físicas.")
                return

            if tipo_v == "Unidad":
                total = cant * info['precio_u']; ganancia = cant * (info['precio_u'] - info['costo_u'])
            else:
                total = cant * info['precio_p']; ganancia = cant * (info['precio_p'] - (info['costo_u'] * info['u_pack']))

            self.app.db.registrar_venta(caja[0], info['id'], prod, cant, tipo_v, pago, total, ganancia)
            self.ent_cant_v.delete(0, 'end')
            from datetime import datetime
            self.ent_fecha.delete(0, 'end'); self.ent_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
            self.app.actualizar_todo()
        except Exception as e: messagebox.showerror("Error", "Verifica los datos ingresados.")

    def actualizar(self):
        # Actualizar vista de Caja
        caja = self.app.db.obtener_estado_caja()
        if caja and caja[2] == 'ABIERTA':
            self.lbl_estado_caja.configure(text="TURNO ABIERTO", text_color="#2ecc71")
            self.lbl_datos_caja.configure(text=f"Fondo Inicial: ${caja[1]:.2f}  |  Estimado Efectivo: ${caja[4]:.2f}")
            self.ent_monto_caja.grid_forget()
            self.btn_caja.configure(text="Cerrar Turno", fg_color="#e74c3c")
        else:
            self.lbl_estado_caja.configure(text="TURNO CERRADO", text_color="#e74c3c")
            self.lbl_datos_caja.configure(text="Abre la caja para comenzar a vender.")
            self.ent_monto_caja.grid(row=0, column=2, padx=10, pady=10)
            self.btn_caja.configure(text="Abrir Turno", fg_color="#2ecc71")

        # Actualizar menú de productos
        prods = list(self.app.mapa_productos.keys())
        self.opt_venta_prod.configure(values=prods if prods else ["No hay stock"])
        self.actualizar_historial()

    def actualizar_historial(self):
        for w in self.marco_hist_v.winfo_children(): w.destroy()
        ventas = self.app.db.obtener_ventas(self.ent_fecha.get())
        if not ventas:
            ctk.CTkLabel(self.marco_hist_v, text="No hay ventas.", font=("Roboto", 14, "italic")).pack(pady=20)
            return
        for v in ventas:
            nom, cant, fecha, total, pago = v
            color = "#3498db" if pago == "Mercado Pago" else "#2ecc71"
            ren = ctk.CTkFrame(self.marco_hist_v, fg_color="transparent")
            ren.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(ren, text=f"📅 {fecha} | {cant}x {nom}", font=("Roboto", 13), width=350, anchor="w").pack(side="left")
            ctk.CTkLabel(ren, text=f"[{pago}]", font=("Roboto", 12, "bold"), text_color=color, width=120, anchor="w").pack(side="left")
            ctk.CTkLabel(ren, text=f"Total: ${total:.2f}", font=("Roboto", 14, "bold"), text_color="#f1c40f").pack(side="right", padx=10)