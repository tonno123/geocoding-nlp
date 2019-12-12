import spacy

#import search_pattern as search_p
from mine_location_descriptions import get_location_descriptions
from import_data import import_data
from collections import Counter

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoRelationshipExtracter")

nlp = spacy.load('nl_core_news_sm')
data = import_data('hetongelukscraped.csv', column="Artikel")
data = data[:200]

input_data = get_location_descriptions(data, nlp)

MARKER_WORDS = ['in', 'op', 'over', 'bij', 'hoogte', 'richting', 'naar', 'tussen', 'kruising']

def extractADPLOCCombination(input_data):
    articlelist = []
    total_article_n = len(input_data)
    for article_n in range(total_article_n):
        sentencelist = []
        total_sentence_n = len(input_data[article_n])
        for sentence_n in range(total_sentence_n):
            spanlist = []
            total_span_n = len(input_data[article_n][sentence_n])
            for span_n in range(total_span_n):
                for token in input_data[article_n][sentence_n][span_n]:
                    if token.pos_ == 'ADP' or token.text in ['richting', 'hoogte', 'kruising']:
                        spanlist.append(token)
                    #elif token.pos_ == 'CONJ':
                    #    spanlist.append('CONJ' + token.text)
                    elif token.ent_type_ in ['GPE', 'FAC', 'LOC', 'NORP']:
                        spanlist.append(token)
            loccounter = -1
            prev_word_type = ''
            spanlist2 = []
            for word in list(reversed(spanlist)):
                if loccounter < 0 and not word.ent_type_ in ['GPE', 'FAC', 'LOC', 'NORP']:
                    continue
                elif word.ent_type_ in ['GPE', 'FAC', 'LOC', 'NORP']:
                    if not prev_word_type == 'LOC':
                        loccounter = loccounter + 1
                        spanlist2.append([[],[]])
                    spanlist2[loccounter][1].insert(0, word)
                    prev_word_type = 'LOC'
                elif word.pos_ == 'ADP' or word.text in ['richting', 'hoogte', 'kruising']:
                    spanlist2[loccounter][0].insert(0, word)
                    prev_word_type = 'ADP'
                elif word.startswith('CNJ') and prev_word_type == 'LOC': #correct? Geen CONJ voor LOC zonder dat het tussen twee LOC's staat?
                    spanlist2[loccounter][1].insert(0, '/')
                else:
                    prev_word_type == ''
                    #else:
                    #    spanlist.append('#')
                #new_span = new_span.rpartition("#loc")  # more filtering required here
                #new_span = new_span[0] + new_span[1]
            sentencelist.append(list(reversed(spanlist2)))
        print(sentencelist)
        print("=====================================================================")
        articlelist.append(sentencelist)
    print(articlelist)
    return articlelist



def chooseADP(ADPlist):
    if not ADPlist:
        return None
    for token in reversed(ADPlist):
        if token.lower_ in MARKER_WORDS:
            return token.lower_
    return None

def predicateSwitcher(ADP):
    switcher = {
        'in'        : 'IN',
        'op'        : 'IN',
        'over'      : 'IN',
        'bij'       : 'AT',
        'hoogte'    : 'AT',
        'richting'  : 'HEADING',
        'naar'      : 'HEADING',
        'tussen'    : 'BETWEEN',
        'kruising'  : 'INTERSECT',
    }
    return switcher.get(ADP)

def NLtoPredicate(articlelist):
    article_pred_list = []
    for article in articlelist:
        sent_pred_list = []
        for sentence in article:
            loc_list = []
            for loc_mention in sentence:
                bestADP = chooseADP(loc_mention[0])
                if bestADP:
                    loc_list.append([predicateSwitcher(bestADP), loc_mention[1]])
            if loc_list: sent_pred_list.append(loc_list)
        print(sent_pred_list)
        print("==========================================")
        article_pred_list.append(sent_pred_list)
    return article_pred_list

            #
            # search_query = ''
            # for location in loc_list:
            #     if location[0] == 'IN':
            #         search_query = search_query + location[1]
            # location = geolocator.geocode(search_query)
            # print(location.address)
            # print(location.latitude, location.longitude)
            # print(location.raw.get('type'))
            # print(location.raw)

# articlelist = extractADPLOCCombination(input_data)
# article_pred_list = NLtoPredicate(articlelist)

# words = []
# span_counter = 0
# span_location = {}
#
# articlelist = []
# total_article_n = len(input_data)
# for article_n in range(total_article_n):
#     sentencelist = []
#     total_sentence_n = len(input_data[article_n])
#     for sentence_n in range(total_sentence_n):
#         spanlist = []
#         total_span_n = len(input_data[article_n][sentence_n])
#         for span_n in range(total_span_n):
#             for token in input_data[article_n][sentence_n][span_n]:
#                 if token.ent_type_ in ['GPE', 'FAC', 'LOC', 'NORP']:
#                     spanlist.append('LOC' + token.text)
#                 elif token.pos_ == 'ADP' or token.text in ['richting', 'hoogte', 'kruising']:
#                     spanlist.append('ADP' + token.text)
#                 #else:
#                 #    spanlist.append('#')
#             #new_span = new_span.rpartition("#loc")  # more filtering required here
#             #new_span = new_span[0] + new_span[1]
#         sentencelist.append(spanlist)
#     articlelist.append(sentencelist)
# print(articlelist)
