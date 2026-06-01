import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class PestañaVentasPanaderia:
    def __init__(self, parent_frame, app):
        self.marco_base = parent_frame
        self.app = app
        self.construir()

    def construir(self):
        # CAJA
        self.marco_caja = ctk.CTkFrame(self.marco_base, corner_radius=8, fg_color="#2b2b2b")
        self.marco_caja.pack(pady=10, fill="x", padx=10)
        self.lbl_estado_caja = ctk.CTkLabel(self.marco_caja, text="CAJA CERRADA", font=("Roboto", 16, "bold"))
        self.lbl_estado_caja.grid(row=0, column=0, padx=20, pady=10)
        self.lbl_datos_caja = ctk.CTkLabel(self.marco_caja, text="", font=("Roboto", 14))
        self.lbl_datos_caja.grid(row=0, column=1, padx=20, pady=10)
        self.ent_monto_caja = ctk.CTkEntry(self.marco_caja, placeholder_text="Monto Inicial $", width=120)
        self.btn_caja = ctk.CTkButton(self.marco_caja, text="Abrir Caja", command=self.gestionar_caja, width=120)
        self.btn_caja.grid(row=0, column=3, padx=10, pady=10)

        # VENTA
        self.marco_v = ctk.CTkFrame(self.marco_base, corner_radius=8)
        self.marco_v.pack(pady=10, fill="x", padx=10)
        ctk.CTkLabel(self.marco_v, text="Venta - Panadería", font=("Roboto", 16, "bold")).grid(row=0, column=0, columnspan=6, pady=5)
        
        self.ent_buscar = ctk.CTkEntry(self.marco_v, placeholder_text="🔎 Buscar...", width=140)
        self.ent_buscar.grid(row=1, column=0, padx=5, pady=10)
        self.ent_buscar.bind("<KeyRelease>", self.filtrar_productos)
        
        self.opt_venta_prod = ctk.CTkOptionMenu(self.marco_v, values=["No hay productos"], width=230, command=self.al_seleccionar_producto)
        self.opt_venta_prod.grid(row=1, column=1, padx=5)
        
        self.opt_modo_v = ctk.CTkOptionMenu(self.marco_v, values=["Por Cant/Peso", "Por Monto ($)"], width=130, command=self.al_cambiar_modo)
        self.opt_modo_v.grid(row=1, column=2, padx=5)
        
        self.ent_cant_v = ctk.CTkEntry(self.marco_v, placeholder_text="Cant / Peso", width=100)
        self.ent_cant_v.grid(row=1, column=3, padx=5)
        
        self.opt_pago = ctk.CTkOptionMenu(self.marco_v, values=["Efectivo", "Mercado Pago"], width=130)
        self.opt_pago.grid(row=1, column=4, padx=5)
        
        ctk.CTkButton(self.marco_v, text="REGISTRAR", fg_color="#2ecc71", hover_color="#27ae60", font=("Roboto", 14, "bold"), command=self.vender, width=110).grid(row=1, column=5, padx=5)

        # HISTORIAL Y RESUMEN PARA PROVEEDOR
        marco_hist = ctk.CTkFrame(self.marco_base, fg_color="transparent")
        marco_hist.pack(fill="x", padx=10, pady=(10,0))
        ctk.CTkLabel(marco_hist, text="Libro Diario Panadería", font=("Roboto", 16, "bold")).pack(side="left")
        
        self.lbl_resumen_dia = ctk.CTkLabel(marco_hist, text="", font=("Roboto", 14, "bold"), text_color="#f39c12")
        self.lbl_resumen_dia.pack(side="left", padx=30)

        self.ent_fecha = ctk.CTkEntry(marco_hist, placeholder_text="DD/MM/AAAA", width=120)
        self.ent_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.ent_fecha.pack(side="right", padx=5)
        ctk.CTkButton(marco_hist, text="Buscar Fecha", width=100, command=self.actualizar_historial).pack(side="right", padx=5)
        
        self.marco_hist_v = ctk.CTkScrollableFrame(self.marco_base, width=1000, height=300)
        self.marco_hist_v.pack(pady=5, padx=10, fill="both", expand=True)

    def al_cambiar_modo(self, seleccion):
        if seleccion == "Por Monto ($)": 
            self.ent_cant_v.configure(placeholder_text="Monto en pesos ($)")
        else: 
            self.al_seleccionar_producto(self.opt_venta_prod.get())

    def filtrar_productos(self, event=None):
        texto = self.ent_buscar.get().lower()
        if not self.app.mapa_productos: return
        filtrados = [p for p, info in self.app.mapa_productos.items() if texto in p.lower() and info['seccion'] == "Panadería"]
        if filtrados:
            self.opt_venta_prod.configure(values=filtrados)
            self.opt_venta_prod.set(filtrados[0])
            self.al_seleccionar_producto(filtrados[0])
        else:
            self.opt_venta_prod.configure(values=["Sin coincidencias"])
            self.opt_venta_prod.set("Sin coincidencias")

    def actualizar_lista_productos(self):
        self.ent_buscar.delete(0, 'end')
        filtrados = [p for p, info in self.app.mapa_productos.items() if info['seccion'] == "Panadería"]
        if filtrados:
            self.opt_venta_prod.configure(values=filtrados)
            self.opt_venta_prod.set(filtrados[0])
            self.al_seleccionar_producto(filtrados[0])
        else:
            self.opt_venta_prod.configure(values=["No hay productos cargados"])
            self.opt_venta_prod.set("No hay productos cargados")

    def al_seleccionar_producto(self, seleccion):
        if seleccion in ["No hay productos cargados", "Sin coincidencias"]: return
        if self.opt_modo_v.get() == "Por Monto ($)": return
        
        info = self.app.mapa_productos[seleccion]
        if info['tipo'] == "Kilo": 
            self.ent_cant_v.configure(placeholder_text="Ej: 1.5 (Kilos)")
        elif info['tipo'] == "100 Gramos": 
            self.ent_cant_v.configure(placeholder_text="Ej: 250 (Gramos)")
        else: 
            self.ent_cant_v.configure(placeholder_text="Cantidad (U)")

    def gestionar_caja(self):
        caja = self.app.db.obtener_estado_caja()
        if not caja or caja[2] == 'CERRADA':
            try:
                self.app.db.abrir_caja(float(self.ent_monto_caja.get() or 0))
                self.ent_monto_caja.delete(0, 'end')
                messagebox.showinfo("Caja", "Turno Iniciado.")
            except: 
                messagebox.showerror("Error", "Monto inválido.")
        else:
            if messagebox.askyesno("Cerrar Turno", f"¿Confirmas el cierre?\nEfectivo esperado: ${caja[4]:.2f}"):
                self.app.db.cerrar_caja(caja[4], 0)
                messagebox.showinfo("Caja", "Turno Cerrado.")
        self.app.actualizar_todo()

    def vender(self):
        caja = self.app.db.obtener_estado_caja()
        if not caja or caja[2] == 'CERRADA': 
            messagebox.showwarning("Caja", "Abre el turno primero.")
            return
            
        try:
            prod = self.opt_venta_prod.get()
            if prod in ["No hay productos cargados", "Sin coincidencias"]: return
            
            info = self.app.mapa_productos[prod]
            tipo_bd = info['tipo']
            modo_ingreso = self.opt_modo_v.get()
            valor_ingresado = float(self.ent_cant_v.get())
            pago = self.opt_pago.get()

            if modo_ingreso == "Por Monto ($)":
                if info['precio_u'] <= 0:
                    messagebox.showerror("Error", "Precio de producto en 0. No se puede calcular inverso.")
                    return
                total = valor_ingresado
                if tipo_bd == "100 Gramos":
                    cant = (total / info['precio_u']) * 100
                else:
                    cant = total / info['precio_u']
            else:
                cant = valor_ingresado
                if tipo_bd == "100 Gramos":
                    total = (cant / 100) * info['precio_u']
                else:
                    total = cant * info['precio_u']
                    
            ganancia = 0.0 
            cant = round(cant, 3)

            self.app.db.registrar_venta(caja[0], info['id'], prod, cant, "Unidad", pago, total, ganancia, "Panadería")
            self.ent_cant_v.delete(0, 'end')
            self.ent_fecha.delete(0, 'end')
            self.ent_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
            self.app.actualizar_todo()
        except ValueError: 
            messagebox.showerror("Error", "Ingresa un valor numérico válido.")

    def actualizar(self):
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

        self.actualizar_lista_productos()
        self.actualizar_historial()

    def actualizar_historial(self):
        for w in self.marco_hist_v.winfo_children(): w.destroy()
        ventas = self.app.db.obtener_ventas(self.ent_fecha.get(), "Panadería")
        
        if not ventas:
            self.lbl_resumen_dia.configure(text="")
            ctk.CTkLabel(self.marco_hist_v, text="No hay ventas registradas en Panadería.", font=("Roboto", 14, "italic")).pack(pady=20)
            return
            
        total_monto = 0.0
        for v in ventas:
            nom, cant, fecha, total, pago, gan = v
            total_monto += total
            color = "#3498db" if pago == "Mercado Pago" else "#2ecc71"
            ren = ctk.CTkFrame(self.marco_hist_v, fg_color="transparent")
            ren.pack(fill="x", padx=10, pady=2)
            
            cant_flotante = float(cant)
            cant_str = f"{int(cant_flotante)}" if cant_flotante.is_integer() else f"{cant_flotante:.3f}"
            
            medida = "x"
            if nom in self.app.mapa_productos:
                t = self.app.mapa_productos[nom]['tipo']
                if t == "Kilo": medida = "kg de"
                elif t == "100 Gramos": medida = "gr de"
            
            ctk.CTkLabel(ren, text=f"📅 {fecha} | {cant_str} {medida} {nom}", font=("Roboto", 13), width=350, anchor="w").pack(side="left")
            ctk.CTkLabel(ren, text=f"[{pago}]", font=("Roboto", 12, "bold"), text_color=color, width=120, anchor="w").pack(side="left")
            ctk.CTkLabel(ren, text=f"Total: ${total:.2f}", font=("Roboto", 14, "bold"), text_color="#f1c40f").pack(side="right", padx=10)

        # Resumen Proveedor
        self.lbl_resumen_dia.configure(text=f"Total Generado: ${total_monto:.2f} (Restar comisión manual)")