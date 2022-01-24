import pandas as pd
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer

def extract(obj):
    result = []
    for item in json.loads(obj):
        result.append(item["name"].replace(' ', ''))
    
    return result 

def extract3(obj):
    result = []
    count = 0
    for item in json.loads(obj):
        if count != 3:
            result.append(item["name"].replace(' ', ''))
            count += 1
        else:
            break

    return result  

def extractDirector(obj):
    result = []
    for item in json.loads(obj):
        if item["job"] == "Director":
            result.append(item["name"].replace(' ', ''))

    return result 

def splitWords(text):
    if type(text) != type(.1):
        return text.split()
    else:
        return []

def joinWords(list):
    return ' '.join(list)

def allLowerCase(text):
    return text.lower()

def extractData():
    movies = pd.read_csv("./data/tmdb_5000_movies.csv")
    credits = pd.read_csv("./data/tmdb_5000_credits.csv")

    movies_genres = movies["genres"].apply(extract)
    movies_keywords = movies["keywords"].apply(extract)
    movies_cast = credits["cast"].apply(extract3)
    movies_directors = credits["crew"].apply(extractDirector)
    movies_overviews = movies["overview"].apply(splitWords)

    data = {
        "movie_id": movies["id"],
        "title": movies["title"],
        "tags": movies_overviews + movies_genres + movies_keywords + movies_cast + movies_directors
    }

    df = pd.DataFrame(data)
    df["tags"] = df["tags"].apply(joinWords)
    df["tags"] = df["tags"].apply(allLowerCase)

    df.to_csv("./data/distances.csv", index=False)

def loadData():
    return pd.read_csv("./data/distances.csv")

# extractData()
df = loadData()

cv_doc = CountVectorizer(max_features=5000)
cv_vectors = cv_doc.fit_transform(df["tags"]).toarray()

ps = PorterStemmer()

def stem(text):
    result = []
    for word in text.split():
        result.append(ps.stem(word))
    
    return ' '.join(result)

df["tags"] = df["tags"].apply(stem)

similarity = cosine_similarity(cv_vectors)

def recommend(movie_id):
    distances = similarity[movie_id]
    movie_list = sorted(list(enumerate(distances)), reverse= True, key= lambda x:x[1])[1:6]
    result = []

    for movie in movie_list:
        result.append(movie[0])
    
    return result
