package com.example.project136.Activities;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.DisplayMetrics;
import android.widget.ImageView;
import android.widget.TextView;

import com.example.project136.Adapters.CategoryAdapter;
import com.example.project136.R;
import com.example.project136.dto.HabitacionDTO;
import com.example.project136.dto.HabitacionesResponseDTO;
import com.example.project136.dto.HotelDTO;
import com.example.project136.dto.LoginResponseDTO;
import com.example.project136.service.Service;
import com.example.project136.config.Apis;
import com.google.gson.Gson;

import java.util.ArrayList;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class listaHabitaciones extends AppCompatActivity {
    private RecyclerView.Adapter adapterPopular;
    private RecyclerView recyclerViewPopular;
    private ImageView backBtn;
    private HotelDTO item;
    private TextView hotel;
    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_lista_habitaciones);
        hotel= findViewById(R.id.hotel);
        backBtn=findViewById(R.id.backBtn);
        backBtn.setOnClickListener(v -> finish());


        item = (HotelDTO) getIntent().getSerializableExtra("object");
        hotel.setText(item.getNombre());
        recyclerViewPopular = findViewById(R.id.habotacionesñista);
        recyclerViewPopular.setLayoutManager(new LinearLayoutManager(this, LinearLayoutManager.HORIZONTAL, false));
        int numberOfColumns = calculateNumberOfColumns();
        recyclerViewPopular.setLayoutManager(new GridLayoutManager(this, numberOfColumns));
        SharedPreferences sharedPreferences = getSharedPreferences("Sesion", Context.MODE_PRIVATE);
        String jsonString = sharedPreferences.getString("response", "");
        if (!TextUtils.isEmpty(jsonString)) {
            Gson gson = new Gson();
            LoginResponseDTO response = gson.fromJson(jsonString, LoginResponseDTO.class);
            Service sevice;

            sevice = Apis.Mediador();
            Call<HabitacionesResponseDTO> call = sevice.obtenerHabitacionesPorHotel("Bearer " + response.getToken(),item.getId());
            call.enqueue(new Callback<HabitacionesResponseDTO>() {
                @Override
                public void onResponse(Call<HabitacionesResponseDTO> call, Response<HabitacionesResponseDTO> response) {
                    if (response.isSuccessful()) {
                        HabitacionesResponseDTO res = response.body();
                        if (res.isEstado()) {
                            adapterPopular = new CategoryAdapter((ArrayList<HabitacionDTO>) res.getDatos());
                            recyclerViewPopular.setAdapter(adapterPopular);
                        }
                    }
                }
                @Override
                public void onFailure(Call<HabitacionesResponseDTO> call, Throwable t) {

                }
            });
        }
    }
    private int calculateNumberOfColumns() {
        DisplayMetrics displayMetrics = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(displayMetrics);
        int screenWidth = displayMetrics.widthPixels;
        int desiredColumnWidthDp = 120;
        int columns = screenWidth / dpToPx(desiredColumnWidthDp);
        return Math.max(columns, 1);
    }

    private int dpToPx(int dp) {
        float density = getResources().getDisplayMetrics().density;
        return Math.round(dp * density);
    }

}