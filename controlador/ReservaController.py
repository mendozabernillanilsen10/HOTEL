from bd import obtener_conexion


class ReservaController:
    @classmethod
    def insertar_reserva(
        cls, p_id, p_cliente_id, p_habitacion_id, p_fecha_inicio, p_fecha_fin, p_estado
    ):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO reservas (id, cliente_id, habitacion_id, fecha_inicio, fecha_fin, estado) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    p_id,
                    p_cliente_id,
                    p_habitacion_id,
                    p_fecha_inicio,
                    p_fecha_fin,
                    p_estado,
                ),
            )
        conexion.commit()
        conexion.close()

    @classmethod
    def actualizar_reserva(
        cls, p_id, p_cliente_id, p_habitacion_id, p_fecha_inicio, p_fecha_fin, p_estado
    ):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE reservas SET cliente_id = %s, habitacion_id = %s, fecha_inicio = %s, fecha_fin = %s, estado = %s WHERE id = %s",
                (
                    p_cliente_id,
                    p_habitacion_id,
                    p_fecha_inicio,
                    p_fecha_fin,
                    p_estado,
                    p_id,
                ),
            )
        conexion.commit()
        conexion.close()

    @classmethod
    def obtener_reserva_por_id(cls, p_id):
        conexion = obtener_conexion()
        reserva = None
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, cliente_id, habitacion_id, fecha_inicio, fecha_fin, estado FROM reservas WHERE id = %s",
                (p_id,),
            )
            reserva = cursor.fetchone()
        conexion.close()
        return reserva

    @classmethod
    def eliminar_reserva(cls, p_id):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM reservas WHERE id = %s", (p_id,))
        conexion.commit()
        conexion.close()

    @classmethod
    def obtener_reservas(cls):
        conexion = obtener_conexion()
        reservas = []
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, cliente_id, habitacion_id, fecha_inicio, fecha_fin, estado FROM reservas"
            )
            reservas = cursor.fetchall()
        conexion.close()
        return reservas

    @classmethod
    def obtener_reservas_por_cliente(cls, cliente_id):
        conexion = obtener_conexion()
        reservas = []
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, cliente_id, habitacion_id, fecha_inicio, fecha_fin, estado FROM reservas WHERE cliente_id = %s",
                (cliente_id,),
            )
            reservas = cursor.fetchall()
        conexion.close()
        return reservas
