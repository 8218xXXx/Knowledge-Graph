# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from bosonnlp import BosonNLP
from settings import boson_token, topic_to_id, model_to_name, models

import json
import requests

def sentiment(contents):
    sentiments = {}
    nlp = BosonNLP(boson_token)
    for model in models:
        sentiment = nlp.sentiment(contents, model=model)
        sentiments[model_to_name[model]] = sentiment
    return sentiments

def tag(entity):
    nlp = BosonNLP(boson_token)
    result = nlp.tag(entity)
    for d in result:
        print(' '.join(['%s/%s' % it for it in zip(d['word'], d['tag'])]))
    return result

def classify(contents):
    nlp = BosonNLP(boson_token)
    result = nlp.classify(contents)
    topics = []
    for topic in result:
        topics.append(topic_to_id[topic])
    return topics

if __name__ == '__main__':
    contents = "俄否决安理会谴责叙军战机空袭阿勒颇平民"
    result = sentiment(contents)
    print(result)
    # print(classify(contents))
    # result = tag("你是风儿，我是沙")
    # print(result)
    # tags = result[0]['tag']
    # if 'nr' in tags:
    #     print("这是一个人名")
    # -*- encoding: utf-8 -*-
