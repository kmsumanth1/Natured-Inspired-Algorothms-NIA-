from eho import EHOFeatureSelection
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

df = pd.read_csv("dataset/soil_data.csv")
X = df.drop("Output", axis=1)
y = df["Output"]

X = StandardScaler().fit_transform(X)
X, y = SMOTE(random_state=42).fit_resample(X, y)

eho = EHOFeatureSelection(n_elephants=10, n_iter=10)
eho.optimize(X, y)

plt.plot(eho.history)
plt.xlabel("Iteration")
plt.ylabel("Best Macro F1")
plt.title("EHO Convergence Curve")
plt.show()