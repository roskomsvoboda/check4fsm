#!/usr/bin/env python

from check4fsm import ProcessText
from check4fsm import TonalText
from check4fsm import ProcessAppeal

from loguru import logger
from natasha import  Segmenter, Doc
import flask
import nltk



class CommunicationFlask:
    app = flask.Flask(__name__)
    @logger.catch
    def __init__(self):
        nltk.download('punkt')
        self.processAppeal = ProcessAppeal()
        self.processText = ProcessText()
        self.tonalText = TonalText()

        self.segmenter = Segmenter()


    @logger.catch
    def __process_text__(self, raw_data: str):

        response_data = list()
        text = tokenize.sent_tokenize(raw_data)

        for sentence  in text:
            output_data = dict()
            text_ = Doc(sentence)
            text_.segment(self.segmenter)

            output_data["emotional"] = self.tonalText(text_)
            output_data["forbidden"] = self.processText(text_)
            output_data["appeal"] = self.processAppeal(text_)

            response_data.append(output_data)
        return response_data


    @logger.catch
    @app.route('/')
    def __call__(self):
        data = request.json
        logger.debug(f"Incoming data is {data}")
        if data is None:
            return 400, {}

        return 400, self.__process_text__(data["text"])

if __name__ == '__main__':
    p = CommunicationFlask()
    p()
