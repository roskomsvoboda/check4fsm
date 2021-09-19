from .prepareData import getFSM, extractDataFromFSM
from .ProccesText import ProcessText
from .TonalizeText import TonalText
from .ProcessAppeal import ProcessAppeal
from .Communication import CommunicationFlask
from .extractAllData import ExtractData

# ed = ExtractData()
# from .Communication import run
# ed = ExtractData(os.getcwd() + "/data/cities.json", os.getcwd() + "/data/NER.json")
p = CommunicationFlask(os.getcwd() + "/data/cities.json", os.getcwd() + "/data/NER.json")
def run():
    global p
    p.run_flask()
# if __name__ == '__main__':
#     run()