from mongo.mongo_dal import Connection
from sub.consumer import Consumer
import logging
class ManagerError(Exception):
    pass

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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
    def consume(self,topic1="enriched_preprocessed_tweets_antisemitic",
                topic2="enriched_preprocessed_tweets_not_antisemitic"):
        try:
            self.stream = Consumer(topic1, topic2).consumer
            print("consume success")
        except Exception as e:
            raise ManagerError(f"Consumer didn't find data: {e}")
    def write_to_mongo(self):
        try:
            for event in self.stream:
                logger.info(f"we are in event")
                if event.topic == "enriched_preprocessed_tweets_antisemitic":
                    if event.value and isinstance(event.value, dict) and event.value.keys():
                        self.collection_anti.insert_one(event.value)
                        logger.info("Inserted into anti collection")
                    else:
                        logger.warning(f"Skipping empty or invalid event.value: {event.value}")
                elif event.topic == "enriched_preprocessed_tweets_not_antisemitic":
                    if event.value and isinstance(event.value, dict) and event.value.keys():
                        self.collection_not_anti.insert_one(event.value)
                        logger.info("Inserted into |not| anti collection")
                    else:
                        logger.warning(f"Skipping empty or invalid event.value: {event.value}")
        except Exception as e:
            raise ManagerError(f"can't sand data to mongo: {e}")


if __name__ == '__main__':
    pass