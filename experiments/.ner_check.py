import spacy
import sys
from mine_location_descriptions import get_location_descriptions
from import_data import import_data

nlp = spacy.load('nl_core_news_sm')

data = import_data('hetongelukscraped.csv', column="Artikel")
#data = data[:50]

input_data = get_location_descriptions(data, nlp)

total_article_n = len(input_data)
for article_n in range(total_article_n):
    total_sentence_n = len(input_data[article_n])
    for sentence_n in range(total_sentence_n):
        total_span_n = len(input_data[article_n][sentence_n])
        for span_n in range(total_span_n):
            for token in input_data[article_n][sentence_n][span_n]:
                if token.ent_type_ in ['GPE', 'FAC', 'LOC', 'NORP']:
                    sys.stdout.write("\033[91m" + token.text + " " + token.ent_type_ + "\033[0m" + " ")
                else:
                    sys.stdout.write(token.text + " ")
            sys.stdout.write('\n')
