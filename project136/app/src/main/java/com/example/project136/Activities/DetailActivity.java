package com.example.project136.Activities;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.AppCompatButton;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.example.project136.R;
import com.example.project136.dto.HotelDTO;

public class DetailActivity extends AppCompatActivity {
    private TextView titleTxt, locationTxt, descriptionTxt, scoreTxt;
    private HotelDTO item;
    private ImageView picImg, backBtn;
    AppCompatButton button;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detail);

        initView();
        setVariable();
    }
    private void setVariable() {
        item = (HotelDTO) getIntent().getSerializableExtra("object");

        titleTxt.setText(item.getNombre());
        scoreTxt.setText("4");
        locationTxt.setText(item.getUbicacion());
        descriptionTxt.setText(item.getDescripcion());
        Glide.with(this)
                .load(item.getFoto_url())
                .into(picImg);

        backBtn.setOnClickListener(v -> finish());
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent=new Intent(DetailActivity.this, listaHabitaciones.class);
                intent.putExtra("object",item);
                startActivity(intent);
            }
        });


    }
    private void initView() {
        titleTxt = findViewById(R.id.titleTxt);
        locationTxt = findViewById(R.id.locationTxt);
        scoreTxt = findViewById(R.id.scoreTxt);
        descriptionTxt = findViewById(R.id.descriptionTxt);
        picImg = findViewById(R.id.picImg);
        backBtn=findViewById(R.id.backBtn);
        button = findViewById(R.id.button);

    }
}