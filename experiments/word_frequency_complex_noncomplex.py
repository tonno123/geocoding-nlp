import matplotlib.pyplot as plt
import sys
import spacy
import numpy
from collections import Counter

sys.path.insert(0, "/home/toon/Documents/Afstudeerproject/geocoding-nlp/implementation/jsonNER_implementation")

import import_data_json as import_json
import mine_location_descriptions_json as mine_json

nlp = spacy.load('nl_core_news_sm')

def word_count(input_data):
    words = []
    total_article_n = len(input_data)
    for article_n in range(total_article_n):
        total_sentence_n = len(input_data[article_n])
        for sentence_n in range(total_sentence_n):
            total_span_n = len(input_data[article_n][sentence_n])
            for span_n in range(total_span_n):
                add_tokens = False
                for token in reversed(input_data[article_n][sentence_n][span_n]):
                    if token.text[:3] == 'LOC':
                        add_tokens = True
                    elif add_tokens and not(token.is_punct) and not(token.text[:3] == 'LOC'): #(token.pos_ == 'ADP'):
                        words.append(token.lower_)
                        #words = words + [(token.lower_, token.pos_)]
                #words = words + [(token.text) for token in input_data[article_n][sentence_n][span_n]]
    word_freq = Counter(words)
    return word_freq

dataN = import_json.import_data_json('../data/flitsservice_trainset_annotated.json', filepath_complex='../data/flitsservice_trainset.csv', complex='N')
dataY = import_json.import_data_json('../data/flitsservice_trainset_annotated.json', filepath_complex='../data/flitsservice_trainset.csv', complex='Y')


input_dataN = mine_json.get_location_descriptions_json(dataN, nlp)
input_dataY = mine_json.get_location_descriptions_json(dataY, nlp)

word_freqN = word_count(input_dataN)
word_freqY = word_count(input_dataY)

keysY, valuesY = zip(*word_freqY.most_common(35))
valuesN = []
for key in keysY:
    valuesN.append(word_freqN.get(key, 0))

valuesY_norm = [x / sum(valuesY) for x in valuesY]
valuesN_norm = [x / sum(valuesN) for x in valuesN]

plt.bar( numpy.arange(len(valuesY_norm)) * 3, height=valuesY_norm, width=1.2, color = 'red' )
plt.bar( numpy.arange(len(valuesN_norm)) * 3 + 1.2, height=valuesN_norm, width=1.2, color = 'blue' )
plt.subplots_adjust(left=0.07, bottom=0.38, right=0.99,top=0.99)
plt.xticks(numpy.arange(len(valuesY_norm)) * 3, keysY, rotation=80)
plt.ylabel('Number of occurrences')
plt.xlabel('35 most common words')
plt.legend(['Complex location', 'Non-complex location'],loc=1)
plt.show()
