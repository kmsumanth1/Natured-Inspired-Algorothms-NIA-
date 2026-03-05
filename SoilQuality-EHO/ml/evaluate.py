import joblib
from sklearn.metrics import accuracy_score, classification_report
from preprocessing import load_and_preprocess

X_train, X_test, y_train, y_test = load_and_preprocess("dataset/soil_data.csv")

model = joblib.load("model.pkl")

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))