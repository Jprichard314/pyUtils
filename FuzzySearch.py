from rapidfuzz import process, utils
import pandas


def FuzzySearch(df1,df2,score=0):    
    '''
    input
        df1 = numypy array of values to lookup
        df2 = numypy array of values to search through
        score = cutoff score to include
    output
        dataframe containing the
            original match search
            attempted match result
            the levenshtein dist. between the original and attempted
            the index location of the result


    '''

    ratio = [(process.extractOne(i,df2,score_cutoff=score),i) for i in df1]
    df3 = pd.DataFrame(ratio,columns = ['ratio','original_search'])
    df3.loc[:,'match_attempt'] = df3.loc[:,'ratio'].apply(lambda x: x[0])
    df3.loc[:,'match_ratio'] = df3.loc[:,'ratio'].apply(lambda x: x[1])
    df3.loc[:,'searched_from_index'] = df3.loc[:,'ratio'].apply(lambda x: x[2])
    del df3['ratio']
    return df3
  
  
 