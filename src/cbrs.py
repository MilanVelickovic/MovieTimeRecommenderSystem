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

def extractTitle(text):
    return [text]

def stem(text):
    ps = PorterStemmer()
    result = []
    for word in text.split():
        result.append(ps.stem(word))
    
    return ' '.join(result)

def extractData():
    movies = pd.read_csv("./data/tmdb_5000_movies.csv")
    credits = pd.read_csv("./data/tmdb_5000_credits.csv")

    movies_genres = movies["genres"].apply(extract)
    movies_keywords = movies["keywords"].apply(extract)
    movies_cast = credits["cast"].apply(extract3)
    movies_directors = credits["crew"].apply(extractDirector)
    movies_overviews = movies["overview"].apply(splitWords)
    movies_titles = movies["title"].apply(extractTitle)

    data = {
        "movie_id": movies["id"],
        "title": movies["title"],
        "tags": movies_overviews + movies_genres + movies_keywords + movies_cast + movies_directors + movies_titles
    }

    df = pd.DataFrame(data)
    df["tags"] = df["tags"].apply(joinWords)
    df["tags"] = df["tags"].apply(allLowerCase)
    df["tags"] = df["tags"].apply(stem)

    df.to_csv("./data/distances.csv", index=False)

def loadData():
    return pd.read_csv("./data/distances.csv")

#extractData()
df = loadData()

cv_doc = CountVectorizer(max_features=5000, stop_words=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"])
cv_vectors = cv_doc.fit_transform(df["tags"]).toarray()

similarity = cosine_similarity(cv_vectors)

def recommend(movie_id):
    index = df.loc[df["movie_id"] == movie_id].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse= True, key= lambda x:x[1])[1:6]
    result = []

    print("--------------------------------------------------")
    print("R E C O M M E N D E D ----------------------------")
    print("--------------------------------------------------")

    for movie in movie_list:
        result.append(int(df.loc[movie[0]]["movie_id"]))
        title = df.loc[movie[0]]["title"]
        print(f"Movie title: {title},       match: {round(movie[1], 2)}%")
    
    print("--------------------------------------------------")
    print("--------------------------------------------------")
    
    return result

# print(df[df["title"].str.contains("Hobbit")])