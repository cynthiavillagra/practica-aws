
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib

# Dataset
X, y = load_iris(return_X_y=True)

# División
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Entrenamiento
model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=200)
)
model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))

# Guardar modelo
joblib.dump(model, "model_sklearn.joblib")
