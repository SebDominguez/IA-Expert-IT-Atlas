import mlflow
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression

from tensorflow.keras.callbacks import EarlyStopping

import joblib

from modules.preprocess import preprocessing, split
from models.models import create_nn_model, train_model, model_predict
from modules.evaluate import evaluate_performance

from os.path import join as join

# todo
# 1a re-cree le model 2024 a partir des data de 2024
# 1b evaluer le model de 2024 avec les data de 2026
# 2 re-entrainer le model de 2024 a partir des data de 2026
# 3a cree un nouveau model a partor des data de 2026
# 3b mesurer les performances du model de 2026 avec les data de 2026

mlflow.tensorflow.autolog()

df_old = pd.read_csv(join('data', 'df_old.csv'))
X_2024, y_2024, _ = preprocessing(df_old)
X_2024_train, X_2024_test, y_2024_train, y_2024_test = split(X_2024, y_2024)


df_new = pd.read_csv(join('data', 'df_new.csv'))
X_2026, y_2026, _ = preprocessing(df_new)
X_2026_train, X_2026_test, y_2026_train, y_2026_test = split(X_2026, y_2026)

# 1a re-cree le model 2024 a partir des data de 2024
with mlflow.start_run(run_name="Nouveau model data 2024"):
    model_2024 = create_nn_model(X_2024_train.shape[1])
    model_2024, _ = train_model(model_2024, X_2024_train, y_2024_train, X_val=X_2024_test, y_val=y_2024_test)
    perf = evaluate_performance(y_2024_test, model_predict(model_2024, X_2024_test))
    mlflow.log_metrics(perf)
    # backup new model
    joblib.dump(model_2024, join('models', 'model_2024.pkl'))

#1b evaluer le model 2024 avec les donnees de 2026
with mlflow.start_run(run_name="Model 2024 avec data 2026"):
    model_2024 = joblib.load(join('models', 'model_2024.pkl'))
    y_pred = model_predict(model_2024, X_2026_test)
    perf = evaluate_performance(y_2026_test, y_pred)
    mlflow.log_metrics(perf)


# 2 re-entrainer le model de 2024 a partir des data de 2026
with mlflow.start_run(run_name="Model 2024 avec data 2026"):
    model_2024_maj, _ = train_model(model_2024, X_2026_train, y_2026_train, X_val=X_2026_test, y_val=y_2026_test)
    perf = evaluate_performance(y_2026_test, model_predict(model_2024_maj, X_2026_test))
    mlflow.log_metrics(perf)
    joblib.dump(model_2024_maj, join('models', 'model_maj_2024.pkl'))


# 3a cree un nouveau model a partor des data de 2026
with mlflow.start_run(run_name="Model 2026 data 2026"):
    model_2026 = create_nn_model(X_2026_train.shape[1])
    model_2026, _ = train_model(model_2026, X_2026_train, y_2026_train, X_val=X_2026_test, y_val=y_2026_test)
    perf = evaluate_performance(y_2026_test, model_predict(model_2026, X_2026_test))
    mlflow.log_metrics(perf)
    joblib.dump(model_2026, join('models', 'model_2026.pkl'))

# 3b mesurer les performances du model de 2026 avec les data de 2026
with mlflow.start_run(run_name="Model 2026 data 2024"):
    model_2026 = joblib.load(join('models', 'model_2026.pkl'))

    y_pred = model_predict(model_2026, X_2024_test)
    perf = evaluate_performance(y_2024_test, y_pred)
    mlflow.log_metrics(perf)