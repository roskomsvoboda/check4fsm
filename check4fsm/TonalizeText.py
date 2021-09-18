#!/usr/bin/env python

from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

class TonalText:
    def __init__(self):

        self.tokenizer = RegexTokenizer()
        self.model = FastTextSocialNetworkModel(tokenizer=self.tokenizer)

    def __call__(self, text) -> tuple:
        model_predict = self.model.predict(text, k=5)[0]
        return max(model_predict.items(), key=lambda k: k[1])


if __name__ == '__main__':
     p = TonalText()
     output = p(['Ебать как это классно'])
     print(f"Ебать как это классно: {output}")

     output = p(['Ебать'])
     print(f"Ебать: {output}")

     output = p(['Вам обязательно надо вступить в нашу бригаду'])
     print(f"Вам обязательно надо вступить в нашу бригаду: {output}")
