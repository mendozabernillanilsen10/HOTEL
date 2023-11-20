from bd import obtener_conexion

class LugarTuristicoController:
    @classmethod
    def insertar_lugar_turistico(cls, p_id, p_nombre, p_descripcion, p_ubicacion, p_foto_url):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO lugares_turisticos (id, nombre, descripcion, ubicacion, foto_url) VALUES (%s, %s, %s, %s, %s)",
                (p_id, p_nombre, p_descripcion, p_ubicacion, p_foto_url)
            )
        conexion.commit()
        conexion.close()

    @classmethod
    def actualizar_lugar_turistico(cls, p_id, p_nombre, p_descripcion, p_ubicacion, p_foto_url):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE lugares_turisticos SET nombre = %s, descripcion = %s, ubicacion = %s, foto_url = %s WHERE id = %s",
                (p_nombre, p_descripcion, p_ubicacion, p_foto_url, p_id)
            )
        conexion.commit()
        conexion.close()

    @classmethod
    def obtener_lugar_turistico_por_id(cls, p_id):
        conexion = obtener_conexion()
        lugar_turistico = None
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, ubicacion, foto_url FROM lugares_turisticos WHERE id = %s", (p_id,))
            lugar_turistico = cursor.fetchone()
        conexion.close()
        return lugar_turistico

    @classmethod
    def eliminar_lugar_turistico(cls, p_id):
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM lugares_turisticos WHERE id = %s", (p_id,))
        conexion.commit()
        conexion.close()

    @classmethod
    def obtener_lugares_turisticos(cls):
        conexion = obtener_conexion()
        lugares_turisticos = []
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, ubicacion, foto_url FROM lugares_turisticos")
            lugares_turisticos = cursor.fetchall()
        conexion.close()
        return lugares_turisticos
