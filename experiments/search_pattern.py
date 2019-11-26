import spacy
import string

from mine_location_descriptions import get_location_descriptions
from import_data import import_data

def search_pattern(search_str, dict, input_data):
    if not dict.get(search_str):
        print("Pattern not found, try again.")
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
                    print(input_data[article_n][sentence_n][span_n].text)
                    if list_n == len(span_list) - 1:
                        return
                    list_n = list_n + 1
                span_counter = span_counter + 1
