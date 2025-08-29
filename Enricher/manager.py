from utiles.sub.consumer import Consumer
from process.process_tweets import Processor
from utiles.pub.producer import Producer
import sys
import logging
class ManagerError(Exception):
    pass

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Manager:
    def __init__(self, topic1="preprocessed_tweets_antisemitic", topic2="preprocessed_tweets_not_antisemitic"):
        logger.info(f"Starting Manager with topics: {topic1}, {topic2}")
        print(f"Starting Manager with topics: {topic1}, {topic2}", flush=True)

        try:
            logger.info("Attempting to create consumer...")
            print("Attempting to create consumer...", flush=True)

            self.stream = Consumer(topic1, topic2).consumer

            logger.info("Consumer created successfully!")
            print("Consumer created successfully!", flush=True)

        except Exception as e:
            error_msg = f"Consumer didn't find data: {e}"
            logger.error(error_msg)
            print(error_msg, flush=True)
            raise ManagerError(error_msg)
        self.producer = Producer()

    def process(self,data: dict):
        try:
            p = Processor(data)
            processor = p.sentiment().find_time().weapon_detected()
            return processor.doc
        except Exception as e:
            raise ManagerError(f"Can't process data: {e}")

    def publish(self,pub_topic,data):
        try:

            self.producer.publish_message(pub_topic,data)
            logger.info(f"Publishing to {pub_topic}: {data}")
            print(f"Publishing to {pub_topic}: {data}", flush=True)

        except Exception as e:
            raise ManagerError(f"Can't publish data: {e}")
    def manage(self):
        for event in self.stream:
            if event.topic == "preprocessed_tweets_antisemitic":
                new_data = self.process(event.value)
                self.publish("enriched_preprocessed_tweets_antisemitic",new_data)
            elif event.topic == "preprocessed_tweets_not_antisemitic":
                new_data = self.process(event.value)
                self.publish("enriched_preprocessed_tweets_not_antisemitic",new_data)