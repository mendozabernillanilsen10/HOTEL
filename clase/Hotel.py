class Hotel:
    id = 0
    nombre = ""
    ubicacion = ""
    ruc = ""
    descripcion = ""
    foto_url = ""
    midic = {}

    def __init__(self, p_id, p_nombre, p_ubicacion, p_ruc, p_descripcion, p_foto_url):
        self.id = p_id
        self.nombre = p_nombre
        self.ubicacion = p_ubicacion
        self.ruc = p_ruc
        self.descripcion = p_descripcion
        self.foto_url = p_foto_url

        self.midic = {
            "id": p_id,
            "nombre": p_nombre,
            "ubicacion": p_ubicacion,
            "ruc": p_ruc,
            "descripcion": p_descripcion,
            "foto_url": p_foto_url,
        }
