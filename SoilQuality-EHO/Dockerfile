FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install fastapi uvicorn numpy joblib pillow python-multipart scikit-learn tensorflow

EXPOSE 10000

CMD ["uvicorn", "ml_service.app:app", "--host", "0.0.0.0", "--port", "10000"]