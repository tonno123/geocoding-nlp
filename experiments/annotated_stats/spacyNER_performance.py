import sys
import spacy
import pandas as pd
import re

def getSpacyEntityList(data_location, num_of_articles):
    nlp = spacy.load('nl_core_news_sm')
    ENTITY_LIST = ['GPE', 'FAC', 'LOC', 'NORP']

    df = pd.read_csv(data_location,skipinitialspace=True)
    df = df.apply(lambda x: x.str.replace("\t", ""))
    df = df.apply(lambda x: x.str.replace("\r", ""))
    data = df.apply(lambda x: x.str.replace("\n", ""))
    data = data['Artikel']
    data = data[:num_of_articles]
    toponym_list = []

    for article in data:
        toponyms_per_article = []
        doc = nlp(article)
        for entity in doc.ents:
            if entity.label_ in ENTITY_LIST:
                toponyms_per_article.append(entity)
        toponym_list.append(toponyms_per_article)
    return toponym_list

def getAnnotatedEntityList(data_location):
    df = pd.read_csv(data_location,skipinitialspace=True,usecols=['Toponiemen','Locaties'])
    toponym_list = []

    for article in df['Toponiemen']:
        toponyms_per_article = []
        article = re.split(r',(?![^\(\[]*[\]\)])', article)
        for toponym in article:
            toponym = toponym.strip().split(" ", 1)
            if len(toponym) > 1:
                if toponym[1][0] is '[':
                    tmp_list = toponym[1].strip('[]').split(',')
                    toponyms_per_article.extend(tmp_list)
                else:
                    toponyms_per_article.append(toponym[1])
            else:
                toponyms_per_article.append(toponym[0])
            toponyms_per_article = [i.replace('_',' ') for i in toponyms_per_article]
        toponym_list.append(toponyms_per_article)
    return toponym_list

getAnnotatedEntityList('../../data/annotated/annotated_flitsservice_testset.csv')
