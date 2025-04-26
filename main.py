from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_transformation import DataTransformation
from network_security.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig,DataTransformationConfig
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
        

        logging.info('data ingestion ended entering in data transformation')

        train_set = pd.read_csv(artifact.trained_file_path)
        test_set = pd.read_csv(artifact.test_file_path)


        transformation_config=DataTransformationConfig()
        data_transformation=DataTransformation(transformation_config)

        x_test,x_train,y_test,y_train=data_transformation.data_loading(train_set,test_set)

        print(x_train)

        logging.info('data transformation ended entering in model training')

    except Exception as e:
        raise NetworkSecurityException(e, sys)
