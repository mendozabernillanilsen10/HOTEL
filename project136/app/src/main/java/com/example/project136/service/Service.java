package com.example.project136.service;

import com.example.project136.dto.EstadoReservas;
import com.example.project136.dto.HabitacionesResponseDTO;
import com.example.project136.dto.HotelesResponseDTO;
import com.example.project136.dto.LoginResponseDTO;
import com.example.project136.dto.LugaresTuristicosDTO;
import com.example.project136.dto.RegistroClienteResponseDTO;
import com.example.project136.dto.ReservaDTO;
import com.example.project136.dto.UsuarioDTO;

import retrofit2.http.Header;
import retrofit2.http.POST;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.Field;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Path;
public interface Service {
    @POST("api_login")
    Call<LoginResponseDTO> login(@Body UsuarioDTO usuario);
    @POST("api_guardar_cliente")
    Call<RegistroClienteResponseDTO> RegistroUsuario(@Body UsuarioDTO usuario);
    @GET("optenerLugaresTuristicos")
    Call<LugaresTuristicosDTO> optenerTuris(@Header("Authorization") String token);

    @GET("api_obtener_hoteles")
    Call<HotelesResponseDTO> optenerhoteles(@Header("Authorization") String token);

    @GET("api_obtener_habitaciones_por_hotel/{hotel_id}")
    Call<HabitacionesResponseDTO> obtenerHabitacionesPorHotel(@Header("Authorization") String token, @Path("hotel_id") int hotel_id);


    @POST("api_guardar_reserva")
    Call<RegistroClienteResponseDTO> registroReserva(@Header("Authorization") String token,@Body ReservaDTO usuario);

    @GET("api_listar_reservas_por_cliente/{cliente_id}")
    Call<EstadoReservas> optenerReserva(@Header("Authorization") String token, @Path("cliente_id") int cliente_id);


}
