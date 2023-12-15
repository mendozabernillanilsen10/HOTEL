package com.example.project136.Adapters;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.example.project136.R;
import com.example.project136.dto.ReservaModel;
import java.util.ArrayList;
public class reservaAdapter extends RecyclerView.Adapter<reservaAdapter.ViewHolder> {
    ArrayList<ReservaModel> items;

    public reservaAdapter(ArrayList<ReservaModel> items) {
        this.items = items;
    }

    @NonNull
    @Override
    public reservaAdapter.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View inflate = LayoutInflater.from(parent.getContext()).inflate(R.layout.iten_recerva, parent, false);
        return new ViewHolder(inflate);
    }
    @Override
    public void onBindViewHolder(@NonNull reservaAdapter.ViewHolder holder, int position) {
        holder.hotelName.setText( items.get(position).getHotel_nombre());
        holder.direccion.setText(items.get(position).getHotel_ubicacion());
        holder.numeeroHabitacion.setText(items.get(position).getHabitacion_tipo() +" #"+items.get(position).getHabitacion_numero() );
        holder.fecha_serva.setText("Fecha de inicio : "+items.get(position).getFecha_inicio());
        holder.fecha_termino.setText("Fecha de Termino : "+items.get(position).getFecha_fin());
    }
    @Override
    public int getItemCount() {
        return items.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        TextView hotelName,direccion,numeeroHabitacion,fecha_serva,fecha_termino;
        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            hotelName = itemView.findViewById(R.id.hotelName);
            direccion = itemView.findViewById(R.id.direccion);
            numeeroHabitacion = itemView.findViewById(R.id.numeeroHabitacion);
            fecha_serva = itemView.findViewById(R.id.fecha_serva);
            fecha_termino = itemView.findViewById(R.id.fecha_termino);
        }
    }
}
