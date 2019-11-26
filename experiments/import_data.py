import pandas as pd
import spacy

data_location = '../data/'

# TODO: add compatability for more file types
# General import function to import data files
# Returns pandas DataFrame
def import_data(file, filetype='csv', column="", usecols=[]):
    loc = data_location + file

    if usecols:
        df = pd.read_csv(loc, skipinitialspace=True, usecols=usecols)
    else:
        df = pd.read_csv(loc, skipinitialspace=True)

    # Remove Whitespaces
    df = df.apply(lambda x: x.str.replace("\t", ""))
    df = df.apply(lambda x: x.str.replace("\r", ""))
    df = df.apply(lambda x: x.str.replace("\n", ""))

    if column:
        df = df[column]

    return df

# Test
if __name__ == '__main__':

    file = 'transport-online_trainset.csv'

    df = import_data(file, column="Artikel", usecols=[1,2,3])

    print(df)
