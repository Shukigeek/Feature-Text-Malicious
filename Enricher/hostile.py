from collections import Counter
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.data.find("sentiment/vader_lexicon.zip")

class Processor:
    def __init__(self,doc):
        self.doc = doc.copy()

    def sentiment(self):
        score = SentimentIntensityAnalyzer().polarity_scores(self.doc["Text"])
        if score["compound"] >= 0.5:
            self.doc["sentiment"] = "positive"
        elif score["compound"] <= -0.5:
            self.doc["sentiment"] = "negative"
        else:
            self.doc["sentiment"] = "neutral"

    def weapon_detected(self):
        with open(r"data/weapons.txt","r") as f:
            weapon_list = [weapon.strip() for weapon in f.readlines()]

        def detect(text):
            words = text.split()
            for i in range(len(words)):
                for weapon in weapon_list:
                    wep_len = len(weapon.split())

                    if " ".join(words[i:i+wep_len]) == weapon:
                        return " ".join(words[i:i+wep_len])
            return ""

        self.df["weapons_detected"] = self.df["Text"].apply(detect)
        return self
    def rename_columns(self):
        self.df.rename(columns={"TweetID":"id","Text":"original_text"}, inplace=True)
        return self


if __name__ == '__main__':
    from manager import Manager
    m = Manager().mongo_to_df()
    p = Processor(m)
    # print(p.rarest_word())
    # print(p.sentiment())
    print(p.weapon_detected())

