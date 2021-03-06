# most of the code in this file has been written by Christian Overdijk.
import spacy
from spacy.matcher import Matcher

#from import_data_json import import_data_json
from spacy.tokens import Span

def entity_detector(doc):
    entity_list = []
    for d in doc:
        if d.text[:3] == 'LOC':
            entity_list.append(d)
    return entity_list

Span.set_extension("entities", method=entity_detector, force=True)

# Takes data as pandas DataFrame (1 column)
# Needs trained nlp model (spaCy)
# Word_distane = number of tokens before and after found entities that are included with result
# Max_token_dist = maximum number op tokens between enities in one sentence before discriptions are considered different ans split
# Returns: list of result split per input, and than per sentence
def get_location_descriptions_json(data, nlpmodel, word_dist=7, max_token_dist=14):
    results = []

    for article in data:
        article_results = []

        doc = nlpmodel(article)

        for sent in doc.sents:
            sentence_results = []

            # Filter specified entities in 'entity_filter'
            ents = sent._.entities()

            # Skip sentence if no entities found
            if len(ents) == 0:
                continue

            # Calculate pairwise index difference
            ent_index_ranges = [(ent.i, ent.i+1) for ent in ents]
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
                start = max(sent.start, entities[0].i - word_dist)
                end = min(sent.end, entities[-1].i+1 + word_dist)
                result = doc[start:end]
                result._.entities = entities

                sentence_results.append(result)

            article_results.append(sentence_results)

        #if len(article_results) > 0:
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
