from .prepareData import getFSM, extractDataFromFSM
from .ProccesText import ProcessText
from .TonalizeText import TonalText
from .ProcessAppeal import ProcessAppeal
from .Communication import CommunicationFlask
from .extractAllData import ExtractData

ed = ExtractData()
from .Communication import run

if __name__ == '__main__':
    run()