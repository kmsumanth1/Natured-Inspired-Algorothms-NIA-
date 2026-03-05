package com.nia.nia_backend.dto;

public class PredictionResponse {

    private String soil_type;
    private String fertility;

    public PredictionResponse() {}

    public String getSoil_type() {
        return soil_type;
    }

    public void setSoil_type(String soil_type) {
        this.soil_type = soil_type;
    }

    public String getFertility() {
        return fertility;
    }

    public void setFertility(String fertility) {
        this.fertility = fertility;
    }
}