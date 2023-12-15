package com.example.project136.dto;

import java.io.Serializable;

public class LugarTuristicoDTO  implements Serializable {
    private int id;
    private String descripcion;
    private String foto_url;
    private String nombre;
    private String ubicacion;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }

    public String getFoto_url() {
        return foto_url;
    }

    public void setFoto_url(String foto_url) {
        this.foto_url = foto_url;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getUbicacion() {
        return ubicacion;
    }

    public void setUbicacion(String ubicacion) {
        this.ubicacion = ubicacion;
    }

    public LugarTuristicoDTO(int id, String descripcion, String foto_url, String nombre, String ubicacion) {
        this.id = id;
        this.descripcion = descripcion;
        this.foto_url = foto_url;
        this.nombre = nombre;
        this.ubicacion = ubicacion;
    }
}
