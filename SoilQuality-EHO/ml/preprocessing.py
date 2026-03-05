import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler, LabelEncoder

def load_and_preprocess(path):
    df = pd.read_csv(path)

    le = LabelEncoder()
    df["Soil_Type"] = le.fit_transform(df["Soil_Type"])

    X = df.drop("Output", axis=1)
    y = df["Output"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return train_test_split(X_scaled, y, test_size=0.2, random_state=42)