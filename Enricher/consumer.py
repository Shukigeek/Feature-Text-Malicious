from kafka import KafkaConsumer
import json
import os
class Consumer:
    def __init__(self, topic):
        kafka_broker = os.getenv("KAFKA_BROKER", "kafka:9092")
        self.consumer = KafkaConsumer(
            topic,
            group_id= "my-group",
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            bootstrap_servers=[kafka_broker],
            auto_offset_reset='earliest'
        )

    def print_messages(self):
        for message in self.consumer:
            print(f"{message.topic}:{message.partition}:{message.offset}: key={message.key} value={message.value}")
    def get_all_messages(self):
        messages = []
        for message in self.consumer:
            messages.append(message.value)
        return messages



if __name__ == '__main__':
    c = Consumer("not_interesting")
    print("\n\n\n\n\n",c.get_all_messages())
    # h = Consumer("interesting","interesting")
    # c.print_messages()
