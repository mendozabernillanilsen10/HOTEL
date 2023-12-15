package com.example.project136.dto;

import java.io.Serializable;
import java.util.List;
public class HabitacionesResponseDTO  implements Serializable {
    private List<HabitacionDTO> Datos;
    private boolean Estado;
    private String Mensaje;

    public List<HabitacionDTO> getDatos() {
        return Datos;
    }

    public void setDatos(List<HabitacionDTO> datos) {
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
