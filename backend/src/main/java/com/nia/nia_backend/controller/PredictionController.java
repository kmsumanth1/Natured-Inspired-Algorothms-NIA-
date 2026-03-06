package com.nia.nia_backend.controller;

import com.nia.nia_backend.dto.PredictionResponse;
import com.nia.nia_backend.entity.Prediction;
import com.nia.nia_backend.repository.PredictionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;

import java.io.IOException;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = {
        "http://localhost:5173",
        "https://kmsumanth1.github.io"
})
public class PredictionController {

    @Autowired
    private PredictionRepository predictionRepository;

    @PostMapping("/predict")
    public ResponseEntity<?> predict(
            @RequestParam("file") MultipartFile file,
            @RequestParam("npk") String npk
    ) throws IOException {

        RestTemplate restTemplate = new RestTemplate();
        String lUrl = "http://localhost:8000/predict";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        ByteArrayResource resource = new ByteArrayResource(file.getBytes()) {
            @Override
            public String getFilename() {
                return file.getOriginalFilename();
            }
        };

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", resource);
        body.add("npk", npk);

        HttpEntity<MultiValueMap<String, Object>> requestEntity =
                new HttpEntity<>(body, headers);

        ResponseEntity<PredictionResponse> response =
                restTemplate.postForEntity(lUrl, requestEntity, PredictionResponse.class);

        PredictionResponse mlResult = response.getBody();

        Prediction prediction = new Prediction();
        prediction.setSoilType(mlResult.getSoil_type());
        prediction.setFertility(mlResult.getFertility());
        prediction.setNpkValues(npk);

        predictionRepository.save(prediction);

        return ResponseEntity.ok(mlResult);
    }

    @GetMapping("/history")
    public ResponseEntity<?> getHistory() {
        return ResponseEntity.ok(predictionRepository.findAll());
    }
}