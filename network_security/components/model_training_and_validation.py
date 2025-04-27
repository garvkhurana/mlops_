import os
import sys
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException
from network_security.entity.config_entity import ModelTrainerConfig
from network_security.utils import model_metrics, print_evaluated_results, save_object

class ModelTraining:
    def __init__(self, model_training_config=ModelTrainerConfig):
        self.model_training_config = model_training_config

    def hyperparameter_tuning(self, models, xtrain, ytrain):
        try:
            best_models = {}
            for model_name, model in models.items():
                logging.info(f"Starting hyperparameter tuning for {model_name}")
                
                

                if model_name == "K-Neighbors Classifier":
                    param_grid = {'n_neighbors': list(range(2,31))}
                    grid = GridSearchCV(model, param_grid, scoring='accuracy', cv=5, n_jobs=-1)
                    grid.fit(xtrain, ytrain)
                    best_models[model_name] = (grid.best_estimator_, grid.best_params_, grid.best_score_)

                elif model_name == "XGBClassifier":
                    param_dist = {'n_estimators': [100,200,300], 'learning_rate': [0.01,0.1,0.2], 
                                  'max_depth': [3,6,10], 'subsample': [0.8,0.9,1.0]}
                    rscv = RandomizedSearchCV(model, param_dist, scoring='accuracy', cv=5, n_jobs=-1)
                    rscv.fit(xtrain, ytrain)
                    best_models[model_name] = (rscv.best_estimator_, rscv.best_params_, rscv.best_score_)

                elif model_name == "Random Forest Classifier":
                    param_grid = {'n_estimators': [50,100,200], 'max_depth': [5,10,15], 'min_samples_split': [2,5,10]}
                    grid = GridSearchCV(model, param_grid, scoring='accuracy', cv=5, n_jobs=-1)
                    grid.fit(xtrain, ytrain)
                    best_models[model_name] = (grid.best_estimator_, grid.best_params_, grid.best_score_)

                elif model_name == "Decision Tree":
                    param_grid = {'max_depth': [3,5,10], 'min_samples_split': [2,5,10]}
                    grid = GridSearchCV(model, param_grid, scoring='accuracy', cv=5, n_jobs=-1)
                    grid.fit(xtrain, ytrain)
                    best_models[model_name] = (grid.best_estimator_, grid.best_params_, grid.best_score_)

                elif model_name == "Logistic Regression":
                    model.fit(xtrain, ytrain)
                    best_models[model_name] = (model, None, model.score(xtrain, ytrain))

                elif model_name == "Naive Bayes":
                    model.fit(xtrain, ytrain)
                    best_models[model_name] = (model, None, model.score(xtrain, ytrain))

                elif model_name == "SVC":
                    param_grid = {'C': [0.1,1,10], 'kernel': ['linear','rbf','poly'], 'gamma': ['scale','auto']}
                    grid = GridSearchCV(model, param_grid, scoring='accuracy', cv=5, n_jobs=-1)
                    grid.fit(xtrain, ytrain)
                    best_models[model_name] = (grid.best_estimator_, grid.best_params_, grid.best_score_)

                

            return best_models
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def model_training(self, x_train, y_train, x_test, y_test):
        try:
            models = {
                "Logistic Regression": LogisticRegression(),
                "Decision Tree": DecisionTreeClassifier(),
                "K-Neighbors Classifier": KNeighborsClassifier(),
                "SVC": SVC(),
                "Random Forest Classifier": RandomForestClassifier(),
                "Naive Bayes": GaussianNB(),
                "XGBClassifier": XGBClassifier()
            }

            best_models = self.hyperparameter_tuning(models, x_train, y_train)

            best_model_name = max(best_models, key=lambda x: best_models[x][2])
            best_model, best_params, best_score = best_models[best_model_name]

            best_model_path = os.path.join("artifacts", "best_model.pkl")
            os.makedirs(os.path.dirname(best_model_path), exist_ok=True)
            save_object(best_model_path, best_model)

            print(f"Best Model Found: {best_model_name} with Accuracy: {best_score}")
            logging.info(f"Best Model Found: {best_model_name} with Accuracy: {best_score}")

            print("\nEvaluating Best Model on Train and Test Data:")
            print_evaluated_results(x_train, y_train, x_test, y_test, best_model)

            mlflow.set_experiment("Model_Training_Classification")

            with mlflow.start_run():
                mlflow.set_tag("model_type", best_model_name)

                if best_params is not None:
                    mlflow.log_params(best_params)

                y_train_pred = best_model.predict(x_train)
                y_test_pred = best_model.predict(x_test)

                train_mae, train_rmse, train_r2 = model_metrics(y_train, y_train_pred)
                test_mae, test_rmse, test_r2 = model_metrics(y_test, y_test_pred)

                mlflow.log_metric("train_mae", train_mae)
                mlflow.log_metric("train_rmse", train_rmse)
                mlflow.log_metric("train_r2", train_r2)

                mlflow.log_metric("test_mae", test_mae)
                mlflow.log_metric("test_rmse", test_rmse)
                mlflow.log_metric("test_r2", test_r2)

                mlflow.sklearn.log_model(best_model, "model")

        except Exception as e:
            raise NetworkSecurityException(e, sys)
