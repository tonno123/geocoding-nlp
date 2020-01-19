
MARKER_WORDS = ['in', 'op', 'over', 'bij', 'hoogte', 'richting', 'naar', 'tussen', 'kruising','kruispunt','te', 'splitsing']

LOCATION_ENTITIES = ['GPE', 'FAC', 'LOC', 'NORP']

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
                    if token.pos_ == 'ADP' or token.text in ['richting', 'hoogte', 'kruising','kruispunt','splitsing']:
                        spanlist.append(token)
                    #elif token.pos_ == 'CONJ':
                    #    spanlist.append('CONJ' + token.text)
                    elif token.ent_type_ in LOCATION_ENTITIES:
                        spanlist.append(token)
            loccounter = -1
            prev_word_type = ''
            spanlist2 = []
            for word in list(reversed(spanlist)):
                if loccounter < 0 and not word.ent_type_ in LOCATION_ENTITIES:
                    continue
                elif word.pos_ != 'ADP' and word.ent_type_ in LOCATION_ENTITIES:
                    if not prev_word_type == 'LOC':
                        loccounter = loccounter + 1
                        spanlist2.append([[],[]])
                    spanlist2[loccounter][1].insert(0, word.text)
                    prev_word_type = 'LOC'
                elif word.pos_ == 'ADP' or word.text in ['richting', 'hoogte', 'kruising', 'kruispunt','splitsing']:
                    spanlist2[loccounter][0].insert(0, word)
                    prev_word_type = 'ADP'
                elif word.text.startswith('CNJ') and prev_word_type == 'LOC': #correct? Geen CONJ voor LOC zonder dat het tussen twee LOC's staat?
                    spanlist2[loccounter][1].insert(0, '/')
                else:
                    prev_word_type == ''
                    #else:
                    #    spanlist.append('#')
                #new_span = new_span.rpartition("#loc")  # more filtering required here
                #new_span = new_span[0] + new_span[1]
            sentencelist.append(list(reversed(spanlist2)))
        articlelist.append(sentencelist)
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
        'op'        : 'ON',
        'over'      : 'ON',
        'te'        : 'IN_LOC',
        'in'        : 'IN_LOC',
        'bij'       : 'AT',
        'hoogte'    : 'AT',
        'richting'  : 'HEADING',
        'naar'      : 'HEADING',
        'tussen'    : 'BETWEEN',
        'kruising'  : 'INTERSECT',
        'kruispunt' : 'INTERSECT',
        'splitsing' : 'INTERSECT'
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
