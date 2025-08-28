from pymongo import MongoClient

class DataRetrieval:
    def __init__(self):
        # שוקי אפשר להוסיף משתנה סביבה של הקונקשיין סטרינג
        self.mongo_url = "mongodb://localhost:27017/"
        self.client = MongoClient(self.mongo_url)
        self.db = self.client["IranMalDB"]

    def get_antisemitic(self):
        return list(self.db["tweets_antisemitic"].find({}, {"_id": 0}))

    def get_not_antisemitic(self):
        return list(self.db["tweets_not_antisemitic"].find({}, {"_id": 0}))


