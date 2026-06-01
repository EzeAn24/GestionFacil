import customtkinter as ctk
from database.controlador import ControladorDB
from gui.pestaña_ventas_general import PestañaVentasGeneral
from gui.pestaña_ventas_panaderia import PestañaVentasPanaderia
from gui.pestaña_inventario import PestañaInventario
from gui.pestaña_estadisticas import PestañaEstadisticas

class VentanaPrincipal:
    def __init__(self, ventana, rol="Admin"):
        self.ventana = ventana
        self.rol = rol
        self.ventana.title(f"GestionFacil PRO - Usuario: {self.rol}")
        self.ventana.after(0, lambda: self.ventana.state('zoomed'))
        self.db = ControladorDB()
        self.mapa_productos = {}

        ctk.CTkLabel(self.ventana, text=f"GestionFacil PRO | {self.rol}", font=("Roboto", 28, "bold"), text_color="#1f538d").pack(pady=10)

        self.pestañas = ctk.CTkTabview(self.ventana)
        self.pestañas.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.pestañas.add("Ventas General")
        self.pestañas.add("Ventas Panadería")
        
        self.tab_ventas_gen = PestañaVentasGeneral(self.pestañas.tab("Ventas General"), self)
        self.tab_ventas_pan = PestañaVentasPanaderia(self.pestañas.tab("Ventas Panadería"), self)
        
        if self.rol == "Admin":
            self.pestañas.add("Inventario")
            self.pestañas.add("Estadísticas")
            self.tab_inventario = PestañaInventario(self.pestañas.tab("Inventario"), self)
            self.tab_estadisticas = PestañaEstadisticas(self.pestañas.tab("Estadísticas"), self)
        
        self.actualizar_todo()

    def actualizar_todo(self):
        if self.rol == "Admin":
            self.tab_inventario.actualizar() 
            self.tab_estadisticas.actualizar()
        else:
            prods = self.db.obtener_productos()
            self.mapa_productos.clear()
            for p in prods:
                id_p, nom, tipo, u_pk, cant, stk_m, costo, gan_u, t_p, g_p, seccion, ctrl_stk = p
                c_u = costo if tipo == "Unidad" else (costo / u_pk)
                p_u = c_u * (1 + gan_u / 100); p_p = (c_u * u_pk) * (1 + g_p / 100) if t_p else 0
                self.mapa_productos[nom] = {'id': id_p, 'tipo': tipo, 'costo_u': c_u, 'precio_u': p_u, 'precio_p': p_p, 'u_pack': u_pk, 'stock': cant, 'seccion': seccion, 'controla_stock': ctrl_stk}
                
        self.tab_ventas_gen.actualizar()
        self.tab_ventas_pan.actualizar()