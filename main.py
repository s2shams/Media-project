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

user_movies = input("Enter 5 movies you like (separated by commas): ").split(",")
user_genre = []
user_synopsis = []
user_title = []
# Use Jikan and IMDb/OMDb APIs above to extract relevant info

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
# i=git test

