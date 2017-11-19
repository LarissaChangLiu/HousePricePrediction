"""mongodb_client"""
from pymongo import MongoClient

MONGO_DB_HOST = "localhost"
MONGO_DB_PORT = 27017
DB_NAME = "zillow-houses"

CLIENT = MongoClient("%s:%s" % (MONGO_DB_HOST, str(MONGO_DB_PORT)))


def get_db(db_name=DB_NAME):
    """get_db"""
    database = CLIENT[db_name]
    return database
