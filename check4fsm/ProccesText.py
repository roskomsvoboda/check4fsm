#!/usr/bin/env python

import os
import json

from loguru import logger
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER, ORG, LOC,
    NamesExtractor,

    Doc
)


class ProcessText:
    @logger.catch
    def __init__(self, cities: str = os.getcwd() + "..//data/cities.json", ner: str = os.getcwd() + "..//data/NER.json"):
        self.cities = json.load(open(cities, 'r'))
        self.ner = json.load(open(ner, 'r'))

        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()

        self.emb = NewsEmbedding()
        self.ner_tagger = NewsNERTagger(self.emb)
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.syntax_parser = NewsSyntaxParser(self.emb)
        self.names_extractor = NamesExtractor(self.morph_vocab)

    @staticmethod
    @logger.catch
    def search(ner, data, type: str) -> tuple:
        for info in ner[type]:
            if info["normal"] == data["normal"]:
                return True, info["normal"]
        return False, {}

    @logger.catch
    def __extract_data(self, text: str):
        doc = Doc(text)
        doc.segment(Segmenter())
        doc.tag_morph(self.morph_tagger)

        for token in doc.tokens:
            token.lemmatize(self.morph_vocab)

        doc.parse_syntax(self.syntax_parser)
        doc.tag_ner(self.ner_tagger)

        for span in doc.spans:
            span.normalize(self.morph_vocab)

        forbidden_info = list()

        for fact in doc.spans:
            if fact.text in self.cities['cities'] or fact.text in self.cities['subjects']:
                continue
            found = False
            if fact.type == PER:
                found, info = ProcessText.search(self.ner, fact.as_json, 'names')
            if fact.type == LOC:
                found, info = ProcessText.search(self.ner, fact.as_json, 'others')
            if fact.type == LOC:
                found, info = ProcessText.search(self.ner, fact.as_json, 'organizations')
            if found is True:
                forbidden_info.append(fact)

        return forbidden_info

    @logger.catch
    def __call__(self, text: str):
        fi = self.__extract_data(text)
        if fi == list():
            return None

        output_data = list()
        for data in fi:
            data = data.as_json
            output_data.append({data["start"], data["stop"], data["text"]})

        return output_data

#
# if __name__ == '__main__':
#     p = ProcessText()
#     print( f" 'Вострягов В.А. Издавалась БЫТЬ!' {p('Вострягов В.А. Издавалась БЫТЬ!')}")