import pandas as pd
from textblob import TextBlob
import os

data = pd.read_csv('../../gen/data-preparation/temp/parsed-data.csv', sep = '\t', encoding='utf-8')
data.head()

for i, j in data.iterrows():
    print(i)

    try:
        blob = TextBlob(j['text'])
        blob = blob.replace('.', ' ').replace(',', ' ').replace('#', ' ').replace('!', ' ').replace('?', ' ')\
            .replace(':', ' ').replace(';', ' ').replace('&', ' ') .replace('/', ' ').replace('&', ' ')
        data.loc[i, 'polarity'] = blob.sentiment.polarity
        data.loc[i, 'subjectivity'] = blob.sentiment.subjectivity
    except:
        data.loc[i, 'polarity'] = ''
        data.loc[i, 'subjectivity'] = ''

data.head()

os.makedirs('../../gen/data-preparation/output/', exist_ok=True)

data.to_csv('../../gen/data-preparation/output/dataset.csv', index = False)

print('done.')
