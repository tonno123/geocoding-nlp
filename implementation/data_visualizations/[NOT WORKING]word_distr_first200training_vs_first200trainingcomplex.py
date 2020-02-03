import sys
sys.path.append('..')

import spacy
nlp = spacy.load('nl_core_news_sm')

from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import import_data_json as import_json
import mine_location_descriptions_json as mine_json
import data_vis_functions as visual

data_200 = import_json.import_data_json('../../data/flitsservice_trainset.json', 200)
data_complex = import_json.import_data_json('../../data/flitsservice_trainset.json', filepath_complex='../../data/flitsservice_trainset.csv', complex='Y')


input_data_200 = mine_json.get_location_descriptions_json(data_200, nlp)
input_data_complex = mine_json.get_location_descriptions_json(data_complex, nlp)

words_200 = visual.word_count(input_data_200)
words_complex = visual.word_count(input_data_complex)

word_distr_200 = Counter(words_200)
word_distr_complex = Counter(words_complex).most_common(35)

print(input_data_complex)
print("Length:", len(input_data_complex))

keysC, valuesC = zip(*word_distr_complex)
values_200 = []
for key in keysC:
    values_200.append(word_distr_200.get(key, 0))

valuesC_norm = [x / len(words_complex) for x in valuesC]
values_200_norm = [x / len(words_200) for x in values_200]

print("keys complex:", keysC)
print("values complex:", valuesC_norm)

################ TOPONYM DISTRIBUTION #########################################################
range = np.arange(0, 35)
sns.distplot(valuesC_norm, bins=keysC, kde_kws={"bw":'1'}, axlabel="Number of toponym mentions per article")
sns.distplot(values_200_norm, bins=keysC, kde_kws={"bw":'1'})
plt.xlim(0, 35)
plt.xticks(range)
plt.ylabel("Distribution")
plt.legend(['Entire trainingset', 'First 200 trainingset articles'],loc=1)
plt.show()
