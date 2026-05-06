import sqlite3
from datetime import datetime

class ControladorDB:
    def __init__(self, nombre_bd="gestion_facil.db"):
        self.nombre_bd = nombre_bd
        self.crear_tablas()

    def conectar(self):
        return sqlite3.connect(self.nombre_bd)

    def crear_tablas(self):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, tipo TEXT, unidades_pack INTEGER,
            cantidad_unidades INTEGER, stock_minimo INTEGER, costo_ingresado REAL, ganancia_unidad REAL,
            tiene_ganancia_pack INTEGER, ganancia_pack REAL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS caja (
            id INTEGER PRIMARY KEY AUTOINCREMENT, fecha_apertura TEXT, monto_inicial REAL,
            monto_final_efectivo REAL, monto_final_digital REAL, estado TEXT, fecha_cierre TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, caja_id INTEGER, producto_id INTEGER, nombre TEXT, 
            cantidad INTEGER, tipo_venta TEXT, metodo_pago TEXT, monto_total REAL, ganancia_real REAL, fecha TEXT)''')
        
        # AUDITORÍA ACTUALIZADA: Ahora guarda el costo/valor asociado a la pérdida
        cursor.execute('''CREATE TABLE IF NOT EXISTS ajustes_stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT, producto_id INTEGER, nombre TEXT,
            tipo_ajuste TEXT, cantidad INTEGER, costo_asociado REAL, motivo TEXT, fecha TEXT)''')
        conexion.commit()
        conexion.close()

    def abrir_caja(self, monto):
        conexion = self.conectar(); cursor = conexion.cursor()
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        cursor.execute("INSERT INTO caja (fecha_apertura, monto_inicial, estado) VALUES (?, ?, 'ABIERTA')", (fecha, monto))
        conexion.commit(); conexion.close()

    def cerrar_caja(self, efectivo_estimado, digital_estimado):
        conexion = self.conectar(); cursor = conexion.cursor()
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        cursor.execute('''UPDATE caja SET monto_final_efectivo = ?, monto_final_digital = ?, 
                          estado = 'CERRADA', fecha_cierre = ? WHERE estado = 'ABIERTA' ''', (efectivo_estimado, digital_estimado, fecha))
        conexion.commit(); conexion.close()

    def obtener_estado_caja(self):
        conexion = self.conectar(); cursor = conexion.cursor()
        cursor.execute("SELECT id, monto_inicial, estado, fecha_apertura FROM caja ORDER BY id DESC LIMIT 1")
        caja = cursor.fetchone(); estimado_efectivo = 0.0
        if caja and caja[2] == 'ABIERTA':
            cursor.execute("SELECT SUM(monto_total) FROM ventas WHERE caja_id = ? AND metodo_pago = 'Efectivo'", (caja[0],))
            estimado_efectivo = caja[1] + (cursor.fetchone()[0] or 0.0)
        conexion.close()
        return caja + (estimado_efectivo,) if caja else None

    def guardar_producto(self, nombre, tipo, u_pack, cant, stk_min, costo, gan_u, tiene_p, gan_p):
        conexion = self.conectar(); cursor = conexion.cursor()
        cursor.execute("""INSERT INTO inventario (nombre, tipo, unidades_pack, cantidad_unidades, stock_minimo, 
                          costo_ingresado, ganancia_unidad, tiene_ganancia_pack, ganancia_pack) 
                          VALUES (?,?,?,?,?,?,?,?,?)""", (nombre, tipo, u_pack, cant, stk_min, costo, gan_u, tiene_p, gan_p))
        conexion.commit(); conexion.close()

    def registrar_ajuste_stock(self, id_prod, nombre, tipo_ajuste, cantidad_cambio, costo_asociado, motivo, nuevo_stock_total, nuevo_nombre):
        conexion = self.conectar(); cursor = conexion.cursor()
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        if cantidad_cambio != 0:
            cursor.execute("INSERT INTO ajustes_stock (producto_id, nombre, tipo_ajuste, cantidad, costo_asociado, motivo, fecha) VALUES (?,?,?,?,?,?,?)",
                           (id_prod, nombre, tipo_ajuste, cantidad_cambio, costo_asociado, motivo, fecha))
        cursor.execute("UPDATE inventario SET nombre = ?, cantidad_unidades = ? WHERE id = ?", (nuevo_nombre, nuevo_stock_total, id_prod))
        conexion.commit(); conexion.close()

    def obtener_auditoria(self):
        conexion = self.conectar(); cursor = conexion.cursor()
        cursor.execute("SELECT nombre, tipo_ajuste, cantidad, costo_asociado, motivo, fecha FROM ajustes_stock ORDER BY id DESC")
        res = cursor.fetchall(); conexion.close()
        return res

    def obtener_productos(self):
        conexion = self.conectar(); cursor = conexion.cursor()
        cursor.execute("SELECT * FROM inventario")
        res = cursor.fetchall(); conexion.close()
        return res

    def registrar_venta(self, caja_id, id_prod, nombre, cant, tipo_v, pago, total, ganancia):
        conexion = self.conectar(); cursor = conexion.cursor()
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        cursor.execute("""INSERT INTO ventas (caja_id, producto_id, nombre, cantidad, tipo_venta, metodo_pago, monto_total, ganancia_real, fecha)
                          VALUES (?,?,?,?,?,?,?,?,?)""", (caja_id, id_prod, nombre, cant, tipo_v, pago, total, ganancia, fecha))
        cursor.execute("SELECT unidades_pack FROM inventario WHERE id = ?", (id_prod,))
        u_pack = cursor.fetchone()[0] or 1
        desc_stock = cant if tipo_v == "Unidad" else (cant * u_pack)
        cursor.execute("UPDATE inventario SET cantidad_unidades = cantidad_unidades - ? WHERE id = ?", (desc_stock, id_prod))
        conexion.commit(); conexion.close()

    def obtener_ventas(self, fecha_filtro=None):
        conexion = self.conectar(); cursor = conexion.cursor()
        if fecha_filtro:
            cursor.execute("SELECT nombre, cantidad, fecha, monto_total, metodo_pago FROM ventas WHERE fecha LIKE ? ORDER BY id DESC", (f"{fecha_filtro}%",))
        else:
            cursor.execute("SELECT nombre, cantidad, fecha, monto_total, metodo_pago FROM ventas ORDER BY id DESC LIMIT 100")
        ventas = cursor.fetchall(); conexion.close()
        return ventas

    def obtener_fechas_ventas(self):
        conexion = self.conectar(); cursor = conexion.cursor()
        cursor.execute("SELECT DISTINCT SUBSTR(fecha, 1, 10) FROM ventas ORDER BY id DESC")
        fechas = ["Global"] + [fila[0] for fila in cursor.fetchall()]
        conexion.close(); return fechas

    def obtener_estadisticas(self, fecha):
        conexion = self.conectar(); cursor = conexion.cursor()
        if fecha == "Global":
            condicion = ""; parametros = ()
        else:
            condicion = "WHERE fecha LIKE ?"; parametros = (f"{fecha}%",)

        cursor.execute(f"SELECT SUM(monto_total), SUM(ganancia_real) FROM ventas {condicion}", parametros)
        totales = cursor.fetchone(); ingresos, ganancia = totales[0] or 0.0, totales[1] or 0.0

        cond_efvo = "metodo_pago = 'Efectivo'" if not condicion else f"fecha LIKE ? AND metodo_pago = 'Efectivo'"
        cursor.execute(f"SELECT SUM(monto_total) FROM ventas WHERE {cond_efvo}", parametros)
        efectivo = cursor.fetchone()[0] or 0.0

        cond_mp = "metodo_pago = 'Mercado Pago'" if not condicion else f"fecha LIKE ? AND metodo_pago = 'Mercado Pago'"
        cursor.execute(f"SELECT SUM(monto_total) FROM ventas WHERE {cond_mp}", parametros)
        mp = cursor.fetchone()[0] or 0.0

        cursor.execute(f"""SELECT nombre, tipo_venta, SUM(cantidad), SUM(monto_total), SUM(ganancia_real) 
            FROM ventas {condicion} GROUP BY producto_id, nombre, tipo_venta ORDER BY SUM(cantidad) DESC""", parametros)
        detalle_productos = cursor.fetchall()
        conexion.close()
        return ingresos, ganancia, efectivo, mp, detalle_productos