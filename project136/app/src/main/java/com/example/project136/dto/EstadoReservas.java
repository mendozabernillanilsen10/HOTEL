package com.example.project136.dto;

import java.io.Serializable;
import java.util.List;

public class EstadoReservas  implements Serializable {

    private boolean Estado;
    private List<ReservaModel> Reservas;

    public boolean isEstado() {
        return Estado;
    }

    public void setEstado(boolean estado) {
        Estado = estado;
    }

    public List<ReservaModel> getReservas() {
        return Reservas;
    }

    public void setReservas(List<ReservaModel> reservas) {
        Reservas = reservas;
    }
}
