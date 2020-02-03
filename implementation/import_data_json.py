import pandas as pd
import json

def import_data_json(filepath, data_lines=100000, filepath_complex="", complex=""):
    if complex != "":
        df = pd.read_csv(filepath_complex, skipinitialspace=True)
        complex_column = df['Complex']
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
    data = data[:data_lines]
    result_articles = []
    for i, article in enumerate(data):
        if complex == "" or complex_column[i] == complex:
            location_list = []
            municipalities = article.get('municipalities')
            if municipalities:
                for el in municipalities:
                    location_list.append(el.get('name'))
            location_list.extend(article.get('annotations').keys())
            location_list = list(set(location_list))
            token_list = article.get('tokenized_text')
            new_token_list = []
            for token in token_list:
                if token in location_list:
                    token = "LOC" + token.replace(" ", "_")
                new_token_list.append(token)
            new_article = " ".join(new_token_list)
            result_articles.append(new_article)
    return result_articles

# result = import_data_json('../../data/flitsservice_trainset_annotated.json', filepath_complex='../../data/flitsservice_trainset.csv', complex='Y')
# for article in result:
#     print(article)
#     print("----------------------------")
# print(len(result))


# def import_data_json(filepath, data_lines=100000, filepath_complex="", complex=""):
#     if complex != "":
#         df = pd.read_csv(filepath_complex, skipinitialspace=True)
#         complex_column = df['Complex']
#     with open(filepath, 'r') as json_file:
#         data = json.load(json_file)
#     data = data[:data_lines]
#     result_articles = []
#     for i, article in enumerate(data):
#         if complex == "" or complex_column[i] == complex:
#             location_list = []
#             municipalities = article.get('municipalities')
#             if municipalities:
#                 for el in municipalities:
#                     location_list.append(el.get('name'))
#             location_list.extend(article.get('annotations').keys())
#             location_list = list(set(location_list))
#             token_list = article.get('tokenized_text')
#             new_token_list = []
#             for token in token_list:
#                 if token in location_list:
#                     token = "LOC" + token.replace(" ", "_")
#                 new_token_list.append(token)
#             new_article = " ".join(new_token_list)
#             result_articles.append(new_article)
#     return result_articles
