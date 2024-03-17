# database.py

from pymongo import MongoClient

def Database():
    client = MongoClient('localhost', 27017)
    return client['moviesDb']
