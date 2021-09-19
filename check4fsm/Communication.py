#!/usr/bin/env python

from check4fsm.ProccesText import ProcessText
from check4fsm.TonalizeText import TonalText
from check4fsm.ProcessAppeal import ProcessAppeal
from check4fsm.extractAllData import ExtractData
from check4fsm import *

from natasha import Segmenter, Doc
from loguru import logger
from flask_cors import CORS
import flask
import time
import nltk

logger.add(".logger.log", format="{time} {level} {message}", rotation="50 MB")

ed = ExtractData()


class CommunicationFlask:
    app = flask.Flask(__name__)
    CORS(app)

    def __init__(self):
        pass

    @staticmethod
    @logger.catch
    @app.route('/', methods=["POST"])
    def hooks():
        data = flask.request.json
        if data is None:
            logger.error(f" failed data is None")
            return {}

        output_data = dict()
        try:
            output_data = ed(data["text"])
        except Exception as ex:
            logger.error(f" failed on the server {ex}")
            return {}

        return output_data

    @logger.catch
    def run_flask(self):
        self.app.run(host="0.0.0.0", port=9000)


def run():
    logger.info("Loading all systems")

    p = CommunicationFlask()

    logger.info("Loaded all systems")

    p.run_flask()
