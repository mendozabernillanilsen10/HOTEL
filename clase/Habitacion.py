class Habitacion:
    id = 0
    numero = 0
    tipo = ""
    precio = 0.0
    hotel_id = 0
    foto_url = ""
    midic = {}

    def __init__(self, p_id, p_numero, p_tipo, p_precio, p_hotel_id, p_foto_url):
        self.id = p_id
        self.numero = p_numero
        self.tipo = p_tipo
        self.precio = p_precio
        self.hotel_id = p_hotel_id
        self.foto_url = p_foto_url

        self.midic = {
            "id": p_id,
            "numero": p_numero,
            "tipo": p_tipo,
            "precio": p_precio,
            "hotel_id": p_hotel_id,
            "foto_url": p_foto_url
        }
