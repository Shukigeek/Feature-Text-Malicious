import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text):
        text = text.lower()
        text = text.translate(str.maketrans('','',string.punctuation))
        text = re.sub(r'[^a-z0-9\s]','',text)
        tokens = text.split()
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word not in self.stop_words]
        text = " ".join(tokens)

        return text
if __name__ == '__main__':
    import nltk

    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')
    p = Preprocessor()
    print(p.clean_text("nkjhfdtfyguk987t565__-----,,..k; i  i and by petahia"))










