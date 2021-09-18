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


@logger.catch
def getFSM(filename: str = os.getcwd() + "/../data/exportfsm.csv",
           encoding_: str = "windows-1251") -> dict:
    output_data = {'sentence': list(), 'date': list()}
    try:
        with open(filename, newline='', encoding=encoding_) as f:
            for data in csv.reader(f, delimiter=';'):
                # Extract data and delete time from the judge
                output_data['sentence'].append(''.join(data[1][:-1].split('(')[:-1]))
                output_data['date'].append(data[2])
    except Exception as ex:
        logger.error(f"Current error is {ex}")

    return output_data


@logger.catch
def extractDataFromFSM(filename: str = os.getcwd() + "/../data/exportfsm.csv",
                       cities: str = os.getcwd() + "/../data/cities.json"):
    all_data = dict()

    all_data['names'] = list()
    all_data['others'] = list()
    all_data['organizations'] = list()

    cities = json.load(open(cities, 'r'))

    segmenter = Segmenter()
    morph_vocab = MorphVocab()

    emb = NewsEmbedding()
    ner_tagger = NewsNERTagger(emb)
    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)
    names_extractor = NamesExtractor(morph_vocab)

    fsm = getFSM(filename)

    for sentence in fsm['sentence']:
        doc = Doc(sentence)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)

        for token in doc.tokens:
            token.lemmatize(morph_vocab)

        doc.parse_syntax(syntax_parser)
        doc.tag_ner(ner_tagger)

        for span in doc.spans:
            span.normalize(morph_vocab)

        for fact in doc.spans:
            if fact.text in cities['cities'] or fact.text in cities['subjects']:
                continue
            if fact.type == PER:
                all_data['names'].append(fact.as_json)
            if fact.type == LOC:
                all_data['others'].append(fact.as_json)
            if fact.type == ORG:
                all_data['organizations'].append(fact.as_json)

    return all_data


if __name__ == '__main__':
    # This is i was trying to download the fucking data
    # url = 'https://minjust.gov.ru/uploaded/files/exportfsm.csv'
    # r = requests.get(url)
    # process = subprocess.Popen(["wget", url, "-O", f"{os.getcwd()}/../data/exportfsm.csv"], stdout=subprocess.PIPE)
    # req = requests.Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
    #
    # print(os.getcwd() + "/../data/" + url.split('/')[-1])
    # open(os.getcwd() + "/../data/" + url.split('/')[-1], 'wb').write(
    #     r.content)

    getFSM()
    prepared_data = extractDataFromFSM()

    with open(os.getcwd() + "/../data/NER.json", 'w') as f:
        json.dump(prepared_data, f, ensure_ascii=False, indent=4)
