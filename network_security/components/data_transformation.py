from network_security.entity.config_entity import DataTransformationConfig
import os
import sys
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import pandas as pd
from sklearn.preprocessing import StandardScaler
from network_security.utils import save_object
from network_security.constant import training_pipeline
import numpy as np

logging.info('Entering into data transformation')



class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig):
        try:
         self.data_transformation_config=data_transformation_config

        except Exception as e:
           raise NetworkSecurityException(e,sys)


    def data_loading(self,train_data,test_data):
       try:
        x_train=train_data.drop(columns="Result",axis=1)
        y_train=train_data["Result"]
        x_test=test_data.drop(columns="Result",axis=1)
        y_test=test_data["Result"]
        
        y_train = np.where(y_train == -1, 0, y_train)
        y_test = np.where(y_test == -1, 0, y_test)
 





        ss=StandardScaler()
        x_train=ss.fit_transform(x_train)
        x_test=ss.transform(x_test)

        os.makedirs(os.path.dirname(self.data_transformation_config.scaler_config), exist_ok=True)


        save_object(os.path.join("artifacts", "scaler.pkl"), ss)
  

        return(x_test,x_train,y_test,y_train) 







       except Exception as e:
          raise NetworkSecurityException(e,sys) 









   













    
    
    
       
           

























