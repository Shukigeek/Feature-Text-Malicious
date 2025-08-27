from mongo.mongo_dal import Connection
from sub.consumer import Consumer


class ManagerError(Exception):
    pass


class Manager:
    def __init__(self):
        self.anti = None
        self.not_anti = None
        self.conn = Connection()
        self.client = self.conn.connect()
        if self.client is None:
            raise Exception(
                "Cannot connect to MongoDB."
            )
        db = self.client[self.conn.db]
        self.collection_anti = db["tweets_antisemitic"]
        self.collection_not_anti = db["tweets_not_antisemitic"]
    def consume(self):
        try:
            self.anti = Consumer("enriched_preprocessed_tweets_antisemitic")
            self.not_anti = Consumer("enriched_preprocessed_tweets_not_antisemitic")
        except Exception as e:
            raise ManagerError(f"Consumer didn't find data: {e}")
    def write_to_mongo(self):
        try:
            self.collection_anti.insert_many(self.anti)
            self.collection_not_anti.insert_many(self.not_anti)
        except Exception as e:
            raise ManagerError(f"can't sand data to mongo: {e}")