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

data = import_json.import_data_json('../data/flitsservice_trainset_annotated.json')
input_data = mine_json.get_location_descriptions_json(data, nlp)

word_freq = word_count(input_data)
keys, values = zip(*word_freq.most_common(35))
plt.bar( numpy.arange(len(values)) * 3, height=values, width=2.4, color = 'green' )
plt.subplots_adjust(left=0.07, bottom=0.38, right=0.99,top=0.99)
plt.xticks(numpy.arange(len(values)) * 3, keys, rotation=80)
plt.ylabel('Number of occurrences')
plt.xlabel('35 most common words')
plt.show()
