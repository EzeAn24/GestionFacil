import customtkinter as ctk

class PestañaEstadisticas:
    def __init__(self, parent_frame, app):
        self.marco_base = parent_frame
        self.app = app
        self.construir()

    def construir(self):
        marco_top = ctk.CTkFrame(self.marco_base, fg_color="transparent")
        marco_top.pack(pady=10, fill="x", padx=20)
        
        ctk.CTkLabel(marco_top, text="Sección:", font=("Roboto", 14, "bold")).pack(side="left", padx=5)
        self.opt_seccion_stats = ctk.CTkOptionMenu(marco_top, values=["Todas", "General", "Panadería"], width=150, command=lambda e: self.actualizar())
        self.opt_seccion_stats.pack(side="left", padx=5)

        ctk.CTkLabel(marco_top, text="Período:", font=("Roboto", 14, "bold")).pack(side="left", padx=(20, 5))
        self.opt_fechas_stats = ctk.CTkOptionMenu(marco_top, values=["Buscando..."], width=150, command=lambda e: self.actualizar())
        self.opt_fechas_stats.pack(side="left", padx=5)

        marco_kpi = ctk.CTkFrame(self.marco_base, fg_color="transparent")
        marco_kpi.pack(pady=15, fill="x", padx=10)
        
        def crear_tarjeta(padre, titulo, color):
            tarjeta = ctk.CTkFrame(padre, width=220, height=100, corner_radius=10, fg_color=color)
            tarjeta.pack(side="left", padx=10, expand=True, fill="both")
            tarjeta.pack_propagate(False)
            ctk.CTkLabel(tarjeta, text=titulo, font=("Roboto", 14, "bold"), text_color="white").pack(pady=(15,0))
            lbl = ctk.CTkLabel(tarjeta, text="$0.00", font=("Roboto", 24, "bold"), text_color="white")
            lbl.pack(pady=(5,15))
            return lbl

        self.lbl_kpi_ingresos = crear_tarjeta(marco_kpi, "Total Ingresos", "#3498db")
        self.lbl_kpi_ganancia = crear_tarjeta(marco_kpi, "Ganancia Neta", "#2ecc71")
        self.lbl_kpi_efectivo = crear_tarjeta(marco_kpi, "En Efectivo", "#f39c12")
        self.lbl_kpi_mp = crear_tarjeta(marco_kpi, "En Mercado Pago", "#9b59b6")

        ctk.CTkLabel(self.marco_base, text="Desglose de Productos", font=("Roboto", 18, "bold")).pack(pady=(20, 5))
        self.marco_tabla = ctk.CTkScrollableFrame(self.marco_base, width=1000, height=300)
        self.marco_tabla.pack(pady=5, padx=20, fill="both", expand=True)

    def actualizar(self):
        fechas = self.app.db.obtener_fechas_ventas()
        
        if len(fechas) > 1:
            self.opt_fechas_stats.configure(values=fechas)
            fecha_seleccionada = self.opt_fechas_stats.get()
            if fecha_seleccionada not in fechas: 
                fecha_seleccionada = "Global"
                self.opt_fechas_stats.set(fecha_seleccionada)
        else:
            self.opt_fechas_stats.configure(values=["Sin ventas"])
            self.opt_fechas_stats.set("Sin ventas")
            fecha_seleccionada = "VACIO"

        sec_db = self.opt_seccion_stats.get()
        self.cargar_datos(fecha_seleccionada, sec_db)

    def cargar_datos(self, fecha_seleccionada, seccion_seleccionada):
        for w in self.marco_tabla.winfo_children(): w.destroy()
            
        if fecha_seleccionada == "VACIO" or fecha_seleccionada == "Sin ventas":
            self.lbl_kpi_ingresos.configure(text="$0.00"); self.lbl_kpi_ganancia.configure(text="$0.00")
            self.lbl_kpi_efectivo.configure(text="$0.00"); self.lbl_kpi_mp.configure(text="$0.00")
            return

        ingresos, ganancia, efectivo, mp, detalle = self.app.db.obtener_estadisticas(fecha_seleccionada, seccion_seleccionada)

        self.lbl_kpi_ingresos.configure(text=f"${ingresos:,.2f}"); self.lbl_kpi_ganancia.configure(text=f"${ganancia:,.2f}")
        self.lbl_kpi_efectivo.configure(text=f"${efectivo:,.2f}"); self.lbl_kpi_mp.configure(text=f"${mp:,.2f}")

        encabezados = ["Producto", "Cant. Vendida", "Ingreso Generado", "Ganancia Aportada"]
        for c, h in enumerate(encabezados): ctk.CTkLabel(self.marco_tabla, text=h, font=("Roboto", 14, "bold"), width=200).grid(row=0, column=c, pady=10)

        for i, fila in enumerate(detalle, 1):
            nom, tipo_v, cant, monto, gan = fila
            
            cant_flotante = float(cant)
            cant_str = f"{int(cant_flotante)}" if cant_flotante.is_integer() else f"{cant_flotante:.3f}"
            texto_cant = f"{cant_str} Pack(s)" if tipo_v == "Pack" else f"{cant_str} medidas"

            ctk.CTkLabel(self.marco_tabla, text=nom, width=200, anchor="w").grid(row=i, column=0, padx=10)
            ctk.CTkLabel(self.marco_tabla, text=texto_cant, width=200).grid(row=i, column=1)
            ctk.CTkLabel(self.marco_tabla, text=f"${monto:,.2f}", width=200, text_color="#3498db").grid(row=i, column=2)
            ctk.CTkLabel(self.marco_tabla, text=f"${gan:,.2f}", width=200, text_color="#2ecc71").grid(row=i, column=3)