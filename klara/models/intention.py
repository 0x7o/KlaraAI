from transformers import pipeline


class Intention:
    def __init__(self):
        self.classification = pipeline("text-classification", model="0x7194633/rubert-base-massive")
        self.ner = pipeline("token-classification", model="0x7194633/rubert-base-massive-ner")

    def get(self, text):
        return self.classification(text)[0]["label"], self.ner(text)
