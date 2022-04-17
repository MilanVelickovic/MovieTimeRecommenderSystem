import requests
from dotenv import load_dotenv
import os

load_dotenv()

class MovieAPI:
    def __init__(self) -> None:
        self.base_url: str = "https://api.themoviedb.org/3/"
        self.api_key: str = os.getenv("MOVIE_API_KEY")

    def getMovieGenres(self) -> dict:
        # Example: https://api.themoviedb.org/3/genre/movie/list?api_key=<<API_KEY>>
        return requests.get(self.base_url + "genre/movie/list?api_key=" + self.api_key).json()
    
    def getMoviesByGenre(self, genreId: int) -> dict:
        # Example: https://api.themoviedb.org/3/discover/movie?api_key=<<API_KEY>>&with_genres=28
        return requests.get(self.base_url + "discover/movie?api_key=" + self.api_key + "&with_genres=" + str(genreId)).json()

