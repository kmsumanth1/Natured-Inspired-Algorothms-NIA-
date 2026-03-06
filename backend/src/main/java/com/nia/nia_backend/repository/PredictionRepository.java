package com.nia.nia_backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.nia.nia_backend.entity.Prediction;

public interface PredictionRepository extends JpaRepository<Prediction, Long> {
}