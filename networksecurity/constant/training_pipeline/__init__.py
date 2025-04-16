import os
import sys
import numpy as np
import pandas as pd

"""
defining common constants var for training pipeline
"""
TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "PhishingDataset.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

"""
Data Ingestion related constant start with Data_ingestion var name
"""

DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "KULDEEP"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: str = 0.2

"""
Data validation realted constant start with Dat_validation var name
"""
DATA_VALIDATION_DIR_NAME: str= "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

import os

ROOT_DIR = os.getcwd()  # or set this to your project root if needed

SCHEMA_FILE_PATH = os.path.join(ROOT_DIR, "data_schema", "schema.yaml")

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_DIR_NAME: str = "transformed_object"

## knn imputer to replace nan values : see 3 nearest neighbir and calculate avg
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict ={
    "missing_values": np.nan,
    "n_neighbors":3,
    "weights": "uniform",
}