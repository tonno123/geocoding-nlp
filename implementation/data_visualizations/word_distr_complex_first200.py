import matplotlib.pyplot as plt
import sys
import spacy
import numpy
from collections import Counter

import sys
sys.path.append('..')

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
    return words

data_200 = import_json.import_data_json('../../data/flitsservice_trainset.json', 200)
dataY = import_json.import_data_json('../../data/flitsservice_trainset.json', filepath_complex='../../data/flitsservice_trainset.csv', complex='Y')


input_data_200 = mine_json.get_location_descriptions_json(data_200, nlp)
input_dataY = mine_json.get_location_descriptions_json(dataY, nlp)

words_200 = word_count(input_data_200)
wordsY = word_count(input_dataY)

word_freq_200 = Counter(words_200)
word_freqY = Counter(wordsY)

print(input_dataY)
print("Length:", len(input_dataY))
keysY, valuesY = zip(*word_freqY.most_common(35))
values_200 = []
for key in keysY:
    values_200.append(word_freq_200.get(key, 0))

valuesY_norm = [x / len(wordsY) for x in valuesY]
values_200_norm = [x / len(words_200) for x in values_200]

plt.bar( numpy.arange(len(valuesY_norm)) * 3, height=valuesY_norm, width=1.2, color = 'lightskyblue' )
plt.bar( numpy.arange(len(values_200_norm)) * 3 + 1.2, height=values_200_norm, width=1.2, color = 'lightsalmon' )
plt.subplots_adjust(left=0.07, bottom=0.38, right=0.99,top=0.99)
plt.xticks(numpy.arange(len(valuesY_norm)) * 3, keysY, rotation=80)
plt.ylabel('Distribution')
plt.xlabel('35 most common words')
plt.legend(['Complex subset of first 200 trainingset articles', 'First 200 trainingset articles'],loc=1)
plt.show()
