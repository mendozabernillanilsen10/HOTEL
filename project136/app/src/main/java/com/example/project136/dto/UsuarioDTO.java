package com.example.project136.dto;

import lombok.Data;
import java.io.Serializable;
import java.util.List;
import java.util.UUID;
import java.io.Serializable;

import java.io.Serializable;
import java.util.List;
import java.util.UUID;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
@Builder
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor

public  class UsuarioDTO implements Serializable {
    private String dni;
    private String password;
    private String apellido;
    private String lugar_procedencia;
    private String nombre;




    public UsuarioDTO(String dni, String password) {
        this.dni = dni;
        this.password = password;
    }

    public UsuarioDTO(String dni, String password, String apellido, String lugar_procedencia, String nombre) {
        this.dni = dni;
        this.password = password;
        this.apellido = apellido;
        this.lugar_procedencia = lugar_procedencia;
        this.nombre = nombre;
    }

    private int id;
    public String getDni() {
        return dni;
    }

    public void setDni(String dni) {
        this.dni = dni;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getApellido() {
        return apellido;
    }

    public void setApellido(String apellido) {
        this.apellido = apellido;
    }

    public String getLugar_procedencia() {
        return lugar_procedencia;
    }

    public void setLugar_procedencia(String lugar_procedencia) {
        this.lugar_procedencia = lugar_procedencia;
    }
    public String getNombre() {
        return nombre;
    }
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }
}