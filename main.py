from network_security.components.data_ingestion import DataIngestion
from network_security.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import sys

if __name__ == "__main__":
    try:
        config = TrainingPipelineConfig()
        ingestion_config = DataIngestionConfig(config)
        data_ingestion = DataIngestion(ingestion_config)

        logging.info("Initiated data ingestion.")
        artifact = data_ingestion.initiate_data_ingestion()
        print(f" Ingested Data Paths: \nTrain: {artifact.trained_file_path}\nTest: {artifact.test_file_path}")

    except Exception as e:
        raise NetworkSecurityException(e, sys)
