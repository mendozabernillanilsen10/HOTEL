package com.example.project136.Activities;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.AppCompatButton;

import android.app.DatePickerDialog;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.DatePicker;
import android.widget.ImageView;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.example.project136.R;
import com.example.project136.dto.HabitacionDTO;
import com.example.project136.dto.LoginResponseDTO;
import com.example.project136.dto.RegistroClienteResponseDTO;
import com.example.project136.dto.ReservaDTO;
import com.example.project136.service.Service;
import com.example.project136.config.Apis;
import com.example.project136.config.Toas;
import com.google.gson.Gson;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Locale;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class Detallehabitacion extends AppCompatActivity {
    private HabitacionDTO item;
    private  AppCompatButton btnFechaFinal,btn_fecha_inicio,reservar;
    Toas toas = new Toas(this);
    private TextView titleTxt, locationTxt, scoreTxt,precio;
    private ImageView picImg, backBtn;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detallehabitacion);
        initView();
        setVariable();
    }
    private void setVariable() {
        item = (HabitacionDTO) getIntent().getSerializableExtra("object");
        titleTxt.setText("Habitacion "+item.getTipo()+"");
        scoreTxt.setText("5");
        locationTxt.setText("Numero de Habitacion   "+item.getNumero()+"");
        precio.setText("s/"+item.getPrecio());
        Glide.with(this)
                .load(item.getFoto_url())
                .into(picImg);
        backBtn.setOnClickListener(v -> finish());

        setCurrentDate();

        btn_fecha_inicio.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showDatePicker();
            }
        });

        btnFechaFinal.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showDatePickerfina();
            }
        });

        reservar.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                SharedPreferences sharedPreferences = getSharedPreferences("Sesion", Context.MODE_PRIVATE);
                String jsonString = sharedPreferences.getString("response", "");
                if (!TextUtils.isEmpty(jsonString)) {
                    Gson gson = new Gson();
                    LoginResponseDTO response = gson.fromJson(jsonString, LoginResponseDTO.class);
                    ReservaDTO dto = new ReservaDTO();
                    dto.setCliente_id(""+response.getUsuario().getId());
                    dto.setHabitacion_id(""+item.getId());
                    dto.setFecha_inicio(btn_fecha_inicio.getText().toString());
                    dto.setFecha_fin(btnFechaFinal.getText().toString());
                    dto.setEstado("Reservado");
                    Service sevice;
                    sevice = Apis.Mediador();
                    final ProgressDialog loading = ProgressDialog.show(Detallehabitacion.this, "Validando Usuario",
                            "Espere un Momento", false, false);
                    Call<RegistroClienteResponseDTO> call = sevice.registroReserva("Bearer " + response.getToken(),dto);
                    call.enqueue(new Callback<RegistroClienteResponseDTO>() {
                        @Override
                        public void onResponse(Call<RegistroClienteResponseDTO> call, Response<RegistroClienteResponseDTO> response) {
                            loading.dismiss();

                            RegistroClienteResponseDTO Response = response.body();
                            if( Response.isEstado()){
                                toas.toastCorrecto(Response.getMensaje());
                                 finish();
                            }else{
                                toas.toastIncorrecto(Response.getMensaje());
                            }
                        }

                        @Override
                        public void onFailure(Call<RegistroClienteResponseDTO> call, Throwable t) {

                        }
                    });
                }
            }
        });
    }
    private void showDatePickerfina() {
        Calendar currentDate = Calendar.getInstance();
        int year = currentDate.get(Calendar.YEAR);
        int month = currentDate.get(Calendar.MONTH);
        int day = currentDate.get(Calendar.DAY_OF_MONTH);
        DatePickerDialog datePickerDialog = new DatePickerDialog(this,
                new DatePickerDialog.OnDateSetListener() {
                    @Override
                    public void onDateSet(DatePicker datePicker, int selectedYear, int selectedMonth, int selectedDay) {
                        // Update your TextView with the selected date
                        btnFechaFinal.setText(selectedYear + "-" + (selectedMonth + 1) + "-" + selectedDay);
                    }
                }, year, month, day);

        datePickerDialog.getDatePicker().setMinDate(currentDate.getTimeInMillis());
        datePickerDialog.show();
    }

    private void showDatePicker() {
        Calendar currentDate = Calendar.getInstance();
        int year = currentDate.get(Calendar.YEAR);
        int month = currentDate.get(Calendar.MONTH);
        int day = currentDate.get(Calendar.DAY_OF_MONTH);

        DatePickerDialog datePickerDialog = new DatePickerDialog(this,
                new DatePickerDialog.OnDateSetListener() {
                    @Override
                    public void onDateSet(DatePicker datePicker, int selectedYear, int selectedMonth, int selectedDay) {
                        // Update your TextView with the selected date
                        btn_fecha_inicio.setText(selectedYear + "-" + (selectedMonth + 1) + "-" + selectedDay);
                    }
                }, year, month, day);

        datePickerDialog.getDatePicker().setMinDate(currentDate.getTimeInMillis());
        datePickerDialog.show();
    }

    private void setCurrentDate() {
        Calendar calendar = Calendar.getInstance();
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd", Locale.getDefault());
        String currentDate = dateFormat.format(calendar.getTime());
        btn_fecha_inicio.setText(currentDate);
        btnFechaFinal.setText(currentDate);
    }

    private void initView() {
        titleTxt = findViewById(R.id.titleTxt);
        locationTxt = findViewById(R.id.locationTxt);
        btnFechaFinal = findViewById(R.id.btn_fecha_final);
        btn_fecha_inicio =findViewById(R.id.btn_fecha_inicio);
        scoreTxt = findViewById(R.id.scoreTxt);
        picImg = findViewById(R.id.picImg);
        scoreTxt = findViewById(R.id.scoreTxt);
        backBtn=findViewById(R.id.backBtn);
        precio = findViewById(R.id.precio);
        reservar = findViewById(R.id.reservar);
    }
}