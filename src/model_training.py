import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from scipy.stats import randint
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_fuctions import read_yaml, load_data


logger = get_logger('Model-Training')


class ModelTraining:

    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.random_search_params = RANDOM_SEARCH_PARAMS
        self.params_dist = LIGHTGBM_PARAMS
    
    def load_and_split_data(self):
        try:
            logger.info(f"Loading data from {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading data from {self.test_path}")
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=['booking_status'])
            y_train = train_df['booking_status']

            X_test = test_df.drop(columns=['booking_status'])
            y_test = test_df['booking_status']

            logger.info("Data loaded and split successfully")

            return X_train, y_train, X_test, y_test
        
        except Exception as e:
            logger.error(f"Error loading and splitting data: {e}")
            raise CustomException("Failed to load and split data", e)
        
    def train_lgbm(self, X_train, y_train):
        try: 
            logger.info("Initializing our model")
            model = lgb.LGBMClassifier(random_state=self.random_search_params['random_state'])

            logger.info("Starting Hyper-parameter tuning with RandomizedSearchCV")
            random_search = RandomizedSearchCV(
                estimator=model, 
                param_distributions=self.params_dist, 
                n_iter=self.random_search_params['n_iter'], 
                cv=self.random_search_params['cv'], 
                random_state=self.random_search_params['random_state'],
                n_jobs=self.random_search_params['n_jobs'],
                verbose=self.random_search_params['verbose'],
                scoring=self.random_search_params['scorring']
            )

            random_search.fit(X_train, y_train)
            logger.info("Hyper-parameter tuning completed")

            best_params = random_search.best_params_
            logger.info(f"Best parameters found: {best_params}")

            best_lgbm_model = random_search.best_estimator_

            logger.info("LightGBM model trained successfully")

            return best_lgbm_model
        
        except Exception as e:
            logger.error(f"Error training LightGBM model: {e}")
            raise CustomException("Failed to train LightGBM model", e)
        
    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Evaluating model performance")
            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            logger.info(f"Accuracy Score: {accuracy}\nPrecision Score: {precision}\nRecall Score: {recall}\nF1 Score: {f1}")
            return {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1}

        except Exception as e:
            logger.error(f"Error evaluating model: {e}")
            raise CustomException("Failed to evaluate model", e)
        
    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)

            logger.info(f"Saving model to {self.model_output_path}")
            joblib.dump(model, self.model_output_path)
            logger.info(f"Model saved successfully to {self.model_output_path}")

        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise CustomException("Failed to save model", e)
        
    def run(self):
        try: 
           logger.info("Starting model training process")
           
           X_train, y_train, X_test, y_test = self.load_and_split_data()
           best_lgbm_model = self.train_lgbm(X_train, y_train)
           metrics = self.evaluate_model(best_lgbm_model, X_test, y_test)
           self.save_model(best_lgbm_model)

           logger.info("Model training completed")

        except Exception as e:
            logger.error(f"Error during model training: {e}")
            raise CustomException("Failed to train model", e)