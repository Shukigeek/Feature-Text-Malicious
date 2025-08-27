import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()

from pymongo import MongoClient ,errors

class FetchData:
    def __init__(self):
        self.user = os.getenv("MONGO_USER")
        self.password = os.getenv("MONGO_PASS")
        self.DB_name = os.getenv("DBname")
        self.collection = os.getenv("collectionName")
        self.conn = None
        self.hundred = 0
    def connect(self):
        try:
            self.conn = MongoClient(f"mongodb+srv://{self.user}:{self.password}"
                                    f"@cluster0.6ycjkak.mongodb.net/")
            self.conn.server_info()
            return self.conn
        except errors.ServerSelectionTimeoutError as e:
            print("Failed to connect to MongoDB:", e)
            return None
        except errors.OperationFailure as e:
            print("Authentication failed:", e)
            return None
    def fetch(self):
        self.connect()
        if self.conn:
            db = self.conn[f"{self.DB_name}"]
            collection = db[f"{self.collection}"]
            hundred = self.hundred
            self.hundred += 100
            return (collection.find({},{"TweetID":1,"CreateDate":1,"Antisemitic":1,"text":1,"_id":0})
                    .sort("CreateDate",1).skip(hundred).limit(100).to_list())
        else:
            return "connection did not created"
if __name__ == '__main__':
    a = FetchData()
    for i in a.fetch():
        for x,y in i.items():
            print(x,":",y)
    # print(a.fetch())