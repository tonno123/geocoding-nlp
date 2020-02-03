from collections import Counter

def isHighway(roadname):
    if roadname[:1] is 'A' or roadname[:1] is 'N':
        if roadname[1:2].isdigit():
            return True
    return False

def toponym_count(data):
    highway_count_list = []
    topo_count_list = []
    for article in data:
        topo_count = 0
        highway_count = 0
        for span in article:
            for sentence in span:
                for token in sentence:
                    if token.text[:3] == 'LOC':
                        topo_count = topo_count + 1
                        if isHighway(token.text[3:]):
                            highway_count = highway_count + 1
        highway_count_list.append(highway_count)
        topo_count_list.append(topo_count)
    return topo_count_list, highway_count_list


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
                    elif add_tokens and not(token.is_punct) and not(token.text[:3] == 'LOC'):
                        words.append(token.lower_)
    return words
