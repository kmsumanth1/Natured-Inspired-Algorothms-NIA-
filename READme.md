 =================Hybrid AI Soil Classification & Fertility System=========================

This project is a full-stack AI-based soil analysis system that predicts the type of soil and its fertility level using both soil images and nutrient parameters. The system combines deep learning for soil image classification with machine learning models for fertility prediction, providing results through an interactive web application.

The main goal of this system is to assist farmers, agricultural researchers, and soil analysts in understanding soil conditions more efficiently and making better crop-related decisions.

 ==================Features=====================

 Soil Type Classification using a deep learning CNN model

 Soil Fertility Prediction using nutrient parameters such as N, P, K, pH, EC, and micronutrients

 Hybrid AI Approach combining image-based deep learning with tabular machine learning models

 Interactive Dashboard to visualize soil distribution and prediction statistics

 Prediction History Storage using a relational database

 Full Stack Web Application with a modern user interface

======================Technologies Used=========================
=========Frontend=========

React (Vite)

Tailwind CSS

Recharts

===========Backend================

Spring Boot (Java)

===========AI / Machine Learning================

Python

TensorFlow

Scikit-learn

FastAPI

==================Database====================

MySQL

==================AI Techniques================

Convolutional Neural Networks (CNN)

MobileNetV2 Transfer Learning

Random Forest Classifier

Elephant Herd Optimization (EHO)

SMOTE for handling class imbalance

====================== System Architecture===================

The system is built using a three-layer architecture:

1️ Frontend (React)

Allows users to upload soil images

Accepts nutrient parameters

Displays soil type, fertility prediction, and statistics

2️ Backend (Spring Boot)

Handles API requests

Communicates with the AI model service

Stores prediction results in the database

3️ AI Model Service (FastAPI + Python)

Performs soil image classification using CNN

Predicts soil fertility using machine learning

Sends results back to the backend

======================= Soil Types Supported==================

The system currently classifies the following soil types:

Alluvial Soil

Arid Soil

Black Soil

Laterite Soil

Mountain Soil

Red Soil

Yellow Soil

 How to Run the Project
1️. Start the AI Model Service
cd SoilQuality-EHO/ml_service
py -3.11 -m uvicorn app:app --reload --port 8000 or python  -m uvicorn app:app --reload --port 8000
2️. Run Spring Boot Backend
cd nia-backend
mvn spring-boot:run
3️. Start React Frontend
cd nia-frontend-clean
npm install
npm run dev

Open the application in your browser:

http://localhost:5173
===================== Model Performance=======================

CNN soil classification model trained using MobileNetV2 transfer learning

Achieved ~80–83% validation accuracy

Model performance improved using fine-tuning and class balancing techniques

 ==================Future Improvements========================

Possible enhancements for this system include:

Crop recommendation system based on soil fertility

Mobile application for farmers

Integration with IoT soil sensors

Larger dataset for improved model accuracy

 =========================Author=============================

KM Sumanth

This project was developed as a hybrid AI-based soil analysis system integrating deep learning, machine learning, and full-stack web technologies.
