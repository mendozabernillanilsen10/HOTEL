package com.example.project136.Activities;

import androidx.appcompat.app.AppCompatActivity;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.example.project136.R;
import com.example.project136.dto.RegistroClienteResponseDTO;
import com.example.project136.dto.UsuarioDTO;
import com.example.project136.service.Service;
import com.example.project136.config.Apis;
import com.example.project136.config.Toas;
import com.google.android.material.textfield.TextInputEditText;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class RegistroClientes extends AppCompatActivity {
    private TextInputEditText edtDni, edtPassword, edtApellido, edtLugarProcedencia, edtNombre;
    private Button btnIniciar;
    Toas toas = new Toas(this);
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_registro_clientes);
        // Inicializar las vistas
        edtDni = findViewById(R.id.inputsuser);
        edtPassword = findViewById(R.id.edtEclave);
        edtApellido = findViewById(R.id.edtApellido);
        edtLugarProcedencia = findViewById(R.id.edtLugarProcedencia);
        edtNombre = findViewById(R.id.edtNombre);
        btnIniciar = findViewById(R.id.addToCartBtn);

        btnIniciar.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // Obtener los valores del formulario
                String dni = edtDni.getText().toString();
                String password = edtPassword.getText().toString();
                String apellido = edtApellido.getText().toString();
                String lugarProcedencia = edtLugarProcedencia.getText().toString();
                String nombre = edtNombre.getText().toString();

                // Validar que los campos no estén vacíos
                if (dni.isEmpty() || password.isEmpty() || apellido.isEmpty() || lugarProcedencia.isEmpty() || nombre.isEmpty()) {

                    toas.toastIncorrecto("algunos campos estan vacios");

                } else {
                    UsuarioDTO user = new UsuarioDTO(dni, password, apellido, lugarProcedencia, nombre);
                   procesoRegistro(user);
                }
            }
        });
    }

    private void procesoRegistro(UsuarioDTO user) {
        Service sevice;
        sevice = Apis.Mediador();
        Call<RegistroClienteResponseDTO> call = sevice.RegistroUsuario(user);
        final ProgressDialog loading = ProgressDialog.show(RegistroClientes.this, "Validando Usuario",
                "Espere un Momento", false, false);

        call.enqueue(new Callback<RegistroClienteResponseDTO>() {
            @Override
            public void onResponse(Call<RegistroClienteResponseDTO> call, Response<RegistroClienteResponseDTO> response) {
                loading.dismiss();

                RegistroClienteResponseDTO Response = response.body();
                if( Response.isEstado()){
                    toas.toastCorrecto(Response.getMensaje());
                    Intent inte = new Intent(RegistroClientes.this, Login.class);
                    startActivity(inte);
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