from sklearn.ensemble import RandomForestClassifier
from preprocessing import load_and_preprocess
import joblib

X_train, X_test, y_train, y_test = load_and_preprocess("dataset/soil_data.csv")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)
model.fit(X_train, y_train)

joblib.dump(model, "model.pkl")

print("Model trained successfully!")
print(y_train.value_counts())