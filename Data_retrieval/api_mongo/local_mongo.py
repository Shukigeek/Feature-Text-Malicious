import os
from pymongo import MongoClient

class MongoTweetReader:
    def __init__(self):
        self.host = os.getenv("MONGO_HOST", "mongodb")
        self.port = os.getenv("MONGO_PORT", "27017")
        self.database = os.getenv("MONGO_DB", "processed_tweets")
        self.client = MongoClient(
            host=self.host,
            port=int(self.port),
            serverSelectionTimeoutMS=5000
        )
        self.db = self.client[self.database]

    def get_antisemitic(self):
        return list(self.db["tweets_antisemitic"].find({}, {"_id": 0}))

    def get_not_antisemitic(self):
        return list(self.db["tweets_not_antisemitic"].find({}, {"_id": 0}))


