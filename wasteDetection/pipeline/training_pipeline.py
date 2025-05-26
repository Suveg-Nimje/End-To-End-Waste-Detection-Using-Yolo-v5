import os, sys
from wasteDetection.logger import logging
from wasteDetection.exception import AppException
from wasteDetection.components.data_ingestion import DataIngestion
from wasteDetection.components.data_validation import DataValidation
from wasteDetection.components.model_trainer import ModelTrainer

from wasteDetection.entity.config_entity import (DataInegstionConfig, DataValidationConfig, ModelTrainerConfig)
from wasteDetection.entity.artifacts_entity import (DataIngestionArtifact, DataValidationArtifact, ModelTrainerArtifact)

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataInegstionConfig()
        self.data_validation_config = DataValidationConfig()
        self.model_trainer_config = ModelTrainerConfig()

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
        
    def start_model_trainer(self) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(
                model_trainer_config=self.model_trainer_config,
            )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise AppException(e, sys)




    def run_pipeline(self)-> None:
        try:
            data_ingetion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact= data_ingetion_artifact
            )
            if data_validation_artifact.validation_status == True:
                model_trainer_artifact = self.start_model_trainer()
            else:
                raise Exception("Your data is not in correct format")

        except Exception as e:
            raise AppException(e, sys)
        


        
        