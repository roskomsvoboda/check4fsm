#!/usr/bin/env python

from check4fsm.ProccesText import ProcessText
from check4fsm.TonalizeText import TonalText
from check4fsm.ProcessAppeal import ProcessAppeal

from natasha import Segmenter, Doc
from loguru import logger
import flask
import time
import nltk

class ExtractData:
    @logger.catch
    def __init__(self):
        nltk.download('punkt')
        self.processAppeal = ProcessAppeal()
        self.processText = ProcessText()
        self.tonalText = TonalText()

        self.segmenter = Segmenter()


    @logger.catch
    def __call__(self, raw_data: str):
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