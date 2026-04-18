package com.nia.nia_backend.controller;

import com.nia.nia_backend.dto.PredictionResponse;
import com.nia.nia_backend.entity.Prediction;
import com.nia.nia_backend.repository.PredictionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = {
        "http://localhost:5173",
        "https://kmsumanth1.github.io"
})
public class PredictionController {

    @Autowired
    private PredictionRepository predictionRepository;

    // ✅ FastAPI URL
    private final String ML_API_URL = "http://127.0.0.1:8000/predict";

    @PostMapping("/predict")
    public ResponseEntity<?> predict(
            @RequestParam("file") MultipartFile file,
            @RequestParam("npk") String npk
    ) {

        try {
            RestTemplate restTemplate = new RestTemplate();

            // ✅ Headers
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);

            // ✅ Convert file
            ByteArrayResource resource = new ByteArrayResource(file.getBytes()) {
                @Override
                public String getFilename() {
                    return file.getOriginalFilename();
                }
            };

            // ✅ Body
            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("file", resource);
            body.add("npk", npk);

            HttpEntity<MultiValueMap<String, Object>> requestEntity =
                    new HttpEntity<>(body, headers);

            // ✅ CALL FASTAPI (FIXED)
            ResponseEntity<PredictionResponse> response =
                    restTemplate.postForEntity(ML_API_URL, requestEntity, PredictionResponse.class);

            System.out.println("🔥 ML RESPONSE: " + response.getBody());

            PredictionResponse mlResult = response.getBody();

            // ❌ fallback if null
            if (mlResult == null) {
                return ResponseEntity.status(HttpStatus.BAD_GATEWAY)
                        .body("ML returned null");
            }

            // ✅ Save to DB
            Prediction prediction = new Prediction();
            prediction.setSoilType(mlResult.getSoil_type());
            prediction.setFertility(mlResult.getFertility());
            prediction.setNpkValues(npk);

            predictionRepository.save(prediction);

            return ResponseEntity.ok(mlResult);

        } catch (Exception e) {
            e.printStackTrace();

            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Backend Error: " + e.getMessage());
        }
    }

    // ✅ HISTORY
    @GetMapping("/history")
    public ResponseEntity<?> getHistory() {
        return ResponseEntity.ok(predictionRepository.findAll());
    }
}