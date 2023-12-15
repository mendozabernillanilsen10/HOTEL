from bd import obtener_conexion


class HotelController:
    @classmethod
    def insertar_hotel(cls, p_nombre, p_ubicacion, p_ruc, p_descripcion, foto_url):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO hoteles ( nombre, ubicacion, ruc, descripcion,	foto_url) VALUES ( %s, %s, %s, %s, %s)",
                (p_nombre, p_ubicacion, p_ruc, p_descripcion, foto_url),
            )
        conexion.commit()
        conexion.close()

    @classmethod
    def actualizar_hotel(
        cls, p_id, p_nombre, p_ubicacion, p_ruc, p_descripcion, nuevo_nombre_seguro
    ):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE hoteles SET nombre = %s, ubicacion = %s, ruc = %s, descripcion = %s  ,foto_url =%s  WHERE id = %s",
                (
                    p_nombre,
                    p_ubicacion,
                    p_ruc,
                    p_descripcion,
                    nuevo_nombre_seguro,
                    p_id,
                ),
            )
        conexion.commit()
        conexion.close()

    @classmethod
    def obtener_hotel_por_id(cls, p_id):
        conexion = obtener_conexion()
        hotel = None
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, ubicacion, ruc, descripcion ,foto_url FROM hoteles WHERE id = %s",
                (p_id,),
            )
            hotel = cursor.fetchone()
        conexion.close()
        return hotel

    @classmethod
    def eliminar_hotel(cls, p_id):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM hoteles WHERE id = %s", (p_id,))
        conexion.commit()
        conexion.close()

    @classmethod
    def obtener_hoteles(cls):
        conexion = obtener_conexion()
        hoteles = []
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, ubicacion, ruc, descripcion,foto_url FROM hoteles"
            )
            hoteles = cursor.fetchall()
        conexion.close()
        return hoteles
