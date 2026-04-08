import mlflow
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression

# training stuff
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


# DB stuff
from app.database import SessionLocal, engine

#ORM stuff
from app.models import User, Finance
from sqlalchemy.orm import joinedload

from tensorflow.keras.callbacks import EarlyStopping

import joblib

from modules.preprocess import preprocessing, split
from modules.evaluate import evaluate_performance

from os.path import join as join

mlflow.tensorflow.autolog()

def create_nn_model(input_dim):
    """
    Fonction pour créer et compiler un modèle de réseau de neurones simple.
    """
    model = Sequential()
    model.add(Dense(64, activation='relu', input_dim=input_dim))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

def train_model(model, X, y, X_val=None, y_val=None, epochs=50, batch_size=32, verbose=0 ):
    hist = model.fit(X, y,
                validation_data=(X_val, y_val) if X_val is not None and y_val is not None else None,
                epochs=epochs, batch_size=batch_size, verbose=verbose)
    return model , hist

def model_predict(model, X):
    y_pred = model.predict(X).flatten()
    return y_pred

db = SessionLocal()
query = db.query(User).options(joinedload(User.finance)).all()
db.close()

data_list = []
for u in query:
    data_list.append({
        "age": u.age,
        "situation_familiale": u.situation_familiale,
        "niveau_etude": u.niveau_etude,
        "sport_licence": u.sport_licence,
        "revenu_estime_mois": u.finance.revenu_estime_mois if u.finance else None,
        "loyer_mensuel": u.finance.loyer_mensuel if u.finance else None,
        "score_credit": u.finance.score_credit if u.finance else None,
        "montant_pret": u.finance.montant_pret if u.finance else None
    })

df = pd.DataFrame(data_list)

# preprocessor black magic
X_processed, y, preprocessor = preprocessing(df)
# backup preprocessor
joblib.dump(preprocessor, join('resources', 'preprocessor.pkl'))

# split data
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)


# entrainement du model ethique
with mlflow.start_run(run_name="Model éthique"):
    model_ethique = create_nn_model(X_train.shape[1])
    model_ethique, hist = train_model(model_ethique, X_train, y_train, X_val=X_test, y_val=y_test, verbose=1)

    perf = evaluate_performance(y_test, model_predict(model_ethique, X_test))
    mlflow.log_metrics(perf)
    # backup new model
    joblib.dump(model_ethique, join('resources', 'model_ethique.pkl'))