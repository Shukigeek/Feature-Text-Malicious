from mongo.mongo_dal import Connection
from sub.consumer import Consumer


class ManagerError(Exception):
    pass


class Manager:
    def __init__(self):
        self.stream = None
        self.conn = Connection()
        self.client = self.conn.connect()
        if self.client is None:
            raise Exception(
                "Cannot connect to MongoDB."
            )
        db = self.client[self.conn.db]
        self.collection_anti = db["tweets_antisemitic"]
        self.collection_not_anti = db["tweets_not_antisemitic"]
    def consume(self,topic1,topic2):
        try:
            self.stream = Consumer(topic1, topic2).consumer
            print("consume success")
        except Exception as e:
            raise ManagerError(f"Consumer didn't find data: {e}")
    def write_to_mongo(self):
        try:
            for event in self.stream:
                if event.topic == "enriched_preprocessed_tweets_antisemitic":
                    self.collection_anti.insert_many(event.value)
                elif event.topic == "enriched_preprocessed_tweets_not_antisemitic":
                    self.collection_not_anti.insert_many(event.value)
        except Exception as e:
            raise ManagerError(f"can't sand data to mongo: {e}")