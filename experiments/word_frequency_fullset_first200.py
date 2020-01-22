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

data_full = import_json.import_data_json('../data/flitsservice_trainset_annotated.json')
data_200 = import_json.import_data_json('../data/flitsservice_trainset_annotated.json', 200)

input_data_full = mine_json.get_location_descriptions_json(data_full, nlp)
input_data_200 = mine_json.get_location_descriptions_json(data_200, nlp)

word_freq_full = word_count(input_data_full)
word_freq_200 = word_count(input_data_200)

keys_full, values_full = zip(*word_freq_full.most_common(35))
values_200 = []
for key in keys_full:
    values_200.append(word_freq_200.get(key, 0))

values_full_norm = [x / sum(values_full) for x in values_full]
values_200_norm = [x / sum(values_200) for x in values_200]

plt.bar( numpy.arange(len(values_full_norm)) * 3, height=values_full_norm, width=1.2, color = 'c' )
plt.bar( numpy.arange(len(values_200_norm)) * 3 + 1.2, height=values_200_norm, width=1.2, color = 'y' )
plt.subplots_adjust(left=0.07, bottom=0.38, right=0.99,top=0.99)
plt.xticks(numpy.arange(len(values_full_norm)) * 3, keys_full, rotation=80)
plt.ylabel('Normalized occurrence frequency')
plt.xlabel('35 most common words')
plt.legend(['Entire training set', 'First 200 articles in training set'],loc=1)
plt.show()
