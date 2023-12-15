package com.example.project136.Activities;

import androidx.appcompat.app.AppCompatActivity;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.example.project136.R;
import com.example.project136.dto.LoginResponseDTO;
import com.example.project136.dto.UsuarioDTO;
import com.example.project136.service.Service;
import com.example.project136.config.Apis;
import com.example.project136.config.Toas;
import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;
import com.google.gson.Gson;

public class Login extends AppCompatActivity {
    TextInputLayout layoutUser ;
    TextInputEditText inputUser ;
    TextInputLayout layoutClave;
    TextInputEditText inputClave ;
    TextView registro;
    Button addToCartBtn;
    Toas toas = new Toas(this);


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        addToCartBtn =findViewById(R.id.addToCartBtn);
        layoutUser = findViewById(R.id.layoutuser);
        inputUser = findViewById(R.id.inputsuser);
        registro=findViewById(R.id.registro);
        layoutClave = findViewById(R.id.layutclave);
        inputClave = findViewById(R.id.edtEclave);
        obtenerPreferencias();
        registro.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent in = new Intent(Login.this , RegistroClientes.class);
                startActivity(in);
            }
        });
        addToCartBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                valida_login1();
            }
        });

    }

    private void valida_login1() {
        // Obtén los valores ingresados por el usuario
        String usuario = inputUser.getText().toString();
        String clave = inputClave.getText().toString();
        boolean isValid = true;

        if (TextUtils.isEmpty(usuario)) {
            layoutUser.setError("Ingrese un nombre de usuario válido");
            isValid = false;
        } else {
            layoutUser.setError(null);
        }

        if (TextUtils.isEmpty(clave)) {
            layoutClave.setError("Ingrese una contraseña válida");
            isValid = false;
        } else {
            layoutClave.setError(null);
        }
        if (isValid) {
            UsuarioDTO user= new UsuarioDTO(usuario,clave);

            valida_login(user);
        }
    }
    public void valida_login(UsuarioDTO user) {

        Service sevice;
        sevice = Apis.Mediador();
        Call<LoginResponseDTO> call = sevice.login(user);

        final ProgressDialog loading = ProgressDialog.show(Login.this, "Validando Usuario",
                "Espere un Momento", false, false);
        call.enqueue(new Callback<LoginResponseDTO>() {
            @Override
            public void onResponse(Call<LoginResponseDTO> call, Response<LoginResponseDTO> response) {
                loading.dismiss();

                LoginResponseDTO Response = response.body();
                if( Response.isEstado()){
                    iniciar_sesion(Response);
                    toas.toastCorrecto(Response.getMensaje());
                    Intent inte = new Intent(Login.this, MainActivity.class);
                    startActivity(inte);
                }else{
                    toas.toastIncorrecto(Response.getMensaje());
                }
            }
            @Override
            public void onFailure(Call<LoginResponseDTO> call, Throwable t) {
                loading.dismiss();

            }
        });


    }

    private void iniciar_sesion(LoginResponseDTO response) {
        Gson gson = new Gson();
        String objetoJson = gson.toJson(response);
        SharedPreferences iniciar_sesion = getSharedPreferences("Sesion", Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = iniciar_sesion.edit();
        editor.putString("response", objetoJson);
        editor.putString("Email", layoutUser.getEditText().getText().toString());
        editor.putString("claveSE", layoutClave.getEditText().getText().toString());
        editor.commit();
    }

    public void obtenerPreferencias(){
        SharedPreferences sharedPreferences= getSharedPreferences("Sesion", Context.MODE_PRIVATE);
        layoutUser.getEditText().setText(sharedPreferences.getString("Email",""));
        layoutClave.getEditText().setText(sharedPreferences.getString("claveSE",""));
    }
}