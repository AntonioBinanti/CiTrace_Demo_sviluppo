import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from pathlib import Path
from sqlalchemy.orm import Session
from app.database.database import engine
from app.database import crud_functions


#%% Variabili globali
__version__ = "0.1.0"
BASE_DIR = Path(__file__).resolve(strict=True).parent

"""
# %% 
resource = pd.read_csv("C:\\Users\\AntonioBinanti\\Documents\\CiTrace\\Datasets\\single_resource.csv")
resource

# %% Conversione dati categorici
resource["time"] = pd.to_datetime(resource["time"])
resource["year"] = resource.time.dt.year
resource["month"] = resource.time.dt.month
resource["day"] = resource.time.dt.day
resource["day_week"] = resource.time.dt.day_of_week
resource["hour"] = resource.time.dt.hour
resource["minute"] = resource.time.dt.minute
resource["resource_id"] = resource["resource"].astype("category").cat.codes
resource["browser_id"] = resource["browser_url"].astype("category").cat.codes
resource["application_id"] = resource["application"].astype("category").cat.codes
resource["application_name_id"] = resource["application_name"].astype("category").cat.codes
resource["action_id"] = resource["action"].astype("category").cat.codes
resource.dtypes

# %% Inserimento valori di X e y
X = ["resource_id", "application_id", "year", "month", "day", "hour", "minute", "day_week"]
y = ["log_type"]

#%% Inserimento modello DecisionTree
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier

features = X

dtree = DecisionTreeClassifier()
dtree = dtree.fit(resource[X], resource[y])

tree.plot_tree(dtree, feature_names = features)

#%% Test
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


X_train, X_test, y_train, y_test = train_test_split(resource[X], resource[y], test_size = 0.15, random_state = 100)

dtree = DecisionTreeClassifier(random_state = 100)
dtree.fit(X_train,y_train)

y_pred = dtree.predict(X_test)

print("Train data accuracy:",accuracy_score(y_true = y_train, y_pred = dtree.predict(X_train)))
print("Test data accuracy:",accuracy_score(y_true = y_test, y_pred = y_pred))

#%% Test Bagging Classifier
from sklearn.ensemble import BaggingClassifier
X_train, X_test, y_train, y_test = train_test_split(resource[X], resource[y], test_size = 0.15, random_state = 100)

estimator_range = [1,2,4,6,8,10,12,14,16]

models = []
scores = []

for n_estimators in estimator_range:

    # Create bagging classifier
    clf = BaggingClassifier(n_estimators = n_estimators, random_state = 100)

    # Fit the model
    clf.fit(X_train, y_train)

    # Append the model and score to their respective list
    models.append(clf)
    scores.append(accuracy_score(y_true = y_test, y_pred = clf.predict(X_test)))

# Generate the plot of scores against number of estimators
plt.figure(figsize=(9,6))
plt.plot(estimator_range, scores)

# Adjust labels and font (to make visable)
plt.xlabel("n_estimators", fontsize = 18)
plt.ylabel("score", fontsize = 18)
plt.tick_params(labelsize = 16)

# Visualize plot
#plt.show()

#%% Predizioni
to_predict = [[0, 0, 2020, 4, 15, 14, 35, 0], #log_type = 6
              [0, 0, 2020, 11, 9, 16, 0, 0], #log_type = 0
              [0, 0, 2023, 12, 8, 18, 30, 3], #log_type = 1
              [0, 0, 2024, 12, 2, 16, 31, 0], #log_type = 3
              [0, 0, 2025, 7, 3, 19, 0, 3], #log_type = 4
              [0, 0, 2020, 4, 16, 14, 35, 1], #log_type = 6
              [0, 1, 2023, 6, 23, 0, 0, 4], #log_type = 7
              [0, 0, 2024, 2, 17, 11, 0, 5], #log_type = 8
              [0, 0, 2023, 8, 25, 19, 15, 6], #log_type = 9
              [0, 1, 2023, 6, 25, 0, 0, 6], #log_type = 7
              [0, 0, 2024, 2, 20, 11, 0, 1], #log_type = 8
              [0, 1, 2023, 6, 27, 0, 0, 1], #log_type = 7
              [0, 0, 2020, 11, 11, 16, 0, 2], #log_type = 0
              [0, 1, 2023, 6, 20, 0, 0, 2], #log_type = 7
              [0, 1, 2023, 6, 20, 0, 0, 2], #log_type = 7
              ]

y_pred = dtree.predict(to_predict)
y_pred
"""

#%% Funzione di retraining
def retrain_action_prediction_model(db: Session):
#%% Connessione al database
    postgresql_connection = engine.connect()
    resource = pd.read_sql("request", postgresql_connection)
    actualUser = pd.read_sql("allUsers", postgresql_connection)
    postgresql_connection.close()

    # %% Conversione dati categorici
    resource["time"] = pd.to_datetime(resource["timestamp"])
    resource["year"] = resource.time.dt.year
    resource["month"] = resource.time.dt.month
    resource["day"] = resource.time.dt.day
    resource["day_week"] = resource.time.dt.day_of_week
    resource["hour"] = resource.time.dt.hour
    resource["minute"] = resource.time.dt.minute
    resource["user_id"] = resource["actualUser"].astype("category").cat.codes
    #resource["resource_id"] = resource["resource"].astype("category").cat.codes
    resource["browser_id"] = resource["page_url_current"].astype("category").cat.codes
    #resource["application_id"] = resource["application"].astype("category").cat.codes
    #resource["application_name_id"] = resource["application_name"].astype("category").cat.codes
    #resource["action_id"] = resource["action"].astype("category").cat.codes
    resource["event_id"] = resource["event"].astype("category").cat.codes
    resource.dtypes

    # %% Inserimento valori di X e y
    X = ["user_id", "browser_id", "year", "month", "day", "hour", "minute", "day_week"]
    y = ["event_id"]

    #%% Inserimento modello DecisionTree
    import matplotlib.pyplot as plt
    from sklearn import tree
    from sklearn.tree import DecisionTreeClassifier

    #features = X
    
    dtree = DecisionTreeClassifier()
    dtree = dtree.fit(resource[X], resource[y]) #ERRORE QUI

    #tree.plot_tree(dtree, feature_names = features)

    #%% Test
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score


    X_train, X_test, y_train, y_test = train_test_split(resource[X], resource[y], test_size = 0.15, random_state = 100)

    dtree = DecisionTreeClassifier(random_state = 100)
    dtree.fit(X_train,y_train)

    y_pred = dtree.predict(X_test)

    print("Train data accuracy:",accuracy_score(y_true = y_train, y_pred = dtree.predict(X_train)))
    print("Test data accuracy:",accuracy_score(y_true = y_test, y_pred = y_pred))

#%% PROVA ESPORTAZIONE MODELLO, SCALER, COMPONENTS E PCA
    import pickle

    pickle.dump(dtree,open(f"{BASE_DIR}/action_predictor_model-{__version__}.pkl",'wb'))

    return {
        "Ok": True,
        "num_users_imported": f"{len(actualUser)}",
        "num_requests_imported": f"{len(resource)}",
        "Train data accuracy": f"{accuracy_score(y_true = y_train, y_pred = dtree.predict(X_train))}",
        "Test data accuracy:": f"{accuracy_score(y_true = y_test, y_pred = y_pred)}"
        }
    
