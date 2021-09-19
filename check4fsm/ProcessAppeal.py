#!/usr/bin/env python
import os

import csv
import json
# import subprocess
#
# import requests
from loguru import logger
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,

    Doc, ORG, LOC
)


class ProcessAppeal:
    @logger.catch
    def __init__(self):
        self.segment = Segmenter()
        self.morph_vocab = MorphVocab()

        self.emb = NewsEmbedding()
        self.ner_tagger = NewsNERTagger(self.emb)
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.syntax_parser = NewsSyntaxParser(self.emb)
        self.names_extractor = NamesExtractor(self.morph_vocab)

    @classmethod
    @logger.catch
    def __prepare_text(self, token: dict) -> list:
        return token.start, token.stop, token.text

    @logger.catch
    def __call__(self, text: str):
        doc = Doc(text)
        doc.segment(self.segment)
        doc.tag_morph(self.morph_tagger)

        for token in doc.tokens:
            token.lemmatize(self.morph_vocab)

        doc.parse_syntax(self.syntax_parser)
        doc.tag_ner(self.ner_tagger)

        for span in doc.spans:
            span.normalize(self.morph_vocab)
        appeals = list()
        for token in doc.tokens:
            if token.pos == 'NOUN' or token.pos == 'VERB':
                head_id = int(token.head_id.split('_')[-1]) - 1
                if doc.tokens[head_id].pos != 'ADJ':
                    continue
                appeals.append(( self.__prepare_text(doc.tokens[head_id]),self.__prepare_text(token)))
        return appeals if len(appeals) else list()


# if __name__ == '__main__':
#     p = ProcessAppeal()
#     print(f"'Ты обязан вступить к нам: {p('Ты обязан вступить к нам.')}")
#     print(f"'Ты вступишь к нам?': {p('Ты вступишь к нам?')}")
