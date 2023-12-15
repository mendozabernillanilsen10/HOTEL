package com.example.project136.dto;

import java.io.Serializable;
import java.util.List;

public class HotelesResponseDTO implements Serializable {
    private List<HotelDTO> Datos;
    private boolean Estado;
    private String Mensaje;

    public List<HotelDTO> getDatos() {
        return Datos;
    }

    public void setDatos(List<HotelDTO> datos) {
        Datos = datos;
    }

    public boolean isEstado() {
        return Estado;
    }

    public void setEstado(boolean estado) {
        Estado = estado;
    }

    public String getMensaje() {
        return Mensaje;
    }

    public void setMensaje(String mensaje) {
        Mensaje = mensaje;
    }
}
