import spacy
from spacy.matcher import Matcher

from import_data import import_data
from spacy.tokens import Span

# TODO -> test results with 'LOC' / 'NORP' entities removed

# Entities to detect in text
# GPE	Countries, cities, states.
# FAC	Buildings, airports, highways, bridges, etc.
# LOC	Non-GPE locations, mountain ranges, bodies of water.
# NORP	Nationalities or religious or political groups.
ENTITY_LIST = ['GPE', 'FAC', 'LOC', 'NORP']

def on_match(matcher, doc, id, matches):
    if doc[matches[0][1]].text == "richting" or doc[matches[0][1]].text == "kruising":
        # print("------------------------------------------------")
        # print(doc[matches[0][1]], " : ", doc[matches[0][1]].pos_)
        doc[matches[0][1]].pos_ = "ADP"
        # print(doc[matches[0][1]], " : ", doc[matches[0][1]].pos_)

def terhoogte_match(matcher, doc, id, matches):
    if doc[matches[0][1]+1].text == "hoogte":
        # print("------------------------------------------------")
        # print(doc[matches[0][1]+1], " : ", doc[matches[0][1]+1].pos_)
        doc[matches[0][1]+1].pos_ = "ADP"
        # print(doc[matches[0][1]+1], " : ", doc[matches[0][1]+1].pos_)

def delete_match(matcher, doc, id, matches):
    if doc[matches[0][1]].text == "van" or doc[matches[0][1]].text == "met":
        # print("------------------------------------------------")
        # print(doc[matches[0][1]], " : ", doc[matches[0][1]].pos_)
        doc[matches[0][1]].pos_ = "X"
        # print(doc[matches[0][1]], " : ", doc[matches[0][1]].pos_)


Span.set_extension("entities", default=[])

# Takes data as pandas DataFrame (1 column)
# Needs trained nlp model (spaCy)
# Word_distane = number of tokens before and after found entities that are included with result
# Max_token_dist = maximum number op tokens between enities in one sentence before discriptions are considered different ans split
# Returns: list of result split per input, and than per sentence
def get_location_descriptions(data, nlpmodel, word_dist=4, max_token_dist=8, entity_filter=ENTITY_LIST):
    results = []



    for article in data:
        article_results = []

        matcher = Matcher(nlpmodel.vocab)
        matcher.add("van", delete_match, [{'LOWER': 'van'}])
        matcher.add("met", delete_match, [{"LOWER":  "met"}])
        matcher.add("richting", on_match, [{"LOWER": "richting"}])
        matcher.add("kruising", on_match, [{"LOWER": "kruising"}])
        matcher.add("testtest", terhoogte_match, [{"LOWER": "ter"},{"LOWER": "hoogte"}])

        doc = nlpmodel(article)

        matches = matcher(doc)

        for sent in doc.sents:
            sentence_results = []

            # Filter specified entities in 'entity_filter'
            ents = []
            for ent in sent.ents:
                if ent.label_ in entity_filter:
                    ents.append(ent)

            # Skip sentence if no entities found
            if len(ents) == 0:
                continue

            # Calculate pairwise index difference
            ent_index_ranges = [(ent.start, ent.end) for ent in ents]
            pairwise_diff = [r[0] - ent_index_ranges[i-1][1] for i,r in enumerate(ent_index_ranges)][1:]

            # Check if multiple descriptions exist in sentence
            # based on MAX_TOKEN_DIST -> split
            entities_to_progress = []
            temp = []
            for i, ent in enumerate(ents):
                temp.append(ent)
                if i >= len(pairwise_diff):
                    entities_to_progress.append(temp)
                    break
                if pairwise_diff[i] > max_token_dist:
                    entities_to_progress.append(temp)
                    temp = []

            # Process entities, get WORD_DIST words before and after entities
            for entities in entities_to_progress:
                start = max(sent.start, entities[0].start - word_dist)
                end = min(sent.end, entities[-1].end + word_dist)
                result = doc[start:end]
                result._.entities = entities

                sentence_results.append(result)

            article_results.append(sentence_results)

        if len(article_results) > 0:
            #print(article_results)
            results.append(article_results)

    return results


# Test
if __name__ == '__main__':
    nlp = spacy.load('nl_core_news_sm')

    data = import_data('hetongelukscraped.csv')
    articles = data['Artikel']

    mydata = articles[:10]

    results = get_location_descriptions(mydata, nlp)
