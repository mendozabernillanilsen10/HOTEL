from bd import obtener_conexion

class HabitacionController:
    @classmethod
    def insertar_habitacion(cls, p_id, p_numero, p_tipo, p_precio, p_hotel_id, p_foto_url):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO habitaciones (id, numero, tipo, precio, hotel_id, foto_url) VALUES (%s, %s, %s, %s, %s, %s)",
                (p_id, p_numero, p_tipo, p_precio, p_hotel_id, p_foto_url)
            )
        conexion.commit()
        conexion.close()

    @classmethod
    def actualizar_habitacion(cls, p_id, p_numero, p_tipo, p_precio, p_hotel_id, p_foto_url):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE habitaciones SET numero = %s, tipo = %s, precio = %s, hotel_id = %s, foto_url = %s WHERE id = %s",
                (p_numero, p_tipo, p_precio, p_hotel_id, p_foto_url, p_id)
            )
        conexion.commit()
        conexion.close()

    @classmethod
    def obtener_habitacion_por_id(cls, p_id):
        conexion = obtener_conexion()
        habitacion = None
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, numero, tipo, precio, hotel_id, foto_url FROM habitaciones WHERE id = %s", (p_id,))
            habitacion = cursor.fetchone()
        conexion.close()
        return habitacion

    @classmethod
    def eliminar_habitacion(cls, p_id):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM habitaciones WHERE id = %s", (p_id,))
        conexion.commit()
        conexion.close()
    @classmethod
    def obtener_habitaciones(cls):
        conexion = obtener_conexion()
        habitaciones = []
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, numero, tipo, precio, hotel_id, foto_url FROM habitaciones")
            habitaciones = cursor.fetchall()
        conexion.close()
        return habitaciones
