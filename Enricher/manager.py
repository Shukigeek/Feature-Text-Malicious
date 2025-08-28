from sub.consumer import Consumer
from process.process_tweets import Processor
from pub.producer import Producer

class ManagerError(Exception):
    pass

class Manager:
    def __init__(self,topic1="preprocessed_tweets_antisemitic",topic2="preprocessed_tweets_not_antisemitic"):
        try:
            self.stream = Consumer(topic1,topic2).consumer
        except Exception as e:
            raise ManagerError(f"Consumer didn't find data: {e}")

    def process(self,data: dict):
        p = Processor(data)
        new_data = p.sentiment().find_time().weapon_detected()
        return new_data


    def publish(self,pub_topic,data):
        try:
            pub = Producer()
            pub.publish_message(pub_topic,data)
            pub.publish_message(pub_topic,data)
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