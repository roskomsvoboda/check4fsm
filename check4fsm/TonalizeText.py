#!/usr/bin/env python

from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from loguru import logger

class TonalText:
    @logger.catch
    def __init__(self):

        self.tokenizer = RegexTokenizer()
        self.model = FastTextSocialNetworkModel(tokenizer=self.tokenizer)

    @logger.catch
    def __call__(self, text: tuple) -> tuple:
        if isinstance(text, str):
            text = [text]
        model_predict = self.model.predict(text, k=5)[0]
        max_values = max(model_predict.items(), key=lambda k: k[1])
        return  max_values if max_values is not None else list()



# if __name__ == '__main__':
#      p = TonalText()
#      output = p(['Ебать как это классно'])
#      print(f"Ебать как это классно: {output}")
#
#      output = p(['Ебать'])
#      print(f"Ебать: {output}")
#
#      output = p(['Вам обязательно надо вступить в нашу бригаду'])
#      print(f"Вам обязательно надо вступить в нашу бригаду: {output}")
