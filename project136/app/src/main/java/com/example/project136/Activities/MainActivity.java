package com.example.project136.Activities;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.TextUtils;
import android.widget.TextView;

import com.example.project136.Adapters.HotelAdapter;
import com.example.project136.Adapters.PupolarAdapter;
import com.example.project136.R;
import com.example.project136.dto.HotelDTO;
import com.example.project136.dto.HotelesResponseDTO;
import com.example.project136.dto.LoginResponseDTO;
import com.example.project136.dto.LugarTuristicoDTO;
import com.example.project136.dto.LugaresTuristicosDTO;
import com.example.project136.service.Service;
import com.example.project136.config.Apis;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.gson.Gson;

import java.util.ArrayList;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {

    private RecyclerView.Adapter adapterPopular, adapterCat;
    private RecyclerView recyclerViewPopular, recyclerViewCategory;
    private TextView textView5;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        textView5 = findViewById(R.id.textView5);
        SharedPreferences sharedPreferences = getSharedPreferences("Sesion", Context.MODE_PRIVATE);
        String jsonString = sharedPreferences.getString("response", "");

        if (!TextUtils.isEmpty(jsonString)) {
            Gson gson = new Gson();
            LoginResponseDTO response = gson.fromJson(jsonString, LoginResponseDTO.class);
            textView5.setText(response.getUsuario().getNombre() +" "+response.getUsuario().getApellido());
        }
        FloatingActionButton myFab = findViewById(R.id.myFloatingActionButton);


        myFab.setOnClickListener(view -> {
            Intent n = new Intent(MainActivity.this, listaReservas.class);
            startActivity(n);
        });
            initRecyclerView();
            hoteleslistar();
    }

    private void hoteleslistar() {
        recyclerViewCategory = findViewById(R.id.view_cat);
        recyclerViewCategory.setLayoutManager(new LinearLayoutManager(this, LinearLayoutManager.HORIZONTAL, false));
        SharedPreferences sharedPreferences = getSharedPreferences("Sesion", Context.MODE_PRIVATE);
        String jsonString = sharedPreferences.getString("response", "");
        if (!TextUtils.isEmpty(jsonString)) {
            Gson gson = new Gson();
            LoginResponseDTO response = gson.fromJson(jsonString, LoginResponseDTO.class);
            textView5.setText(response.getUsuario().getNombre() + " " + response.getUsuario().getApellido());

            Service sevice;
            sevice = Apis.Mediador();
            Call<HotelesResponseDTO> call = sevice.optenerhoteles("Bearer " + response.getToken());
            call.enqueue(new Callback<HotelesResponseDTO>() {
                @Override
                public void onResponse(Call<HotelesResponseDTO> call, Response<HotelesResponseDTO> response) {
                    if (response.isSuccessful()) {
                        HotelesResponseDTO res = response.body();
                        if (res.isEstado()) {
                            adapterCat = new HotelAdapter((ArrayList<HotelDTO>) res.getDatos());
                            recyclerViewCategory.setAdapter(adapterCat);
                        }
                    }
                }
                @Override
                public void onFailure(Call<HotelesResponseDTO> call, Throwable t) {

                }
            });
        }
    }

    private void initRecyclerView() {
        recyclerViewPopular = findViewById(R.id.view_pop);
        recyclerViewPopular.setLayoutManager(new LinearLayoutManager(this, LinearLayoutManager.HORIZONTAL, false));

        SharedPreferences sharedPreferences = getSharedPreferences("Sesion", Context.MODE_PRIVATE);
        String jsonString = sharedPreferences.getString("response", "");
        if (!TextUtils.isEmpty(jsonString)) {
            Gson gson = new Gson();
            LoginResponseDTO response = gson.fromJson(jsonString, LoginResponseDTO.class);
            textView5.setText(response.getUsuario().getNombre() + " " + response.getUsuario().getApellido());

            Service sevice;
            sevice = Apis.Mediador();

            Call<LugaresTuristicosDTO> call = sevice.optenerTuris("Bearer " + response.getToken());

            call.enqueue(new Callback<LugaresTuristicosDTO>() {
                @Override
                public void onResponse(Call<LugaresTuristicosDTO> call, Response<LugaresTuristicosDTO> response) {
                    if (response.isSuccessful()) {
                        LugaresTuristicosDTO res = response.body();
                        if (res.isEstado()) {
                            adapterPopular = new PupolarAdapter((ArrayList<LugarTuristicoDTO>) res.getDatos());
                            recyclerViewPopular.setAdapter(adapterPopular);
                        }
                    }
                }

                @Override
                public void onFailure(Call<LugaresTuristicosDTO> call, Throwable t) {

                }
            });

        }

    }
}