package com.example.project136.Adapters;

import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.resource.bitmap.CenterCrop;
import com.bumptech.glide.load.resource.bitmap.GranularRoundedCorners;
import com.example.project136.Activities.DetailActivity;
import com.example.project136.R;
import com.example.project136.dto.LugarTuristicoDTO;

import java.text.DecimalFormat;
import java.util.ArrayList;
public class PupolarAdapter extends RecyclerView.Adapter<PupolarAdapter.ViewHolder> {
    ArrayList<LugarTuristicoDTO> items;

    public PupolarAdapter(ArrayList<LugarTuristicoDTO> items) {
        this.items = items;
    }

    @NonNull
    @Override
    public PupolarAdapter.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View inflate = LayoutInflater.from(parent.getContext()).inflate(R.layout.viewholder_popular, parent, false);
        return new ViewHolder(inflate);
    }
    @Override
    public void onBindViewHolder(@NonNull PupolarAdapter.ViewHolder holder, int position) {
        holder.titleTxt.setText(items.get(position).getNombre());
        holder.locationTxt.setText(items.get(position).getUbicacion());
        holder.scoreTxt.setText("5.00" );


        Glide.with(holder.itemView.getContext())
                .load(items.get(position).getFoto_url()+"")
                .transform(new CenterCrop(), new GranularRoundedCorners(40, 40, 40, 40))
                .into(holder.pic);


      /*  holder.itemView.setOnClickListener(v -> {
            Intent intent=new Intent(holder.itemView.getContext(), DetailActivity.class);
            intent.putExtra("object",items.get(position));
            holder.itemView.getContext().startActivity(intent);
        });
        */

    }

    @Override
    public int getItemCount() {
        return items.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        TextView titleTxt, locationTxt, scoreTxt;
        ImageView pic;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            titleTxt = itemView.findViewById(R.id.titleTxt);
            locationTxt = itemView.findViewById(R.id.locationTxt);
            scoreTxt = itemView.findViewById(R.id.scoreTxt);
            pic = itemView.findViewById(R.id.picImg);
        }
    }
}
