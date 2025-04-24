import json
import sys
import certifi
import pandas as pd
import pymongo
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

MONGO_DB_URL = "mongodb+srv://garvkhurana1234567:admin@cluster0.3kpje.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

if not MONGO_DB_URL:
    raise ValueError("MONGO_DB_URL is not set. Please check your .env file!")

class NetworkDataExtract:
    def __init__(self):
        try:
            # Connect to MongoDB with TLS
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=certifi.where())
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, file_path):
        """Convert CSV data to JSON format for MongoDB insertion."""
        try:
            # Read CSV file into a DataFrame
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            # Convert DataFrame to JSON format (records)
            records = json.loads(data.to_json(orient="records")) 
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongodb(self, records, database, collection):
        """Insert JSON data into MongoDB."""
        try:
            # Connect to the specific database and collection
            db = self.mongo_client[database]
            coll = db[collection]
            # Insert the records into the MongoDB collection
            coll.insert_many(records)

            # Log the available collections in the database
            collections = db.list_collection_names()
            logging.info(f"Collections in database '{database}': {collections}")

            # Return the number of inserted records
            return len(records)  
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == '__main__':
    FILE_PATH = "network_data/phisingData.csv"  # Specify the path to your CSV file
    DATABASE = "shreshtha"  # Name of your MongoDB database
    COLLECTION = "sunshine"  # Name of the collection in the database

    # Initialize the NetworkDataExtract object
    network_obj = NetworkDataExtract()

    # Convert CSV to JSON format
    records = network_obj.csv_to_json_converter(file_path=FILE_PATH)
    print(f"Converted {len(records)} records from CSV.")

    # Insert data into MongoDB
    try:
        num_inserted = network_obj.insert_data_to_mongodb(records=records, database=DATABASE, collection=COLLECTION)
        print(f"Inserted {num_inserted} records into MongoDB.")
    except Exception as e:
        print(f" Error during data insertion: {e}")
