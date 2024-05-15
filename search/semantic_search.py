from re import sub
import numpy as np
from nltk.stem.snowball import RussianStemmer
import gensim.downloader as api
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import SparseTermSimilarityMatrix, WordEmbeddingSimilarityIndex, SoftCosineSimilarity
from gensim.utils import simple_preprocess

from nltk.corpus import stopwords
import string
import pandas as pd
import sqlite3
import json
from difflib import SequenceMatcher
np.seterr(all= 'ignore')
ru_stemmer = RussianStemmer()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
def MatchSemantic(query_string, documents):
    stopwords = ['the', 'and', 'are', 'a', 'как', 'кто', 'зачем', 'и', 'а', 'такой', 'такая', 'такие','почему']
    if len(documents) == 1: documents.append('')

    def preprocess(doc):
        doc = sub(r'<img[^<>]+(>|$)', " image_token ", doc)
        doc = sub(r'<[^<>]+(>|$)', " ", doc)
        doc = sub(r'\[img_assist[^]]*?\]', " ", doc)
        doc = sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', " url_token ", doc)
        return [token for token in simple_preprocess(doc, min_len=0, max_len=float("inf")) if token not in stopwords]

    corpus = [preprocess(document) for document in documents]
    query = preprocess(query_string)

    glove = api.load("glove-wiki-gigaword-50")
    similarity_index = WordEmbeddingSimilarityIndex(glove)

    dictionary = Dictionary(corpus + [query])
    tfidf = TfidfModel(dictionary=dictionary)

    similarity_matrix = SparseTermSimilarityMatrix(similarity_index, dictionary, tfidf)

    query_tf = tfidf[dictionary.doc2bow(query)]

    index = SoftCosineSimilarity(
        tfidf[[dictionary.doc2bow(document) for document in corpus]],
        similarity_matrix)

    return index[query_tf]

sex = {}

def UpdateDataBase():
    cnx = sqlite3.connect('database\\wikipedia_articles.db')
    documents = pd.read_sql_query("SELECT title, content FROM articles", cnx)
    for i in range(len(documents["title"])):
        words = documents["title"][i].lower().split()
        stemmer_sentence = [ru_stemmer.stem(word) for word in words]
        stemmer_sentence = str(stemmer_sentence).translate(str.maketrans('', '', string.punctuation))
        sex[stemmer_sentence] = documents["content"][i]
    with open('database\\UpdatedDataBase.json', 'w') as f:
        json.dump(sex, f)

def PorterInput(query_string):
    words = query_string.split()
    stemmer_sentence = [ru_stemmer.stem(word) for word in words]
    stemmer_sentence = str(stemmer_sentence).translate(str.maketrans('', '', string.punctuation))
    print(stemmer_sentence)
    return stemmer_sentence

def SemanticSearch(question):
    with open('database\\UpdatedDataBase.json', 'r') as f:
        sex = json.load(f)
    question = question.lower()
    stemmer_sentence = PorterInput(question)
    print(sex.keys())

    result = list((MatchSemantic(stemmer_sentence, sex), ' '))[0][:-1]
    AnswerIndex = max(enumerate(result), key=lambda x: x[1])[0]
    print(sorted(result))

    if max(result) > 0.18:
        Answer = sex[list(sex)[AnswerIndex]]
        return Answer
    else:
        kef = 0
        Results = []
        for question in sex:
            Results.append(similar(stemmer_sentence, question))
        AnswerIndex = max(enumerate(Results), key=lambda x: x[1])[0]
        return sex[list(sex)[AnswerIndex]]




