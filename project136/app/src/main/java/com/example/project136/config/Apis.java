package com.example.project136.config;

import com.example.project136.service.Service;

public class Apis  {

    public static final String URL_001= "http://172.20.10.5:5000/";

    public static Service Mediador(){
        return  Cliente.getClient(URL_001).create(Service.class);
    }


}
