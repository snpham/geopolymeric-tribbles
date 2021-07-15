import numpy as np
import pandas as pd


def get_cols():
    data = pd.read_feather('study_data/integrated_data.feather')

    print(data.head())
    print(data.columns)

    with open('outputs/columns.csv', 'w') as f:
        for ii, column in enumerate(data.columns):
            f.writelines(f'{ii}, {column}, {data[column][:3].values} \n')



if __name__ == '__main__':

    # get_cols()

    data = pd.read_feather('study_data/integrated_data.feather')

    # print(data.head())
    # print(data.columns)

    attributes = {'Residency': 1,
                  'Trustingroups': 13,
                  'COVIDexp': 1,
                  'COVIDeffect': 4,
                  'CultCog': 6,
                  'FinitePool': 8,
                  'Longitude': 3,
                  'Personal': 8,
                  'Friends': 8,
                  'MediaExp': 7,
                  'Govresponse': 9,
                  'Govrestrict': 3,
                  'KnowledgeCert': 2,
                  'Vaccine': 2}

    # for att in range(1, trust_groups+1):
    #     print(data[f'Trustingroups_{att}'].describe())
    dfout = pd.DataFrame(index=[np.arange(0,len(data.columns), 1)], 
                         columns=['attr', 'count', 'unique', 'top', 'freq'])

    cases2run = ['Trustingroups']

    for case in cases2run:
        for att in range(1, attributes[case]+1):
            try:
                print(f'{case}_{att}', 
                    ' count:', data[f'{case}_{att}'].describe()[0],
                    ' unique:', data[f'{case}_{att}'].describe()[1],
                    ' top:', data[f'{case}_{att}'].describe()[2],
                    ' freq:', data[f'{case}_{att}'].describe()[3])
            except KeyError:
                print(f'{case}', 
                    ' count:', data[f'{case}'].describe()[0],
                    ' unique:', data[f'{case}'].describe()[1],
                    ' top:', data[f'{case}'].describe()[2],
                    ' freq:', data[f'{case}'].describe()[3])



