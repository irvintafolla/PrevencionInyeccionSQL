import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

df = pd.read_csv("backend/dataset/Codigos.csv")

df["code"] = df["code"].fillna("")

df = df.dropna(subset=["label"])

X = df["code"]
y = df["label"]

vectorizer = TfidfVectorizer(stop_words="english", max_features=80000)
X = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Precision del modelo: {accuracy:.2%}")

joblib.dump(clf, "backend/modelos/Modelo_de_Deteccion.pkl")
joblib.dump(vectorizer, "backend/modelos/vectorizador.pkl")

print ("Modelo creado y guardado con exito!")