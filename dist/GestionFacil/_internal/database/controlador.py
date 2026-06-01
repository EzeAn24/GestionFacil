import sqlite3
from datetime import datetime

class ControladorDB:
    def __init__(self, nombre_bd="gestion_facil.db"):
        self.nombre_bd = nombre_bd
        self.crear_tablas()

    def conectar(self):
        return sqlite3.connect(self.nombre_bd)

    def crear_tablas(self):
        conexion = self.conectar(); cursor = conexion.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, tipo TEXT, unidades_pack INTEGER,
            cantidad_unidades REAL, stock_minimo INTEGER, costo_ingresado REAL, ganancia_unidad REAL,
            tiene_ganancia_pack INTEGER, ganancia_pack REAL, seccion TEXT, controla_stock INTEGER)''')
            
        cursor.execute('''CREATE TABLE IF NOT EXISTS caja (
            id INTEGER PRIMARY KEY AUTOINCREMENT, fecha_apertura TEXT, monto_inicial REAL,
            monto_final_efectivo REAL, monto_final_digital REAL, estado TEXT, fecha_cierre TEXT)''')
            
        cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, caja_id INTEGER, producto_id INTEGER, nombre TEXT, 
            cantidad REAL, tipo_venta TEXT, metodo_pago TEXT, monto_total REAL, ganancia_real REAL, fecha TEXT, seccion TEXT)''')
            
        cursor.execute('''CREATE TABLE IF NOT EXISTS ajustes_stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT, producto_id INTEGER, nombre TEXT,
            tipo_ajuste TEXT, cantidad REAL, costo_asociado REAL, motivo TEXT, fecha TEXT)''')
        conexion.commit(); conexion.close()

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
        caja = cursor.fetchone()
        
        if not caja:
            conexion.close()
            return None
            
        estimado_efectivo = 0.0
        if caja[2] == 'ABIERTA':
            cursor.execute("SELECT COALESCE(SUM(monto_total), 0) FROM ventas WHERE caja_id = ? AND metodo_pago = 'Efectivo'", (caja[0],))
            estimado_efectivo = caja[1] + cursor.fetchone()[0]
        conexion.close()
        return (caja[0], caja[1], caja[2], caja[3], estimado_efectivo)

    def guardar_producto(self, nombre, tipo, u_pack, cant, stk_min, costo, gan_u, tiene_p, gan_p, seccion, controla_stock):
        conexion = self.conectar(); cursor = conexion.cursor()
        cursor.execute("""INSERT INTO inventario (nombre, tipo, unidades_pack, cantidad_unidades, stock_minimo, 
                          costo_ingresado, ganancia_unidad, tiene_ganancia_pack, ganancia_pack, seccion, controla_stock) 
                          VALUES (?,?,?,?,?,?,?,?,?,?,?)""", 
                       (nombre, tipo, u_pack, cant, stk_min, costo, gan_u, tiene_p, gan_p, seccion, controla_stock))
        conexion.commit(); conexion.close()

    def registrar_ajuste_stock(self, id_prod, nombre, tipo_ajuste, cantidad_cambio, costo_asociado, motivo, nuevo_stock_total, nuevo_nombre, nuevo_costo, nueva_gan_u, nueva_gan_p):
        conexion = self.conectar(); cursor = conexion.cursor()
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        if cantidad_cambio != 0:
            cursor.execute("INSERT INTO ajustes_stock (producto_id, nombre, tipo_ajuste, cantidad, costo_asociado, motivo, fecha) VALUES (?,?,?,?,?,?,?)",
                           (id_prod, nombre, tipo_ajuste, cantidad_cambio, costo_asociado, motivo, fecha))
        cursor.execute("""UPDATE inventario SET nombre = ?, cantidad_unidades = ?, costo_ingresado = ?, ganancia_unidad = ?, ganancia_pack = ? 
                          WHERE id = ?""", (nuevo_nombre, nuevo_stock_total, nuevo_costo, nueva_gan_u, nueva_gan_p, id_prod))
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

    def registrar_venta(self, caja_id, id_prod, nombre, cant, tipo_v, pago, total, ganancia, seccion):
        conexion = self.conectar(); cursor = conexion.cursor()
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        cursor.execute("""INSERT INTO ventas (caja_id, producto_id, nombre, cantidad, tipo_venta, metodo_pago, monto_total, ganancia_real, fecha, seccion)
                          VALUES (?,?,?,?,?,?,?,?,?,?)""", (caja_id, id_prod, nombre, cant, tipo_v, pago, total, ganancia, fecha, seccion))
        
        cursor.execute("SELECT unidades_pack, controla_stock FROM inventario WHERE id = ?", (id_prod,))
        res = cursor.fetchone()
        if res and res[1] == 1: 
            u_pack = res[0]
            desc_stock = cant if tipo_v == "Unidad" else (cant * u_pack)
            cursor.execute("UPDATE inventario SET cantidad_unidades = cantidad_unidades - ? WHERE id = ?", (desc_stock, id_prod))
        conexion.commit(); conexion.close()

    def obtener_ventas(self, fecha_filtro=None, seccion="General"):
        conexion = self.conectar(); cursor = conexion.cursor()
        query = "SELECT nombre, cantidad, fecha, monto_total, metodo_pago, ganancia_real FROM ventas WHERE seccion = ?"
        parametros = [seccion]
        if fecha_filtro:
            query += " AND fecha LIKE ?"
            parametros.append(f"{fecha_filtro}%")
        query += " ORDER BY id DESC"
        cursor.execute(query, tuple(parametros))
        ventas = cursor.fetchall(); conexion.close()
        return ventas

    def obtener_fechas_ventas(self):
        conexion = self.conectar(); cursor = conexion.cursor()
        cursor.execute("SELECT DISTINCT SUBSTR(fecha, 1, 10) FROM ventas")
        dias = sorted([fila[0] for fila in cursor.fetchall()], reverse=True)
        cursor.execute("SELECT DISTINCT SUBSTR(fecha, 4, 7) FROM ventas")
        meses = sorted([f"Mes: {fila[0]}" for fila in cursor.fetchall()], reverse=True)
        conexion.close()
        return ["Global"] + meses + dias

    def obtener_estadisticas(self, fecha, seccion="Todas"):
        conexion = self.conectar(); cursor = conexion.cursor()
        condiciones = []; parametros = []

        if fecha != "Global":
            if fecha.startswith("Mes: "):
                mes_anio = fecha.replace("Mes: ", "")
                condiciones.append("fecha LIKE ?"); parametros.append(f"%/{mes_anio}%")
            else:
                condiciones.append("fecha LIKE ?"); parametros.append(f"{fecha}%")

        if seccion != "Todas":
            condiciones.append("seccion = ?"); parametros.append(seccion)

        where_clause = ""
        if condiciones:
            where_clause = "WHERE " + " AND ".join(condiciones)

        cursor.execute(f"SELECT COALESCE(SUM(monto_total), 0), COALESCE(SUM(ganancia_real), 0) FROM ventas {where_clause}", tuple(parametros))
        totales = cursor.fetchone(); ingresos, ganancia = totales[0], totales[1]

        # AQUÍ ESTÁ EL ARREGLO DEL BUG DE LOS BINDINGS (Pusimos el = ? para que acepte el parámetro)
        cond_efvo = list(condiciones) + ["metodo_pago = ?"]; param_efvo = list(parametros) + ["Efectivo"]
        cursor.execute(f"SELECT COALESCE(SUM(monto_total), 0) FROM ventas WHERE " + " AND ".join(cond_efvo), tuple(param_efvo))
        efectivo = cursor.fetchone()[0]

        cond_mp = list(condiciones) + ["metodo_pago = ?"]; param_mp = list(parametros) + ["Mercado Pago"]
        cursor.execute(f"SELECT COALESCE(SUM(monto_total), 0) FROM ventas WHERE " + " AND ".join(cond_mp), tuple(param_mp))
        mp = cursor.fetchone()[0]

        cursor.execute(f"""SELECT nombre, tipo_venta, SUM(cantidad), SUM(monto_total), SUM(ganancia_real) 
            FROM ventas {where_clause} GROUP BY producto_id, nombre, tipo_venta ORDER BY SUM(monto_total) DESC""", tuple(parametros))
        detalle_productos = cursor.fetchall()
        
        conexion.close()
        return ingresos, ganancia, efectivo, mp, detalle_productos