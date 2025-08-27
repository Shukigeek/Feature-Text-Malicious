
class Process:
    def __init__(self):
        self.raw_tweets_antisemitic = list()
        self.raw_tweets_not_antisemitic = list()
    def divide_tweets(self,tweets):
        for doc in tweets:
            if doc["Antisemitic"] == 1:
                self.raw_tweets_antisemitic.append(doc)
            else:
                self.raw_tweets_not_antisemitic.append(doc)
        return {"antisemitic":self.raw_tweets_antisemitic,
            "not_antisemitic":self.raw_tweets_not_antisemitic}
if __name__ == '__main__':
    from fetch_tweets import FetchData
    p = Process()
    print(p.divide_tweets(FetchData().fetch()))