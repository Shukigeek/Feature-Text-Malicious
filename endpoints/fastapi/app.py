from fastapi import FastAPI
from local_mongo import DataRetrieval

app = FastAPI()
service = DataRetrieval()

#
# @app.get("/tweets/antisemitic")
# def get_antisemitic():
#     tweets = service.get_antisemitic()
#     return {"count": len(tweets), "data": tweets}
#
#
# @app.get("/tweets/not_antisemitic")
# def get_not_antisemitic():
#     tweets = service.get_not_antisemitic()
#     return {"count": len(tweets), "data": tweets}

print(service.)