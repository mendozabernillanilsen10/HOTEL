package com.example.project136.config;

import com.example.project136.service.Service;

public class Apis  {

    public static final String URL_001= "https://ballenaruiz27.pythonanywhere.com/";

    public static Service Mediador(){
        return  Cliente.getClient(URL_001).create(Service.class);
    }


}
