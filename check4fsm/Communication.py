#!/usr/bin/env python

from check4fsm.ProccesText import ProcessText
from check4fsm.TonalizeText import TonalText
from check4fsm.ProcessAppeal import ProcessAppeal
from check4fsm.extractAllData import ExtractData
from check4fsm import *

from natasha import Segmenter, Doc
from loguru import logger
import flask
import time
import nltk

logger.add(".logger.log", format="{time} {level} {message}", rotation="50 MB")



class CommunicationFlask:

    app = flask.Flask(__name__)
    def __init__(self):
        pass

    @staticmethod
    @logger.catch
    @app.route('/', methods=["POST"])
    def hooks():
        data = flask.request.json
        if data is None:
            return 400, {}

        output_data = dict()
        try:
            output_data = ed(data["text"])
        except Exception as ex:
            logger.error(f" failed on the server {ex}")
            abort(400)
        
        return output_data

    @logger.catch
    def run_flask(self):
        self.app.run(host="0.0.0.0", port=9000, ssl_context='adhoc')


if __name__ == '__main__':
    logger.info("Loading all systems")

    p = CommunicationFlask()

    logger.info("Loaded all systems")

    ed('я ебал в рот эту систему. Но если так подумать не так все плохо. вступайте к нам! У нас хорошо')
    p.run_flask()
