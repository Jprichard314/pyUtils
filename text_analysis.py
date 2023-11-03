from dataclasses import field
import pandas
import numpy
from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
import nltk

class LemmaTokenizer(object):
  '''
  Placeheld
  '''
  
  def __init__(self):
      self.wnl = WordNetLemmatizer()
  def __call__(self, articles):
      return [
          self.wnl.lemmatize(t) for t in word_tokenize(articles)
              if re.fullmatch('[a-zA-Z]+',t) 
      ]

class SnowballTokenizer(object):
  '''
  Placeheld
  '''
  class SnowballTokenizer(object):
    def __init__(self):
        self.wnl = nltk.stem.SnowballStemmer('english')
    def __call__(self, articles):
        return [
            self.wnl.stem(t) for t in word_tokenize(articles)
                if re.fullmatch('[a-zA-Z]+',t) 
        ]



def aggregate_and_vectorize(df,field_aggregate,field_value):
  
  '''
  Input
      - df -- dataframe
      - field_aggregate -- the field you'd like to aggregate by
      - field_value -- the field you'd like to aggregate (a notes field)

  output
      - A breakdown of how many times each term in the aggregated field_value appears per
          field_aggregate. 

  '''
  # Aggregate note fields
  aggregate = df.assign(
    clean_value = df[field_value].fillna('')
  ).pivot_table(
        index = field_aggregate
      , values = 'clean_value'
      , aggfunc =  (' || ').join
  )


  # Vectorize aggregated descriptions
  vectorizer = CountVectorizer(
        stop_words = 'english'
      , tokenizer = LemmaTokenizer()
  )
  vectors = vectorizer.fit_transform(aggregate['clean_value'].values)
  product = pandas.DataFrame(
        vectors.toarray()
      , columns = vectorizer.get_feature_names()
  ).set_index(
      aggregate.index
  )

  return(
    product
  )
  

def textAnalytics_drivingTerms(
      df
    , field_aggregate
    , field_value
):

    '''
    Input
      - df -- dataframe
      - field_aggregate -- the field you'd like to aggregate by
      - field_value -- the field you'd like to aggregate (a notes field)

    Output
      - A breakdown by field_aggregate of the 10 most common terms in field_ values
      
    '''

    df_textFields = aggregate_and_vectorize(
      df
      , field_aggregate=field_aggregate
      , field_value=field_value
    )

    product = pandas.concat([
      pandas.DataFrame(
              df_textFields.loc[
                    field
                  , df_textFields.columns
              ]
              .sort_values(ascending = False)
              .head(10)
          )
          .assign(
                aggregate_field = field
              , rank = range(0,10)
          )
          .reset_index()
          .set_index(
              [    
                    'rank'
                  , 'aggregate_field'
              ]
          )
          .unstack(
              level = 1
          ).reorder_levels(
              [
                  'aggregate_field'
                  , None
              ]
              , axis = 1
          )
          .rename(
              columns = {'index':'term',field:'count'},level = 1
          )
      for field in df_textFields.index                
    ]
    , axis = 1)

    return(product)


def textAnalytics_drivingTerms_dataClass(
        textMatrix
      , x = 10
):

    '''
    Input
      - textMatrix -- dataframe with aggregate index and fields for each word.

    Output
      - A breakdown by field_aggregate of the 10 most common terms in field_ values
      - term: a word found within the aggregate
      - count: the number of time that word occurs
      - occurence: that terms occurence as a percentage of the total words within that aggregate.
      
    '''

    df_textFields = textMatrix

    product = pandas.concat(
      [
            pandas.DataFrame.from_dict({
            'term'        :df_textFields.loc[i].sort_values(ascending = False).head(x).index
          , 'count'       :df_textFields.loc[i].sort_values(ascending = False).head(x).values
          , 'occurence'   :((df_textFields.loc[i].sort_values(ascending = False).head(x).values / df_textFields.loc[i].sum())*100).round(2)
        })
        .assign(
          aggregate_field = i
        )
        .reset_index()
        .set_index(
            [    
                  'index'
                , 'aggregate_field'
            ]
        )
        .unstack(
            level = 1
        ).reorder_levels(
            [
                'aggregate_field'
                , None
            ]
            , axis = 1
        )
        for i in df_textFields.index           
      ]
    , axis = 1)

    return(product)