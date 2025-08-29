import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.data.find("sentiment/vader_lexicon.zip")
import re
from process.clean_data import Preprocessor


class Processor:
    def __init__(self,doc):
        self.doc = doc.copy()

    def sentiment(self):
        score = SentimentIntensityAnalyzer().polarity_scores(self.doc["clean_text"])
        if score["compound"] >= 0.5:
            self.doc["sentiment"] = "positive"
        elif score["compound"] <= -0.5:
            self.doc["sentiment"] = "negative"
        else:
            self.doc["sentiment"] = "neutral"
        return self

    def weapon_detected(self):
        p = Preprocessor()
        with open(r"data/weapon.txt","r") as f:
            weapon_list = [p.clean_text(weapon) for weapon in f.readlines()]
        weapon_in = list()
        for weapon in weapon_list:
            if weapon in self.doc["clean_text"]:
                weapon_in.append(weapon)
        self.doc["weapons_detected"] = weapon_in or ""
        return self

    def find_time(self):
        date_pattern = r"\d{4}-\d{2}-\d{2}"
        max_date = ""
        for word in self.doc["original_text"].split():
            if re.fullmatch(date_pattern, word):
                max_date = max(max_date,word)
        self.doc["relevant_timestamp"] = max_date
        return self




if __name__ == '__main__':
    p = Processor({"original_text":"dsf ljf  v 2022-10-01  2019-10-10",
            "clean_text":"dsf ljf v 2022-10-01   2019-10-10"})
    p.find_time().sentiment().weapon_detected()
    for x,y in p.doc.items():
        print(x,".",y)


