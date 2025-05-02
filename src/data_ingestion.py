import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_fuctions import read_yaml
import sys

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(f"Data Ingestion initialized with {self.bucket_name} and file is {self.file_name}")

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)

            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"Successfully downloaded {self.file_name} from GCP Bucket to {RAW_FILE_PATH}.")
        
        except Exception as e:
            logger.error(f"Error downloading file from GCP: {e}")
            raise CustomException("Failed to download file from GCP", e)
        
    def split_data(self):
        try:
            logger.info("Splitting data into train and test sets")

            df = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(df, test_size=1-self.train_test_ratio, random_state=99)

            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)

            logger.info(f"Successfully split data into train and test sets and saved to {TRAIN_FILE_PATH} and {TEST_FILE_PATH}")

        except Exception as e:
            logger.error(f"Error splitting data: {e}")
            raise CustomException("Failed to split data into train and test set", e)
        
    def run(self):
        try:
            logger.info("Starting data ingestion process")
            self.download_csv_from_gcp()    
            self.split_data()
            logger.info("Data ingestion process completed successfully")
        
        except CustomException as ce:
            logger.error(f"Error in data ingestion process: {str(ce)}")
        
        finally:
            logger.info("Data ingestion process completed")


if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()