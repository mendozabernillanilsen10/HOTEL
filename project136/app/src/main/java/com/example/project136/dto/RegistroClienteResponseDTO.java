package com.example.project136.dto;
import java.io.Serializable;

public class RegistroClienteResponseDTO implements Serializable {
    private boolean Estado;
    private String Mensaje;

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

    public RegistroClienteResponseDTO(boolean estado, String mensaje) {
        Estado = estado;
        Mensaje = mensaje;
    }
}
