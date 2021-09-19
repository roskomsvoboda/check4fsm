from .prepareData import getFSM, extractDataFromFSM
from .ProccesText import ProcessText
from .TonalizeText import TonalText
from .ProcessAppeal import ProcessAppeal
from .Communication import CommunicationFlask
from .extractAllData import ExtractData

from .Communication import run

import os


if __name__ == '__main__':
    run( os.getcwd() + "/data/cities.json", os.getcwd() + "/data/NER.json")