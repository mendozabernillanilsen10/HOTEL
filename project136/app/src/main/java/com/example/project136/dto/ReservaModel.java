package com.example.project136.dto;

import java.io.Serializable;

public class ReservaModel implements Serializable {
    private int cliente_id;
    private String estado;
    private String fecha_fin;
    private String fecha_inicio;
    private int habitacion_id;
    private int habitacion_numero;
    private String habitacion_precio;
    private String habitacion_tipo;
    private String hotel_nombre;
    private String hotel_ubicacion;
    private int reserva_id;

    public ReservaModel() {
    }

    public ReservaModel(int cliente_id, String estado, String fecha_fin, String fecha_inicio, int habitacion_id, int habitacion_numero, String habitacion_precio, String habitacion_tipo, String hotel_nombre, String hotel_ubicacion, int reserva_id) {
        this.cliente_id = cliente_id;
        this.estado = estado;
        this.fecha_fin = fecha_fin;
        this.fecha_inicio = fecha_inicio;
        this.habitacion_id = habitacion_id;
        this.habitacion_numero = habitacion_numero;
        this.habitacion_precio = habitacion_precio;
        this.habitacion_tipo = habitacion_tipo;
        this.hotel_nombre = hotel_nombre;
        this.hotel_ubicacion = hotel_ubicacion;
        this.reserva_id = reserva_id;
    }

    public int getCliente_id() {
        return cliente_id;
    }

    public void setCliente_id(int cliente_id) {
        this.cliente_id = cliente_id;
    }

    public String getEstado() {
        return estado;
    }

    public void setEstado(String estado) {
        this.estado = estado;
    }

    public String getFecha_fin() {
        return fecha_fin;
    }

    public void setFecha_fin(String fecha_fin) {
        this.fecha_fin = fecha_fin;
    }

    public String getFecha_inicio() {
        return fecha_inicio;
    }

    public void setFecha_inicio(String fecha_inicio) {
        this.fecha_inicio = fecha_inicio;
    }

    public int getHabitacion_id() {
        return habitacion_id;
    }

    public void setHabitacion_id(int habitacion_id) {
        this.habitacion_id = habitacion_id;
    }

    public int getHabitacion_numero() {
        return habitacion_numero;
    }

    public void setHabitacion_numero(int habitacion_numero) {
        this.habitacion_numero = habitacion_numero;
    }

    public String getHabitacion_precio() {
        return habitacion_precio;
    }

    public void setHabitacion_precio(String habitacion_precio) {
        this.habitacion_precio = habitacion_precio;
    }

    public String getHabitacion_tipo() {
        return habitacion_tipo;
    }

    public void setHabitacion_tipo(String habitacion_tipo) {
        this.habitacion_tipo = habitacion_tipo;
    }

    public String getHotel_nombre() {
        return hotel_nombre;
    }

    public void setHotel_nombre(String hotel_nombre) {
        this.hotel_nombre = hotel_nombre;
    }

    public String getHotel_ubicacion() {
        return hotel_ubicacion;
    }

    public void setHotel_ubicacion(String hotel_ubicacion) {
        this.hotel_ubicacion = hotel_ubicacion;
    }

    public int getReserva_id() {
        return reserva_id;
    }

    public void setReserva_id(int reserva_id) {
        this.reserva_id = reserva_id;
    }
}
