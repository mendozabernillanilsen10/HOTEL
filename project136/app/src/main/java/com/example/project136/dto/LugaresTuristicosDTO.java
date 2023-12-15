package com.example.project136.dto;
import java.io.Serializable;
import java.util.List;
public class LugaresTuristicosDTO  implements Serializable {
    private List<LugarTuristicoDTO> Datos;
    private boolean Estado;
    private String Mensaje;

    public LugaresTuristicosDTO() {
    }

    public LugaresTuristicosDTO(List<LugarTuristicoDTO> datos, boolean estado, String mensaje) {
        Datos = datos;
        Estado = estado;
        Mensaje = mensaje;
    }

    public List<LugarTuristicoDTO> getDatos() {
        return Datos;
    }

    public void setDatos(List<LugarTuristicoDTO> datos) {
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
