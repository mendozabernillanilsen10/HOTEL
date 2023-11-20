
class Reserva:
    id = 0
    cliente_id = 0
    habitacion_id = 0
    fecha_inicio = ""
    fecha_fin = ""
    estado = ""
    midic = {}

    def __init__(self, p_id, p_cliente_id, p_habitacion_id, p_fecha_inicio, p_fecha_fin, p_estado):
        self.id = p_id
        self.cliente_id = p_cliente_id
        self.habitacion_id = p_habitacion_id
        self.fecha_inicio = p_fecha_inicio
        self.fecha_fin = p_fecha_fin
        self.estado = p_estado

        self.midic = {
            "id": p_id,
            "cliente_id": p_cliente_id,
            "habitacion_id": p_habitacion_id,
            "fecha_inicio": p_fecha_inicio,
            "fecha_fin": p_fecha_fin,
            "estado": p_estado
        }