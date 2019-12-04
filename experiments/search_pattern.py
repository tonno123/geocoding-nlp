# import spacy
# import string
import sys
import matplotlib.pyplot as plt
import pandas as pd

#from mine_location_descriptions import get_location_descriptions
from collections import Counter
from mine_location_descriptions import ENTITY_LIST
#from import_data import import_data

def show_pattern_occurrences(search_str, dict, input_data):
    if not dict.get(search_str):
        print("Pattern not found, try a different pattern.")
        return
    span_list = dict.get(search_str)
    list_n = 0
    span_counter = 0
    total_article_n = len(input_data)
    for article_n in range(total_article_n):
        total_sentence_n = len(input_data[article_n])
        for sentence_n in range(total_sentence_n):
            total_span_n = len(input_data[article_n][sentence_n])
            for span_n in range(total_span_n):
                if span_list[list_n] == span_counter:
                    for token in input_data[article_n][sentence_n][span_n]:
                        if token.pos_ == "ADP":
                            sys.stdout.write(" " + "\033[92m" + token.text + "\033[0m")
                        elif token.ent_type_ in ENTITY_LIST:
                            sys.stdout.write(" " + "\033[91m" + token.text + "\033[0m" + token.ent_type_)
                        else:
                            sys.stdout.write(" " + token.text + "\033[33m" + token.pos_ + "\033[0m")
                    sys.stdout.write('\n')
                    if list_n == len(span_list) - 1:
                        return
                    list_n = list_n + 1
                span_counter = span_counter + 1

def adposition_frequencies_per_pattern(search_str, dict, input_data):
    if not dict.get(search_str):
        print("Pattern not found, try a different pattern.")
        return
    span_list = dict.get(search_str)
    list_n = 0
    span_counter = 0
    all_spans = []
    span_locations = {}
    total_article_n = len(input_data)
    for article_n in range(total_article_n):
        total_sentence_n = len(input_data[article_n])
        for sentence_n in range(total_sentence_n):
            total_span_n = len(input_data[article_n][sentence_n])
            for span_n in range(total_span_n):
                new_span = ''
                if span_list[list_n] == span_counter:
                    for token in input_data[article_n][sentence_n][span_n]:
                        if token.pos_ == "ADP":
                            new_span = new_span + token.lower_ + ' '
                        elif token.ent_type_ in ENTITY_LIST:
                            new_span = new_span + "#loc" + ' '

                    # deleting all adpositions after the last detected toponym
                    new_span = new_span.rpartition("#loc")  # more filtering required here
                    new_span = new_span[0] + new_span[1]

                    all_spans.append(new_span)
                    if list_n == len(span_list) - 1:
                        break
                    list_n = list_n + 1

                # adding each new span to dict for possible retrieval by
                # function adposition_frequencies_per_pattern
                    if new_span in span_locations:
                        span_locations[new_span].append(span_counter)
                    else:
                        span_locations[new_span] = [span_counter]

                span_counter = span_counter + 1
    adp_frequency = pd.DataFrame(Counter(all_spans).most_common(50), columns=['pattern', 'frequency'])
    adp_frequency.plot(kind='bar', figsize=[13,6], position=0.65, x='pattern', y='frequency')
    plt.show()
    return span_locations
