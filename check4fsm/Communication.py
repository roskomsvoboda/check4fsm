#!/usr/bin/env python

from check4fsm.ProccesText import ProcessText
from check4fsm.TonalizeText import TonalText
from check4fsm.ProcessAppeal import ProcessAppeal

from natasha import Segmenter, Doc
from loguru import logger
import flask
import time
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
        """
        raw_data: String which consist all needed information for processing
        """
        response_data = list()
        logger.debug(f"Incoming data is {raw_data}")
        text = nltk.tokenize.sent_tokenize(raw_data)

        for sentence in text:
            logger.debug(f"Sentence: {sentence}")

            output_data = dict()
            output_data["emotional"] = self.tonalText(sentence)
            output_data["forbidden"] = self.processText(sentence)
            output_data["appeal"] = self.processAppeal(sentence)
            output_data["text"] = sentence

            response_data.append(output_data)

        response_data.append({"summary": self.tonalText(raw_data)})
        logger.debug(f"Output data is {response_data}")
        return response_data

    @logger.catch
    @app.route('/')
    def __call__(self):
        data = req.json
        if data is None:
            return 400, {}

        return 400, self.__process_text__(data["text"])


if __name__ == '__main__':
    logger.info("Loading all systems")

    p = CommunicationFlask()

    logger.info("Loaded all systems")

    p.__process_text__('я ебал в рот эту систему. Но если так подумать не так все плохо. вступайте к нам! У нас хорошо')
    p.app.run(debug=False)
