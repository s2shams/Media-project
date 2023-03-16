import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from jikanpy import Jikan
import requests
import json

# Get user input and relevant information:
jikan = Jikan()

user_title = input("Enter 5 movies you like (separated by commas): ").split(",")
user_genre = []
user_synopsis = []

# Use Jikan and IMDb/OMDb APIs above to extract relevant info

for name in user_title:
    url = 'http://www.omdbapi.com/?t=' + name.replace(' ', '+') + '&plot=full' + '&apikey=' + API_KEY + '&'
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            data = response.json()
            synopsis = data['Plot']
            user_synopsis.appennd(synopsis)
            
            genre = data['Genre']
            user_genre.append(genre)
            
        except KeyError:
            user_genre.append('none')
            user_synopsis.append('none')
            

# if the lists have 'none' in them, then the user probably inputted an anime that isnt in OMDb

for index, name in enumerate(user_genre):
    if name != 'none':
        continue
    else:
        anime = user_title[index]
        # JIKAN API functionality problem, limitation is that user must search using name
        # as how it appears in MAL which is usually its japanese title.
        
        
# Create existing dataframe and vectorize it:
df = pd.read_csv('df.csv')
vectorize_df = df.drop(['title', 'score'], axis=1)
genre_array = np.array(vectorize_df.iloc[:, 1:])

vectorizer = CountVectorizer()

synopsis_vectors = vectorizer.fit_transform(vectorize_df['synopsis'])
combined_array = np.concatenate([synopsis_vectors.toarray(), genre_array], axis=1)
feature_names = list(vectorizer.vocabulary_.keys()) + list(vectorize_df.columns[1:])
vectorized_df = pd.DataFrame(combined_array, columns=feature_names)

# Start creating user dataframe:
user_df = df.copy()
user_df.drop(index=user_df.index, inplace=True)
columns = user_df.columns.tolist()


