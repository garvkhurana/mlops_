from network_security.entity.config_entity import DataTransformationConfig
import os
import sys
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import pandas as pd

logging.info('Entering into data transformation')



class DataTransformatiion:
    def __init__(self,data_transformation_config:DataTransformationConfig):
        try:
         self.data_transformation_config=data_transformation_config

        except Exception as e:
           raise NetworkSecurityException(e,sys)


    def data_loading(self,train_data,test_data):
       
           

























