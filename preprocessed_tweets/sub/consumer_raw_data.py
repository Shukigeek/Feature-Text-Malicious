from kafka import KafkaConsumer
import json

class Subscriber:
    def __init__(self,topic):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=['kafka:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def consume(self):
        return self.print_messages()

    def print_messages(self):
        for message in self.consumer:
            print(f"{message.topic}:{message.partition}:{message.offset}: "
                f"key={message.key} value={message.value}")


    def __iter__(self):
        return self.consumer




# psfpasfasf