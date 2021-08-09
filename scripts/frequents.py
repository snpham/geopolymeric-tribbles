import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def data_gen(dataset):
    for row in dataset.iloc[:,0]:
        yield row.replace(" ", "").split(",")


def row_gen(dataset):
    for row in dataset:
        yield row.replace(" ", "").split(",")


def threshold(data, min_sup):
    return {item:count for item, count in data.items() if count >= min_sup}


def union_set(datadict):
    return set([','.join((i, j)) for i in datadict for j in datadict if i < j])


def apriori_assoc(df, datadict1, datadict2, label):
    # support
    splitlabel = label.split(',')
    for key, _ in datadict2.items():
        if set(splitlabel).issubset(key.split(',')):
            labl = key
        else:
            continue
    supp = datadict2[labl]/len(df.index)

    # confidence
    for key1, val1 in datadict1.items():
        if set(splitlabel[:-1]).issubset(key1.split(',')):
            for key2, val2 in datadict2.items():
                if set(splitlabel).issubset(key2.split(',')):
                    conf = val2/val1
    string = f'{splitlabel[:-1]} -> {splitlabel[-1]}'
    return string, supp, conf


def apriori(dataset, min_sup):

    freq1_items = set()
    for data in data_gen(dataset):
        for item in data:
            freq1_items.add(item)
    # print('itemset:', freq1_items)

    scan1 = dict.fromkeys(freq1_items, 0)
    for data in data_gen(dataset):
        for item in data:
            scan1[item] += 1
    scan1 = threshold(scan1, min_sup)
    scan1 = dict(sorted(scan1.items()))

    unionset1 = union_set(scan1)
    scan2 = dict.fromkeys(unionset1, 0)
    for data in data_gen(dataset):
        for row in scan2:
            if set(row.split(',')).issubset(set(data)):
                scan2[row] += 1
    scan2 = threshold(scan2, min_sup)
    scan2 = dict(sorted(scan2.items()))

    unionset2 = union_set(scan2)
    newunion2 = set()
    for row in unionset2:
        newset = set(sorted(row.split(',')))
        for col in row_gen(scan2):
            if set(col).issubset(newset) and scan2[','.join(col)] >= 3 and len(newset) == 3:
                newunion2.add(','.join(newset))
    scan3 = dict.fromkeys(newunion2, 0)

    for data in data_gen(dataset):
        for row in scan3:
            if set(row.split(',')).issubset(set(data)):
                scan3[row] += 1
    scan3 = threshold(scan3, min_sup)
    scan3 = dict(sorted(scan3.items()))

    # print('frequent-1 itemset:', scan1)
    # print('frequent-2 itemset:', scan2)
    # print('frequent-3 itemset:', scan3)
    
    return scan1, scan2, scan3


