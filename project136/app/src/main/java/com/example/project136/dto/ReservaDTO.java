package com.example.project136.dto;

public class ReservaDTO {
    private String cliente_id;
    private String habitacion_id;
    private String fecha_inicio;
    private String fecha_fin;
    private String estado;

    public String getCliente_id() {
        return cliente_id;
    }

    public void setCliente_id(String cliente_id) {
        this.cliente_id = cliente_id;
    }

    public String getHabitacion_id() {
        return habitacion_id;
    }

    public void setHabitacion_id(String habitacion_id) {
        this.habitacion_id = habitacion_id;
    }

    public String getFecha_inicio() {
        return fecha_inicio;
    }

    public void setFecha_inicio(String fecha_inicio) {
        this.fecha_inicio = fecha_inicio;
    }

    public String getFecha_fin() {
        return fecha_fin;
    }

    public void setFecha_fin(String fecha_fin) {
        this.fecha_fin = fecha_fin;
    }

    public String getEstado() {
        return estado;
    }

    public void setEstado(String estado) {
        this.estado = estado;
    }
}
