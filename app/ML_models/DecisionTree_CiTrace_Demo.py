#%% Import librerie 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import ast
from pathlib import Path
from sqlalchemy.orm import Session
from app.database.database import engine
from app.database import crud_functions

#%% Variabili globali
__version__ = "0.1.0"
BASE_DIR = Path(__file__).resolve(strict=True).parent
      
#%% Funzione modello
def retrain_components_prediction_model(db: Session):

#%% Connessione al database
    postgresql_connection = engine.connect()
    
    request = pd.read_sql("request", postgresql_connection)
    actualUser = pd.read_sql("allUsers", postgresql_connection)
    device_info = pd.read_sql("device_info", postgresql_connection)
    
    postgresql_connection.close()
    
    #%% Conversione dati categorici
    request["timestamp"] = pd.to_datetime(request["timestamp"])
    request["year"] = request.timestamp.dt.year
    request["month"] = request.timestamp.dt.month
    request["day"] = request.timestamp.dt.day
    request["day_week"] = request.timestamp.dt.day_of_week
    request["hour"] = request.timestamp.dt.hour
    request["minute"] = request.timestamp.dt.minute
    request["event"] = request["event"].astype("category")#.cat.codes
    request["component"] = request["component"].astype("category")#.cat.codes
    
    actualUser["role"] = actualUser["role"].astype("category")#.cat.codes
    actualUser["city"] = actualUser["city"].astype("category")#.cat.codes
    actualUser["main_language_used"] = actualUser["main_language_used"].astype("category")#.cat.codes
    actualUser.dtypes
    
    #%% Join tra colonne request e actualUser (Magari da inserire nel modello a kluster, non qui)
    X_r = request[["actualUser", "device_info"]]
    X_u = pd.DataFrame()
    max_interests = 0
    for user in range(0, len(actualUser)):
        model_user = crud_functions.get_user_id(db, user)
        user_interests = crud_functions.get_user_interests(db, model_user)
        for i in range(0, len(user_interests)):
            X_u.loc[user, f"i{i}"] = user_interests[i]
        if max_interests < len(user_interests):
            max_interests = len(user_interests)
    X_m = X_r.merge(X_u, left_on = "actualUser", right_index = True)
    for c in range(0, max_interests):
        X_m[f"i{c}"] = X_m[f"i{c}"].astype("category").cat.codes
        
    #%% Inserimento valori in X e y
    X = X_r[["actualUser", "device_info"]]
    y = request["component"]
    
    #%% Creazione plot del modello DecisionTree
    dtree = DecisionTreeClassifier()
    dtree = dtree.fit(X, y)
    
    tree.plot_tree(dtree)
    
    #%% Test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 100)
    
    dtree = DecisionTreeClassifier(random_state = 100)
    dtree.fit(X_train, y_train)
    
    y_pred = dtree.predict(X_test)
    print("Train data accuracy:",accuracy_score(y_true = y_train, y_pred = dtree.predict(X_train)))
    print("Test data accuracy:",accuracy_score(y_true = y_test, y_pred = y_pred))
    
    y_proba = dtree.predict_proba(X_test)
    
    #%% Riconversione in valori categorici di y_proba
    #codes = request.component.cat.codes
    categories = request["component"].cat.categories
    y_proba = pd.DataFrame(y_proba, columns = categories)
    
    #%% Esportazione modello 
    import pickle
    pickle.dump(dtree,open(f"{BASE_DIR}/decisionTree_model-{__version__}.pkl",'wb'))
    
    return{
        "Ok": True,
        "num_users_imported": f"{len(actualUser)}",
        "num_requests_imported": f"{len(request)}",
        "num_devices_imported": f"{len(device_info)}",
        "num_requests_used_for_training": f"{len(X_train)}",
        "num_requests_used_for_testing": f"{len(X_test)}",
        "Train data accuracy": f"{accuracy_score(y_true = y_train, y_pred = dtree.predict(X_train))}",
        "Test data accuracy:": f"{accuracy_score(y_true = y_test, y_pred = y_pred)}"
        }