
"""
defining common constant variable for training pipeline

"""

TARGET_COLUMN= "Result"
PIPELINE_NAME : str= "NetworkSecurity"
ARTIFACT_NAME : str = "artifacts"
FILE_NAME : str = "phisingData.csv"
TRAIN_FILE_NAME : str = "Train.csv"
TEST_FILE_NAME : str = "test.csv"
PREPROCESSOR : str = "preprocessor.pkl"
STANDARDSCALER : str = "scaler.pkl"
MODEL : str = "model.pkl"


"""
Data ingestion related content start with DATA_INGESTION VAR NAME

"""

DATA_INGESTION_COLLECTION_NAME : str = "sunshine" 
DATA_INGESTION_DATABASE_NAME: str = "shreshtha"  
DATA_INGESTION_DIR_NAME : str = "data_ingestion"  
DATA_INGESTION_FEATURE_STORE_DIR : str= "feature_store" 
DATA_INGESTION_INGESTED_DIR : str= "ingested" 
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO= float= 0.2
P_AND_S_STORE_DIR: str ="saved preprocessor and scaler"
PREPROCESSOR_DIR_NAME : str= "preprocessor"
SCALER_DIR_NAME : str= "scaler"


