import numpy as np
import pandas as pd


def get_cols():
    data = pd.read_feather('study_data/integrated_data_old.feather')

    print(data.head())
    print(data.columns)

    with open('outputs/columns.csv', 'w') as f:
        for ii, column in enumerate(data.columns):
            f.writelines(f'{ii}, {column}, {data[column][:3].values} \n')


if __name__ == '__main__':

    # get headers for reference
    # get_cols()

    # get a list of attributes and their types
    d = {}
    with open('code/attr_types.txt') as f:
        d = dict(x.rstrip().split(None, 1) for x in f)

    # read integrated dataset
    data = pd.read_feather('study_data/integrated_data_old.feather')

    # print(data.head())
    # print(data.columns)

    # how many subset of attributes are in each attribute set in the data
    attributes = {'DemGen': 1,
                  'quota_age': 1,
                  'Residency': 1,
                  'GenSocTrust': 1,
                  'Trustingroups': 13,
                  'COVIDexp': 1,
                  'COVIDeffect': 4,
                  'SARS': 1,
                  'CultCog': 6,
                  'prosocial': 1,
                  'CanadaQ': 3,
                  'FinitePool': 8,
                  'Longitude': 3,
                  'Personal': 8,
                  'Friends': 8,
                  'MediaExp': 7,
                  'PosterstrustQ1': 1,
                  'SocialmediatrustQ1': 1,
                  'journalisttrustQ1': 1,
                  'govtrustQ1': 1,
                  'workplacetrustQ1': 1,
                  'FriendstrustQ1': 1,
                  'WHOtrustQ1': 1,
                  'Soughtinfo': 1,
                  'prep': 1,
                  'Govresponse': 9,
                  'Govrestrict': 3,
                  'Sciunderstand': 1,
                  'KnowledgeCert': 2,
                  'Vaccine': 2,
                  'Num1': 1,
                  'Num2a': 1,
                  'Num2b': 1,
                  'Num3': 1,
                  'NumeracyQ1': 1,
                  'DemAge': 1,
                  'DemEdu': 1,
                  'DemHealthcare': 1,
                  'Ethnic min': 1,
                  'Politics': 1,}

    # which cases to we want to run to see pandas' describe() results?
    all_cases = True
    if all_cases: # all cases
        cases2run = []
        for attr in attributes.keys():
            cases2run.append(attr)
    else: # single or set of cases
        cases2run = ['Trustingroups']

    # run describe() function
    dfstats = pd.DataFrame()
    for case in cases2run:
        for att in range(1, attributes[case]+1):
            if attributes[case] > 1:
                dfstats[f'{case}_{att}'] = data[f'{case}_{att}'].describe()
            else:
                dfstats[f'{case}'] = data[f'{case}'].describe()
    dfstats = dfstats.T

    dfstats.to_csv('outputs/df_stats.csv')

