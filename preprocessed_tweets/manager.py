from sub.consumer_raw_data import Subscriber
from pub.publish_processed_data import Producer
from clean_data.process_data import Preprocessor


class Main:
    def __init__(self):

        self.preprocessor = Preprocessor()
        self.consumer = Subscriber()
        self.producer = Producer()

    def run(self):
        print("Processor is running and waiting for messages...")
        for message in self.consumer:
            data = message.value
            original_text = data.get("text","")

            # processed text
            processed_text = self.preprocessor.clean_text(original_text)
            data["preprocessed_text"] = processed_text

            # publish to specific tpoic
            if data.get("category") == "antisemitic":
                self.producer.publish_message("preprocessed_tweets_antisemitic", message=data)
            else:
                self.producer.publish_message("preprocessed_tweets_not_antisemitic", message=data)

            print("Processed & published:", data)



if __name__ == "__main__":
    service = Main()
    service.run()