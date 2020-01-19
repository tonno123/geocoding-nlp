import spacy
from spacy.symbols import ORTH, NORM
import matplotlib.pyplot as plt
import tkinter
import string
import numpy

import search_pattern as search_p
from mine_location_descriptions import get_location_descriptions
from import_data import import_data
from import_data_complex import import_data_complex

from collections import Counter

def word_count():
    words = []
    total_article_n = len(input_data)
    for article_n in range(total_article_n):
        total_sentence_n = len(input_data[article_n])
        for sentence_n in range(total_sentence_n):
            total_span_n = len(input_data[article_n][sentence_n])
            for span_n in range(total_span_n):
                for token in input_data[article_n][sentence_n][span_n]:
                    if (token.pos_ == 'ADP'): #not(token.is_punct)# and
                        words.append(token.lower_)
                        #words = words + [(token.lower_, token.pos_)]
                #words = words + [(token.text) for token in input_data[article_n][sentence_n][span_n]]
    word_freq = Counter(words)
    keys, values = zip(*word_freq.most_common(35))
    plt.figure(figsize=[13,6])
    plt.subplots_adjust(left=0.07, bottom=0.3, right=0.97)
    plt.bar(keys, values)
    plt.title('Frequency of adposition words in \'hetongelukscraped.csv\' with word to entity distance of 3 and distance between entities 6.')
    plt.xticks(rotation=60)
    plt.xlabel('35 most common adpositions')
    plt.ylabel('Frequency')
    plt.show()


# this function takes a list of articles, divided into sentences, and those sentences
# divided into spans. It also takes a list of words or list of POS-tags to look for
# in the dataset. It outputs a graph showing the most frequently occurring combinations
# of words of POS-tags together with the location mentions. It also outputs a dict
# which contains the locations of all relevant span combinations in the dataset.
def word_pos_frequency(input_data, word_list=[], pos_list=[], pos_or_word=1):
    words = []
    span_counter = 0
    span_location = {}

    total_article_n = len(input_data)
    for article_n in range(total_article_n):
        total_sentence_n = len(input_data[article_n])
        for sentence_n in range(total_sentence_n):
            total_span_n = len(input_data[article_n][sentence_n])
            for span_n in range(total_span_n):

                new_span = ''
                current_span = input_data[article_n][sentence_n][span_n]
                span_str = current_span.text.strip('.')
                for entity in current_span._.entities:
                    if entity.label_ in ['GPE', 'FAC', 'LOC', 'NORP']: # nodig?
                        span_str = span_str.replace(entity.text, "#loc", 1)


                # in case one or more words are entered
                if word_list:
                    if any(elem in span_str.split() for elem in word_list) and "#loc" in span_str.split():
                        for word in span_str.split():
                            if word.lower() in word_list or word == "#loc":
                                new_span = new_span + word.lower() + ' '

                # in case one or more POS-tags are entered
                elif pos_list:
                    for i, word in enumerate(span_str.split()):
                        if current_span[i].pos_ in pos_list:
                            if pos_or_word:
                                new_span = new_span + current_span[i].pos_ + ' '
                            else:
                                new_span = new_span + word.lower() + ' '
                        elif word == "#loc":
                            new_span = new_span + "#loc" + ' '
                    if all(i == "#loc" for i in new_span.split()) or not "#loc" in new_span:
                        new_span = ''
                new_span = new_span[:-1]

                # deleting all adpositions after the last detected toponym
                new_span = new_span.rpartition("#loc")  # more filtering required here
                new_span = new_span[0] + new_span[1]

                # this saves all word and POS-tag combinations in a dict, where
                # the key is the combination itself, and the key is a list of
                # numbers that indicate where in the data the combination occurs.
                if new_span != '':
                    if new_span in span_location:
                        span_location[new_span].append(span_counter)
                    else:
                        span_location[new_span] = [span_counter]
                    words.append(new_span)
                span_counter = span_counter + 1


    ent_freq = Counter(words)
    keys, values = zip(*ent_freq.most_common(50))
    plt.figure(figsize=[13,6])
    plt.subplots_adjust(left=0.07, bottom=0.35, right=0.97)
    plt.plot(keys, values)
    plt.xlabel('Most common occurrences')
    plt.ylabel('Frequency')
    plt.xticks(rotation=85)
    plt.show()
    return span_location, ent_freq


nlp = spacy.load('nl_core_news_sm')

dataN = import_data_complex('flitsservice_trainset.csv', column="Artikel", complex='N')
dataY = import_data_complex('flitsservice_trainset.csv', column="Artikel", complex='Y')
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

input_dataN = get_location_descriptions(dataN, nlp)
input_dataY = get_location_descriptions(dataY, nlp)

word_pos_location_dict4, ent_freqN = word_pos_frequency(input_dataN, pos_list=["ADP"], pos_or_word=0)
word_pos_location_dict5, ent_freqY = word_pos_frequency(input_dataY, pos_list=["ADP"], pos_or_word=0)

keysY, valuesY = zip(*ent_freqY.most_common(50))
print("keysN:", keysY)
print("valuesN:", valuesY)

valuesN_list = []
for key in keysY:
    valuesN_list.append(ent_freqN.get(key, 0))



plt.bar( numpy.arange(len(valuesY)) * 3, height=valuesY, color = 'red' )
plt.bar( numpy.arange(len(valuesY)) * 3 + 1, height=valuesN_list, color = 'blue' )
plt.subplots_adjust(left=0.07, bottom=0.35, right=0.97)
plt.xticks(numpy.arange(len(valuesY)) * 3, keysY, rotation=80)
plt.show()

#search_p.show_pattern_occurrences("ADP #loc", word_pos_location_dict4, input_data)

#span_locations_ADPloc = search_p.adposition_frequencies_per_pattern("ADP #loc", word_pos_location_dict4, input_data)

#search_p.show_pattern_occurrences("naar #loc", span_locations_ADPloc, input_data)
