from sub.consumer import Consumer
from process.hostile import Processor
from pub.producer import Producer

class ManagerError(Exception):
    pass

class Manager:
    def __init__(self):
        self.antisemitic_stream = None
        self.non_antisemitic_stream = None
        self.enriched_antisemitic_docs = []
        self.enriched_non_antisemitic_docs = []

    def consume(self):
        try:
            self.antisemitic_stream = Consumer("preprocessed_tweets_antisemitic")
            self.non_antisemitic_stream = Consumer("preprocessed_tweets_not_antisemitic")
        except Exception as e:
            raise ManagerError(f"Consumer didn't find data: {e}")

    def _process_stream(self, stream):
        enriched = []
        for doc in stream:
            p = Processor(doc)
            enriched.append(p.sentiment().weapon_detected().find_time())
        return enriched

    def process(self):
        try:
            self.enriched_antisemitic_docs = self._process_stream(self.antisemitic_stream)
            self.enriched_non_antisemitic_docs = self._process_stream(self.non_antisemitic_stream)
        except Exception as e:
            raise ManagerError(f"Can't process data: {e}")

    def publish(self):
        try:
            pub = Producer()
            pub.publish_message("enriched_preprocessed_tweets_antisemitic",
                                self.enriched_antisemitic_docs)
            pub.publish_message("enriched_preprocessed_tweets_not_antisemitic",
                                self.enriched_non_antisemitic_docs)
        except Exception as e:
            raise ManagerError(f"Can't publish data: {e}")

    def manage(self):
        self.consume()
        self.process()
        self.publish()
