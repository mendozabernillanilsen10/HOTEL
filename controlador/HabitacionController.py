from bd import obtener_conexion
from clase.Habitacion import Habitacion


class HabitacionController:
    @classmethod
    def obtener_habitaciones(cls, hotel_id):
        conexion = obtener_conexion()
        habitaciones = []
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, numero, tipo, precio, foto_url FROM habitaciones WHERE hotel_id = %s",
                (hotel_id,),
            )
            habitaciones_data = cursor.fetchall()
            habitaciones = [Habitacion(*data) for data in habitaciones_data]
        conexion.close()
        return habitaciones

    @classmethod
    def obtener_habitacion_por_id(cls, p_id):
        conexion = obtener_conexion()
        habitacion = None
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, numero, tipo, precio, hotel_id, foto_url FROM habitaciones WHERE id = %s",
                (p_id,),
            )
            habitacion_data = cursor.fetchone()
            if habitacion_data:
                habitacion = Habitacion(*habitacion_data)
        conexion.close()
        return habitacion

    @classmethod
    def insertar_habitacion(cls, p_numero, p_tipo, p_precio, p_hotel_id, p_foto_url):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO habitaciones ( numero, tipo, precio, hotel_id, foto_url) VALUES ( %s, %s, %s, %s, %s)",
                (p_numero, p_tipo, p_precio, p_hotel_id, p_foto_url),
            )
        conexion.commit()
        conexion.close()

    @classmethod
    def actualizar_habitacion(cls, p_id, p_numero, p_tipo, p_precio, p_foto_url):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE habitaciones SET numero = %s, tipo = %s, precio = %s,  foto_url = %s WHERE id = %s",
                (p_numero, p_tipo, p_precio, p_foto_url, p_id),
            )
        conexion.commit()
        conexion.close()

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
            cursor.execute(
                "SELECT id, numero, tipo, precio, hotel_id, foto_url FROM habitaciones"
            )
            habitaciones_data = cursor.fetchall()
            habitaciones = [Habitacion(*data) for data in habitaciones_data]
        conexion.close()
        return habitaciones

    @classmethod
    def obtener_habitaciones_por_hotel(cls, p_hotel_id):
        conexion = obtener_conexion()
        habitaciones = []
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, numero, tipo, precio, hotel_id, foto_url FROM habitaciones WHERE hotel_id = %s",
                (p_hotel_id,),
            )
            habitaciones = cursor.fetchall()
        conexion.close()
        return habitaciones
