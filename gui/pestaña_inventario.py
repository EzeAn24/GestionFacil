import customtkinter as ctk
from tkinter import messagebox

class PestañaInventario:
    def __init__(self, parent_frame, app):
        self.marco_base = parent_frame
        self.app = app
        self.construir()

    def construir(self):
        marco_formulario = ctk.CTkFrame(self.marco_base, corner_radius=10)
        marco_formulario.pack(pady=10, fill="x", padx=10)
        ctk.CTkLabel(marco_formulario, text="📥 Nuevo Ingreso de Mercadería / Panadería", font=("Roboto", 18, "bold")).pack(pady=(10, 5))

        self.marco_col = ctk.CTkFrame(marco_formulario, fg_color="transparent")
        self.marco_col.pack(fill="x", padx=10, pady=5)
        self.marco_col.grid_columnconfigure((0, 1, 2), weight=1)

        self.col1 = ctk.CTkFrame(self.marco_col, fg_color="#2b2b2b", corner_radius=8)
        self.col1.grid(row=0, column=0, sticky="nsew", padx=5)
        ctk.CTkLabel(self.col1, text="1. Clasificación", font=("Roboto", 14, "bold"), text_color="#3498db").pack(pady=(10, 5))
        
        self.ent_nombre = ctk.CTkEntry(self.col1, placeholder_text="Nombre del Producto", height=35)
        self.ent_nombre.pack(pady=5, padx=15, fill="x")
        self.opt_seccion = ctk.CTkOptionMenu(self.col1, values=["General", "Panadería"], height=35, command=self.al_cambiar_seccion)
        self.opt_seccion.pack(pady=5, padx=15, fill="x")
        self.opt_tipo = ctk.CTkOptionMenu(self.col1, values=["Unidad", "Pack"], command=self.al_cambiar_tipo, height=35)
        self.opt_tipo.pack(pady=5, padx=15, fill="x")
        self.ent_uni_pack = ctk.CTkEntry(self.col1, placeholder_text="Unidades por Pack", height=35)

        self.col2 = ctk.CTkFrame(self.marco_col, fg_color="#2b2b2b", corner_radius=8)
        self.col2.grid(row=0, column=1, sticky="nsew", padx=5)
        ctk.CTkLabel(self.col2, text="2. Control de Stock", font=("Roboto", 14, "bold"), text_color="#e67e22").pack(pady=(10, 5))
        
        self.ent_cant = ctk.CTkEntry(self.col2, placeholder_text="Cantidad física ingresada", height=35)
        self.ent_cant.pack(pady=5, padx=15, fill="x")
        self.ent_stk_min = ctk.CTkEntry(self.col2, placeholder_text="Alerta de Stock Mínimo", height=35)
        self.ent_stk_min.pack(pady=5, padx=15, fill="x")

        self.col3 = ctk.CTkFrame(self.marco_col, fg_color="#2b2b2b", corner_radius=8)
        self.col3.grid(row=0, column=2, sticky="nsew", padx=5)
        self.lbl_col3 = ctk.CTkLabel(self.col3, text="3. Finanzas", font=("Roboto", 14, "bold"), text_color="#2ecc71")
        self.lbl_col3.pack(pady=(10, 5))
        
        self.ent_costo = ctk.CTkEntry(self.col3, placeholder_text="Costo ($)", height=35)
        self.ent_costo.pack(pady=5, padx=15, fill="x")
        self.ent_gan_u = ctk.CTkEntry(self.col3, placeholder_text="Tu Ganancia (%)", height=35)
        self.ent_gan_u.pack(pady=5, padx=15, fill="x")
        self.var_v_pack = ctk.IntVar(value=0)
        self.chk_v_pack = ctk.CTkCheckBox(self.col3, text="¿Vende pack cerrado?", variable=self.var_v_pack, command=self.al_cambiar_checkbox)
        self.ent_gan_p = ctk.CTkEntry(self.col3, placeholder_text="Ganancia x Pack (%)", height=35)

        ctk.CTkButton(marco_formulario, text="GUARDAR EN INVENTARIO", font=("Roboto", 14, "bold"), height=40, command=self.guardar_producto_gui).pack(pady=(15, 5), padx=15, fill="x")
        ctk.CTkButton(marco_formulario, text="👁️ Ver Auditoría de Movimientos", fg_color="#34495e", hover_color="#2c3e50", font=("Roboto", 14, "bold"), height=35, command=self.ver_auditoria).pack(pady=(5, 15), padx=15, fill="x")

        self.marco_inv = ctk.CTkScrollableFrame(self.marco_base, height=350)
        self.marco_inv.pack(pady=5, padx=10, fill="both", expand=True)

    def al_cambiar_tipo(self, seleccion):
        if seleccion == "Pack":
            self.ent_uni_pack.pack(pady=5, padx=15, fill="x"); self.chk_v_pack.pack(pady=5, padx=15, anchor="w")
        else:
            self.ent_uni_pack.pack_forget(); self.chk_v_pack.pack_forget()
            self.ent_gan_p.pack_forget(); self.var_v_pack.set(0)

    def al_cambiar_checkbox(self):
        if self.var_v_pack.get() == 1: self.ent_gan_p.pack(pady=5, padx=15, fill="x")
        else: self.ent_gan_p.pack_forget(); self.ent_gan_p.delete(0, 'end')

    def al_cambiar_seccion(self, seleccion):
        if seleccion == "Panadería":
            self.opt_tipo.configure(values=["Unidad", "Kilo", "100 Gramos"]); self.opt_tipo.set("Unidad"); self.al_cambiar_tipo("Unidad") 
            self.col2.grid_forget()
            self.lbl_col3.configure(text="2. Precio de Venta"); self.ent_costo.configure(placeholder_text="Precio de Venta al Público ($)")
            self.ent_gan_u.pack_forget(); self.chk_v_pack.pack_forget()
        else:
            self.opt_tipo.configure(values=["Unidad", "Pack"]); self.opt_tipo.set("Unidad")
            self.col2.grid(row=0, column=1, sticky="nsew", padx=5)
            self.lbl_col3.configure(text="3. Finanzas"); self.ent_costo.configure(placeholder_text="Costo ($)")
            self.ent_gan_u.pack(pady=5, padx=15, fill="x")
            self.ent_cant.delete(0, 'end'); self.ent_stk_min.delete(0, 'end')

    def guardar_producto_gui(self):
        try:
            nombre = self.ent_nombre.get(); tipo = self.opt_tipo.get(); seccion = self.opt_seccion.get()
            if seccion == "Panadería":
                costo = float(self.ent_costo.get())
                gan_u = 0.0; u_pck = 1; v_pack = 0; gan_p = 0.0; cant_total = 0.0; stk_min = 0; controla_stock = 0
            else:
                costo = float(self.ent_costo.get()); gan_u = float(self.ent_gan_u.get())
                u_pck = int(self.ent_uni_pack.get()) if tipo == "Pack" else 1
                v_pack = self.var_v_pack.get(); gan_p = float(self.ent_gan_p.get()) if v_pack == 1 else 0.0
                cant_total = float(self.ent_cant.get()) * u_pck; stk_min = int(self.ent_stk_min.get()); controla_stock = 1
            
            self.app.db.guardar_producto(nombre, tipo, u_pck, cant_total, stk_min, costo, gan_u, v_pack, gan_p, seccion, controla_stock)
            
            self.ent_nombre.delete(0, 'end'); self.ent_costo.delete(0, 'end'); self.ent_gan_u.delete(0, 'end')
            self.ent_uni_pack.delete(0, 'end'); self.ent_gan_p.delete(0, 'end'); self.ent_cant.delete(0, 'end'); self.ent_stk_min.delete(0, 'end')
            self.opt_seccion.set("General"); self.al_cambiar_seccion("General")
            
            self.app.actualizar_todo(); messagebox.showinfo("Éxito", "Cargado correctamente.")
        except ValueError: messagebox.showerror("Error", "Campos numéricos incorrectos.")

    def actualizar(self):
        for w in self.marco_inv.winfo_children(): w.destroy()
        heads = ["Sección", "Producto", "Stock / Medida", "Precios de Venta", "Estado", "Acciones"]
        for c, h in enumerate(heads): ctk.CTkLabel(self.marco_inv, text=h, font=("Roboto", 13, "bold"), width=130).grid(row=0, column=c, pady=10)
        
        prods = self.app.db.obtener_productos(); self.app.mapa_productos.clear()

        for i, p in enumerate(prods, 1):
            id_p, nom, tipo, u_pk, cant, stk_m, costo, gan_u, t_p, g_p, seccion, ctrl_stk = p
            if seccion == "Panadería":
                p_u = costo; p_p = 0; c_u = costo
            else:
                c_u = costo if tipo == "Unidad" else (costo / u_pk)
                p_u = c_u * (1 + gan_u / 100)
                p_p = (c_u * u_pk) * (1 + g_p / 100) if t_p else 0
            
            self.app.mapa_productos[nom] = {'id': id_p, 'tipo': tipo, 'costo_u': c_u, 'precio_u': p_u, 'precio_p': p_p, 'u_pack': u_pk, 'stock': cant, 'seccion': seccion, 'controla_stock': ctrl_stk}
            estado = "Libre" if ctrl_stk == 0 else ("⚠️ REPONER" if cant <= stk_m else "✅ OK")
            col_est = "#3498db" if ctrl_stk == 0 else ("#e74c3c" if cant <= stk_m else "#2ecc71")
            
            # ESCUDO MATEMÁTICO AQUÍ TAMBIÉN
            cant_flotante = float(cant)
            texto_stock = f"Venta x {tipo}" if ctrl_stk == 0 else (f"{int(cant_flotante)} u" if cant_flotante.is_integer() else f"{cant_flotante:.3f} u")
            texto_precio = f"U: ${p_u:.2f} | P: ${p_p:.2f}" if tipo=="Pack" and t_p else f"${p_u:.2f} x {tipo}"
            
            ctk.CTkLabel(self.marco_inv, text=seccion, width=130, anchor="w", text_color="#f39c12").grid(row=i, column=0, padx=5)
            ctk.CTkLabel(self.marco_inv, text=nom, width=130, anchor="w").grid(row=i, column=1, padx=5)
            ctk.CTkLabel(self.marco_inv, text=texto_stock, text_color=col_est, width=130).grid(row=i, column=2, padx=5)
            ctk.CTkLabel(self.marco_inv, text=texto_precio, width=180).grid(row=i, column=3, padx=5)
            ctk.CTkLabel(self.marco_inv, text=estado, text_color=col_est, width=130).grid(row=i, column=4, padx=5)
            ctk.CTkButton(self.marco_inv, text="Ajuste ✎", width=100, command=lambda x=p: self.abrir_edicion(x)).grid(row=i, column=5)

    def abrir_edicion(self, p):
        id_prod, nom_act, tipo_p, u_pack, stk_act, stk_min, cos_act, g_u_act, t_p, g_p_act, seccion, ctrl_stk = p
        ed = ctk.CTkToplevel(self.app.ventana); ed.title("Ajuste"); ed.geometry("500x750"); ed.attributes('-topmost', True)
        ctk.CTkLabel(ed, text=f"Editando: {nom_act}", font=("Roboto", 18, "bold"), text_color="#3498db").pack(pady=10)
        
        m_fin = ctk.CTkFrame(ed, corner_radius=8); m_fin.pack(pady=5, padx=20, fill="x")
        
        if seccion == "Panadería":
            ctk.CTkLabel(m_fin, text="1. Actualizar Precio de Venta", font=("Roboto", 14, "bold")).pack(pady=5)
            e_nom = ctk.CTkEntry(m_fin, width=300); e_nom.insert(0, nom_act); e_nom.pack(pady=5)
            e_cos = ctk.CTkEntry(m_fin, width=300, placeholder_text="Nuevo Precio ($)"); e_cos.insert(0, str(cos_act)); e_cos.pack(pady=5)
            def conf_pan():
                try:
                    self.app.db.registrar_ajuste_stock(id_prod, nom_act, "Sin movimiento", 0, 0, "Actualización precio", 0, e_nom.get(), float(e_cos.get()), 0.0, 0.0)
                    ed.destroy(); self.app.actualizar_todo(); messagebox.showinfo("Éxito", "Actualizado.")
                except: messagebox.showerror("Error", "Valor inválido.")
            ctk.CTkButton(ed, text="GUARDAR PRECIO", command=conf_pan, fg_color="#e67e22").pack(pady=30)
            return

        ctk.CTkLabel(m_fin, text="1. Actualizar Costos y Precios", font=("Roboto", 14, "bold")).pack(pady=5)
        e_nom = ctk.CTkEntry(m_fin, width=300); e_nom.insert(0, nom_act); e_nom.pack(pady=5)
        e_cos = ctk.CTkEntry(m_fin, width=300, placeholder_text="Nuevo Costo ($)"); e_cos.insert(0, str(cos_act)); e_cos.pack(pady=5)
        e_g_u = ctk.CTkEntry(m_fin, width=300, placeholder_text="Tu Ganancia (%)"); e_g_u.insert(0, str(g_u_act)); e_g_u.pack(pady=5)
        e_g_p = ctk.CTkEntry(m_fin, width=300, placeholder_text="Ganancia Pack (%)")
        if t_p == 1: e_g_p.insert(0, str(g_p_act)); e_g_p.pack(pady=5)

        m_stk = ctk.CTkFrame(ed, corner_radius=8); m_stk.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(m_stk, text="2. Movimiento Físico", font=("Roboto", 14, "bold")).pack(pady=5)
        ctk.CTkLabel(m_stk, text=f"Stock actual: {stk_act} u").pack(pady=(0, 10))
        
        opt_t = ctk.CTkOptionMenu(m_stk, values=["Sin movimiento", "Ingreso (+)", "Pérdida / Egreso (-)"], width=300, command=lambda e: camb(e))
        opt_t.set("Sin movimiento"); opt_t.pack(pady=5)
        opt_f = ctk.CTkOptionMenu(m_stk, values=["Packs Cerrados", "Unidades Sueltas"], width=300)
        e_can = ctk.CTkEntry(m_stk, placeholder_text="Cantidad", width=300)
        e_per = ctk.CTkEntry(m_stk, placeholder_text="Dinero asociado a pérdida ($)", width=300)
        e_mot = ctk.CTkEntry(m_stk, placeholder_text="Justificativo obligatorio", width=300)

        def camb(sel):
            if sel == "Sin movimiento": opt_f.pack_forget(); e_can.pack_forget(); e_per.pack_forget(); e_mot.pack_forget()
            elif sel == "Ingreso (+)":
                if tipo_p == "Pack": opt_f.pack(pady=5)
                e_can.pack(pady=5); e_per.pack_forget(); e_mot.pack(pady=5)
            else: opt_f.pack_forget(); e_can.pack(pady=5); e_per.pack(pady=5); e_mot.pack(pady=5)
                
        def conf_c():
            try:
                t = opt_t.get(); n_nom = e_nom.get(); n_cos = float(e_cos.get())
                n_g_u = float(e_g_u.get()); n_g_p = float(e_g_p.get()) if e_g_p.winfo_ismapped() else 0.0
                if t == "Sin movimiento": cam=0; n_s=stk_act; c_a=0.0; m="Ajuste"
                else:
                    v = float(e_can.get() or 0); m = e_mot.get()
                    if t == "Ingreso (+)":
                        cam = v * u_pack if tipo_p == "Pack" and opt_f.get() == "Packs Cerrados" else v
                        n_s = stk_act + cam; c_a = 0.0
                    else: cam = -v; n_s = stk_act - v; c_a = float(e_per.get() or 0.0)
                self.app.db.registrar_ajuste_stock(id_prod, nom_act, t, cam, c_a, m, n_s, n_nom, n_cos, n_g_u, n_g_p)
                ed.destroy(); self.app.actualizar_todo()
            except: messagebox.showerror("Error", "Valores numéricos inválidos.")
        ctk.CTkButton(ed, text="GUARDAR CAMBIOS", command=conf_c, fg_color="#e67e22").pack(pady=20)

    def ver_auditoria(self):
        audi = ctk.CTkToplevel(self.app.ventana); audi.title("Auditoría"); audi.geometry("800x400"); audi.attributes('-topmost', True)
        ctk.CTkLabel(audi, text="Historial de Ajustes", font=("Roboto", 18, "bold")).pack(pady=10)
        m = ctk.CTkScrollableFrame(audi, width=750, height=300); m.pack(pady=10, padx=10, fill="both", expand=True)
        reg = self.app.db.obtener_auditoria()
        if not reg: return
        for r in reg:
            t = f"📅 {r[5]} | {r[0]} | {r[1]}: {r[2]}u | Valor: ${r[3]:.2f} | Motivo: {r[4]}"
            ctk.CTkLabel(m, text=t, text_color="#e74c3c" if "Pérdida" in r[1] else "#2ecc71", anchor="w").pack(fill="x", pady=2, padx=5)