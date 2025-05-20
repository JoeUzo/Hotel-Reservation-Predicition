import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_fuctions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:

    def __init__ (self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir

        self.config = read_yaml(config_path)

        os.makedirs(self.processed_dir, exist_ok=True)

    def preprocessed_data(self, df):
        try:
            logger.info("Starting Data Processing Step")

            logger.info("Dropping 'Booking_ID Column' and duplicates")
            df.drop(columns=['Booking_ID'], inplace=True)
            df.drop_duplicates(inplace=True)

            logger.info("Grouping columns into categorical and numerical")
            cat_cols = self.config['data_processing']['categorical_columns']
            num_cols = self.config['data_processing']['numerical_columns']


            logger.info("Applying Label Encoding")
            label_encoder = LabelEncoder()

            mappings = {}

            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {label:code for label, code in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))}
            
            logger.info(f"Label Mappings are: ")
            for col, map in mappings.items():
                logger.info(f"{col} : {map}")


            logger.info("Carrying out Skewness Handling")
            skewness_threshold = self.config['data_processing']['skewness_threshold']

            skewness = df[num_cols].apply(lambda x:x.skew())
            for col in skewness[skewness > skewness_threshold].index:
                df[col] = np.log1p(df[col])

            return df
        
        except Exception as e:
            logger.error(f"Error during preprocessing step {e}")
            raise CustomException("Error while preprocessing data", e)
        
    def balance_data(self, df):
        try: 
            logger.info("Handling imbalanced data")
            X = df.drop(columns=['booking_status'])
            y = df['booking_status']

            smote = SMOTE(random_state=97)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df['booking_status'] = y_resampled

            logger.info("Data balanced successfully")

            return balanced_df

        except Exception as e:
            logger.error(f"Error during dalancing data step {e}")
            raise CustomException("Error while balancing data", e)
        


