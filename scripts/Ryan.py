def DF(filename):
    return pd.read_csv(filename, dtype=str)

#The basic function for getting data based on column name. Returns a dictionary
def getColStats(df, columnName, mean=True, median=True, mode=True, std=True, var=True):
    retDict = {}
    series = pd.to_numeric(df[columnName], errors='coerce')
    retDict['ColName'] = columnName
    if mean:
        retDict["Mean"] = series.mean()
    if median:
        retDict["Median"] = series.median()
    if mode:
        retDict["Mode"] = series.mode(dropna = True)
    if std:
        retDict["Std"] = series.std()
    return retDict


def getAllStats(df):
    #Takes a dataframe
    #Mode often doesn't work properly with sparse values,
    # so it's off by default
    for col in df.columns:
        return getColStats(df, col, mode=False)
    
           
def getCountryStats(df, countryName):
    #Returns all column stats for a specified 'Residency' value 
    filteredDF = df[df['Residency'] == countryName]
    return getAllStats(filteredDF)

def makeBetterFile(fileName):
    #The original file had multiple title lines at random points
    # in the csv file, so this function just creates a new, cleaner
    # version
    counter = 0
    with open(fileName, 'r') as f:
        with open(fileName[0:-4] + "New" + fileName[-4:], 'w+') as f2:
            for line in f.readlines():
                if counter == 0:
                    f2.write(line)
                lineList = line.split(',')
                if len(lineList) < 20:
                    continue
                try:
                    lineList[2] = int(lineList[2])
                except:
                    continue
                f2.write(line)
                counter += 1

def pltColumns(dfI, col1, col2, numClusters=2, plot=True, country=None, alp=0.01):
    # dfI is the (uncleaned) dataframe. Col1 and Col2 are the string titles of the columns.
    # You can filter by country using the 'country' variable
    # 'alp'  is the transparency value on the scatter plot (0 is non-existent, 1 is completely opaque)
    if country != None:
        df = dfI[dfI['Residency'] == country]
        df = df[[col1,col2]][4:]
    else:
        df = dfI[[col1,col2]][4:]
    df = df.dropna()
    df = df.astype(float)
    kmeans = skl.KMeans(n_clusters= numClusters)
    kmeans.fit(df)
    print(df.corr())
    #print("Cluster centers: ", kmeans.cluster_centers_)
    if plot:
        plt.plot(df[col1].to_numpy(), df[col2].to_numpy(), "o", alpha=30/(len(df[col1])))
        plt.xlabel(str(dfI[col1][1]), wrap=True)
        plt.ylabel(str(dfI[col2][1]), wrap=True)
        
        #plt.plot(kmeans.cluster_centers_)
        plt.show()

def scatterColumns(dfI, col1, col2):
    df = dfI[[col1,col2]][4:]
    df = df.dropna()
    plt.plot(df[col1], df[col2], alpha=0.1)
    plt.show()
    
    
def getDFcorr(df, cleaned=False):
    #Cleans the dataframe, returns a correlation table
    # as well as a simplified Min/Max value table
    if not cleaned:
        df = cleanDF(df)
    df = df.apply(pd.to_numeric, errors='coerce')
    c = df.corr().round(2)
    for col in c.columns:
        c[col][col] = 0
    retdf = pd.DataFrame()
    retdf['Max'] = c.idxmax(axis=1)
    retdf['Max_Value'] = c.max(skipna=True)
    retdf['Min'] = c.idxmin(axis=1)
    retdf['Min_Value'] = c.min(skipna=True)
    return c, retdf


def cleanDF(df):
    # Drops the non-numeric columns and the highly-skipped ones
    df1 = df.drop(["EndDate", "Residency","Num1","Num2a","Num2b","Num3","prep",
                   "Unnamed: 0", "MediaExp_1", "MediaExp_2", "MediaExp_3",
                   "MediaExp_4", "MediaExp_5", "MediaExp_6", "MediaExp_7"], axis=1)
    df1 = df1.drop(["Trustingroups_2", "Trustingroups_3", "Trustingroups_4", "Trustingroups_5",
                   "Trustingroups_7", "Trustingroups_8", "Trustingroups_9", "Trustingroups_10",
                   "Trustingroups_12", "Trustingroups_13", "CultCog_4", "CultCog_5", "CultCog_6",
                   "Friends_1", "Friends_2", "Friends_3", "Friends_4", "Friends_5", "Friends_6",
                   "Friends_7", "Friends_8", "Govresponse_1", "Govresponse_2", "Govresponse_3",
                   "Govresponse_4", "Govresponse_5", "Govresponse_6", "Govresponse_7", "Govresponse_9",
                   "KnowledgeCert_2", "Vaccine_2", "Personal_3", "Personal_4", "Personal_5",
                    "Personal_6", "Personal_7", "Personal_8", "CultCog_2", "CultCog_3",
                   "Longitude_2", "Longitude_3", "Govrestrict_2", "Govrestrict_3",
                   "FinitePool_6", "FinitePool_7", "FinitePool_8", "COVIDeffect_2", "COVIDeffect_3",
                   "FinitePool_1", "FinitePool_3", "FinitePool_5"], axis=1)
    df1 = df1.drop(0)
    df1 = df1.dropna()
    return df1
