ARTIFACTS_DIR: str  = "artifacts"

"""
Data ingestion related constant start with DATA_INGESTION VAR NAME
"""

DATA_INGETION_DIR_NAME: str = "data_ingestion"

DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"

DATA_DOWNLOAD_URL:  str =  "https://drive.google.com/file/d/1ARMXL1Whjhc0xRc91CzlfC0z4OFU_diX/view?usp=sharing"

"""
Data validation related constant start with DATA_VALIDATION VAR NAME 
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"

DATA_VALIDATION_STATUS_FILE = "status.txt"

DATA_VALIDATION_ALL_REQUIRED_FILES = ["train", "valid", "data.yaml"]

"""
MODEL TRAINER related constant start with MODEL_TRAINER var name
"""

MODEL_TRAINER_DIR_NAME: str = "model_trainer"

MODEL_TRAINER_PRETRAINED_WEIGHT_NAME: str = "yolov5s.pt"

MODEL_TRAINER_NO_EPOCHS: int = 50

MODEL_TRAINER_BATCH_SIZE: int = 16
