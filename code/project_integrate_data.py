import pandas as pd
import os
import glob

cwd=os.getcwd()
csv=glob.glob('data/COVID_19_misinformation/WintonCentreCleaned_covid_*_labelled.csv')

df=pd.read_csv(cwd + '\\' + csv[1])
standard_columns=list(df.columns)
# these attributes appear in some data sets but not all
missing=set(['Vaccine_1', 'CultCog_3', 'CultCog_5', 'CultCog_6', 'CultCog_2', 'CultCog_4', 'Vaccine_2', 'CultCog_1'])
truncated=list(set(standard_columns)-missing)
combined_df=pd.DataFrame(columns=standard_columns)
for i in csv[1:]:
    new_df=pd.read_csv(cwd + '\\' + i)
    try:
        combined_df=combined_df.append(new_df[standard_columns])
    except KeyError:
        # KeyError: "['Vaccine_1', 'CultCog_3', 'CultCog_5', 'CultCog_6', 'CultCog_2', 'CultCog_4', 'Vaccine_2', 'CultCog_1'] not in index"
        try:
            combined_df=combined_df.append(new_df[truncated])
        except:
            new_df.rename(columns={'Ethnic.min': 'Ethnic min'}, inplace=True)
            combined_df=combined_df.append(new_df[truncated])

# remove rows of not-data
combined_df=combined_df.loc[~combined_df.EndDate.isnull()]
combined_df=combined_df.loc[~(combined_df.EndDate=='End Date (GMT)')]
combined_df=combined_df.loc[~(combined_df.DemGen=='DemGen')]
combined_df=combined_df.reset_index().drop(columns=['index'])
combined_df=combined_df.drop([0])
attr=list(combined_df.columns)
#exclude columns that don't need to be floats
attr.remove('EndDate')
attr.remove('Residency')
attr.remove('prep')
float_df = combined_df[attr].astype('float')
combined_df=combined_df[['EndDate','Residency','prep']].join(float_df)
combined_df.to_csv("integrated_data.csv")
combined_df.reset_index().to_feather("integrated_data.feather")
df=pd.read_feather("integrated_data.feather")

