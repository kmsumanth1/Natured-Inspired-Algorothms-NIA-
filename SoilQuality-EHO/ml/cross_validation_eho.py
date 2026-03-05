from preprocessing import load_and_preprocess
from eho import EHOFeatureSelection
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import numpy as np

# Load full dataset (before split)
import pandas as pd
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

df = pd.read_csv("dataset/soil_data.csv")

X = df.drop("Output", axis=1)
y = df["Output"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_scaled, y)

# Apply EHO Feature Selection
eho = EHOFeatureSelection(n_elephants=10, n_clans=2, n_iter=10)
best_features = eho.optimize(X_resampled, y_resampled)

selected_indices = np.where(best_features == 1)[0]
X_selected = X_resampled[:, selected_indices]

# Tuned Random Forest (use best config)
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42
)

scores = cross_val_score(
    model,
    X_selected,
    y_resampled,
    cv=5,
    scoring="f1_macro"
)

print("Selected Features:", selected_indices)
print("5-Fold Macro F1 Scores:", scores)
print("Average Macro F1:", scores.mean())