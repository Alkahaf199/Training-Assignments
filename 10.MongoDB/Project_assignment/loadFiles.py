import os
import json
import bson.json_util
from pymongo import errors

def load_json_files(json_dir, db):
    """Load JSON files from a directory into the MongoDB database.

    Args:
        json_dir (str): Path to the directory containing JSON files.
        db (Database): Database connection object.

    Returns:
        None
    """
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            collection_name = os.path.splitext(filename)[0]  # Extract collection name from filename
            collection = db[collection_name]
            total_documents = 0

            # Read JSON data from file
            with open(os.path.join(json_dir, filename), 'r') as file:
                # Iterate over each line in the file
                for line in file:
                    try:
                        data = json.loads(line)
                        bson_data = bson.json_util.loads(bson.json_util.dumps(data))

                        # Insert JSON data into MongoDB collection
                        collection.insert_one(bson_data)
                        total_documents += 1  # Increment total documents count
                    except (json.JSONDecodeError, errors.BulkWriteError) as e:
                        print(f"Error inserting document into collection '{collection_name}': {e}")

                # Print the total number of documents inserted for the collection
                print(f"Inserted {total_documents} documents into collection '{collection_name}'")
