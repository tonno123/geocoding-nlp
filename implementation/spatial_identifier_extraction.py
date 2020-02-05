
MARKER_WORDS = ['in', 'op', 'over', 'te', 'bij', 'nabij', 'hoogte', 'richting', 'naar', 'tussen', 'kruising','kruispunt', 'splitsing', 't-splitsing']

def extractADPLOC(input_data):
    articlelist = []
    for article in input_data:
        sentencelist = []
        for sentence in article:
            spanlist = []
            for span in sentence:
                ADP_LOC = [[], []]
                spanlist2 = []
                loc_detected = False
                for word in list(reversed(span)):
                    if word.text[:3] == 'LOC':
                        loc_detected = True
                        if ADP_LOC[0]:
                            spanlist2.insert(0, ADP_LOC)
                            ADP_LOC = [[], [word.text[3:].replace("_", " ")]]
                        else:
                            ADP_LOC[1].insert(0, word.text[3:].replace("_", " "))
                    elif loc_detected and word.lower_ in MARKER_WORDS:
                        ADP_LOC[0].insert(0, word.lower_)
                spanlist2.insert(0, ADP_LOC)
            sentencelist.append(spanlist2)
        articlelist.append(sentencelist)
    return articlelist

def chooseADP(ADPlist):
    if not ADPlist:
        return None
    result_list = []
    for ADP in ADPlist:
        result_list.append(predicateSwitcher(ADP))
    if 'INTERSECT' in result_list:
        return 'INTERSECT'
    else:
        return result_list[-1]

def predicateSwitcher(ADP):
    switcher = { #nabij?
        'op'        : 'ON',
        'over'      : 'ON',
        'te'        : 'IN_LOC',
        'in'        : 'IN_LOC',
        'bij'       : 'AT',
        'nabij'     : 'AT',
        'hoogte'    : 'AT',
        'richting'  : 'HEADING',
        'naar'      : 'HEADING',
        'tussen'    : 'BETWEEN',
        'kruising'  : 'INTERSECT',
        'kruispunt' : 'INTERSECT',
        'splitsing' : 'INTERSECT',
        't-splitsing':'INTERSECT'
    }
    return switcher.get(ADP)

def ADPLOCtoPredicate(articlelist):
    article_pred_list = []
    for article in articlelist:
        sent_pred_list = []
        for sentence in article:
            loc_list = []
            for loc_mention in sentence:
                bestADP = chooseADP(loc_mention[0])
                if bestADP:
                    loc_list.append([bestADP, loc_mention[1]])
            if loc_list: sent_pred_list.append(loc_list)
        article_pred_list.append(sent_pred_list)
    return article_pred_list

def matchSentence(match, article):
    for sentence in article:
        for location in sentence:
            if match == location:
                return True
    return False

def deleteDuplicateEntries(articlelist):
    new_articlelist = []
    for article in articlelist:
        i = 0
        while i < len(article):
            article_copy = article[:i] + article[(i+1):]
            if matchSentence(article[i][0], article_copy):
                article = article_copy
            else:
                i = i+1
        else:
            i = i+1
            new_articlelist.append(article)
    return new_articlelist

#articlelist = extractADPLOCCombination(input_data)
#article_pred_list = NLtoPredicate(articlelist)
#print(article_pred_list)
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
