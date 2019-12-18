import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt


def readData():
    data_location = '../../data/annotated/annotated_flitsservice_testset.csv'
    df = pd.read_csv(data_location,skipinitialspace=True,usecols=['Toponiemen','Locaties'])
    return df

def annotatedToponymStats():
    df = readData()
    toponym_frequency_list = []
    for article in df['Toponiemen']:
        article = re.split(r',(?![^\(\[]*[\]\)])', article)
        toponym_frequency_list.append(len(article))
    topo_freq = pd.Series(Counter(toponym_frequency_list), name='number_of_toponyms')
    topo_freq.index.name = 'Number of toponyms'
    topo_freq = topo_freq.sort_index(axis=0)
    topo_freq.plot(kind='bar', figsize=[13,6], position=0.65, bottom=0.20)
    plt.show()

def annotatedLocationStats():
    df = readData()
    location_frequency_list = []
    for article in df['Locaties']:
        article = article.split(';')
        article = list(filter(None, article))
        location_frequency_list.append(len(article))
    loc_freq = pd.Series(Counter(location_frequency_list), name='number_of_locations')
    loc_freq.index.name = 'Number of locations'
    loc_freq = loc_freq.sort_index(axis=0)
    loc_freq.plot(kind='bar', figsize=[13,6], position=0.65, bottom=0.20)
    plt.show()

annotatedToponymStats()

annotatedLocationStats()
