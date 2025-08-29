from utiles.sub.consumer import Consumer
from clean_data.process_data import Preprocessor
from utiles.pub.producer import Producer

class ManagerError(Exception):
    pass

class Manager:
    def __init__(self, topic1="raw_tweets_antisemitic", topic2="raw_tweets_not_antisemitic"):
        try:
            self.stream = Consumer(topic1, topic2).consumer
            print("consume success")
        except Exception as e:
            raise ManagerError(f"Consumer didn't find data: {e}")

        self.antisemitic = None
        self.non_antisemitic = None

    def process(self, event):
        try:
            p = Preprocessor()
            original = event.pop("text")
            event["original_text"] = original
            event["clean_text"] = p.clean_text(original)
            print("process success")
        except Exception as e:
            raise ManagerError(f"Can't process data: {e}")

    def publish(self, pub_topic, data):
        try:
            pub = Producer()
            pub.publish_message(pub_topic, data)
            print("publish success")
        except Exception as e:
            raise ManagerError(f"Can't publish data: {e}")

    def manage(self):
        print(type(self.stream))
        for event in self.stream:
            print(event.value)
            if event.topic == "raw_tweets_antisemitic":
                print(event.value)
                self.antisemitic = event.value
                self.process(self.antisemitic)
                self.publish("preprocessed_tweets_antisemitic", self.antisemitic)

            elif event.topic == "raw_tweets_not_antisemitic":
                self.non_antisemitic = event.value
                self.process(self.non_antisemitic)
                self.publish("preprocessed_tweets_not_antisemitic", self.non_antisemitic)


if __name__ == '__main__':
    m = Manager()
    m.manage()
