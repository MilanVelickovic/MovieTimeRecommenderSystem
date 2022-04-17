import pandas as pd
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer


def extract(obj) -> list:
    return [item["name"].replace(' ', '') for item in json.loads(obj)]


def extract3(obj) -> list:    
    return [item["name"].replace(' ', '') for item in json.loads(obj)[:3]]


def extractDirector(obj) -> list:
    return [item["name"].replace(' ', '') for item in json.loads(obj) if item["job"] == "Director"]


def splitWords(text: str) -> list:
    return text.split() if type(text) != type(.1) else []


def joinWords(list: str) -> str:
    return ' '.join(list)


def allLowerCase(text: str) -> str:
    return text.lower()


def extractTitle(text: str) -> list:
    return [text]


def stem(text) -> str:
    ps: PorterStemmer = PorterStemmer()
    result: list = [ps.stem(word) for word in text.split()]
    return ' '.join(result)


def extractData() -> None:
    movies = pd.read_csv("./data/tmdb_5000_movies.csv")
    credits = pd.read_csv("./data/tmdb_5000_credits.csv")

    movies_genres: list = movies["genres"].apply(extract)
    movies_keywords: list = movies["keywords"].apply(extract)
    movies_cast: list = credits["cast"].apply(extract3)
    movies_directors: list = credits["crew"].apply(extractDirector)
    movies_overviews: list = movies["overview"].apply(splitWords)
    movies_titles: list = movies["title"].apply(extractTitle)

    data: dict = {
        "movie_id": movies["id"],
        "title": movies["title"],
        "tags": movies_overviews + movies_genres + movies_keywords + movies_cast + movies_directors + movies_titles
    }

    df: pd.DataFrame = pd.DataFrame(data)
    df["tags"] = df["tags"].apply(joinWords)
    df["tags"] = df["tags"].apply(allLowerCase)
    df["tags"] = df["tags"].apply(stem)

    df.to_csv("./data/distances.csv", index=False)


def loadData() -> pd.DataFrame:
    return pd.read_csv("./data/distances.csv")


def loadStopWords() -> list:
    with open("data/stop_words.csv") as file:
        return [word for word in file.readline().split(', ')]


#extractData()
df = loadData()

cv_doc: CountVectorizer = CountVectorizer(max_features= 5000, stop_words= loadStopWords())
cv_vectors = cv_doc.fit_transform(df["tags"]).toarray()

similarity = cosine_similarity(cv_vectors)


def recommend(movie_id: int) -> list:
    index: int = df.loc[df["movie_id"] == movie_id].index[0]
    distances = similarity[index]
    movie_list: list = sorted(list(enumerate(distances)), reverse= True, key= lambda x:x[1])[1:6]
    result: list = []

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


#print(df[df["title"].str.contains("Hobbit")])
recommend(127585)