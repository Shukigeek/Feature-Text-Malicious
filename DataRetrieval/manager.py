from fetch_tweets import FetchData
from process_tweet import Process
from producer import Producer

class Manager:
    def __init__(self):
        self.antisemitic = None
        self.not_antisemitic = None
    def fetch_process(self):
        tweets = FetchData().fetch()
        div_tweet = Process().divide_tweets(tweets)
        self.antisemitic = div_tweet["antisemitic"]
        self.not_antisemitic = div_tweet["not_antisemitic"]
    def publish_tweets(self):
        pro = Producer()
        for doc in self.antisemitic:
            pro.publish_message("raw_tweets_antisemitic",str(doc))

        for doc in self.not_antisemitic:
            pro.publish_message("raw_tweets_not_antisemitic",str(doc))
    def manage(self):
        self.fetch_process()
        self.publish_tweets()
        return {"fetch":"success","publish":"success"}
if __name__ == '__main__':
    g = Manager()
    print(g.manage())


