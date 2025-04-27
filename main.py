from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_training_and_validation import ModelTraining
from network_security.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataTransformationConfig, ModelTrainerConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import pandas as pd
import sys
import warnings

warnings.filterwarnings('ignore')

if __name__ == "__main__":
    try:
        config = TrainingPipelineConfig()
        
        ingestion_config = DataIngestionConfig(config)
        data_ingestion = DataIngestion(ingestion_config)

        logging.info("Initiated data ingestion.")
        artifact = data_ingestion.initiate_data_ingestion()

        logging.info("Data ingestion ended. Entering data transformation.")

        train_set = pd.read_csv(artifact.trained_file_path)
        test_set = pd.read_csv(artifact.test_file_path)

        transformation_config = DataTransformationConfig()
        data_transformation = DataTransformation(transformation_config)

        x_test, x_train, y_test, y_train = data_transformation.data_loading(train_set, test_set)

        logging.info("Data transformation ended. Entering model training.")

        training_config = ModelTrainerConfig()
        model_training = ModelTraining(training_config)
        
        model_training.model_training(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
