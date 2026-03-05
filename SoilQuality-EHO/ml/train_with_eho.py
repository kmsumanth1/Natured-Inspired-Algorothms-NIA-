from preprocessing import load_and_preprocess
from eho import EHOFeatureSelection
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import numpy as np

X_train, X_test, y_train, y_test = load_and_preprocess("dataset/soil_data.csv")

eho = EHOFeatureSelection(n_elephants=10, n_clans=2, n_iter=10)
best_features = eho.optimize(X_train, y_train)

selected_indices = np.where(best_features == 1)[0]

X_train_selected = X_train[:, selected_indices]
X_test_selected = X_test[:, selected_indices]

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42
)
model.fit(X_train_selected, y_train)

y_pred = model.predict(X_test_selected)

print("Selected Feature Indices:", selected_indices)
print(classification_report(y_test, y_pred))