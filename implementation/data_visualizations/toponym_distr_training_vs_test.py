import sys
sys.path.append('..')

import spacy
nlp = spacy.load('nl_core_news_sm')

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import import_data_json as import_json
import mine_location_descriptions_json as mine_json
import data_vis_functions as visual

data = import_json.import_data_json('../../data/testsets/flitsservice_testset.json')
input_data = mine_json.get_location_descriptions_json(data, nlp)
topo_count_list, highway_count_list = visual.toponym_count(input_data)

data2 = import_json.import_data_json('../../data/flitsservice_trainset.json')
input_data2 = mine_json.get_location_descriptions_json(data2, nlp)
topo_count_list2, highway_count_list2 = visual.toponym_count(input_data2)


################ TOPONYM DISTRIBUTION #########################################################
range = np.arange(0, 20)
sns.distplot(topo_count_list2, bins=range, kde_kws={"bw":'1'}, axlabel="Number of toponym mentions per article")
sns.distplot(topo_count_list, bins=range, kde_kws={"bw":'1'})
plt.xlim(0, 20)
plt.xticks(range)
plt.ylabel("Distribution")
plt.legend(['Trainingset', 'Testset'],loc=1)
plt.show()

############### HIGHWAY DISTRIBUTION #########################################################
range = np.arange(0, 9)
sns.distplot(highway_count_list2, bins=range, kde_kws={"bw":'1'}, axlabel="Number of highway mentions per article")
sns.distplot(highway_count_list, bins=range, kde_kws={"bw":'1'})
plt.xlim(0, 9)
plt.xticks(range)
plt.ylabel("Distribution")
plt.legend(['Trainingset', 'Testset'],loc=1)
plt.show()
