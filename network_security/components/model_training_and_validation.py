from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
import logging

models = {
    "Logistic Regression": LogisticRegression(),
    "Decision Tree": DecisionTreeClassifier(),
    "K-Neighbors Classifier": KNeighborsClassifier(),
    "SVC": SVC(),
    "Random Forest Classifier": RandomForestClassifier(),
    "Naive Bayes": GaussianNB(),
    "GradientBoosting Classifier": GradientBoostingClassifier(),
    "CatBoosting Classifier": CatBoostClassifier(verbose=False),
    "XGBClassifier": XGBClassifier()
}

def hyperparameter_tuning(models, xtrain, ytrain):
    best_models = {}

    for model_name, model in models.items():
        logging.info(f"Starting hyperparameter tuning for {model_name}")
        
        if model_name == "CatBoosting Classifier":
            param_dist = {'depth': [4, 5, 6, 7, 8, 9, 10],
                          'learning_rate': [0.01, 0.02, 0.03, 0.04],
                          'iterations': [300, 400, 500, 600]}
            rscv = RandomizedSearchCV(model, param_dist, scoring='accuracy', cv=5, n_jobs=-1)
            rscv.fit(xtrain, ytrain)
            best_models[model_name] = (rscv.best_estimator_, rscv.best_params_, rscv.best_score_)

        elif model_name == "K-Neighbors Classifier":
            param_grid = {'n_neighbors': list(range(2, 31))}
            grid = GridSearchCV(model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
            grid.fit(xtrain, ytrain)
            best_models[model_name] = (grid.best_estimator_, grid.best_params_, grid.best_score_)

        elif model_name == "XGBClassifier":
            param_dist = {'n_estimators': [100, 200, 300], 'learning_rate': [0.01, 0.1, 0.2], 
                          'max_depth': [3, 6, 10], 'subsample': [0.8, 0.9, 1.0]}
            rscv = RandomizedSearchCV(model, param_dist, scoring='accuracy', cv=5, n_jobs=-1)
            rscv.fit(xtrain, ytrain)
            best_models[model_name] = (rscv.best_estimator_, rscv.best_params_, rscv.best_score_)

        elif model_name == "Random Forest Classifier":
            param_grid = {'n_estimators': [50, 100, 200], 'max_depth': [5, 10, 15], 'min_samples_split': [2, 5, 10]}
            grid = GridSearchCV(model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
            grid.fit(xtrain, ytrain)
            best_models[model_name] = (grid.best_estimator_, grid.best_params_, grid.best_score_)

        elif model_name == "Decision Tree":
            param_grid = {'max_depth': [3, 5, 10], 'min_samples_split': [2, 5, 10]}
            grid = GridSearchCV(model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
            grid.fit(xtrain, ytrain)
            best_models[model_name] = (grid.best_estimator_, grid.best_params_, grid.best_score_)

        elif model_name == "Logistic Regression":
            model.fit(xtrain, ytrain)
            best_models[model_name] = (model, None, model.score(xtrain, ytrain))

        elif model_name == "Naive Bayes":
            model.fit(xtrain, ytrain)
            best_models[model_name] = (model, None, model.score(xtrain, ytrain))

        elif model_name == "SVC":
            param_grid = {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf', 'poly'], 'gamma': ['scale', 'auto']}
            grid = GridSearchCV(model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
            grid.fit(xtrain, ytrain)
            best_models[model_name] = (grid.best_estimator_, grid.best_params_, grid.best_score_)

        elif model_name == "GradientBoosting Classifier":
            param_grid = {'n_estimators': [100, 200], 'learning_rate': [0.01, 0.05, 0.1], 'max_depth': [3, 5, 10]}
            grid = GridSearchCV(model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
            grid.fit(xtrain, ytrain)
            best_models[model_name] = (grid.best_estimator_, grid.best_params_, grid.best_score_)

        print(f"Best {model_name} Parameters: {best_models[model_name][1]}")
        print(f"Best {model_name} Score: {best_models[model_name][2]}")
        logging.info(f"Best {model_name} Parameters: {best_models[model_name][1]}")
        logging.info(f"Best {model_name} Score: {best_models[model_name][2]}")
        print("====================================================================================")

    return best_models


