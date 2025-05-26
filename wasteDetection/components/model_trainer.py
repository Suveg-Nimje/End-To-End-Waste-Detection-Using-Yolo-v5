import os
import sys
import yaml
import zipfile
import shutil

from wasteDetection.utils.mian_utils import read_yaml_file
from wasteDetection.logger import logging
from wasteDetection.exception import AppException
from wasteDetection.entity.config_entity import ModelTrainerConfig
from wasteDetection.entity.artifacts_entity import ModelTrainerArtifact


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig):
        self.model_trainer_config = model_trainer_config

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            # Step 1: Unzip data
            logging.info("Unzipping data.zip")
            with zipfile.ZipFile("data.zip", 'r') as zip_ref:
                zip_ref.extractall("data")
            os.remove("data.zip")

            # Step 2: Read number of classes from data.yaml
            with open("data/data.yaml", 'r') as stream:
                num_classes = int(yaml.safe_load(stream)['nc'])

            # Step 3: Modify model config YAML
            model_config_file_name = self.model_trainer_config.weight_name.split(".")[0]
            logging.info(f"Model config file: {model_config_file_name}")
            config = read_yaml_file(f"yolov5/models/{model_config_file_name}.yaml")
            config['nc'] = num_classes

            custom_config_path = f'yolov5/models/custom_{model_config_file_name}.yaml'
            with open(custom_config_path, 'w') as f:
                yaml.dump(config, f)

            # Step 4: Train model
            train_command = (
                f"cd yolov5 && python train.py --img 416 "
                f"--batch {self.model_trainer_config.batch_size} "
                f"--epochs {self.model_trainer_config.no_epochs} "
                f"--data ../data/data.yaml "
                f"--cfg ./models/custom_{model_config_file_name}.yaml "
                f"--weights {self.model_trainer_config.weight_name} "
                f"--name yolov5s_results --cache"
            )
            os.system(train_command)

            # Step 5: Copy best.pt to yolov5 root
            best_model_src = os.path.join("yolov5", "runs", "train", "yolov5s_results", "weights", "best.pt")
            best_model_dst = os.path.join("yolov5", "best.pt")
            shutil.copy(best_model_src, best_model_dst)

            # Step 6: Copy model to model trainer directory
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            final_model_path = os.path.join(self.model_trainer_config.model_trainer_dir, "best.pt")
            shutil.copy(best_model_src, final_model_path)

            # Step 7: Cleanup optional directories
            logging.info("Cleaning up temporary folders")
            shutil.rmtree("yolov5/runs", ignore_errors=True)
            shutil.rmtree("data/train", ignore_errors=True)
            shutil.rmtree("data/valid", ignore_errors=True)
            data_yaml_path = os.path.join("data", "data.yaml")
            if os.path.exists(data_yaml_path):
                os.remove(data_yaml_path)

            # Step 8: Return artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=best_model_dst
            )
            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise AppException(e, sys)
