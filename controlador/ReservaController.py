from bd import obtener_conexion


class ReservaController:
    @classmethod
    def insertar_reserva(
        cls, p_cliente_id, p_habitacion_id, p_fecha_inicio, p_fecha_fin, p_estado
    ):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO reservas ( cliente_id, habitacion_id, fecha_inicio, fecha_fin, estado) VALUES ( %s, %s, %s, %s, %s)",
                (
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
                """
                SELECT
                    r.id as reserva_id,
                    r.cliente_id,
                    r.habitacion_id,
                    r.fecha_inicio,
                    r.fecha_fin,
                    r.estado,
                    h.numero as habitacion_numero,
                    h.tipo as habitacion_tipo,
                    h.precio as habitacion_precio,
                    ho.nombre as hotel_nombre,
                    ho.ubicacion as hotel_ubicacion
                FROM reservas r
                INNER JOIN habitaciones h ON r.habitacion_id = h.id
                INNER JOIN hoteles ho ON h.hotel_id = ho.id
                WHERE r.cliente_id = %s
            """,
                (cliente_id,),
            )
            reservas = cursor.fetchall()
        conexion.close()
        return reservas

    @classmethod
    def obtener_reservas_por_habitacion_y_periodo(
        cls, habitacion_id, fecha_inicio, fecha_fin
    ):
        conexion = obtener_conexion()
        reservas = []
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, cliente_id, habitacion_id, fecha_inicio, fecha_fin, estado FROM reservas WHERE habitacion_id = %s AND ((fecha_inicio >= %s AND fecha_inicio <= %s) OR (fecha_fin >= %s AND fecha_fin <= %s))",
                (habitacion_id, fecha_inicio, fecha_fin, fecha_inicio, fecha_fin),
            )
            reservas = cursor.fetchall()
        conexion.close()
        return reservas

    @classmethod
    def obtener_reservas_por_hotel(cls, hotel_id):
        conexion = obtener_conexion()
        reservas = []
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    r.id as reserva_id,
                    r.cliente_id,
                    c.nombre as cliente_nombre,
                    c.apellido as cliente_apellido,
                    c.dni as cliente_dni,
                    c.lugar_procedencia as cliente_lugar_procedencia,
                    r.habitacion_id,
                    r.fecha_inicio,
                    r.fecha_fin,
                    r.estado,
                    h.numero as habitacion_numero,
                    h.tipo as habitacion_tipo,
                    h.precio as habitacion_precio,
                    ho.nombre as hotel_nombre,
                    ho.ubicacion as hotel_ubicacion
                FROM reservas r
                INNER JOIN habitaciones h ON r.habitacion_id = h.id
                INNER JOIN hoteles ho ON h.hotel_id = ho.id
                INNER JOIN clientes c ON r.cliente_id = c.id
                WHERE ho.id = %s
                """,
                (hotel_id,),
            )

            reservas = cursor.fetchall()
        conexion.close()
        return reservas
