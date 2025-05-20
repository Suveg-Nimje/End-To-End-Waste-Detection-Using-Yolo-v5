import os, sys
from wasteDetection.logger import logging
from wasteDetection.exception import AppException
from wasteDetection.components.data_ingestion import DataIngestion
from wasteDetection.components.data_validation import DataValidation

from wasteDetection.entity.config_entity import (DataInegstionConfig, DataValidationConfig)
from wasteDetection.entity.artifacts_entity import (DataIngestionArtifact, DataValidationArtifact)

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataInegstionConfig()
        self.data_validation_config = DataValidationConfig()

    def start_data_ingestion(self)-> DataIngestionArtifact:
        try:
            logging.info("Entered the start_data_ingestion_method of TrainPipeline class")

            logging.info("Getting  the data from url")

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Gpt the data from URL")
            logging.info("Exited the start_data_ingestion_method of TrainPipeline class")

            return data_ingestion_artifact
        
        except Exception as e:
            raise AppException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact)-> DataValidationArtifact:
        logging.info("Entered the start_data_validation method of Trainpipeline class")

        try:
            data_valdation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config= self.data_validation_config
            )

            data_valdation_artifact = data_valdation.initiate_data_validation()
            logging.info("Performed the data_validation operation")
            logging.info("Exited the start_data_validation method of Trainpipeline class")

            return data_valdation_artifact
        
        except Exception as e:
            raise AppException(e, sys)

    def run_pipeline(self)-> None:
        try:
            data_ingetion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact= data_ingetion_artifact
            )

        except Exception as e:
            raise AppException(e, sys)
        


        
        