if __name__ == '__main__':


    ## project - frequent itemsets
    dataset = pd.read_csv('study_data/integrated_data_v3.csv', index_col=0, header=0)
    dataset_prep = dataset[['prep']].dropna()
    dataset_prep = dataset_prep[~dataset_prep.prep.str.contains("E+")]
    dataset_country = dataset[['Residency','prep']].dropna()
    dataset_country = dataset_country[~dataset_country.prep.str.contains("E+")]

    # get all countries with frequent-set 1
    countries = ['US', 'CN', 'AU', 'DE', 'ES', 'IT', 'JP', 'KR', 'MX', 'UK', 'SE']
    df_countries = []
    minsup_countries = []
    scans1_countries = []
    scans2_countries = []
    scans3_countries = []
    gobars = []
    for ii, country in enumerate(countries):
        df_country = dataset_country[dataset_country['Residency'] == country]
        minsup_country = 0.010 * len(df_country)
        df_country = df_country.drop('Residency', axis=1)
        scans1_country, _, _ = apriori(df_country, minsup_country)
        scans1_country = {key:value/len(df_country) for (key, value) in scans1_country.items()}
        gobars.append(go.Bar(name=country, x=list(scans1_country.keys()), 
                             y=list(scans1_country.values()), base=0))
    fig = go.Figure(data=gobars[:])
    # Change the bar mode
    fig.update_layout(barmode='relative', xaxis=dict(
        title='activities',titlefont_size=16,tickfont_size=14),yaxis=dict(
        title='support',titlefont_size=16,tickfont_size=14))
    # fig.write_image("outputs/plots/support_countries.pdf")
    # fig.show()


    # get global frequentset-1
    min_sup = 0.01
    min_sup *= len(dataset_prep)
    scan1, scan2, scan3 = apriori(dataset_prep, min_sup)
    dfprep = pd.read_csv('study_data/metadata.csv', index_col=0, 
                         header=None, usecols=range(1,4), encoding='latin1')

    prep_dict = {}
    for val in dfprep.loc['prep', 3].strip().split(','):
        val = val.split('=')
        prep_dict[val[0].strip()] = val[1].strip()
    
    dfprep_desc = pd.DataFrame.from_dict(prep_dict, orient='index', columns=['Description'])
    table = go.Figure(data=[go.Table(
                            columnwidth=[1, 4],
                            header=dict(values=['Activity', 'Description']),
                            cells=dict(values=[list(prep_dict.keys()),
                                               list(prep_dict.values())]))])
    # table.write_image("outputs/plots/table.pdf")
    # table.show()

    # # to use activity description instead
    # prep_merged = {value:scan1[key] for (key, value) in prep_dict.items()}
    # prep_merged = {key:value/len(dataset_prep) for (key, value) in prep_merged.items()}
    # # print(prep_merged)

    update_layout = dict(barmode='group', title='Support of Preparation Activities',
                        yaxis=dict( titlefont_size=16, tickfont_size=16, range=[0, 1]),
                        xaxis=dict( tickangle=-45, titlefont_size=16, tickfont_size=16))
    update_traces = dict(marker_color='rgb(55, 83, 109)', marker_line_color='rgb(8,48,107)',
                    marker_line_width=1.5, opacity=0.7)

    prep_merged = {key:value/len(dataset_prep) for (key, value) in scan1.items()}

    prep_merged = pd.DataFrame.from_dict(prep_merged, orient='index', columns=['support'])
    # print(prep_merged)
    fig = px.bar(prep_merged, x=prep_merged.index, y='support', labels={'index': 'activities'})
    fig.update_traces(update_traces)
    fig.update_layout(update_layout)
    # fig.write_image("outputs/plots/frequent_itemset1.pdf")
    # fig.show()

    # increase support and view higher frequentsets (2 and 3)
    update_layout = dict(barmode='relative',
                        yaxis=dict(titlefont_size=16, tickfont_size=16, range=[0.4, 0.90]),
                        xaxis=dict(tickangle=-45, titlefont_size=16, tickfont_size=16))
    min_sup = 0.5
    min_sup *= len(dataset_prep)
    scan1, scan2, scan3 = apriori(dataset_prep, min_sup)
    prep2 =  {key:value/len(dataset_prep) for (key, value) in scan2.items()}
    prep2_supp = pd.DataFrame.from_dict(prep2, orient='index', columns=['support'])
    fig = px.bar(prep2_supp, x=prep2_supp.index, y='support', labels={'index': 'activities'})
    fig.update_traces(update_traces)
    fig.update_layout(update_layout)
    fig.update_layout(title='Support of Preparation Activities - frequentset-2')
    # fig.write_image("outputs/plots/frequent_itemset2.pdf")
    # fig.show()


    prep3 =  {key:value/len(dataset_prep) for (key, value) in scan3.items()}
    prep3_supp = pd.DataFrame.from_dict(prep3, orient='index', columns=['support'])
    fig = px.bar(prep3_supp, x=prep3_supp.index, y='support', labels={'index': 'activities'})
    fig.update_traces(update_traces)
    fig.update_layout(update_layout)
    fig.update_layout(title='Support of Preparation Activities - frequentset-3')
    # fig.write_image("outputs/plots/frequent_itemset3.pdf")
    # fig.show()
