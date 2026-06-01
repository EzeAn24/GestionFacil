import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class PestañaVentas:
    def __init__(self, parent_frame, app):
        self.marco_base = parent_frame
        self.app = app
        self.seccion_activa = "General" 
        self.construir()

    def construir(self):
        marco_top = ctk.CTkFrame(self.marco_base, fg_color="transparent")
        marco_top.pack(pady=5, fill="x", padx=10)
        self.seg_seccion = ctk.CTkSegmentedButton(marco_top, values=["Negocio General", "Panadería"], command=self.cambiar_seccion, font=("Roboto", 14, "bold"))
        self.seg_seccion.pack(pady=5); self.seg_seccion.set("Negocio General")

        self.marco_caja = ctk.CTkFrame(self.marco_base, corner_radius=8, fg_color="#2b2b2b")
        self.marco_caja.pack(pady=5, fill="x", padx=10)
        self.lbl_estado_caja = ctk.CTkLabel(self.marco_caja, text="CAJA CERRADA", font=("Roboto", 16, "bold")); self.lbl_estado_caja.grid(row=0, column=0, padx=20, pady=10)
        self.lbl_datos_caja = ctk.CTkLabel(self.marco_caja, text="", font=("Roboto", 14)); self.lbl_datos_caja.grid(row=0, column=1, padx=20, pady=10)
        self.ent_monto_caja = ctk.CTkEntry(self.marco_caja, placeholder_text="Monto Inicial $", width=120)
        self.btn_caja = ctk.CTkButton(self.marco_caja, text="Abrir Caja", command=self.gestionar_caja, width=120); self.btn_caja.grid(row=0, column=3, padx=10, pady=10)

        self.marco_v = ctk.CTkFrame(self.marco_base, corner_radius=8)
        self.marco_v.pack(pady=10, fill="x", padx=10)
        self.lbl_titulo_venta = ctk.CTkLabel(self.marco_v, text="Nueva Venta - General", font=("Roboto", 16, "bold")); self.lbl_titulo_venta.grid(row=0, column=0, columnspan=7, pady=5)
        
        self.ent_buscar = ctk.CTkEntry(self.marco_v, placeholder_text="🔎 Buscar...", width=130); self.ent_buscar.grid(row=1, column=0, padx=5, pady=10)
        self.ent_buscar.bind("<KeyRelease>", self.filtrar_productos)
        
        self.opt_venta_prod = ctk.CTkOptionMenu(self.marco_v, values=["No hay stock"], width=200, command=self.al_seleccionar_producto)
        self.opt_venta_prod.grid(row=1, column=1, padx=5)
        
        self.opt_tipo_v = ctk.CTkOptionMenu(self.marco_v, values=["Unidad", "Pack"], width=90); self.opt_tipo_v.grid(row=1, column=2, padx=5)
        
        self.opt_modo_v = ctk.CTkOptionMenu(self.marco_v, values=["Por Cant/Peso", "Por Monto ($)"], width=130, command=self.al_cambiar_modo)
        self.opt_modo_v.grid(row=1, column=3, padx=5)
        
        self.ent_cant_v = ctk.CTkEntry(self.marco_v, placeholder_text="Cant.", width=90); self.ent_cant_v.grid(row=1, column=4, padx=5)
        self.opt_pago = ctk.CTkOptionMenu(self.marco_v, values=["Efectivo", "Mercado Pago"], width=120); self.opt_pago.grid(row=1, column=5, padx=5)
        ctk.CTkButton(self.marco_v, text="REGISTRAR", fg_color="#2ecc71", hover_color="#27ae60", font=("Roboto", 14, "bold"), command=self.vender, width=100).grid(row=1, column=6, padx=5)

        marco_hist = ctk.CTkFrame(self.marco_base, fg_color="transparent"); marco_hist.pack(fill="x", padx=10, pady=(10,0))
        self.lbl_historial = ctk.CTkLabel(marco_hist, text="Libro Diario", font=("Roboto", 16, "bold")); self.lbl_historial.pack(side="left")
        self.lbl_resumen_dia = ctk.CTkLabel(marco_hist, text="", font=("Roboto", 14, "bold"), text_color="#f39c12"); self.lbl_resumen_dia.pack(side="left", padx=30)
        self.ent_fecha = ctk.CTkEntry(marco_hist, placeholder_text="DD/MM/AAAA", width=120)
        self.ent_fecha.insert(0, datetime.now().strftime("%d/%m/%Y")); self.ent_fecha.pack(side="right", padx=5)
        ctk.CTkButton(marco_hist, text="Buscar Fecha", width=100, command=self.actualizar_historial).pack(side="right", padx=5)
        
        self.marco_hist_v = ctk.CTkScrollableFrame(self.marco_base, width=1000, height=300); self.marco_hist_v.pack(pady=5, padx=10, fill="both", expand=True)

    def al_cambiar_modo(self, seleccion):
        if seleccion == "Por Monto ($)": self.ent_cant_v.configure(placeholder_text="Monto ($)")
        else: self.al_seleccionar_producto(self.opt_venta_prod.get())

    def cambiar_seccion(self, seleccion):
        self.seccion_activa = "General" if seleccion == "Negocio General" else "Panadería"
        self.lbl_titulo_venta.configure(text=f"Nueva Venta - {self.seccion_activa}")
        self.lbl_historial.configure(text=f"Libro Diario - {self.seccion_activa}")
        self.opt_tipo_v.configure(state="disabled" if self.seccion_activa == "Panadería" else "normal")
        self.actualizar_lista_productos()

    def filtrar_productos(self, event=None):
        texto = self.ent_buscar.get().lower()
        if not self.app.mapa_productos: return
        filtrados = [p for p, info in self.app.mapa_productos.items() if texto in p.lower() and info['seccion'] == self.seccion_activa]
        if filtrados:
            self.opt_venta_prod.configure(values=filtrados); self.opt_venta_prod.set(filtrados[0]); self.al_seleccionar_producto(filtrados[0])
        else:
            self.opt_venta_prod.configure(values=["Sin coincidencias"]); self.opt_venta_prod.set("Sin coincidencias")

    def actualizar_lista_productos(self):
        self.ent_buscar.delete(0, 'end')
        filtrados = [p for p, info in self.app.mapa_productos.items() if info['seccion'] == self.seccion_activa]
        if filtrados:
            self.opt_venta_prod.configure(values=filtrados); self.opt_venta_prod.set(filtrados[0]); self.al_seleccionar_producto(filtrados[0])
        else:
            self.opt_venta_prod.configure(values=["No hay productos cargados"]); self.opt_venta_prod.set("No hay productos cargados")

    def al_seleccionar_producto(self, seleccion):
        if seleccion in ["No hay productos cargados", "Sin coincidencias"]: return
        if self.opt_modo_v.get() == "Por Monto ($)": return
        info = self.app.mapa_productos[seleccion]
        if info['tipo'] == "Kilo": self.ent_cant_v.configure(placeholder_text="Ej: 1.5 (Kilos)")
        elif info['tipo'] == "100 Gramos": self.ent_cant_v.configure(placeholder_text="Ej: 250 (Gramos)")
        else: self.ent_cant_v.configure(placeholder_text="Cantidad (U)")

    def gestionar_caja(self):
        caja = self.app.db.obtener_estado_caja()
        if not caja or caja[2] == 'CERRADA':
            try:
                self.app.db.abrir_caja(float(self.ent_monto_caja.get() or 0))
                self.ent_monto_caja.delete(0, 'end'); messagebox.showinfo("Caja", "Turno Iniciado.")
            except: messagebox.showerror("Error", "Monto inválido.")
        else:
            if messagebox.askyesno("Cerrar Turno", f"¿Confirmas el cierre?\nEfectivo esperado: ${caja[4]:.2f}"):
                self.app.db.cerrar_caja(caja[4], 0); messagebox.showinfo("Caja", "Turno Cerrado.")
        self.app.actualizar_todo()

    def vender(self):
        caja = self.app.db.obtener_estado_caja()
        if not caja or caja[2] == 'CERRADA': messagebox.showwarning("Caja", "Abre el turno primero."); return
        try:
            prod = self.opt_venta_prod.get()
            if prod in ["No hay productos cargados", "Sin coincidencias"]: return
            
            info = self.app.mapa_productos[prod]
            tipo_bd = info['tipo']; tipo_v = self.opt_tipo_v.get() if self.seccion_activa == "General" else tipo_bd
            modo_ingreso = self.opt_modo_v.get()
            valor_ingresado = float(self.ent_cant_v.get())
            pago = self.opt_pago.get()

            # Evitar error por dividir por 0 si el precio quedó en $0
            if modo_ingreso == "Por Monto ($)":
                precio_base = info['precio_u'] if self.seccion_activa == "Panadería" or tipo_v == "Unidad" else info['precio_p']
                if precio_base <= 0:
                    messagebox.showerror("Error", "Este producto tiene un precio de $0, no se puede calcular a la inversa.")
                    return
                
                total = valor_ingresado
                if self.seccion_activa == "Panadería":
                    cant = (total / info['precio_u']) * 100 if tipo_bd == "100 Gramos" else (total / info['precio_u'])
                    ganancia = 0.0
                else: 
                    if tipo_v == "Unidad":
                        cant = total / info['precio_u']; ganancia = cant * (info['precio_u'] - info['costo_u'])
                    else:
                        cant = total / info['precio_p']; ganancia = cant * (info['precio_p'] - (info['costo_u'] * info['u_pack']))
            else:
                cant = valor_ingresado
                if self.seccion_activa == "Panadería":
                    total = (cant / 100) * info['precio_u'] if tipo_bd == "100 Gramos" else cant * info['precio_u']
                    ganancia = 0.0 
                else: 
                    if tipo_v == "Unidad":
                        total = cant * info['precio_u']; ganancia = cant * (info['precio_u'] - info['costo_u'])
                    else:
                        total = cant * info['precio_p']; ganancia = cant * (info['precio_p'] - (info['costo_u'] * info['u_pack']))

            cant = round(cant, 3)

            if info['controla_stock'] == 1:
                cant_desc = cant if tipo_v == "Unidad" else cant * info['u_pack']
                if cant_desc > info['stock']: messagebox.showerror("Error", f"Stock insuficiente. Quedan {info['stock']}."); return

            self.app.db.registrar_venta(caja[0], info['id'], prod, cant, tipo_v, pago, total, ganancia, self.seccion_activa)
            self.ent_cant_v.delete(0, 'end')
            self.ent_fecha.delete(0, 'end'); self.ent_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
            self.app.actualizar_todo()
        except ValueError: messagebox.showerror("Error", "Ingresa un número válido.")

    def actualizar(self):
        caja = self.app.db.obtener_estado_caja()
        if caja and caja[2] == 'ABIERTA':
            self.lbl_estado_caja.configure(text="TURNO ABIERTO", text_color="#2ecc71")
            self.lbl_datos_caja.configure(text=f"Fondo Inicial: ${caja[1]:.2f}  |  Estimado Efectivo: ${caja[4]:.2f}")
            self.ent_monto_caja.grid_forget(); self.btn_caja.configure(text="Cerrar Turno", fg_color="#e74c3c")
        else:
            self.lbl_estado_caja.configure(text="TURNO CERRADO", text_color="#e74c3c")
            self.lbl_datos_caja.configure(text="Abre la caja para comenzar a vender.")
            self.ent_monto_caja.grid(row=0, column=2, padx=10, pady=10); self.btn_caja.configure(text="Abrir Turno", fg_color="#2ecc71")

        self.actualizar_lista_productos(); self.actualizar_historial()

    def actualizar_historial(self):
        for w in self.marco_hist_v.winfo_children(): w.destroy()
        ventas = self.app.db.obtener_ventas(self.ent_fecha.get(), self.seccion_activa)
        
        if not ventas:
            self.lbl_resumen_dia.configure(text="")
            ctk.CTkLabel(self.marco_hist_v, text=f"No hay ventas registradas en {self.seccion_activa}.", font=("Roboto", 14, "italic")).pack(pady=20)
            return
            
        total_monto = 0.0; total_ganancia = 0.0
        for v in ventas:
            nom, cant, fecha, total, pago, gan = v
            total_monto += total; total_ganancia += gan
            color = "#3498db" if pago == "Mercado Pago" else "#2ecc71"
            ren = ctk.CTkFrame(self.marco_hist_v, fg_color="transparent"); ren.pack(fill="x", padx=10, pady=2)
            
            # EL ESCUDO MATEMÁTICO: Convertimos explicitamente a float para no causar errores de 'int' object
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

        if self.seccion_activa == "Panadería":
            a_pagar = total_monto - total_ganancia 
            self.lbl_resumen_dia.configure(text=f"A Pagar a Panadero: ${a_pagar:.2f}")
        else:
            self.lbl_resumen_dia.configure(text="")