from api.movie_api import MovieAPI
from api.user_api import UserAPI
from api.rating_api import RatingAPI

import pandas as pd

from matplotlib import pyplot as plt

users = []
genres = []

usersGenresDf = pd.DataFrame()

def loadUsers(users):
    users_data = UserAPI().getAllUsers()

    for user in users_data.get("users"):
        users.append({"email": user.get("email"), "favGenres": user.get("favGenres")})

def loadGenres(genres):
    genres_data = MovieAPI().getMovieGenres()

    for genre in genres_data.get("genres"):
        genres.append(genre.get("name"))
    
loadUsers(users)
loadGenres(genres)

def createUsersGenresTable(users, genres, dataframe):
    for genre in genres:
        column_data = []
        for user in users:
            if genre in user.get("favGenres"):
                column_data.append(1)
            else:
                column_data.append(0)
                
        dataframe[genre] = column_data
    
createUsersGenresTable(users, genres, usersGenresDf)

def createPieChartUsersGenres(dataframe):
    data = {}
    
    for column in dataframe.columns:
        if 1 in dataframe[column].value_counts().keys().tolist():
            data[column] = dataframe[column].value_counts()[1]

    plt.pie(data.values(), labels=data.keys(), autopct="%1.1f%%", startangle=10, wedgeprops={"edgecolor": "white"})
    plt.show()

createPieChartUsersGenres(usersGenresDf)
