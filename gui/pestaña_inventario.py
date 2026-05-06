import customtkinter as ctk
from tkinter import messagebox

class PestañaInventario:
    def __init__(self, parent_frame, app):
        self.marco_base = parent_frame
        self.app = app
        self.construir()

    def construir(self):
        # --- PANEL ESTRUCTURADO DE CARGA ---
        marco_formulario = ctk.CTkFrame(self.marco_base, corner_radius=10)
        marco_formulario.pack(pady=10, fill="x", padx=10)
        
        ctk.CTkLabel(marco_formulario, text="📥 Nuevo Ingreso de Mercadería", font=("Roboto", 18, "bold")).pack(pady=(10, 5))

        # Contenedor para las 3 columnas
        marco_columnas = ctk.CTkFrame(marco_formulario, fg_color="transparent")
        marco_columnas.pack(fill="x", padx=10, pady=5)

        # COLUMNA 1: Información Básica
        col1 = ctk.CTkFrame(marco_columnas, fg_color="#2b2b2b", corner_radius=8)
        col1.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(col1, text="1. Información Básica", font=("Roboto", 14, "bold"), text_color="#3498db").pack(pady=(10, 5))
        
        self.ent_nombre = ctk.CTkEntry(col1, placeholder_text="Nombre del Producto", height=35)
        self.ent_nombre.pack(pady=5, padx=15, fill="x")
        
        self.opt_tipo = ctk.CTkOptionMenu(col1, values=["Unidad", "Pack"], command=self.al_cambiar_tipo, height=35)
        self.opt_tipo.pack(pady=5, padx=15, fill="x")
        
        self.ent_uni_pack = ctk.CTkEntry(col1, placeholder_text="Unidades por Pack", height=35)
        # Nace oculto

        # COLUMNA 2: Control de Stock
        col2 = ctk.CTkFrame(marco_columnas, fg_color="#2b2b2b", corner_radius=8)
        col2.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(col2, text="2. Control de Stock", font=("Roboto", 14, "bold"), text_color="#e67e22").pack(pady=(10, 5))
        
        self.ent_cant = ctk.CTkEntry(col2, placeholder_text="Cantidad ingresada (Unidades)", height=35)
        self.ent_cant.pack(pady=5, padx=15, fill="x")
        
        self.ent_stk_min = ctk.CTkEntry(col2, placeholder_text="Alerta de Stock Mínimo", height=35)
        self.ent_stk_min.pack(pady=5, padx=15, fill="x")

        # COLUMNA 3: Costos y Rentabilidad
        col3 = ctk.CTkFrame(marco_columnas, fg_color="#2b2b2b", corner_radius=8)
        col3.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(col3, text="3. Finanzas", font=("Roboto", 14, "bold"), text_color="#2ecc71").pack(pady=(10, 5))
        
        self.ent_costo = ctk.CTkEntry(col3, placeholder_text="Costo de la unidad ($)", height=35)
        self.ent_costo.pack(pady=5, padx=15, fill="x")
        
        self.ent_gan_u = ctk.CTkEntry(col3, placeholder_text="Ganancia x Unidad (%)", height=35)
        self.ent_gan_u.pack(pady=5, padx=15, fill="x")
        
        self.var_v_pack = ctk.IntVar(value=0)
        self.chk_v_pack = ctk.CTkCheckBox(col3, text="¿Vende pack cerrado?", variable=self.var_v_pack, command=self.al_cambiar_checkbox)
        self.ent_gan_p = ctk.CTkEntry(col3, placeholder_text="Ganancia x Pack (%)", height=35)

        # BOTÓN GUARDAR (Ocupa todo el ancho abajo de las columnas)
        ctk.CTkButton(marco_formulario, text="GUARDAR INGRESO EN INVENTARIO", font=("Roboto", 14, "bold"), height=40, command=self.guardar_producto_gui).pack(pady=15, padx=15, fill="x")

        # --- TABLA VISUAL DE INVENTARIO ---
        self.marco_inv = ctk.CTkScrollableFrame(self.marco_base, height=350)
        self.marco_inv.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Botón Auditoría (Se agrega al final de construir)
        ctk.CTkButton(marco_formulario, text="👁️ Ver Auditoría de Movimientos", fg_color="#34495e", hover_color="#2c3e50", 
                      font=("Roboto", 14, "bold"), command=self.ver_auditoria).pack(pady=5, padx=15, fill="x")

    # --- LÓGICA DINÁMICA MEJORADA ---
    def al_cambiar_tipo(self, seleccion):
        if seleccion == "Pack":
            self.ent_uni_pack.pack(pady=5, padx=15, fill="x")
            self.chk_v_pack.pack(pady=5, padx=15, anchor="w")
            self.ent_cant.configure(placeholder_text="Packs ingresados físicos")
            self.ent_costo.configure(placeholder_text="Costo del Pack completo ($)")
        else:
            self.ent_uni_pack.pack_forget()
            self.chk_v_pack.pack_forget()
            self.ent_gan_p.pack_forget()
            self.var_v_pack.set(0)
            self.ent_cant.configure(placeholder_text="Cantidad ingresada (Unidades)")
            self.ent_costo.configure(placeholder_text="Costo de la unidad ($)")

    def al_cambiar_checkbox(self):
        if self.var_v_pack.get() == 1: 
            self.ent_gan_p.pack(pady=5, padx=15, fill="x")
        else: 
            self.ent_gan_p.pack_forget()
            self.ent_gan_p.delete(0, 'end')

    def guardar_producto_gui(self):
        try:
            nombre = self.ent_nombre.get(); tipo = self.opt_tipo.get()
            cant_ingresada = int(self.ent_cant.get()); stk_min = int(self.ent_stk_min.get())
            costo = float(self.ent_costo.get()); gan_u = float(self.ent_gan_u.get())
            u_pck = int(self.ent_uni_pack.get()) if tipo == "Pack" else 1
            cant_total = cant_ingresada * u_pck
            v_pack = self.var_v_pack.get(); gan_p = float(self.ent_gan_p.get()) if v_pack == 1 else 0.0
            
            self.app.db.guardar_producto(nombre, tipo, u_pck, cant_total, stk_min, costo, gan_u, v_pack, gan_p)
            
            # Limpiar todos los campos después de guardar
            self.ent_nombre.delete(0, 'end')
            self.ent_cant.delete(0, 'end')
            self.ent_stk_min.delete(0, 'end')
            self.ent_costo.delete(0, 'end')
            self.ent_gan_u.delete(0, 'end')
            self.ent_uni_pack.delete(0, 'end')
            self.ent_gan_p.delete(0, 'end')
            self.opt_tipo.set("Unidad")
            self.al_cambiar_tipo("Unidad")

            self.app.actualizar_todo()
            messagebox.showinfo("Éxito", "Producto guardado y listado en la tabla.")
        except ValueError: 
            messagebox.showerror("Error", "Asegúrate de no dejar campos numéricos vacíos o con letras.")

    def actualizar(self):
        for w in self.marco_inv.winfo_children(): w.destroy()
        
        # Encabezados
        heads = ["Producto", "Pres.", "Stock Físico", "Precios de Venta", "Estado", "Acciones"]
        for c, h in enumerate(heads): 
            ctk.CTkLabel(self.marco_inv, text=h, font=("Roboto", 13, "bold"), width=150).grid(row=0, column=c, pady=10)
        
        prods = self.app.db.obtener_productos()
        self.app.mapa_productos.clear()

        for i, p in enumerate(prods, 1):
            id_p, nom, tipo, u_pk, cant, stk_m, costo, gan_u, t_p, g_p = p
            c_u = costo if tipo == "Unidad" else (costo / u_pk)
            p_u = c_u * (1 + gan_u / 100); p_p = (c_u * u_pk) * (1 + g_p / 100) if t_p else 0
            self.app.mapa_productos[nom] = {'id': id_p, 'costo_u': c_u, 'precio_u': p_u, 'precio_p': p_p, 'u_pack': u_pk, 'stock': cant}
            
            estado = "⚠️ REPONER" if cant <= stk_m else "✅ OK"
            col_est = "#e74c3c" if cant <= stk_m else "#2ecc71"
            
            ctk.CTkLabel(self.marco_inv, text=nom, width=150, anchor="w").grid(row=i, column=0, padx=5)
            ctk.CTkLabel(self.marco_inv, text=f"Pack({u_pk}u)" if tipo=="Pack" else "Unidad", width=100).grid(row=i, column=1)
            ctk.CTkLabel(self.marco_inv, text=f"{cant} u", text_color=col_est, width=100).grid(row=i, column=2)
            ctk.CTkLabel(self.marco_inv, text=f"Uni: ${p_u:.2f} | Pck: ${p_p:.2f}" if tipo=="Pack" and t_p else f"${p_u:.2f} c/u", width=180).grid(row=i, column=3)
            ctk.CTkLabel(self.marco_inv, text=estado, text_color=col_est, width=100).grid(row=i, column=4)
            ctk.CTkButton(self.marco_inv, text="Ajuste ✎", width=100, command=lambda x=p: self.abrir_edicion(x)).grid(row=i, column=5)

    def abrir_edicion(self, p):
        edicion = ctk.CTkToplevel(self.app.ventana); edicion.title("Ajuste de Stock"); edicion.geometry("450x650"); edicion.attributes('-topmost', True)
        ctk.CTkLabel(edicion, text=f"Ajuste: {p[1]}", font=("Roboto", 18, "bold")).pack(pady=10)
        ctk.CTkLabel(edicion, text=f"Stock actual: {p[4]} unidades").pack()
        
        ent_nom = ctk.CTkEntry(edicion, width=250); ent_nom.insert(0, p[1]); ent_nom.pack(pady=10)
        
        # NUEVA LÓGICA DE OPCIONES
        ctk.CTkLabel(edicion, text="Tipo de movimiento:").pack(pady=(10,0))
        opt_tipo = ctk.CTkOptionMenu(edicion, values=["Ingreso de mercadería (+)", "Pérdida / Egreso (-)"], width=250, command=lambda e: al_cambiar_ajuste(e))
        opt_tipo.pack(pady=5)
        
        ent_cant = ctk.CTkEntry(edicion, placeholder_text="Cantidad física", width=150); ent_cant.pack(pady=10)
        
        # Campo dinámico para el costo
        ent_costo_perdida = ctk.CTkEntry(edicion, placeholder_text="Dinero asociado al egreso ($)", width=250)
        
        ent_motivo = ctk.CTkEntry(edicion, placeholder_text="Justificativo (Ej: Vencimiento, Error...)", width=250); ent_motivo.pack(pady=10)

        def al_cambiar_ajuste(seleccion):
            if seleccion == "Pérdida / Egreso (-)":
                ent_costo_perdida.pack(pady=10)
            else:
                ent_costo_perdida.pack_forget()
                ent_costo_perdida.delete(0, 'end')
                
        def confirmar():
            try:
                t = opt_tipo.get(); v = int(ent_cant.get()); stk = p[4]
                costo_asociado = float(ent_costo_perdida.get()) if ent_costo_perdida.get() else 0.0
                
                if t == "Ingreso de mercadería (+)": 
                    n_stk = stk + v; cam = v
                else: 
                    n_stk = stk - v; cam = -v

                self.app.db.registrar_ajuste_stock(p[0], p[1], t, cam, costo_asociado, ent_motivo.get(), n_stk, ent_nom.get())
                edicion.destroy(); self.app.actualizar_todo(); messagebox.showinfo("Éxito", "Inventario ajustado correctamente.")
            except: messagebox.showerror("Error", "Por favor ingresa valores válidos numéricos.")
        
        ctk.CTkButton(edicion, text="Registrar Movimiento", command=confirmar, fg_color="#e67e22").pack(pady=20)

    def ver_auditoria(self):
        audi = ctk.CTkToplevel(self.app.ventana)
        audi.title("Auditoría de Movimientos")
        audi.geometry("800x400")
        audi.attributes('-topmost', True)
        
        ctk.CTkLabel(audi, text="Historial de Ajustes", font=("Roboto", 18, "bold")).pack(pady=10)
        marco = ctk.CTkScrollableFrame(audi, width=750, height=300)
        marco.pack(pady=10, padx=10, fill="both", expand=True)
        
        registros = self.app.db.obtener_auditoria()
        if not registros:
            ctk.CTkLabel(marco, text="No hay registros de auditoría.").pack(pady=20)
            return
            
        for r in registros:
            # r = (nombre, tipo, cant, costo, motivo, fecha)
            texto = f"📅 {r[5]} | {r[0]} | {r[1]}: {r[2]}u | Valor: ${r[3]:.2f} | Motivo: {r[4]}"
            color = "#e74c3c" if "Pérdida" in r[1] else "#2ecc71"
            ctk.CTkLabel(marco, text=texto, text_color=color, anchor="w").pack(fill="x", pady=2, padx=5)