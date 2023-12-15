package com.example.project136.Activities;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.TextUtils;
import android.widget.ImageView;

import com.example.project136.Adapters.reservaAdapter;
import com.example.project136.R;
import com.example.project136.dto.EstadoReservas;
import com.example.project136.dto.LoginResponseDTO;
import com.example.project136.dto.ReservaModel;
import com.example.project136.service.Service;
import com.example.project136.config.Apis;
import com.example.project136.config.Toas;
import com.google.gson.Gson;

import java.util.ArrayList;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class listaReservas extends AppCompatActivity {
    private RecyclerView.Adapter  adapterCat;
    private RecyclerView  recyclerViewCategory;
    private ImageView backBtn;
    Toas toas = new Toas(this);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_lista_reservas);
        backBtn=findViewById(R.id.backBtns);
        backBtn.setOnClickListener(v -> finish());
        proceso();

    }
    private void proceso() {
        recyclerViewCategory = findViewById(R.id.listaReserva);
        recyclerViewCategory.setLayoutManager(new LinearLayoutManager(this, LinearLayoutManager.VERTICAL, false));
        SharedPreferences sharedPreferences = getSharedPreferences("Sesion", Context.MODE_PRIVATE);
        String jsonString = sharedPreferences.getString("response", "");
        if (!TextUtils.isEmpty(jsonString)) {
            Gson gson = new Gson();
            LoginResponseDTO response = gson.fromJson(jsonString, LoginResponseDTO.class);
            Service sevice;
            sevice = Apis.Mediador();

            Call<EstadoReservas> call = sevice.optenerReserva("Bearer " + response.getToken(),response.getUsuario().getId());
            call.enqueue(new Callback<EstadoReservas>() {
                @Override
                public void onResponse(Call<EstadoReservas> call, Response<EstadoReservas> response) {

                    if (response.isSuccessful()) {
                        EstadoReservas res = response.body();
                        if (res.isEstado()) {
                            adapterCat = new reservaAdapter((ArrayList<ReservaModel>) res.getReservas());
                            recyclerViewCategory.setAdapter(adapterCat);
                        }else{
                            toas.toastIncorrecto(""+res.isEstado());
                        }
                    }
                }
                @Override
                public void onFailure(Call<EstadoReservas> call, Throwable t) {
                    toas.toastIncorrecto(t.getMessage());

                }
            });
        }

    }
}