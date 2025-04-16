from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import numpy as np
import pymongo
import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            
            print(f"Connecting to MongoDB with URL: {MONGO_DB_URL[:20]}...")  # Only show beginning for security
            print(f"Attempting to access database: {database_name}, collection: {collection_name}")
            
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            
            # Check if connection is successful
            self.mongo_client.server_info()  # Will raise exception if connection fails
            print("MongoDB connection successful")
            
            # Print available databases to verify
            print(f"Available databases: {self.mongo_client.list_database_names()}")
            
            collection = self.mongo_client[database_name][collection_name]
            
            # Check if collection exists
            print(f"Collection exists: {collection_name in self.mongo_client[database_name].list_collection_names()}")
            print(f"Document count in collection: {collection.count_documents({})}")
            
            # Get a sample document to verify structure
            sample_doc = collection.find_one()
            print(f"Sample document: {sample_doc}")
            
            df = pd.DataFrame(list(collection.find()))
            logging.info(f"Fetched {len(df)} records from MongoDB collection '{collection_name}'.")
            
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace({"na": np.nan}, inplace=True)
            print(f"Data fetched: {df.head()}")
            return df
        except Exception as e:
            print(f"Error connecting to MongoDB: {str(e)}")
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
     try:
         # Check if the dataframe is empty
         if dataframe.empty:
             raise ValueError("The dataframe is empty. Cannot perform train-test split.")

         train_set, test_set = train_test_split(
             dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
         )
         logging.info("Exited split_data_as_train_test method of DataIngestion class")

         dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
         os.makedirs(dir_path, exist_ok=True)

         logging.info(f"Exporting train and test files to path: {dir_path}")

         train_set.to_csv(
             self.data_ingestion_config.training_file_path, index=False, header=True
         )
         test_set.to_csv(
             self.data_ingestion_config.testing_file_path, index=False, header=True
         )

         return train_set, test_set

     except Exception as e:
         raise NetworkSecurityException(e, sys)


    def initiate_data_ingestion(self):
     try:
         dataframe = self.export_collection_as_dataframe()
         print(f"Data after loading from MongoDB: {dataframe.head()}")  # Add this line to see the data
         dataframe = self.export_data_into_feature_store(dataframe)
         print(f"Data after saving to feature store: {dataframe.head()}")  # Add this line to verify

         self.split_data_as_train_test(dataframe)
         dataingestionArtifact = DataIngestionArtifact(
             train_file_path=self.data_ingestion_config.training_file_path,
             test_file_path=self.data_ingestion_config.testing_file_path
         )

         return dataingestionArtifact

     except Exception as e:
         raise NetworkSecurityException(e, sys)
