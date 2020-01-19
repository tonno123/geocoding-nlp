import json
import spacy
from spacy.tokens import Span
from spacy.tokens import Doc

nlp = spacy.load('nl_core_news_sm')

def entity_detector(doc):
    entity_list = []
    for d in doc:
        if d.text[:3] == 'LOC':
            entity_list.append(d)
    return entity_list


def load_json_file(filepath):
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
    return data

data = load_json_file('flitsservice_trainset_annotated.json')
data = data[10:11]
for article in data:
    location_list = []
    municipalities = article.get('municipalities')
    if municipalities:
        for el in municipalities:
            location_list.append(el.get('name'))
    location_list.extend(article.get('annotations').keys())
    location_list = list(set(location_list))
    #print(location_list)
    token_list = article.get('tokenized_text')
    new_token_list = []
    for token in token_list:
        if token in location_list:
            token = "LOC" + token.replace(" ", "_")
        new_token_list.append(token)
    new_article = " ".join(new_token_list)
    print(new_article)
    doc = nlp(new_article)
    Span.set_extension("entities", method=entity_detector, force=True)
    results = []
    article_results = []
    for sent in doc.sents:
        ents = sent._.entities()
        word_dist=4
        max_token_dist=8
        sentence_results = []


        ent_index_ranges = [(ent.i, ent.i + 1) for ent in ents]
        print(ent_index_ranges)
        pairwise_diff = [r[0] - ent_index_ranges[i-1][1] for i,r in enumerate(ent_index_ranges)][1:]
        print(pairwise_diff)
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
        print(entities_to_progress)
        # Process entities, get WORD_DIST words before and after entities
        for entities in entities_to_progress:
            start = max(sent.start, entities[0].i - word_dist)
            end = min(sent.end, entities[-1].i + 1 + word_dist)
            result = doc[start:end]
            result._.entities = entities
            sentence_results.append(result)
        article_results.append(sentence_results)
    if len(article_results) > 0:
        #print(article_results)
        results.append(article_results)
print(results)




# extract toponyms CHECK
# remove duplicates CHECK
# mark toponyms in tokenized text CHECK
# replace spaces with underscore CHECK
# make tokenized text into sentences
# run spacy
