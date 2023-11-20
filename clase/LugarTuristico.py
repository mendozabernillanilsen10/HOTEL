
class LugarTuristico:
    id = 0
    nombre = ""
    descripcion = ""
    ubicacion = ""
    foto_url = ""
    midic = {}

    def __init__(self, p_id, p_nombre, p_descripcion, p_ubicacion, p_foto_url):
        self.id = p_id
        self.nombre = p_nombre
        self.descripcion = p_descripcion
        self.ubicacion = p_ubicacion
        self.foto_url = p_foto_url

        self.midic = {
            "id": p_id,
            "nombre": p_nombre,
            "descripcion": p_descripcion,
            "ubicacion": p_ubicacion,
            "foto_url": p_foto_url
        }