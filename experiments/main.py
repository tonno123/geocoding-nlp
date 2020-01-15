import spacy
from spacy.pipeline import merge_entities
import importlib as imp

nlp = spacy.load('nl_core_news_sm')
nlp.add_pipe(merge_entities)
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoRelationshipExtracter")

imp_data2 = imp.import_module('import_data_complex')
imp_data = imp.import_module('import_data')

predicates = imp.import_module('implementation')
geomap = imp.import_module('geomapping')
mining = imp.import_module('mine_location_descriptions')


def main_application(dataset, data_start, datarange):
    data = imp_data.import_data(dataset, column="Artikel") #,complex='Y')
    data = data[data_start:data_start+datarange]
    input_data = mining.get_location_descriptions(data, nlp)
    articlelist = predicates.extractADPLOCCombination(input_data)
    article_pred_list = predicates.NLtoPredicate(articlelist)
    article_pred_list = predicates.deleteDuplicateEntries(article_pred_list)
    for i in range(len(input_data)):
        print("Location spans detected in article:")
        print(input_data[i])
        print("Predicates found in article:")
        print(article_pred_list[i])
        print(geomap.findLocations(article_pred_list[i]))
        print("==========================================================")

# main_application('hetongelukscraped.csv',1000,7)
