import spacy
import importlib as imp

nlp = spacy.load('nl_core_news_sm')
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoRelationshipExtracter")

imp_data2 = imp.import_module('import_data_complex')
imp_data = imp.import_module('import_data')

predicates = imp.import_module('implementation')
geomap = imp.import_module('geomapping')
mining = imp.import_module('mine_location_descriptions')

data = imp_data2.import_data_complex('flitsservice_trainset.csv', column="Artikel",complex='Y')
data = data[:30]
input_data = mining.get_location_descriptions(data, nlp)



articlelist = predicates.extractADPLOCCombination(input_data)
article_pred_list = predicates.NLtoPredicate(articlelist)
article_pred_list = predicates.deleteDuplicateEntries(article_pred_list)
print(article_pred_list)
print(article_pred_list[20])


geomap.findLocations(article_pred_list[20])
